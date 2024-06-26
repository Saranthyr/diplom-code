import { twMerge } from "tailwind-merge";

export const Input = ({
  label,
  type = "text",
  placeholder,
  required,
  inputClassName,
}) => {
  return (
    <label className="flex flex-col w-full gap-1">
      <span className="pl-4 text-sm">
        {label}
        {required && <span className="text-red-500">*</span>}
      </span>
      <input
        type={type}
        placeholder={placeholder}
        required={required}
        className={twMerge(
          "px-4 py-3 border rounded-[10px] font-semibold bg-custom-lightblue",
          inputClassName
        )}
      />
    </label>
  );
};
