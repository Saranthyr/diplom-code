import { twMerge } from "tailwind-merge";

export const TabButton = ({ children, active, type = "button", ...props }) => {
  return (
    <button
      className={twMerge(
        "font-semibold text-xl hover:text-blue-600 transition-colors",
        active &&
          "underline decoration-blue-600 decoration-4 underline-offset-4 text-blue-600"
      )}
      type={type}
      {...props}
    >
      {children}
    </button>
  );
};
