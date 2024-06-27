"use client";

import { PiTelegramLogo } from "react-icons/pi";
import { BsGeoAlt } from "react-icons/bs";
import { twMerge } from "tailwind-merge";
import { MdOutlineStickyNote2 } from "react-icons/md";
import { CiCalendar } from "react-icons/ci";
import { PostCard } from "@/components/post-card";
import Link from "next/link";
import { useEffect, useState } from "react";
import { updateToken } from "@/utils";

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
  const [user, setUser] = useState({});
  const [posts, setPosts] = useState([]);

  const fetchData = async () => {
    await updateToken();
    fetch("/user/", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("access_token"),
      },
    }).then((res) => {
      res.json().then((data) => {
        setUser(data);

        fetch(
          "/search/posts?order_by=rating&rating=0&way=desc&page=1&draft=false&archived=false",
          {
            method: "POST",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("access_token"),
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              author: [data.id],
              approved: [1, 2, 3],
              tourism_type: [],
              region: [],
            }),
          }
        ).then((res) => {
          res.json().then((data) => {
            setPosts(data);
          });
        });
      });
    });
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="flex flex-col items-center gap-8 p-4">
      <div className="rounded-3xl bg-custom-lightblue w-full max-w-4xl overflow-hidden">
        <div className="flex-1 bg-custom-bg bg-cover bg-center h-56"></div>
        <div className="p-8 flex flex-col gap-10">
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
                {`${user.first_name ?? ""} ${user.last_name ?? ""}`}
              </span>
              <span className="text-xl leading-none">@{user.nickname}</span>
            </div>
          </div>
          <div className="flex gap-8 justify-between">
            <p className="font-semibold text-sm">
              {user.about || "О себе не указано"}
            </p>
            <div className="shrink-0 flex flex-col gap-8 max-w-64">
              <IconWrapper className="p-4">
                <PiTelegramLogo size={32} />
              </IconWrapper>
              <div className="flex flex-col gap-2">
                <InfoItem icon={<BsGeoAlt size={16} />}>
                  {user.locationName || "Локация не указана"}
                </InfoItem>
                <InfoItem icon={<MdOutlineStickyNote2 size={16} />}>
                  {`${user.posts_total} пост${
                    user.posts_total === 1 ? "" : "ов"
                  }`}
                </InfoItem>
                <InfoItem icon={<CiCalendar size={16} />}>
                  с {new Date(user.created_at).toLocaleDateString("ru-RU")}
                </InfoItem>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="flex flex-col gap-5 w-full max-w-4xl">
        <div className="flex w-full justify-between items-center">
          <div className="flex gap-6 font-semibold self-center">
            <button className="underline decoration-blue-600 decoration-4 underline-offset-4">
              Все посты
            </button>
            <button>Популярные</button>
            <button>Новые</button>
          </div>
          <Link
            href="/new-article"
            className="bg-blue-500 px-24 py-3.5 text-white rounded-[10px] text-sm normal-case font-normal "
          >
            Новая статья
          </Link>
        </div>
        <div className="grid grid-cols-3 gap-4">
          {posts?.map((post) => (
            <Link key={post.id} href={"/article/" + post.id}>
              <PostCard post={post} className="w-72" footer={false} />
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
