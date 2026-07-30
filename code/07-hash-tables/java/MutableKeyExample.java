import java.util.HashMap;
import java.util.Map;

/** lecture-notes/code/lecture07/java/MutableKeyExample.java와 같은 실패 사례
 * (hash/equality-relevant field를 key가 table 안에 있는 동안 mutate) -- 실제 관찰
 * 결과를 print하도록 main만 바꿨다(원본은 assert만 쓰는데, run_examples.py는
 * assertions 없이 java를 실행하므로 대신 값을 출력해 확인한다). */
public final class MutableKeyExample {
    // snippet:mutable-key-example:start
    static final class StudentKey {
        int id;

        StudentKey(int id) {
            this.id = id;
        }

        @Override
        public int hashCode() {
            return Integer.hashCode(id);
        }

        @Override
        public boolean equals(Object obj) {
            return obj instanceof StudentKey other
                    && id == other.id;
        }
    }
    // snippet:mutable-key-example:end

    public static void main(String[] args) {
        Map<StudentKey,String> map = new HashMap<>();
        StudentKey key = new StudentKey(10);
        map.put(key, "Ada");
        System.out.println("size after put: " + map.size());

        key.id = 20; // dangerous: hash/equality-relevant mutation

        System.out.println("size after mutation: " + map.size());
        System.out.println("get(mutatedKey): " + map.get(key));
        System.out.println("get(new StudentKey(10)): " + map.get(new StudentKey(10)));
        System.out.println("get(new StudentKey(20)): " + map.get(new StudentKey(20)));
    }
}
