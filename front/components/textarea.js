import { forwardRef } from "react";
import { twMerge } from "tailwind-merge";

export const Textarea = forwardRef(
  ({ label, required, inputClassName, ...props }, ref) => {
    return (
      <label className="flex flex-col w-full gap-1">
        <span className="pl-4 text-sm">
          {label}
          {required && <span className="text-red-500">*</span>}
        </span>
        <textarea
          ref={ref}
          required={required}
          className={twMerge(
            "px-4 py-3 border rounded-[10px] font-semibold bg-custom-lightblue",
            inputClassName
          )}
          {...props}
        />
      </label>
    );
  }
);
Textarea.displayName = "Textarea";
