import { BackButton } from "@/components/back-button";
import { Button } from "@/components/button";
import { Heading } from "@/components/heading";
import { Input } from "@/components/input";
import { redirect } from "next/navigation";

export default function Register({ searchParams }) {
  const confirmation = searchParams.confirmation === "true";
  const password = searchParams.password === "true";

  const handleSubmit = async () => {
    "use server";

    if (!confirmation && !password) {
      redirect("/register?confirmation=true");
    } else if (confirmation) {
      redirect("/register?password=true");
    }
  };

  return (
    <form
      action={handleSubmit}
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
              key={2}
              name="password"
              type="password"
              required
              label="Пароль"
              placeholder="Введите..."
              inputClassName="bg-white"
            />
            <Input
              key={3}
              name="oldPassword"
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
              key={4}
              required
              name="name"
              label="Имя"
              placeholder="Введите..."
              inputClassName="bg-white"
            />
            <Input
              key={5}
              required
              name="surname"
              label="Фамилия"
              placeholder="Введите..."
              inputClassName="bg-white"
            />
            <Input
              key={6}
              required
              name="nickname"
              label="Никнейм"
              placeholder="Введите..."
              inputClassName="bg-white"
            />
            <div className="w-full border-b border-custom-gray"></div>
            <div className="flex flex-col gap-1">
              <Input
                key={7}
                name="email"
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
