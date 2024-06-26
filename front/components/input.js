import { forwardRef } from "react";
import { twMerge } from "tailwind-merge";

export const Input = forwardRef(
  (
    { label, type = "text", placeholder, required, inputClassName, ...props },
    ref
  ) => {
    return (
      <label className="flex flex-col w-full gap-1">
        <span className="pl-4 text-sm">
          {label}
          {required && <span className="text-red-500">*</span>}
        </span>
        <input
          ref={ref}
          type={type}
          placeholder={placeholder}
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
Input.displayName = "Input";
