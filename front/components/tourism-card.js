import { twMerge } from "tailwind-merge";

export const TourismCard = ({ name, raiting, className }) => {
  return (
    <div
      className={twMerge(
        "w-full h-60 bg-gray-200 rounded-xl flex flex-col justify-between p-4",
        className
      )}
    >
      <div className="text-xs rounded-full p-2 bg-black bg-opacity-10 w-fit self-end">
        {raiting}
      </div>
      <span className="font-bold text-white text-base">{name}</span>
    </div>
  );
};
