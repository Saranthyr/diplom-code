"use client";

import { Input } from "@/components/input";
import { Selector } from "@/components/selector";
import { Textarea } from "@/components/textarea";
import { BackButton } from "@/components/back-button";
import { Button } from "@/components/button";
import { Controller, useForm } from "react-hook-form";
import { MarkdownEditor } from "@/components/markdown-editor";
import { useState } from "react";
import { Heading } from "@/components/heading";
import { updateToken } from "@/utils";

export default function NewArticle() {
  const {
    control,
    register,
    handleSubmit,
    formState: { isDirty, isValid },
  } = useForm({
    defaultValues: {
      hashtags: [],
      content: "",
    },
  });

  const [stage, setStage] = useState(1);
  const [name, setName] = useState("");
  const [regions, setRegions] = useState([
    { id: 1, name: "Такой" },
    { id: 2, name: "Сякой" },
  ]);
  const [tourism, setTourism] = useState([
    { id: 1, name: "Такой" },
    { id: 2, name: "Сякой" },
  ]);

  const onSubmit = async (data) => {
    setName(data.title);
    if (stage === 1) {
      setStage(2);
    } else {
      const form = new FormData();
      form.append("name", data.title);
      form.append("header", data.description);
      form.append("thumbnail", data.image[0]);
      form.append("tourism_type", data.tourism_type);
      form.append("region", data.region);
      form.append("body", data.content);
      data.coordinates &&
        form.append("longitude", data.coordinates.split(" ")[0]);
      data.coordinates &&
        form.append("latitude", data.coordinates.split(" ")[1]);
      data.link && form.append("link", data.link);

      await updateToken();

      const res = await fetch("/posts/create", {
        method: "POST",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: form,
      });

      if (res.ok) {
        const response = await res.json();
        console.log(response);
      }
    }
  };

  return (
    <div className="flex flex-col items-center gap-11 p-4">
      {stage === 2 && (
        <BackButton onClick={() => setStage(1)} className="self-start" />
      )}
      <Heading className="uppercase text-4xl">
        {stage === 1 ? "Cоздать новую статью" : name}
      </Heading>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col max-w-4xl w-full gap-6"
      >
        {stage === 1 ? (
          <>
            <Input
              {...register("title")}
              required
              label="Введите название поста"
              placeholder="Введите..."
            />
            <Textarea
              {...register("description", { required: true })}
              required
              label="Введите короткое описание (для отображения на главной)"
              placeholder="Введите..."
              rows={3}
            />
            <label className="bg-blue-500 px-4 py-3.5 text-white rounded-[10px] text-sm w-fit cursor-pointer self-center">
              Выбрать основное фото
              <input
                type="file"
                id="imageUpload"
                accept="image/*"
                style={{ display: "none" }}
                {...register("image")}
              />
            </label>
            <div className="w-full border-t"></div>
            <Controller
              control={control}
              name="tourism_type"
              rules={{ required: true }}
              render={({ field }) => {
                return (
                  <Selector
                    {...field}
                    required
                    label="Выберите тип туризма"
                    options={tourism}
                    value={
                      tourism.find((option) => option.id === field.value)?.name
                    }
                  />
                );
              }}
            />
            <Controller
              control={control}
              name="hashtags"
              render={({ field }) => {
                const options = [
                  { id: 1, value: "Такой" },
                  { id: 2, value: "Сякой" },
                ];
                return (
                  <Selector
                    {...field}
                    label="Добавьте хэштеги"
                    options={options}
                    value={options
                      .filter((option) => field.value?.includes(option.id))
                      .map((option) => option.value)
                      .join(", ")}
                    onChange={(value) => {
                      if (field.value?.includes(value)) {
                        field.onChange(field.value.filter((v) => v !== value));
                      } else {
                        field.onChange([...field.value, value]);
                      }
                    }}
                  />
                );
              }}
            />
            <div className="w-full border-t"></div>
            <Controller
              control={control}
              name="region"
              rules={{ required: true }}
              render={({ field }) => {
                return (
                  <Selector
                    {...field}
                    required
                    label="Выберите регион"
                    options={regions}
                    value={
                      regions.find((option) => option.id === field.value)?.name
                    }
                  />
                );
              }}
            />
            <Input
              {...register("coordinates")}
              label="Координаты места"
              placeholder="Введите..."
            />
            <Input
              {...register("link")}
              label="Ссылка на Яндекс Картах"
              placeholder="Введите..."
            />
          </>
        ) : (
          <Controller
            control={control}
            name="content"
            render={({ field }) => (
              <MarkdownEditor {...field} markdown={field.value} />
            )}
          />
        )}
        <Button type="submit" disabled={!isDirty | !isValid}>
          {stage === 1 ? "Продолжить" : "Опубликовать"}
        </Button>
      </form>
    </div>
  );
}
