from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QWidget, QFileDialog
from PyQt6.QtGui import QPixmap
import matplotlib.image as mpimg
from PyQt6.QtCore import Qt
import pandas as pd
import sqlite3
from sqlite3 import Error
import pyqtgraph as pg
import sys, os
 
class TableModel(QtCore.QAbstractTableModel):
 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
 
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()] #pandas's iloc method
            return str(value)
 
        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#F0F8FF')
 
    def rowCount(self, index):
        return self._data.shape[0]
 
    def columnCount(self, index):
        return self._data.shape[1]
     # Add Row and Column header
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

class AnotherWindow(QWidget):
    # create a customized signal 
    submitted = QtCore.pyqtSignal(str) # "submitted" is like a component name 
 
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('PySQLite_hw2_sub.ui', self)
        self.setGeometry(400, 80, 800, 600)
         
        # Signal
        self.pButton_back.setGeometry(0,0,5,5)
        self.pButton_back.clicked.connect(self.BackMainWin)

    def passInfo(self, title, Texttype, authorname, abstract, papertext, imgname):      #主程式要丟東西到副程式
        self.textBrowser_abstract.setText(abstract)
        self.textBrowser_all.setText(papertext)
        self.textBrowser_author.setText(authorname)
        self.label_type.setText(Texttype)
        self.label_title.setText(title)

        image = mpimg.imread(r"./Database/NIP2015_Images/" + imgname)
        img_item = pg.ImageItem(image, axisOrder='row-major')
        self.graphicsView.addItem(img_item)
        self.graphicsView.invertY(True)
        self.graphicsView.hideAxis('left')
        self.graphicsView.hideAxis('bottom')
        self.graphicsView.setBackground('w')
        
     
    def BackMainWin(self):
        self.close()
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super().__init__()
        uic.loadUi('PySQLite_hw2.ui', self)
        self.setGeometry(300, 50, 620, 620)
        self.table = self.tableView
        
        #目前頁
        self.pageNum = 1
        #總筆數
        self.dataCount = 0
        #每頁顯示筆數
        self.PageShowCount = 10
        self.lst = []

        database = r"./Database/database.sqlite"
        # create a database connect
        self.conn = create_connection(database)
        self.setWindowTitle('Paper Query System')
 
        # Signals
        self.actionEXIT.triggered.connect(self.appEXIT)
        self.pBut_query.clicked.connect(self.searchData)
        self.table.doubleClicked.connect(self.rowSelected)
        self.actionSave_Data.triggered.connect(self.saveData)
        self.cBox_page.currentIndexChanged.connect(self.PageChange)
        self.pButton_pre.clicked.connect(self.PrePage)
        self.pButton_next.clicked.connect(self.NextPage)
        self.pButton_first.clicked.connect(self.firstPage)
        self.pButton_last.clicked.connect(self.lastPage)
        

    # Slots
    def searchData(self):
        self.cBox_page.clear()
        name_key = self.lineEdit_name.text()
        title_key = self.lineEdit_title.text()
        type_text = self.cBox_type.currentText()
        
        sql = "select id, title, eventtype, abstract, papertext, imgfile"
        if type_text != "ALL":
            #搜尋標題名，作者名為空值
            if (name_key == "") and (title_key != ""):
                sql = sql + " from papers where (title like '% " + title_key + "%') and (eventtype = '" + type_text +"')"
            #搜尋作者名，標題為空值
            if (name_key != "") and (title_key == ""):
                sql = "select B.id, title, eventtype, abstract, B.papertext, B.imgfile" + " from paperauthors A, papers B where (A.authorid in (select id \
                from authors where name like '%" + name_key +"%')" + "and A.paperid = B.id ) and (B.eventtype = '" + type_text + "')" 
            #作者及標題均不為空值
            if (name_key != "") and (title_key != ""):
                sql = "select B.id, title, eventtype, abstract, B.papertext, B.imgfile" + " from paperauthors A, papers B where (A.authorid in (select id \
                from authors where name like '%" + name_key + "%')" + "and A.paperid = B.id ) and (B.title like '% " + title_key + "%')" + \
                "and (B.eventtype = '" + type_text + "')"  

        if type_text == "ALL":
            #搜尋標題名，作者名為空值
            if (name_key == "") and (title_key != ""):
                sql = sql + " from papers where (title like '% " + title_key + "%') "
            #搜尋作者名，標題為空值
            if (name_key != "") and (title_key == ""):
                sql = "select B.id, title, eventtype, abstract, B.papertext, B.imgfile" + " from paperauthors A, papers B where (A.authorid in (select id \
                from authors where name like '%" + name_key +"%')" + "and A.paperid = B.id )" 
            #作者及標題均不為空值
            if (name_key != "") and (title_key != ""):
                sql = "select B.id, title, eventtype, abstract, B.papertext, B.imgfile" + " from paperauthors A, papers B where (A.authorid in (select id \
                from authors where name like '%" + name_key + "%')" + "and A.paperid = B.id ) and (B.title like '% " + title_key + "%')" 


        with self.conn:
            self.rows = SQLExecute(self, sql)
            if len(self.rows) > 0: 
                self.pageNum = 1
                showPage(self, self.rows, self.pageNum) #
                self.label_dataCount.setText("資料筆數：" + str(self.dataCount))
                self.label_totalPage.setText("/ 總共 " + str(getTotalPageCount(self)) + " 頁" )
                self.label_nowpage.setText("目前頁數：" + str(self.pageNum))
                self.lst = [str(i) for i in list(range(1, getTotalPageCount(self) + 1))]
                self.cBox_page.addItems(self.lst)
            if len(self.rows) == 0:
                display_message("No data found for this query!")
                return

    def firstPage(self):
        self.pageNum = 1
        showPage(self, self.rows, self.pageNum) #
        self.label_nowpage.setText("目前頁數：" + str(self.pageNum))
    
    def lastPage(self):
        self.pageNum = getTotalPageCount(self)
        showPage(self, self.rows, self.pageNum) 
        self.label_nowpage.setText("目前頁數：" + str(self.pageNum))
    
    def NextPage(self):
        if self.dataCount < 10:
            self.pageNum = 1
        elif self.pageNum == getTotalPageCount(self):
            self.pageNum = getTotalPageCount(self)
        else:
            self.pageNum += 1
        showPage(self, self.rows, self.pageNum) 
        self.label_nowpage.setText("目前頁數：" + str(self.pageNum))
    
    def PrePage(self):
        if self.pageNum <= 1:
            showPage(self, self.rows, 1)    
        else : 
            self.pageNum -= 1
        showPage(self, self.rows, self.pageNum) 
        self.label_nowpage.setText("目前頁數：" + str(self.pageNum))
    
    def PageChange(self):
        if self.cBox_page.currentText() != '':
            self.pageNum = int(self.cBox_page.currentText())
            showPage(self, self.rows, self.pageNum) 
            self.label_nowpage.setText("目前頁數：" + str(self.pageNum))

    def rowSelected(self, mi):
        self.anotherwindow = AnotherWindow()
        col_list = list(self.df.columns)       
        rowCount = (self.pageNum - 1) * 10 + mi.row()
        abstract = self.df.iloc[rowCount, col_list.index('Abstract')]
        title = self.df.iloc[rowCount, col_list.index('Title')]
        Texttype = self.df.iloc[rowCount, col_list.index('EventType')]
        authorname = show_authors(self, self.df.iloc[rowCount, 0])
        papertext = self.df.iloc[rowCount, col_list.index('PaperText')]
        imgname = self.df.iloc[rowCount, col_list.index('imgfile')]

        self.anotherwindow.passInfo(title, Texttype, authorname, abstract, papertext, imgname)   
        self.anotherwindow.show()
 
    
    def saveData(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 
            "", "EXCEL files (*.xlsx)")
        if len(fname) != 0:
            self.df.to_excel(fname)
 
    def appEXIT(self):
        self.conn.close() # close database
        self.close() # close app
     
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn



