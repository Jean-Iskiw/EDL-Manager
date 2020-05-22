class TableModelInfo:
    def __init__(self, row = 10, col = 6):
        self.row_count = row
        self.col_count = col

class TableModel:

    def __init__(self, size=10):
        self._size = size
        self.data = []
        self.init_cache()

    def init_cache(self):
        for row in range(0, self._size):
            if len(self.data) < row+1:
                self.data.append([])

            for col in range(6):
                self.data[row].append("")

    def info(self):
        info = TableModelInfo(self._size, 6)
        return info

    def update_cell(self, row, col, value):
        self.data[row][col] = value
        return True

    def setRowCount(self, count):
        for row in range (0, count):
            if len(self.data) < row+1:
                self.data.append([])

            for col in range(0, 5):
                if self.data[row][col] == None:
                    self.data[row].append("")
        return count
