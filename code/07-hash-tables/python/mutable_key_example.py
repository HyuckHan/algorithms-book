"""code/07-hash-tables/java/MutableKeyExample.java와 같은 실패 사례
(hash/equality-relevant field를 key가 table 안에 있는 동안 mutate).
StudentKey는 Java 판의 같은 클래스를 옮긴 것이고, main도 같은 순서로
put -> mutate -> 세 lookup을 관찰값으로 출력한다."""


# snippet:mutable-key-example:start
class StudentKey:
    def __init__(self, id):
        self.id = id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, StudentKey) and self.id == other.id
# snippet:mutable-key-example:end


def fmt(v):
    return "not found" if v is None else v


if __name__ == "__main__":
    table = {}
    key = StudentKey(10)
    table[key] = "Ada"
    print("size after put:", len(table))

    key.id = 20  # dangerous: hash/equality-relevant mutation

    print("size after mutation:", len(table))
    print("get(mutatedKey):", fmt(table.get(key)))
    print("get(new StudentKey(10)):", fmt(table.get(StudentKey(10))))
    print("get(new StudentKey(20)):", fmt(table.get(StudentKey(20))))
