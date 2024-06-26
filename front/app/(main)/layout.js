import Link from "next/link";
import { HeaderLink } from "@/components/header-link";

export default function MainLayout({ children }) {
  return (
    <>
      <main className="flex flex-1 flex-col">{children}</main>
      <footer className="mt-32 py-8 flex flex-col px-4">
        <div className="flex flex-1 justify-between font-semibold text-base items-center px-24">
          <div className="uppercase flex flex-col items-center gap-8">
            <Link href="/" className="px-[15px]">
              Лого
            </Link>
            <HeaderLink href="/internal-tourism">Внутренний туризм</HeaderLink>
          </div>
          <div className="flex space-x-32">
            <div className="flex flex-col gap-4">
              <HeaderLink href="/regions">Регионы</HeaderLink>
              <HeaderLink href="/type-of-tourism">Тип туризма</HeaderLink>
              <HeaderLink href="/authors">Авторы</HeaderLink>
            </div>
            <div className="flex flex-col gap-4">
              <HeaderLink href="/profile">Личный кабинет</HeaderLink>
              <HeaderLink href="/support">Поддержка</HeaderLink>
            </div>
          </div>
        </div>
        <div className="border-t w-full mt-24"></div>
      </footer>
    </>
  );
}
