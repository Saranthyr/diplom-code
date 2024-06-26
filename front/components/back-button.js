"use client";

import { useRouter } from "next/navigation";
import { IoArrowBack } from "react-icons/io5";
import { twMerge } from "tailwind-merge";

export const BackButton = ({ onClick, className }) => {
  const router = useRouter();
  return (
    <button
      onClick={onClick ?? router.back}
      className={twMerge(
        "flex items-center gap-2 hover:underline font-semibold",
        className
      )}
    >
      <IoArrowBack size={16} />
      Назад
    </button>
  );
};
