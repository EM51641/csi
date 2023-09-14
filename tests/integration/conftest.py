import asyncio


def is_divisible_by_three(x: float):
    return x % 3 == 0


def is_all_positive(numbers: list[float]):
    return all(number > 0 for number in numbers)


def is_quotient_positive(x: float, y: float):
    return x / y > 0


async def async_is_divisible_by_three(x: float) -> bool:
    await asyncio.sleep(0.1)
    return is_divisible_by_three(x)


async def async_is_all_positive(numbers: list[float]) -> bool:
    await asyncio.sleep(0.1)
    return is_all_positive(numbers)
