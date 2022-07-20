from typing import Generator

def fib(k: int) -> Generator[int, None, None]:
    x, y = 0, 1
    yield x

    while True:
        yield y
        x, y = y * k, x + y

def mortal_fib(m: int) -> Generator[int, None, None]:
    ages = [1] + [0] * (m-1)

    while True:
        yield sum(ages)
        ages = [sum(ages[1:])] + ages[:-1]
