"use client";

import React, { useEffect, useMemo, useState } from "react";
import Layout from "@/components/layout/Layout";
import Button from "@/components/ui/Button";
import { Sparkles, RefreshCw, AlertCircle, Wand2 } from "lucide-react";

interface ToolPropertySchema {
  type?: string;
  description?: string;
  minLength?: number;
  minimum?: number;
  maximum?: number;
}

interface ToolSchema {
  name: string;
  description?: string;
  inputSchema?: {
    type?: string;
    properties?: Record<string, ToolPropertySchema>;
    required?: string[];
  };
}

interface ToolListResponse {
  tools: ToolSchema[];
}

type FormValues = Record<string, string>;

export default function PlaygroundPage() {
  const [tools, setTools] = useState<ToolSchema[]>([]);
  const [loadingTools, setLoadingTools] = useState<boolean>(true);
  const [toolsError, setToolsError] = useState<string | null>(null);

  const [selectedToolName, setSelectedToolName] = useState<string | null>(null);
  const [formValues, setFormValues] = useState<FormValues>({});
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [resultText, setResultText] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    async function fetchTools() {
      try {
        setLoadingTools(true);
        const response = await fetch("/api/playground/mcp");
        if (!response.ok) {
          throw new Error("Kunne ikke hente MCP-verktøy.");
        }
        const data = (await response.json()) as ToolListResponse;
        if (isMounted) {
          setTools(data.tools);
          if (data.tools.length > 0) {
            setSelectedToolName(data.tools[0].name);
          }
        }
      } catch (error) {
        console.error("Failed to load MCP tools", error);
        if (isMounted) {
          setToolsError(
            "Klarte ikke å laste Playground-verktøy. Sjekk at MCP-serveren er tilgjengelig."
          );
        }
      } finally {
        if (isMounted) {
          setLoadingTools(false);
        }
      }
    }

    void fetchTools();
    return () => {
      isMounted = false;
    };
  }, []);

  const selectedTool = useMemo(() => {
    return tools.find((tool) => tool.name === selectedToolName) ?? null;
  }, [selectedToolName, tools]);

  useEffect(() => {
    if (!selectedTool) {
      setFormValues({});
      return;
    }

    const properties = selectedTool.inputSchema?.properties ?? {};
    const initial: FormValues = {};
    for (const key of Object.keys(properties)) {
      initial[key] = "";
    }
    setFormValues(initial);
    setResultText(null);
    setSubmitError(null);
  }, [selectedTool]);

  const handleInputChange = (name: string, value: string) => {
    setFormValues((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!selectedTool) return;

    const properties = selectedTool.inputSchema?.properties ?? {};
    const payload: Record<string, unknown> = {};

    for (const [key, schema] of Object.entries(properties)) {
      const rawValue = formValues[key];
      if (!rawValue) {
        continue;
      }

      if (schema.type === "number") {
        const parsed = Number(rawValue);
        if (!Number.isNaN(parsed)) {
          payload[key] = parsed;
        }
      } else {
        payload[key] = rawValue;
      }
    }

    setIsSubmitting(true);
    setSubmitError(null);
    setResultText(null);

    try {
      const response = await fetch("/api/playground/mcp", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          tool: selectedTool.name,
          arguments: payload,
        }),
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => null);
        throw new Error(errorBody?.error || "Ukjent MCP-feil.");
      }

      const data = await response.json();
      setResultText(data.text || "MCP-verktøyet returnerte ingen tekstlig respons.");
    } catch (error) {
      console.error("Failed to call MCP tool", error);
      setSubmitError(
        error instanceof Error
          ? error.message
          : "Kunne ikke generere forslag. Prøv igjen."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Layout>
      <div className="space-y-6">
        <header className="bg-white border border-[var(--color-bg-tertiary)] rounded-2xl shadow-[var(--shadow-md)] p-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <div className="flex items-center gap-3">
                <Sparkles className="h-8 w-8 text-[var(--color-secondary)]" />
                <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">
                  Ubuntu Playground
                </h1>
              </div>
              <p className="text-sm text-[var(--color-text-secondary)] mt-2 max-w-2xl">
                Utforsk kreative mikro-økter, tidslinjer og refleksjoner drevet av
                OpenAI MCP. Verktøyene er kuratert for å støtte trygg aktivering,
                lek og biofelt-forankrede overgangsritualer.
              </p>
            </div>
            <div className="flex items-center gap-2 text-sm text-[var(--color-text-secondary)]">
              <RefreshCw className="h-4 w-4" />
              <span>
                Data hentes direkte fra MCP-serveren for hver forespørsel.
              </span>
            </div>
          </div>
        </header>

        <section className="grid lg:grid-cols-[320px,1fr] gap-6">
          <aside className="bg-white border border-[var(--color-bg-tertiary)] rounded-2xl shadow-[var(--shadow-sm)] p-5">
            <h2 className="text-lg font-semibold text-[var(--color-text-primary)] mb-4">
              MCP-verktøy
            </h2>
            {loadingTools && (
              <p className="text-sm text-[var(--color-text-secondary)]">
                Laster verktøy…
              </p>
            )}
            {toolsError && (
              <div className="text-sm text-[var(--color-error)] flex items-start gap-2">
                <AlertCircle className="h-4 w-4 mt-0.5" />
                <span>{toolsError}</span>
              </div>
            )}
            <ul className="space-y-3">
              {tools.map((tool) => {
                const isActive = tool.name === selectedToolName;
                return (
                  <li key={tool.name}>
                    <button
                      type="button"
                      onClick={() => setSelectedToolName(tool.name)}
                      className={`w-full text-left p-3 rounded-xl border transition-colors ${
                        isActive
                          ? "border-[var(--color-primary)] bg-[var(--color-primary)]/10"
                          : "border-[var(--color-bg-tertiary)] hover:border-[var(--color-primary)]/40"
                      }`}
                    >
                      <h3 className="font-semibold text-sm text-[var(--color-text-primary)]">
                        {tool.name}
                      </h3>
                      {tool.description && (
                        <p className="text-xs text-[var(--color-text-secondary)] mt-1">
                          {tool.description}
                        </p>
                      )}
                    </button>
                  </li>
                );
              })}
            </ul>
          </aside>

          <article className="bg-white border border-[var(--color-bg-tertiary)] rounded-2xl shadow-[var(--shadow-md)] p-6">
            {selectedTool ? (
              <form className="space-y-6" onSubmit={handleSubmit}>
                <header>
                  <div className="flex items-center gap-2 text-[var(--color-secondary)] mb-2">
                    <Wand2 className="h-5 w-5" />
                    <span className="uppercase tracking-wide text-xs font-semibold">
                      Verktøy valgt
                    </span>
                  </div>
                  <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
                    {selectedTool.name.replace(/_/g, " ")}
                  </h2>
                  {selectedTool.description && (
                    <p className="text-sm text-[var(--color-text-secondary)] mt-2">
                      {selectedTool.description}
                    </p>
                  )}
                </header>

                <div className="space-y-4">
                  {Object.entries(selectedTool.inputSchema?.properties ?? {}).map(
                    ([name, schema]) => {
                      const isRequired =
                        selectedTool.inputSchema?.required?.includes(name) ?? false;
                      const label = name
                        .replace(/_/g, " ")
                        .replace(/\b\w/g, (char) => char.toUpperCase());

                      const inputType =
                        schema.type === "number" ? "number" : "text";
                      const isLongField =
                        name.toLowerCase().includes("notes") ||
                        name.toLowerCase().includes("context") ||
                        (schema.minLength ?? 0) > 80;

                      return (
                        <div key={name} className="space-y-2">
                          <label className="block text-sm font-medium text-[var(--color-text-primary)]">
                            {label}
                            {isRequired && (
                              <span className="text-[var(--color-error)]"> *</span>
                            )}
                          </label>
                          {isLongField ? (
                            <textarea
                              rows={4}
                              required={isRequired}
                              value={formValues[name] ?? ""}
                              onChange={(event) =>
                                handleInputChange(name, event.target.value)
                              }
                              className="w-full rounded-xl border border-[var(--color-bg-tertiary)] focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)]/20 transition-colors p-3 text-sm"
                              placeholder={schema.description}
                            />
                          ) : (
                            <input
                              type={inputType}
                              required={isRequired}
                              value={formValues[name] ?? ""}
                              onChange={(event) =>
                                handleInputChange(name, event.target.value)
                              }
                              className="w-full rounded-xl border border-[var(--color-bg-tertiary)] focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)]/20 transition-colors p-3 text-sm"
                              placeholder={schema.description}
                              min={
                                schema.type === "number" && schema.minimum !== undefined
                                  ? schema.minimum
                                  : undefined
                              }
                              max={
                                schema.type === "number" && schema.maximum !== undefined
                                  ? schema.maximum
                                  : undefined
                              }
                            />
                          )}
                          {schema.description && (
                            <p className="text-xs text-[var(--color-text-secondary)]">
                              {schema.description}
                            </p>
                          )}
                        </div>
                      );
                    }
                  )}
                </div>

                <Button
                  type="submit"
                  variant="primary"
                  size="large"
                  isLoading={isSubmitting}
                >
                  Generer Playground-forslag
                </Button>

                {submitError && (
                  <div className="text-sm text-[var(--color-error)] flex items-start gap-2">
                    <AlertCircle className="h-4 w-4 mt-0.5" />
                    <span>{submitError}</span>
                  </div>
                )}

                {resultText && (
                  <section className="mt-6">
                    <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-2">
                      Resultat
                    </h3>
                    <div className="bg-[var(--color-bg-secondary)] border border-[var(--color-bg-tertiary)] rounded-2xl p-4 whitespace-pre-wrap text-sm text-[var(--color-text-primary)]">
                      {resultText}
                    </div>
                  </section>
                )}
              </form>
            ) : (
              <p className="text-sm text-[var(--color-text-secondary)]">
                Velg et MCP-verktøy fra listen for å starte.
              </p>
            )}
          </article>
        </section>
      </div>
    </Layout>
  );
}
