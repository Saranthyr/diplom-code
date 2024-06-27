"use client";

import { BackButton } from "@/components/back-button";
import { PostCard } from "@/components/post-card";
import { TabButton } from "@/components/tab-button";
import { useEffect, useState } from "react";

export default function SearchPage({ searchParams }) {
  const request = searchParams.request;

  const [activeTab, setActiveTab] = useState("1");
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const url = new URL(window.location.href);
    url.searchParams.delete("request");
    !!request && url.searchParams.append("s", request);
    url.searchParams.append("typ", activeTab);

    fetch("http://localhost:5000/search/" + url.search).then(async (res) => {
      const postsResponse = await res.json();
      setPosts(postsResponse);
    });
  }, [activeTab, request]);

  return (
    <div className="flex flex-col p-4 gap-8">
      <BackButton />
      <h1 className="font-semibold text-4xl">
        Результаты по поиску {request && `“${request}”`}
      </h1>
      <div className="flex gap-6">
        <TabButton active={activeTab === "1"} onClick={() => setActiveTab("1")}>
          Посты
        </TabButton>
        <TabButton active={activeTab === "2"} onClick={() => setActiveTab("2")}>
          Регионы
        </TabButton>
        <TabButton active={activeTab === "3"} onClick={() => setActiveTab("3")}>
          Тип туризма
        </TabButton>
        <TabButton active={activeTab === "4"} onClick={() => setActiveTab("4")}>
          Авторы
        </TabButton>
      </div>
      <div>
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>
    </div>
  );
}
