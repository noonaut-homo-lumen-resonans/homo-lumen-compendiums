import React from "react";
import { cn } from "@/lib/utils";
import { ButtonVariant, ButtonSize } from "@/types";
import { Loader2 } from "lucide-react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

/**
 * Button Component
 *
 * Based on NAV-Losen Design System v1.0
 * Implements Triadisk Ethics with clear, accessible interactions
 *
 * @example
 * <Button variant="primary">Send søknad</Button>
 * <Button variant="secondary" size="small">Avbryt</Button>
 * <Button variant="text" leftIcon={<InfoIcon />}>Les mer</Button>
 */
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = "primary",
      size = "medium",
      isLoading = false,
      leftIcon,
      rightIcon,
      fullWidth = false,
      className,
      disabled,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          // Base styles
          "inline-flex items-center justify-center gap-2",
          "font-semibold rounded transition-all duration-200",
          "focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-primary)]",
          "disabled:opacity-50 disabled:cursor-not-allowed",
          fullWidth && "w-full",

          // Variant styles
          {
            // Primary button
            "bg-[var(--color-primary)] text-white hover:bg-[#0056A3] active:bg-[#004580] shadow-[var(--shadow-sm)]":
              variant === "primary",

            // Secondary button
            "bg-white text-[var(--color-primary)] border-2 border-[var(--color-primary)] hover:bg-gray-50 active:bg-gray-100":
              variant === "secondary",

            // Text button
            "bg-transparent text-[var(--color-primary)] underline hover:text-[#0056A3] active:text-[#004580]":
              variant === "text",

            // Destructive button
            "bg-[var(--color-error)] text-white hover:bg-red-600 active:bg-red-700 shadow-[var(--shadow-sm)]":
              variant === "destructive",
          },

          // Size styles
          {
            "px-4 py-2 text-sm h-8": size === "small",
            "px-6 py-3 text-base h-10": size === "medium",
            "px-8 py-4 text-lg h-12": size === "large",
          },

          className
        )}
        {...props}
      >
        {isLoading && (
          <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
        )}
        {leftIcon && !isLoading && (
          <span className="flex-shrink-0" aria-hidden="true">
            {leftIcon}
          </span>
        )}
        <span>{children}</span>
        {rightIcon && !isLoading && (
          <span className="flex-shrink-0" aria-hidden="true">
            {rightIcon}
          </span>
        )}
      </button>
    );
  }
);

Button.displayName = "Button";

export default Button;
