from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt

class TableWidget(QTableWidget):
    def __init__(self, headers):
        super().__init__(0, len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.headers = headers
        self.setColumnCount(len(headers))
        self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def _clear(self):
        self.setRowCount(0)

    def _exsitsInColumn(self, fixed_col, val):
        rowCount = self.rowCount()
        itemRow = -1
        for row in range(rowCount):
            itemExists = self._exsits(row, fixed_col, val)
            if itemExists:
                itemRow = row
                break
      
        return itemRow

    def _exsits(self, row, col, val):
        ex = False
        item = self.item(row, col)
        if item != None:
            if isinstance(val, int):
                if int(item.text()) == val:
                    ex = True
            elif item.text() == val:
                ex = True
        return ex
                
    def _addRow(self, new_row):
        if len(new_row) == len(self.headers):
            col_index = 0
            rowCount = self.rowCount()
            self.insertRow(rowCount)
            #self.setRowCount(rowCount + 1)
            for i,val in enumerate(new_row):
                item = QTableWidgetItem(str(val))
                item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                if i != 1:
                    item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.setItem(rowCount, col_index, item)
                col_index += 1

    def _get_all_rows(self):
        rowCount = self.rowCount()
        rows = []
        for row in range(rowCount):
            row_data = tuple(self._getRow(row))
            rows.append(row_data)
        return rows

    def _get_col_values(self, col):
        rowCount = self.rowCount()
        values = []
        for row in range(rowCount):
            val = self._get_value(row, col)
            values.append({'row': row, 'value': val})
        return values

    def _get_value(self, row, col):
        return self.item(row, col).text()
        
    def _getRow(self, row):
        data = []
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item != None:
                data.append(item.text())
        return data

    def _checkRowChange(self, row, new_row):
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item.text() != new_row[col]:
                item.setText(new_row[col])

    def _setValue(self, row, col, value):
        item = self.item(row, col)
        item.setText(value)

    def _getByValue(self, col, value):
        rowCount = self.rowCount()
        rowToGet = self._exsitsInColumn(col, value)
        return self._getRow(rowToGet)

    def _removeRow(self, rowNum):
        if rowNum >= 0:
            self.removeRow(rowNum)

    def _copyRow(self, row_num):
        self.insertRow(self.rowCount())
        rowCount = self.rowCount()
        columnCount = self.columnCount()

        for j in range(columnCount):
            if not self.item(row_num, j) is None:
                self.setItem(rowCount-1, j, QTableWidgetItem(self.item(row_num, j).text()))

    def _to_bottom(self, row):
        self._copyRow(row)
        self._removeRow(row)
        
    def _moveDown(self, row):
        if row < self.rowCount() - 1:
            self.insertRow(row + 2)
            for col in range(self.columnCount()):
               #self.setItem(row + 1, col, self.takeItem(row, col))
               self.setItem(row + 2, col, QTableWidgetItem(self.item(row, col).text()))
            self.removeRow(row)        

    def _moveUp(self, row):   
        if row > 0:
            self.insertRow(row - 1)
            for col in range(self.columnCount()):
               # self.setItem(row - 1, col, self.takeItem(row, col))
               self.setItem(row - 1, col, QTableWidgetItem(self.item(row + 1, col).text()))
            self.removeRow(row + 1) 
