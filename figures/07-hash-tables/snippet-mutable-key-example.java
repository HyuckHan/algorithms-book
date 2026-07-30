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
