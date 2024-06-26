"use client";

import Link from "next/link";
import { twMerge } from "tailwind-merge";
import { HeaderLink } from "@/components/header-link";
import { redirect } from "next/navigation";
import { useState, useEffect } from "react";

const HeaderSection = ({ children, className }) => {
  return (
    <div className={twMerge("flex items-center gap-[33px]", className)}>
      {children}
    </div>
  );
};

export const Header = () => {
  const [isAuthorized, setIsAuthorized] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setIsAuthorized(!!token);
  }, []);

  return (
    <header className="w-full">
      <div className="container mx-auto grid grid-cols-[1fr_minmax(900px,_1fr)_1fr] h-[72px] max-w-[1440px] px-[16px] font-semibold text-xs uppercase">
        <HeaderSection>
          <Link href="/" className="px-[15px]">
            Лого
          </Link>
          <HeaderLink href="/internal-tourism">Внутренний туризм</HeaderLink>
        </HeaderSection>
        <HeaderSection className="justify-center">
          <Link href="/regions" className="text-gray-700 hover:text-blue-500">
            РЕГИОНЫ
          </Link>
          <Link
            href="/type-of-tourism"
            className="text-gray-700 hover:text-blue-500"
          >
            ТИП ТУРИЗМА
          </Link>
          <Link href="/authors" className="text-gray-700 hover:text-blue-500">
            АВТОРЫ
          </Link>
          <form
            action={(data) => {
              const request = data.get("search");
              redirect(`/search-page` + (request ? `?request=${request}` : ""));
            }}
          >
            <input
              type="text"
              name="search"
              placeholder="Поиск"
              className="p-2.5 border rounded-[10px] text-sm normal-case font-normal"
            />
          </form>
        </HeaderSection>
        <HeaderSection className="justify-end">
          {isAuthorized ? (
            <Link href="/profile">
              <div className="w-12 h-12 bg-custom-gray rounded-full"></div>
            </Link>
          ) : (
            <Link
              href="/login"
              className="bg-blue-500 px-4 py-3.5 text-white rounded-[10px] text-sm normal-case font-normal"
            >
              Войти
            </Link>
          )}
        </HeaderSection>
      </div>
    </header>
  );
};
