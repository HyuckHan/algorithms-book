"""Comparator/정렬 API 데모. Java Comparator.thenComparing 체이닝(FruitSorting.java)과
C qsort의 relational comparator(qsort_examples.c)와 같은 두 성질을 확인한다:
extreme-value 정수의 오름차순 정렬, 그리고 중복 key가 있는 다중 key 정렬의 stability.
Python은 comparator 대신 key= 함수가 관용구이므로 그 방식을 쓴다."""

from dataclasses import dataclass


def require(condition, message):
    assert condition, message


@dataclass(frozen=True)
class Fruit:
    name: str
    quantity: int

    def __repr__(self):
        return f"{self.name}:{self.quantity}"


def main():
    extremes = [2**63 - 1, 0, -(2**63), 0]
    extremes.sort()
    require(extremes == [-(2**63), 0, 0, 2**63 - 1], "primitive ascending order")

    descending = [-(2**63), 7, 2**63 - 1]
    descending.sort(reverse=True)
    require(descending == [2**63 - 1, 7, -(2**63)], "descending order")

    fruits = [
        Fruit("Pineapple", 70), Fruit("Apple", 100),
        Fruit("Orange", 80), Fruit("Banana", 90),
        Fruit("Apricot", 90), Fruit("Apple", 100),
    ]
    fruits.sort(key=lambda f: (f.quantity, f.name))
    require(
        [str(f) for f in fruits]
        == ["Pineapple:70", "Orange:80", "Apricot:90", "Banana:90", "Apple:100", "Apple:100"],
        "quantity/name multi-key order with duplicates",
    )

    print("comparator_demo tests passed")


if __name__ == "__main__":
    main()
