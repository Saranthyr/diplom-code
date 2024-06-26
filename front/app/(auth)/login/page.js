"use client";

import { Button } from "@/components/button";
import { Heading } from "@/components/heading";
import { Input } from "@/components/input";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import jwt_decode from "jwt-decode";

export default function Login() {
  const router = useRouter();
  const {
    register,
    handleSubmit,
    formState: { isValid, isDirty },
  } = useForm();

  const onSubmit = async (data) => {
    const form = new FormData();
    form.append("username", data.email);
    form.append("password", data.password);

    const res = await fetch("/auth/login", {
      method: "POST",
      body: form,
    });

    if (res.ok) {
      const { access_token, refresh_token } = await res.json();
      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);

      router.push("/");
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="flex flex-col items-center gap-8 bg-custom-lightblue p-16 rounded-[20px] min-w-[328px] box-content"
    >
      <Heading>Вход в личный кабинет</Heading>
      <div className="flex flex-col gap-6 w-full">
        <Input
          {...register("email", { required: true })}
          type="email"
          label="E-mail"
          placeholder="name@example.ru"
          inputClassName="bg-white"
        />
        <Input
          {...register("password", { required: true })}
          type="password"
          label="Пароль"
          placeholder="Введите..."
          inputClassName="bg-white"
        />
      </div>
      <div className="flex flex-col gap-4 w-full">
        <Button type="submit" disabled={!isDirty | !isValid}>
          Войти
        </Button>
        <Link
          href="/register"
          className="self-center hover:underline font-semibold text-sm"
        >
          или Зарегистрируйтесь
        </Link>
      </div>
    </form>
  );
}
