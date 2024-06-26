import { twMerge } from "tailwind-merge";

export const Button = ({ children, className, disabled, ...props }) => {
  return (
    <button
      className={twMerge(
        "bg-blue-500 px-4 py-3.5 text-white rounded-[10px] text-sm normal-case font-normal disabled:bg-custom-grays",
        disabled && "bg-custom-gray",
        className
      )}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};
