import { twMerge } from "tailwind-merge";

export const Heading = ({ children, className }) => {
  return (
    <h1 className={twMerge("text-2xl font-semibold leading-none", className)}>
      {children}
    </h1>
  );
};
