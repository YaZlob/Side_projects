import sys

from PyQt5 import QtWidgets

import window
from back import Main_part as bk
import add_in_file

class FirstlyWindow(QtWidgets.QMainWindow, window.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.back = bk()
        self.secondary_window = SecondaryWindow()

        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.resizeColumnsToContents()

        self.pushButton_1.clicked.connect(self.find_dishes)
        self.pushButton_2.clicked.connect(self.show_all)
        self.pushButton_3.clicked.connect(self.find_dishes_on_product)
        # show second window in Main Window
        self.pushButton_5.clicked.connect(self.qt_clear_table)

        self.pushButton_3.setToolTip("Вводить через запятую!")
        self.pushButton_4.setToolTip("После нажатия остальные данные будут потеряны!")
        self.pushButton_5.setToolTip("Удаляет все!")

    def standart_output(self, matrix):
        for row in range(len(matrix)):
            for column in range(4):
                text = matrix[row][column]
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(text))

    def qt_clear_table(self):
        self.tableWidget.setRowCount(0)
        self.lineEdit.clear()

    def find_dishes(self):
        dish = self.lineEdit.text()
        all_about_dish = self.back.find_dishes(dish)
        self.tableWidget.setRowCount(len(all_about_dish))
        self.standart_output(all_about_dish)

    def find_dishes_on_product(self):
        products = self.lineEdit.text().split(',')
        result = self.back.recommend(products)
        self.tableWidget.setRowCount(len(result))
        self.standart_output(result)
        self.lineEdit.clear()

    def show_all(self):
        dishes_list = self.back.show_all_dishes()
        # row count its max size in excel file
        self.tableWidget.setRowCount(self.back.max_size - 1)
        self.standart_output(dishes_list)
        self.tableWidget.resizeRowsToContents()

class SecondaryWindow(QtWidgets.QMainWindow, add_in_file.Ui_MainWindow_2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setFixedSize(383, 265)
        # show first window in main window
        self.pushButton_2.clicked.connect(self.add_in_file)

        self.back = bk()

    def add_in_file(self):
        temp=[]
        # append dish , recipe , product , time
        temp.append(self.lineEdit_6.text())
        temp.append(self.lineEdit_7.text())
        temp.append(self.lineEdit_5.text())
        temp.append(self.lineEdit_4.text())


        self.back.write_in_file(temp)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('MainWindow')
        self.w1 = FirstlyWindow()
        self.w2 = SecondaryWindow()

    def show_first_window(self):
        self.w1.show()
        self.w1.pushButton_4.clicked.connect(self.show_second_window)
        self.w1.pushButton_4.clicked.connect(self.w1.close)

    def show_second_window(self):

        self.w2.show()
        self.w2.pushButton_2.clicked.connect(self.show_first_window)
        self.w2.pushButton_2.clicked.connect(self.w2.close)

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show_first_window()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
