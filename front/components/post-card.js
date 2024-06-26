import { FaRegCommentDots } from "react-icons/fa";
import { TourismCard } from "./tourism-card";
import { twMerge } from "tailwind-merge";

export const PostCard = ({ raiting, name, className, footer = true }) => (
  <div
    className={twMerge(
      "bg-custom-lightblue p-4 rounded-md flex flex-col gap-3 w-96",
      className
    )}
  >
    <TourismCard raiting="4,9" />
    <div className="flex flex-wrap gap-2">
      {["Выборг", "История", "Замок", "Культура"].map((item, index) => (
        <span key={index} className="bg-white rounded-md p-1 text-xs">
          {item}
        </span>
      ))}
    </div>
    <div className="flex flex-col gap-2 h-32">
      <h3 className="font-bold">Выборгский замок</h3>
      <p className="text-sm">
        Средневековый замок в Выборге, до XVII века служил резиденцией шведских
        наместников, управлявших...
      </p>
    </div>
    <div className="flex justify-between text-xs">
      <span>Ленинградская область</span>
      <span>15.02.2024</span>
    </div>
    <div className="w-full border-t border-black"></div>
    {!!footer && (
      <div className="flex justify-between text-sm">
        <div className="flex gap-2 items-center">
          <div className="w-7 h-7 rounded-full bg-gray-300 shrink-0"></div>
          <div className="flex flex-col leading-none">
            <span>Юрий Долгорукий</span>
            <span className="font-light">@iv.iv</span>
          </div>
        </div>
        <div className="flex items-center self-end gap-0.5">
          <FaRegCommentDots size={16} />
          <span>65</span>
        </div>
      </div>
    )}
  </div>
);
