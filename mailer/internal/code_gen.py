class CodeGenerator:
    """Класс генератор кода"""

    def __init__(self, seed_limit: int = 5) -> None:
        """Конструктор класса

        Args:
            seed_limit (int, optional): Ограничение количества символов начального числа. По умолчанию - 5
        """
        self.seed_limit = seed_limit

    async def generate_seed(self, email: str) -> int:
        """Функция генерации начального числа

        Args:
            email (str): электронная почта пользователя

        Returns:
            int: начальное число
        """
        ords = []
        for i in email:
            ords.append(ord(i))
        res = str(sum(ords))
        res = res[::-1]
        if len(res) > self.seed_limit:
            res = str(int(res) // len(res))
            res = res[0 : self.seed_limit - 1]
        return int(res[::-1])

    async def generate_code(self, seed: int, epoch: int) -> int:
        """Функция генерации кода

        Args:
            seed (int): начальное число
            epoch (int): текущее время в формате UNIX epoch

        Returns:
            int: код
        """
        num1 = seed % 64
        num2 = epoch << num1
        num3 = epoch % seed
        num4 = str(abs((num2 << num3)))
        res_str = "".join([num4[-3:], num4[0:3]])
        if len(res_str) < 6:
            res_str = "".join(str(epoch)[-1:])
        return int(res_str)
