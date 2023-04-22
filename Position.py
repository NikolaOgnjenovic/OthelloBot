class Position(object):
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __eq__(self, other: object):
        if isinstance(other, Position):
            return self.row == other.row and self.column == other.column
        return False

    def __hash__(self):
        return 8 * self.row + self.column

    def __str__(self):
        return chr(self.column + ord('A')) + ' ' + str(self.row + 1)