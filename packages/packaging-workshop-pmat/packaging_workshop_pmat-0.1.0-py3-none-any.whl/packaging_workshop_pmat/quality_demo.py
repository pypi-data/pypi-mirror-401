def add(a: int, b: int) -> int:
    return a + b


def greet_all(names: list[str]) -> list[str]:
    results = []
    for n in names:
        if n is None:
            continue
        results.append("Hello, " + n)
    return results


def get_first(items: list[str]) -> str:
    return items[0]


def write_temp() -> None:
    f = open("tmp.txt", "w")
    f.write("hi")
    f.close()
