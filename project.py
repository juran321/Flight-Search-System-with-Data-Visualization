from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import database

d = database.DB('Scores.db')
list1 = d.getAss()
list2 = d.getLab()
list3 = d.getExam()
dic = d.getTarget()

class Ui_Dialog(object):
    def __init__(self):
        self.lst = ['HW', 'Lab', 'Exam']


    def setupUi(self, Dialog):
        #create a QTableWidget that can show the database
        self.table = QTableWidget(0,2,Dialog)
        #set up the size of table
        self.table.setMaximumHeight(370)
        self.table.setMinimumHeight(370)
        self.table.setMinimumWidth(400)
        self.table.setMinimumWidth(400)
        #set up the header
        self.table.setHorizontalHeaderLabels(['ID', 'Name'])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.move(10,40)
        #set up the default value
        d.cu.execute("select * from Students")
        student = d.cu.fetchall()
        index = 0
        for i in student:
            self.table.setRowCount(index + 1)
            self.table.setItem(index,0,QTableWidgetItem(str(i[0])))
            self.table.setItem(index, 1, QTableWidgetItem(str(i[1])))
            index += 1

        #set up name label and its line edit
        self.name = QLabel("name:",Dialog)
        self.name.move(10,10)
        self.le_name = QLineEdit(Dialog)
        self.le_name.setMinimumWidth(360)
        self.le_name.move(50,10)
        #call back when entering the student's name
        self.le_name.textChanged.connect(self.search)
        #set up target and score label
        self.le_target = QLineEdit(Dialog)
        self.le_target.setReadOnly(True)
        self.le_target.setText('60.0')
        self.le_target.move(500, 300)
        self.le_score = QLineEdit(Dialog)
        self.le_score.move(500, 330)
        self.target = QLabel('Target:', Dialog)
        self.target.move(450, 300)
        self.score = QLabel('Score:', Dialog)
        self.score.move(450, 330)
        #set up radioButton
        self.radio1 = QRadioButton('HW',Dialog)
        self.radio2 = QRadioButton('Lab', Dialog)
        self.radio3 = QRadioButton('Exam', Dialog)

        #callback when changing radio button
        self.radio1.clicked.connect(self.selectionchange1)
        self.radio2.clicked.connect(self.selectionchange2)
        self.radio3.clicked.connect(self.selectionchange3)

        self.box = QGroupBox('Type', Dialog)
        self.combobox = QComboBox(Dialog)
        self.combobox.setMaximumSize(190,100)
        self.combobox.move(450,60)
        self.combobox.addItems(list1)
        self.radio1.setChecked(True)
        self.vbox = QGridLayout()
        self.vbox.addWidget(self.radio1, 0, 0)
        self.vbox.addWidget(self.radio2, 0, 1)
        self.vbox.addWidget(self.radio3, 0, 2)

        self.box.setLayout(self.vbox)
        self.box.move(450, 0)

        self.combobox.currentIndexChanged.connect(self.change)
        self.button = QGridLayout()
        self.cancel = QPushButton('cancel', Dialog)
        self.save = QPushButton('save', Dialog)

        self.cancel.move(450, 380)
        self.save.move(550, 380)
        #callback funtion using in cancel and save button
        self.cancel.clicked.connect(self.reset)
        self.save.clicked.connect(self.input)
        Dialog.setGeometry(500, 500, 670, 430)
        Dialog.setWindowTitle('Main Windows')
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    #funtion that using when clicking cancel button
    def reset(self,i):
        self.le_score.setText('')
        self.le_name.setText('')

    #funtion that using when entering name
    def search(self,i):
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['ID', 'Name'])
        d.cu.execute("select * from Students where name like '%{0}%'".format(self.le_name.text()))
        student = d.cu.fetchall()
        index = 0
        for i in student:
            self.table.setItem(index, 0, QTableWidgetItem(str(i[0])))
            self.table.setItem(index, 1, QTableWidgetItem(str(i[1])))
            index += 1
    #function to insert score to database
    def input(self,i):
        name = self.table.currentItem().text()
        count = d.getCountScore()
        d.cu.execute("select ID from Students where name = '{0}'".format(name))
        stdid = d.cu.fetchall()
        studentId = stdid[0][0]
        score = self.le_score.text()
        assignment = self.combobox.currentText()
        d.cu.execute("select ID from Assignments where name = '{0}'".format(assignment))
        id = d.cu.fetchall()
        assignmentId = id[0][0]
        d.cu.execute("insert into Scores values({0}, {1}, {2},{3})".format(count+1, assignmentId, studentId, score))
        count += 1

    #change the content of combobox when changing different radio button
    def selectionchange1(self,i):
        self.combobox.clear()
        self.combobox.addItems(list1)
    def selectionchange2(self,i):
        self.combobox.clear()
        self.combobox.addItems(list2)
    def selectionchange3(self,i):
        self.combobox.clear()
        self.combobox.addItems(list3)
    def change(self,i):
        a = dic.get(self.combobox.currentText())
        self.le_target.setText(str(a))

    def on_reset(self,event):
        self.depart.clear()
        self.depart.addItems(list)
        self.destin.clear()
        self.destin.addItems(list)
        self.result.clear()
        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # print(cp)
        MainWindow.move(959,514)


    def on_search(self,event):
        location1 = self.depart.currentText()
        location2 = self.destin.currentText()
        self.error = errorMessage()
        if location1 == list[0] or location2 == list[0]:

            self.error.show()

        else:
            ans = g.getShortestPath(location1,location2)
            self.result.setText(ans)
    def on_click(self):
        self.se = errorMessage()
        self.se.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


class errorMessage(QWidget):
    def __init__(self):
        super(errorMessage, self).__init__()
        lbl = QLabel('Please select the city !', self)
        lyt1 = QHBoxLayout()
        lyt1.addWidget(lbl)
        self.setLayout(lyt1)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())