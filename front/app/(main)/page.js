"use client";

import { PostCard } from "@/components/post-card";
import { CustomSlider } from "@/components/slider";
import { TourismCard } from "@/components/tourism-card";
import { useEffect, useState } from "react";
import Link from "next/link";

export default function Home() {
  const [newPosts, setNewPosts] = useState([]);
  const [popularPosts, setPopularPosts] = useState([]);

  useEffect(() => {
    fetch(
      "/search/posts?order_by=created_at&rating=0&way=desc&page=1&draft=false&archived=false",
      {
        method: "POST",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          author: [],
          approved: [1, 2, 3],
          tourism_type: [],
          region: [],
        }),
      }
    ).then((res) => {
      res.json().then((data) => {
        setNewPosts(data);
      });
    });
    fetch(
      "/search/posts?order_by=raiting&rating=0&way=desc&page=1&draft=false&archived=false",
      {
        method: "POST",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          author: [],
          approved: [1, 2, 3],
          tourism_type: [],
          region: [],
        }),
      }
    ).then((res) => {
      res.json().then((data) => {
        setPopularPosts(data);
      });
    });
  }, []);

  return (
    <div className="flex flex-col gap-8 py-8">
      <h1 className="uppercase text-custom-main text-7xl font-bold text-center">
        Внутренний туризм
      </h1>

      <CustomSlider>
        {popularPosts.map((post) => (
          <Link href={"/article/" + post.id} key={post.id}>
            <TourismCard className="max-w-80" {...post} />
          </Link>
        ))}
      </CustomSlider>

      <div className="">
        <h2 className="uppercase text-4xl font-semibold px-4">Новые статьи</h2>
        <CustomSlider buttonsWithBg={false} slidesToShow={3}>
          {newPosts.map((post) => (
            <Link href={"/article/" + post.id} key={post.id}>
              <PostCard post={post} />
            </Link>
          ))}
        </CustomSlider>
      </div>
    </div>
  );
}
