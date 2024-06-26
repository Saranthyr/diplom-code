import { PiTelegramLogo } from "react-icons/pi";
import { BsGeoAlt } from "react-icons/bs";
import { twMerge } from "tailwind-merge";
import { MdOutlineStickyNote2 } from "react-icons/md";
import { CiCalendar } from "react-icons/ci";
import { PostCard } from "@/components/post-card";
import Link from "next/link";

const IconWrapper = ({ children, className }) => (
  <div
    className={twMerge(
      "p-2 rounded-full shrink-0 bg-blue-200 text-blue-600 w-fit h-fit",
      className
    )}
  >
    {children}
  </div>
);

const InfoItem = ({ icon, children }) => (
  <div className="flex gap-2 items-center text-sm font-semibold">
    <IconWrapper>{icon}</IconWrapper>
    <span>{children}</span>
  </div>
);

export default function AuthorPage() {
  return (
    <div className="flex flex-col items-center gap-8 p-4">
      <div className="rounded-3xl bg-custom-lightblue w-full max-w-4xl overflow-hidden">
        <div className="flex-1 bg-custom-bg bg-cover bg-center h-56"></div>
        <div className="p-8 flex flex-col gap-8">
          <div className="flex gap-8">
            <div className="w-60 shrink-0">
              <div className="w-60 h-60 bg-custom-gray rounded-full -translate-y-36 shrink-0 absolute">
                <div className="bg-white w-12 h-12 rounded-full flex items-center justify-center font-semibold text-xl absolute right-4">
                  4,9
                </div>
              </div>
            </div>
            <div className="flex flex-col gap-2 font-semibold">
              <span className="text-4xl leading-none">
                Константин Константинопольский
              </span>
              <span className="text-xl leading-none">@const-const</span>
            </div>
          </div>
          <div className="flex gap-8">
            <p className="font-semibold text-sm">
              Привет, путешественники! Я - ваш проводник в мир приключений и
              открытий. Я - тревел блогер, стремящийся делиться своими
              незабываемыми путешествиями и впечатлениями с вами. Каждый новый
              день для меня - это возможность погрузиться в новую культуру,
              исследовать удивительные уголки планеты и встречать удивительных
              людей. Мой блог - это не просто набор фотографий и описаний мест,
              которые я посетил, это настоящая история моих приключений, эмоций
              и открытий.
            </p>
            <div className="shrink-0 flex flex-col gap-8 max-w-64">
              <IconWrapper className="p-4">
                <PiTelegramLogo size={32} />
              </IconWrapper>
              <div className="flex flex-col gap-2">
                <InfoItem icon={<BsGeoAlt size={16} />}>
                  Ханты-Мансийский автономный округ - Югра
                </InfoItem>
                <InfoItem icon={<MdOutlineStickyNote2 size={16} />}>
                  38 постов
                </InfoItem>
                <InfoItem icon={<CiCalendar size={16} />}>
                  с 12.02.2012
                </InfoItem>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="flex flex-col gap-5">
        <div className="flex gap-6 font-semibold self-center">
          <button className="underline decoration-blue-600 decoration-4 underline-offset-4">
            Все посты
          </button>
          <button>Популярные</button>
          <button>Новые</button>
        </div>
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5].map((item) => (
            <Link key={item} href={"/article/" + item}>
              <PostCard className="w-72" footer={false} />
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
