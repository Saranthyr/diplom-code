"use client";

import { Heading } from "@/components/heading";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { IoMdStar } from "react-icons/io";

export default function ArticlePage() {
  const params = useParams();
  const [post, setPost] = useState(null);

  useEffect(() => {
    console.log(params);
    fetch("/posts/" + params.id).then((res) => {
      res.json().then((data) => {
        setPost(data);
      });
    });
    fetch("/posts/" + params.id + "/comments", {
      // headers: {
      //   Authorization: "Bearer " + localStorage.getItem("access_token"),
      //   "Content-Type": "application/json",
      // },
    }).then((res) => {
      console.log(res);
    });
  }, []);

  return (
    <div className="flex flex-col items-center gap-16 p-4">
      <div className="rounded-3xl bg-custom-lightblue w-full max-w-4xl p-6 overflow-hidden flex flex-col gap-8">
        <Heading className="text-4xl leading-none">{post?.name}</Heading>
        <div className="w-full bg-custom-bg bg-cover bg-center h-96 rounded-xl"></div>
        <div className="flex flex-wrap font-semibold">
          {post?.tags.map((item, index) => (
            <span key={index} className="bg-white p-2 rounded-md">
              {item}
            </span>
          ))}
        </div>
        <div className="flex gap-6 justify-between">
          <p>{post?.header}</p>
          <div className="flex flex-col p-6 gap-5 rounded-md bg-blue-200 w-80 shrink-0">
            <div className="flex items-center gap-2">
              <span>Рейтинг:</span>
              <span>{post?.rating}</span>
              <div className="flex">
                {[0, 1, 2, 3, 4].map((item) => (
                  <IoMdStar key={item} size={16} />
                ))}
              </div>
            </div>
            <div className="flex gap-2">
              <span>Регион:</span>
              <span className="font-semibold">{post?.region?.[1]}</span>
            </div>
            <div className="flex gap-2">
              <span>Координаты:</span>
              <span className="font-semibold">
                {post?.coordinates?.join(" ")}
              </span>
            </div>
          </div>
        </div>
        <p>{post?.body}</p>
      </div>
    </div>
  );
}