def SQLExecute(self, SQL):
    """
    Execute a SQL command
    :param conn: SQL command
    :return: None
    """
    self.cur = self.conn.cursor()
    try:
        self.cur.execute(SQL)
    except Error as e:
        display_message(str(e))
        # return None
    
    self.cur.execute(SQL)
    rows = self.cur.fetchall()
    return rows

def display_message(message):
    dlg = QMessageBox()
    dlg.setWindowTitle("SQL Information: ")
    dlg.setText(message)
    dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
    buttonY = dlg.button(QMessageBox.StandardButton.Yes)
    buttonY.setText('OK')
    dlg.setIcon(QMessageBox.Icon.Information)
    dlg.exec()

def showPage(self, rows, pageNum):  #
    self.names = [description[0] for description in self.cur.description]   # extract column names
    self.df = pd.DataFrame(rows)
    self.df.columns = self.names
    self.df.index = range(1, len(rows)+1)
    start = (pageNum - 1) * self.PageShowCount
    end = pageNum * self.PageShowCount - 1
    self.PageData = self.df[start:end+1]
    self.model = TableModel(self.PageData)
    self.table.setModel(self.model)
    self.table.resizeColumnToContents(0)
    self.dataCount = self.df.shape[0]
    
#獲得資料總筆數
def getDataCount(self):
    self.dataCount = self.df.shape[0]
    return self.dataCount

#獲得頁數
def getTotalPageCount(self):
    if self.df.shape[0] % self.PageShowCount == 0:
        return (self.df.shape[0] / self.PageShowCount) 
    else:
        return (self.df.shape[0] // self.PageShowCount + 1)

#執行獲得作者名的SQL程式碼
def SQLExecuteName(self, SQLname):
    """
    Execute a SQL command
    :param conn: SQL command
    :return: None
    """
    self.cur_ = self.conn.cursor()
    self.cur_.execute(SQLname)
    rows_names = self.cur_.fetchall()
    return rows_names


def show_authors(self, paperid):
    sql_author = "select name from authors A, paperauthors B where B.paperid=" + str(paperid) + " and A.id=B.authorid"
    with self.conn:
        self.rows_names = SQLExecuteName(self, sql_author)
        authornames =""
        for row in self.rows_names:
            authornames = authornames + row[0] +"; "
    return authornames
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()