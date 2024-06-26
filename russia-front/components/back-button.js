"use client";

import { useRouter } from "next/navigation";
import { IoArrowBack } from "react-icons/io5";

export const BackButton = () => {
  const router = useRouter();
  return (
    <button
      onClick={router.back}
      className="flex items-center gap-2 hover:underline font-semibold"
    >
      <IoArrowBack size={16} />
      Назад
    </button>
  );
};
