"use client";

import { useState, useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Layout from "@/components/layout/Layout";
import Button from "@/components/ui/Button";
import DocumentHelper from "@/components/veiledninger/DocumentHelper";
import {
  FileText,
  Search,
  Upload,
  Download,
  Trash2,
  Eye,
  FolderOpen,
  AlertCircle,
  Sparkles,
  MessageCircle,
  Calendar,
  FileIcon,
  X,
  Edit2,
  Check,
} from "lucide-react";

type DocumentCategory = "Alle" | "Personalia" | "Arbeid" | "Økonomi" | "Helse" | "Diverse";

interface StoredDocument {
  id: string;
  name: string;
  category: DocumentCategory;
  type: string; // MIME type
  size: number;
  uploadDate: Date;
  file: string; // Base64 encoded for localStorage
  notes?: string;
}

const categories: DocumentCategory[] = ["Alle", "Personalia", "Arbeid", "Økonomi", "Helse", "Diverse"];

const categoryDescriptions: Record<DocumentCategory, string> = {
  "Alle": "Alle dokumenter",
  "Personalia": "Pass, fødselsattest, ID-kort",
  "Arbeid": "CV, attester, arbeidskontrakter, lønnslipper",
  "Økonomi": "Skattemeldinger, kontoutskrifter, faktura",
  "Helse": "Legeerklæringer, sykemeldinger, resepter",
  "Diverse": "Andre viktige dokumenter"
};

export default function DokumenterPage() {
  const router = useRouter();
  const [documents, setDocuments] = useState<StoredDocument[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<DocumentCategory>("Alle");
  const [searchTerm, setSearchTerm] = useState("");
  const [showUploadSection, setShowUploadSection] = useState(false);
  const [previewDocument, setPreviewDocument] = useState<StoredDocument | null>(null);
  const [editingDocument, setEditingDocument] = useState<StoredDocument | null>(null);
  const [editName, setEditName] = useState("");
  const [editCategory, setEditCategory] = useState<DocumentCategory>("Diverse");
  const [editNotes, setEditNotes] = useState("");

  // Load documents from localStorage on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      try {
        const saved = localStorage.getItem("navlosen-documents");
        if (saved) {
          const parsed = JSON.parse(saved);
          // Convert date strings back to Date objects
          const docs = parsed.map((doc: any) => ({
            ...doc,
            uploadDate: new Date(doc.uploadDate)
          }));
          setDocuments(docs);
        }
      } catch (error) {
        console.error("Failed to load documents:", error);
      }
    }
  }, []);

  // Save documents to localStorage whenever they change
  useEffect(() => {
    if (typeof window !== "undefined" && documents.length > 0) {
      try {
        localStorage.setItem("navlosen-documents", JSON.stringify(documents));
      } catch (error) {
        console.error("Failed to save documents:", error);
      }
    }
  }, [documents]);

  // Handle document upload
  const handleDocumentAdded = async (file: File, type: "upload" | "camera" | "voice") => {
    try {
      // Convert file to base64 for storage
      const reader = new FileReader();
      reader.onload = (e) => {
        const base64 = e.target?.result as string;

        const newDoc: StoredDocument = {
          id: `doc-${Date.now()}-${Math.random()}`,
          name: file.name,
          category: "Diverse",
          type: file.type,
          size: file.size,
          uploadDate: new Date(),
          file: base64,
        };

        setDocuments(prev => [newDoc, ...prev]);
        setShowUploadSection(false);
      };
      reader.readAsDataURL(file);
    } catch (error) {
      console.error("Failed to add document:", error);
    }
  };

  // Filter documents
  const filteredDocuments = useMemo(() => {
    return documents.filter(doc => {
      const matchesCategory = selectedCategory === "Alle" || doc.category === selectedCategory;
      const matchesSearch = searchTerm === "" ||
        doc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doc.notes?.toLowerCase().includes(searchTerm.toLowerCase());
      return matchesCategory && matchesSearch;
    });
  }, [documents, selectedCategory, searchTerm]);

  // Calculate statistics
  const stats = useMemo(() => {
    const totalSize = documents.reduce((sum, doc) => sum + doc.size, 0);
    const categoryCounts = documents.reduce((acc, doc) => {
      acc[doc.category] = (acc[doc.category] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return {
      total: documents.length,
      totalSize,
      categoryCounts
    };
  }, [documents]);

  // Delete document
  const handleDelete = (id: string) => {
    if (confirm("Er du sikker på at du vil slette dette dokumentet?")) {
      setDocuments(prev => prev.filter(doc => doc.id !== id));
      setPreviewDocument(null);
    }
  };

  // Download document
  const handleDownload = (doc: StoredDocument) => {
    const link = document.createElement("a");
    link.href = doc.file;
    link.download = doc.name;
    link.click();
  };

  // Start editing
  const startEdit = (doc: StoredDocument) => {
    setEditingDocument(doc);
    setEditName(doc.name);
    setEditCategory(doc.category);
    setEditNotes(doc.notes || "");
  };

  // Save edit
  const saveEdit = () => {
    if (!editingDocument) return;

    setDocuments(prev => prev.map(doc =>
      doc.id === editingDocument.id
        ? { ...doc, name: editName, category: editCategory, notes: editNotes }
        : doc
    ));
    setEditingDocument(null);
    setPreviewDocument(null);
  };

  // Cancel edit
  const cancelEdit = () => {
    setEditingDocument(null);
  };

  // Format file size
  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  // Format date
  const formatDate = (date: Date): string => {
    return new Date(date).toLocaleDateString("no-NO", {
      day: "numeric",
      month: "long",
      year: "numeric"
    });
  };

  return (
    <Layout>
      <div className="space-y-12">
        {/* Breadcrumb */}
        <div className="text-sm text-[var(--color-text-secondary)]">
          <Link
            href="/"
            className="transition-colors hover:text-[var(--color-primary)]"
          >
            NAV-Losen
          </Link>
          <span className="mx-2">/</span>
          <span className="text-[var(--color-text-primary)] font-medium">Dokumenter</span>
        </div>

        {/* Hero Section */}
        <section className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-8 rounded-3xl bg-white/80 p-8 md:p-12 shadow-sm backdrop-blur">
          <div className="space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full bg-purple-100 px-3 py-1 text-sm font-medium text-purple-700">
              <Sparkles className="h-4 w-4" />
              Dokumenthåndtering
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-[var(--color-text-primary)] md:text-5xl">
              Mine dokumenter
            </h1>
            <p className="text-lg text-[var(--color-text-secondary)]">
              Last opp, organiser og håndter alle dine NAV-dokumenter på ett sted. Sikker lagring og enkel tilgang når du trenger det.
            </p>
            <div className="flex flex-wrap gap-4 text-sm text-[var(--color-text-secondary)]">
              <span className="inline-flex items-center gap-2">
                <FileText className="h-4 w-4 text-purple-500" />
                {stats.total} dokumenter
              </span>
              <span className="inline-flex items-center gap-2">
                <FolderOpen className="h-4 w-4 text-purple-500" />
                {Object.keys(stats.categoryCounts).length} kategorier
              </span>
            </div>
          </div>
          <div className="hidden lg:flex items-start justify-center">
            <div className="flex h-24 w-24 items-center justify-center rounded-2xl bg-purple-100">
              <FileText className="h-12 w-12 text-purple-600" />
            </div>
          </div>

          {/* Search and Upload */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex flex-col sm:flex-row gap-3">
              {/* Search Bar */}
              <div className="relative flex-1">
                <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Søk etter dokumentnavn..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full rounded-xl border-2 border-gray-200 bg-white py-3 pl-12 pr-4 text-base transition-colors focus:border-[var(--color-primary)] focus:outline-none"
                />
              </div>

              {/* Upload Button */}
              <Button
                variant="primary"
                size="medium"
                leftIcon={<Upload className="h-5 w-5" />}
                onClick={() => setShowUploadSection(!showUploadSection)}
              >
                Last opp dokument
              </Button>
            </div>

            {/* Category Filters */}
            <div className="flex flex-wrap gap-2" role="tablist" aria-label="Filtrer dokumenter etter kategori">
              {categories.map((category) => {
                const isActive = selectedCategory === category;
                const count = category === "Alle" ? stats.total : (stats.categoryCounts[category] || 0);

                return (
                  <button
                    key={category}
                    type="button"
                    role="tab"
                    aria-selected={isActive}
                    onClick={() => setSelectedCategory(category)}
                    className={`rounded-full border px-4 py-2 text-sm font-medium transition-colors ${
                      isActive
                        ? "border-[var(--color-primary)] bg-[var(--color-primary)] text-white"
                        : "border-gray-200 bg-white text-[var(--color-text-secondary)] hover:border-[var(--color-primary)]/60 hover:text-[var(--color-primary)]"
                    }`}
                  >
                    {category} {count > 0 && `(${count})`}
                  </button>
                );
              })}
            </div>
          </div>
        </section>

        {/* Local Storage Notice */}
        <section>
          <div className="rounded-2xl border-2 border-yellow-200 bg-yellow-50 p-4 shadow-sm">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 flex-shrink-0 text-yellow-600" />
              <div className="flex-1">
                <p className="text-sm text-yellow-800">
                  <strong>Lokal lagring:</strong> Dokumentene lagres i nettleserens localStorage. De er ikke synkronisert med NAV og vil bli slettet hvis du tømmer nettleserdata. Bruk dette som midlertidig lagring før innsending.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Upload Section */}
        {showUploadSection && (
          <section className="rounded-2xl border-2 border-purple-200 bg-purple-50/50 p-6">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-lg font-bold text-[var(--color-text-primary)]">
                Last opp nytt dokument
              </h3>
              <button
                onClick={() => setShowUploadSection(false)}
                className="rounded-lg p-2 transition-colors hover:bg-white"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <DocumentHelper
              documentType="NAV-dokument"
              onDocumentAdded={handleDocumentAdded}
            />
          </section>
        )}

        {/* Lira Chatbot CTA */}
        <section>
          <div className="rounded-2xl border-2 border-[var(--color-secondary)] bg-gradient-to-r from-teal-50 to-blue-50 p-6 shadow-sm">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-[var(--color-secondary)]">
                <MessageCircle className="h-6 w-6 text-white" />
              </div>
              <div className="flex-1 space-y-3">
                <h3 className="text-lg font-bold text-[var(--color-text-primary)]">
                  Trenger du hjelp med dokumenter?
                </h3>
                <p className="text-sm text-[var(--color-text-secondary)]">
                  Lira kan hjelpe deg med å forstå hvilke dokumenter du trenger for ulike NAV-tjenester og hvordan du organiserer dem.
                </p>
                <Button
                  variant="primary"
                  size="medium"
                  leftIcon={<MessageCircle className="h-5 w-5" />}
                  onClick={() => router.push("/chatbot")}
                >
                  Chat med Lira om dokumenter
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Document Grid */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
              {selectedCategory === "Alle" ? "Alle dokumenter" : selectedCategory}
            </h2>
            <span className="text-sm text-[var(--color-text-secondary)]">
              Viser {filteredDocuments.length} av {documents.length}
            </span>
          </div>

          {/* Empty State */}
          {filteredDocuments.length === 0 && documents.length === 0 && (
            <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-12 text-center">
              <FileText className="mx-auto mb-4 h-16 w-16 text-gray-300" />
              <h3 className="mb-2 text-lg font-semibold text-[var(--color-text-primary)]">
                Ingen dokumenter ennå
              </h3>
              <p className="mb-4 text-sm text-[var(--color-text-secondary)]">
                Start med å laste opp ditt første dokument
              </p>
              <Button
                variant="primary"
                size="medium"
                leftIcon={<Upload className="h-5 w-5" />}
                onClick={() => setShowUploadSection(true)}
              >
                Last opp dokument
              </Button>
            </div>
          )}

          {/* No Search Results */}
          {filteredDocuments.length === 0 && documents.length > 0 && (
            <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-8 text-center text-[var(--color-text-secondary)]">
              <Search className="mx-auto mb-4 h-12 w-12 text-gray-300" />
              <p className="text-lg font-semibold">Ingen dokumenter funnet</p>
              <p className="mt-2 text-sm">
                Prøv å endre søkeord eller kategori
              </p>
            </div>
          )}

          {/* Document Grid */}
          {filteredDocuments.length > 0 && (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {filteredDocuments.map((doc) => (
                <article
                  key={doc.id}
                  className="group flex flex-col rounded-2xl border border-gray-200 bg-white p-4 shadow-sm transition-all hover:shadow-md"
                >
                  {/* Document Icon/Preview */}
                  <div className="mb-3 flex h-32 items-center justify-center rounded-lg bg-gray-50">
                    {doc.type.startsWith("image/") ? (
                      <img
                        src={doc.file}
                        alt={doc.name}
                        className="h-full w-full rounded-lg object-cover"
                      />
                    ) : (
                      <FileIcon className="h-16 w-16 text-purple-400" />
                    )}
                  </div>

                  {/* Document Info */}
                  <div className="flex-1 space-y-2">
                    <h3 className="line-clamp-2 text-sm font-semibold text-[var(--color-text-primary)]">
                      {doc.name}
                    </h3>
                    <div className="space-y-1 text-xs text-[var(--color-text-tertiary)]">
                      <div className="flex items-center gap-1">
                        <FolderOpen className="h-3 w-3" />
                        {doc.category}
                      </div>
                      <div className="flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        {formatDate(doc.uploadDate)}
                      </div>
                      <div>{formatFileSize(doc.size)}</div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="mt-3 flex gap-2">
                    <button
                      onClick={() => setPreviewDocument(doc)}
                      className="flex-1 rounded-lg border border-gray-200 p-2 text-xs font-medium transition-colors hover:bg-gray-50"
                      title="Forhåndsvisning"
                    >
                      <Eye className="mx-auto h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDownload(doc)}
                      className="flex-1 rounded-lg border border-gray-200 p-2 text-xs font-medium transition-colors hover:bg-gray-50"
                      title="Last ned"
                    >
                      <Download className="mx-auto h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(doc.id)}
                      className="flex-1 rounded-lg border border-red-200 p-2 text-xs font-medium text-red-600 transition-colors hover:bg-red-50"
                      title="Slett"
                    >
                      <Trash2 className="mx-auto h-4 w-4" />
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {/* Preview Modal */}
        {previewDocument && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
            <div className="max-h-[90vh] w-full max-w-4xl overflow-auto rounded-2xl bg-white p-6 shadow-xl">
              {editingDocument ? (
                /* Edit Mode */
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xl font-bold">Rediger dokument</h3>
                    <button
                      onClick={() => setPreviewDocument(null)}
                      className="rounded-lg p-2 hover:bg-gray-100"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Dokumentnavn
                      </label>
                      <input
                        type="text"
                        value={editName}
                        onChange={(e) => setEditName(e.target.value)}
                        className="w-full rounded-lg border border-gray-300 px-3 py-2"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Kategori
                      </label>
                      <select
                        value={editCategory}
                        onChange={(e) => setEditCategory(e.target.value as DocumentCategory)}
                        className="w-full rounded-lg border border-gray-300 px-3 py-2"
                      >
                        {categories.filter(c => c !== "Alle").map(cat => (
                          <option key={cat} value={cat}>{cat}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Merknader
                      </label>
                      <textarea
                        value={editNotes}
                        onChange={(e) => setEditNotes(e.target.value)}
                        rows={3}
                        className="w-full rounded-lg border border-gray-300 px-3 py-2"
                        placeholder="Legg til notater..."
                      />
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Button
                      variant="primary"
                      size="medium"
                      leftIcon={<Check className="h-5 w-5" />}
                      onClick={saveEdit}
                      className="flex-1"
                    >
                      Lagre
                    </Button>
                    <Button
                      variant="secondary"
                      size="medium"
                      onClick={cancelEdit}
                      className="flex-1"
                    >
                      Avbryt
                    </Button>
                  </div>
                </div>
              ) : (
                /* View Mode */
                <>
                  <div className="mb-4 flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-[var(--color-text-primary)]">
                        {previewDocument.name}
                      </h3>
                      <div className="mt-2 flex flex-wrap gap-4 text-sm text-[var(--color-text-secondary)]">
                        <span className="flex items-center gap-1">
                          <FolderOpen className="h-4 w-4" />
                          {previewDocument.category}
                        </span>
                        <span className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          {formatDate(previewDocument.uploadDate)}
                        </span>
                        <span>{formatFileSize(previewDocument.size)}</span>
                      </div>
                      {previewDocument.notes && (
                        <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
                          {previewDocument.notes}
                        </p>
                      )}
                    </div>
                    <button
                      onClick={() => setPreviewDocument(null)}
                      className="rounded-lg p-2 hover:bg-gray-100"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  </div>

                  {/* Preview Content */}
                  <div className="mb-4 rounded-lg bg-gray-50 p-4">
                    {previewDocument.type.startsWith("image/") ? (
                      <img
                        src={previewDocument.file}
                        alt={previewDocument.name}
                        className="mx-auto max-h-96 rounded-lg"
                      />
                    ) : (
                      <div className="flex flex-col items-center justify-center py-12 text-gray-500">
                        <FileIcon className="mb-4 h-24 w-24" />
                        <p>Forhåndsvisning ikke tilgjengelig for denne filtypen</p>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex flex-wrap gap-2">
                    <Button
                      variant="secondary"
                      size="medium"
                      leftIcon={<Edit2 className="h-5 w-5" />}
                      onClick={() => startEdit(previewDocument)}
                    >
                      Rediger
                    </Button>
                    <Button
                      variant="secondary"
                      size="medium"
                      leftIcon={<Download className="h-5 w-5" />}
                      onClick={() => handleDownload(previewDocument)}
                    >
                      Last ned
                    </Button>
                    <Button
                      variant="destructive"
                      size="medium"
                      leftIcon={<Trash2 className="h-5 w-5" />}
                      onClick={() => handleDelete(previewDocument.id)}
                    >
                      Slett
                    </Button>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
