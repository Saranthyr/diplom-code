"use client";

import { BackButton } from "@/components/back-button";
import { Button } from "@/components/button";
import { Heading } from "@/components/heading";
import { Input } from "@/components/input";
import { useForm } from "react-hook-form";
import { useState } from "react";

export default function Register() {
  const [stage, setStage] = useState(0);
  const confirmation = stage === 2;
  const password = stage === 1;
  const {
    register,
    handleSubmit,
    formState: { isDirty, isValid },
  } = useForm();

  const onSubmit = async (data) => {
    console.log(data);
    if (stage === 0) {
      setStage(1);
    }
    // "use server";
    // if (!confirmation && !password) {
    //   redirect("/register?confirmation=true");
    // } else if (confirmation) {
    //   redirect("/register?password=true");
    // }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="flex flex-col items-center gap-8 bg-custom-lightblue p-16 rounded-[20px] w-[328px] box-content"
    >
      <div className="flex flex-col gap-4 w-full">
        <BackButton />
        <Heading className="self-center text-center">
          {confirmation
            ? "Мы отправили письмо с кодом для подтверждения регистрации на почту"
            : password
            ? "Придумайте пароль"
            : "Регистрация"}
        </Heading>
      </div>
      <div className="flex flex-col gap-6 w-full">
        {confirmation ? (
          <Input
            key={1}
            name="code"
            required
            label="Введите код"
            placeholder="000 000"
            inputClassName="bg-white"
          />
        ) : password ? (
          <>
            <Input
              {...register("password")}
              type="password"
              required
              label="Пароль"
              placeholder="Введите..."
              inputClassName="bg-white"
            />
            <Input
              {...register("password_repeat")}
              type="password"
              required
              label="Повторите пароль"
              placeholder="Введите..."
              inputClassName="bg-white"
            />
          </>
        ) : (
          <>
            <Input
              {...register("first_name", { required: true })}
              required
              label="Имя"
              placeholder="Введите..."
              inputClassName="bg-white"
            />
            <Input
              {...register("last_name", { required: true })}
              required
              label="Фамилия"
              placeholder="Введите..."
              inputClassName="bg-white"
            />
            <Input
              {...register("nickname", { required: true })}
              required
              label="Никнейм"
              placeholder="Введите..."
              inputClassName="bg-white"
            />
            <div className="w-full border-b border-custom-gray"></div>
            <div className="flex flex-col gap-1">
              <Input
                {...register("username", { required: true })}
                type="email"
                required
                label="E-mail"
                placeholder="name@example.ru"
                inputClassName="bg-white"
              />
              <span className="text-[10px] self-center">
                Мы отправим код на почту для подтверждения учётной записи{" "}
              </span>
            </div>
          </>
        )}
      </div>
      <Button type="submit">
        {password ? "Зарегистрироваться" : "Продолжить"}
      </Button>
    </form>
  );
}
