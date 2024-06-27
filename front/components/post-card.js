import { FaRegCommentDots } from "react-icons/fa";
import { TourismCard } from "./tourism-card";
import { twMerge } from "tailwind-merge";
import Image from "next/image";

export const PostCard = ({
  post: { name, header, raiting, hashtags, region, created_at, author },
  className,
  footer = true,
}) => (
  <div
    className={twMerge(
      "bg-custom-lightblue p-4 rounded-md flex flex-col gap-3 w-96",
      className
    )}
  >
    <TourismCard raiting={raiting} />
    <div className="flex flex-wrap gap-2">
      {hashtags.length > 0 &&
        hashtags.map((item, index) => (
          <span key={index} className="bg-white rounded-md p-1 text-xs">
            {item}
          </span>
        ))}
    </div>
    <div className="flex flex-col gap-2 h-32">
      <h3 className="font-bold">{name}</h3>
      <p className="text-sm">{header}</p>
    </div>
    <div className="flex justify-between text-xs">
      <span>{region.name}</span>
      <span>{new Date(created_at).toLocaleDateString()}</span>
    </div>
    <div className="w-full border-t border-black"></div>
    {!!footer && (
      <div className="flex justify-between text-sm">
        <div className="flex gap-2 items-center">
          {author.avatar ? (
            <Image
              src={author.avatar}
              alt=""
              className="w-7 h-7 rounded-full shrink-0"
            />
          ) : (
            <div className="w-7 h-7 rounded-full bg-gray-300 shrink-0"></div>
          )}
          <div className="flex flex-col leading-none">
            <span>
              {author.nickname || `${author.first_name} ${author.last_name}`}
            </span>
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
