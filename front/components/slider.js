"use client";

import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { IoArrowBack } from "react-icons/io5";
import { twMerge } from "tailwind-merge";

export const CustomSlider = ({
  children,
  buttonsWithBg = true,
  slidesToShow = 4,
}) => {
  const NextArrow = ({ onClick }) => {
    return (
      <button
        type="button"
        onClick={onClick}
        className={twMerge(
          "w-fit p-1 rounded-lg  absolute left-4 top-1/2 transform -translate-y-1/2 z-10",
          buttonsWithBg ? "bg-custom-blue text-white" : "text-gray-600"
        )}
      >
        <IoArrowBack size={26} />
      </button>
    );
  };

  const PrevArrow = ({ onClick }) => {
    return (
      <button
        type="button"
        onClick={onClick}
        className={twMerge(
          "w-fit p-1 rounded-lg  absolute right-4 top-1/2 transform -translate-y-1/2 z-10 rotate-180",
          buttonsWithBg ? "bg-custom-blue text-white" : "text-gray-600"
        )}
      >
        <IoArrowBack size={26} />
      </button>
    );
  };

  const settings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToScroll: 1,
    slidesToShow,
    centerMode: true,
    prevArrow: <NextArrow />,
    nextArrow: <PrevArrow />,
  };

  return (
    <div className="relative">
      <Slider {...settings}>{children}</Slider>
    </div>
  );
};
