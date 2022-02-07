import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.a)
        self.pushButton_2.clicked.connect(self.b)
        self.titles = None

    def a(self):
        a = self.lineEdit.text()
        cur = self.con.cursor()
        result = cur.execute("""SELECT * FROM cof WHERE title = ?""", (a,)).fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def b(self):
        self.add = Add()
        self.add.show()


class Add(MyWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.cur = self.con.cursor()
        self.f()

        self.pushButton.clicked.connect(self.c)
        self.pushButton_2.clicked.connect(self.d)
        self.tableWidget.itemChanged.connect(self.e)

    def c(self):
        self.n += 1
        self.cur.execute("INSERT INTO cof VALUES (?, ?, ?, ?, ?, ?, ?)",
                         (self.n,
                          "title",
                          "roasting",
                          "grains",
                          "taste",
                          0,
                          0,))
        self.con.commit()
        self.f()

    def d(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE cof SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE ID = ?"
            print(que)
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()
        self.hide()

    def e(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def f(self):
        self.result = self.cur.execute("""SELECT * FROM cof""").fetchall()
        self.n = len(self.result)
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.titles = [description[0] for description in self.cur.description]
        for i, elem in enumerate(self.result):
            print(i)
            print(elem)
            for j, val in enumerate(elem):
                print(j)
                print(val)
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())