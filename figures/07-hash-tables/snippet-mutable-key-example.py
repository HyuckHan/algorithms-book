class StudentKey:
    def __init__(self, id):
        self.id = id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, StudentKey) and self.id == other.id
