"use client";

import { forwardRef, useState } from "react";
import { twMerge } from "tailwind-merge";
import { IoChevronDown } from "react-icons/io5";

export const Selector = forwardRef(
  ({ label, options, required, selectorClassName, value, onChange }, ref) => {
    const [open, setOpen] = useState(false);

    return (
      <label className="flex flex-col w-full gap-1 relative">
        <span className="pl-4 text-sm">
          {label}
          {required && <span className="text-red-500">*</span>}
        </span>
        <div
          ref={ref}
          className={twMerge(
            "px-4 py-3 border rounded-[10px] font-semibold bg-custom-lightblue flex justify-between items-center cursor-pointer",
            selectorClassName
          )}
          onClick={() => setOpen(!open)}
        >
          {!!value ? value : <span className="text-black/40">Выберите</span>}
          <span
            className={twMerge(
              "transform transition-transform",
              open && "rotate-180"
            )}
          >
            <IoChevronDown />
          </span>
        </div>
        {open && !!options?.length && (
          <div className="absolute top-full mt-1 w-full z-10 bg-white border rounded-[10px]">
            {options.map((option) => (
              <div
                key={option.id}
                className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                onClick={() => {
                  onChange(option.id);
                  setOpen(false);
                }}
              >
                {option.name}
              </div>
            ))}
          </div>
        )}
      </label>
    );
  }
);
Selector.displayName = "Selector";
