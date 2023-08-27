from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtWidgets import QMessageBox, QWidget, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from bs4 import BeautifulSoup
import pyqtgraph as pg
import pandas as pd
import numpy as np
import requests
import sys, json
from datetime import datetime
 
 
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
            # return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#CCE5FF')
 
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
 
            # if orientation == Qt.Orientation.Vertical:
            #     return str(self._data.index[section])
 
class MainWindow(QtWidgets.QMainWindow):

    # signal = pyqtSignal()
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        uic.loadUi('PyQt_hw03.ui', self)
        self.tabWidget.setCurrentIndex(0)
        # self.stock_date = self.lineEdit_year.text() + "01"
        # self.stock_no = self.lineEdit_company.text()
        # self.signal.connect(self.showStockNo)
        stock_no = '1234'

        # page1
        self.stock_price()
        self.pBut_query.clicked.connect(self.stock_price)
        self.table.doubleClicked.connect(self.rowSelected)
        self.pBut_export.clicked.connect(self.SaveTable)
        self.lineEdit_company.setText(stock_no)
        self.pBut_query.clicked.connect(lambda:self.showStockNo(self.lineEdit_company.text()))
        
        #page2
        # self.getInfo()
        self.pBut_info_query.clicked.connect(self.getInfo)

        #page3
        self.cBox_A.setChecked(True)
        self.cBox_B.setChecked(True)
        self.pBut_plot.clicked.connect(self.LinePlot_Y)
        self.pBut_plot.clicked.connect(self.LinePlot_PE)
        self.pBut_plot.clicked.connect(self.LinePlot_PBR)
        self.pBut_exitapp.clicked.connect(self.ExitApp)
        self.cBox_A.stateChanged.connect(self.LinePlot_Y)
        self.cBox_B.stateChanged.connect(self.LinePlot_Y)
        self.cBox_A.stateChanged.connect(self.LinePlot_PE)
        self.cBox_B.stateChanged.connect(self.LinePlot_PE)
        self.cBox_A.stateChanged.connect(self.LinePlot_PBR)
        self.cBox_B.stateChanged.connect(self.LinePlot_PBR)
     
    # Slot1
    def stock_price(self):
        stock_date = self.lineEdit_year.text() + "01"
        stock_no = self.lineEdit_company.text()
        url = f'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={stock_date}&stockNo={stock_no}&response=html'
        res = requests.get(url, cert = '', timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        title = soup.find_all("tr")  
        # table_name = title[0].find_all("th")[0].find_all("div")[0].text
        # self.table_name.setText(table_name)

        #查詢不到資料就跳出視窗
        if title == []:
            display_message("No data found for this query!")
        else : 
            table_name = title[0].find_all("th")[0].find_all("div")[0].text
            self.table_name.setText(table_name)
            headers = []
            for i in title[1].find_all("th"):
                headers.append(i.text)

            content = soup.find_all("tbody")
            tmp = content[0].find_all("td")
            deal_info = []
            for j in tmp:
                deal_info.append(j.text)

            deal_info = np.reshape(deal_info, (int(len(deal_info)/len(headers)), len(headers)))
            data = pd.DataFrame(deal_info, columns = headers)           
            self.model = TableModel(data)
            self.table.setModel(self.model)
            self.table.resizeColumnsToContents()
            # self.pBut_query.clicked.connect(lambda:self.showStockNo(stock_no))
            return data  #, stock_no

    def rowSelected(self, mi):
        self.anotherwindow = AnotherWindow()
        data = self.stock_price()
        date = self.lineEdit_year.text()
        self.anotherwindow.passInfo(data, date)   
        self.anotherwindow.show()

    def SaveTable(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 
            "", "EXCEL files (*.xlsx)")
        if len(fname) != 0:
            self.df.to_excel(fname)

    def showStockNo(self, t):
        self.lineEdit_info.setText(t)
        # self.getInfo()
        print(self.lineEdit_info.text())

    #slot2
    def getInfo(self):
        # self.lineEdit_info.setText(t)
        stockNo = self.lineEdit_info.text()
        # print(type(stockNo))
        # stock_no = self.lineEdit_company.text()
        # self.lineEdit_info.setText(stockNo)
        url = 'https://mops.twse.com.tw/mops/web/ajax_t05st03'
        payloads = {"encodeURIComponent": 1,
        "step": 1,
        "firstin": 1,
        "off": 1,
        "queryName": 'co_id',
        "inpuType": 'co_id',
        "TYPEK": all,
        "co_id": stockNo
        }

        res = requests.post(url, data = payloads, timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        if soup.find_all('th') == []:
            msg = soup.find_all('h3')[0].text
            display_message(msg)
        else:
            data = pd.read_html(res.text)
            # if data[1][2][9] == '&nbsp': 
            #     data[1][2][9] == ""
            # else:
            self.company.setText(data[1][2][1])
            self.ceo.setText(data[1][2][3])
            self.cfo.setText(data[1][5][3])
            self.talk.setText(data[1][2][4])
            self.found.setText(data[1][2][7])
            if data[1][5][8] == '&nbsp':
                data[1][5][8] == ""
            else:
                self.ipo.setText(data[1][5][8])

            if data[1][2][9] == '&nbsp': 
                data[1][2][9] == ""
            else:
                self.otc.setText(data[1][2][9])

            self.industry.setText(data[1][3][0])
            self.equity.setText(data[1][2][8])
            self.address_c.setText(data[1][2][2])
            self.business.setText(data[1][2][6])
            self.tdr.setText(data[1][2][11])
            self.com.setText(data[1][5][10])
            self.spe.setText(data[1][5][11])
            self.agency.setText(data[1][2][13])
            self.tel.setText(data[1][5][13])
            self.address_a.setText(data[1][2][14])
            self.auditor.setText(data[1][2][15])
            self.cpa1.setText(data[1][2][16])
            self.cpa2.setText(data[1][2][17])

    #slot3
    def GetDF_A(self):
        date_A = self.lEdit_dateA.text()
        stockNo_A = self.lEdit_ComA.text()
        url = f'https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU?date={date_A}&stockNo={stockNo_A}&response=json&_=1686645769785'
        res = requests.get(url, cert = '', timeout=5)
        PE = json.loads(res.text)
        title_A = PE.get('title').split(" ")[:2]
        cols = PE.get('fields')
        data_plot = PE.get('data')
        data_PE_A = pd.DataFrame(data_plot)
        data_PE_A.columns = cols
        return data_PE_A, title_A
    
    #取得B公司的DF
    def GetDF_B(self):
        date_B = self.lEdit_dateB.text()
        stockNo_B = self.lEdit_ComB.text()
        url = f'https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU?date={date_B}&stockNo={stockNo_B}&response=json&_=1686645769785'
        res_B = requests.get(url, cert = '', timeout=5)
        PE_B = json.loads(res_B.text)
        title_B = PE_B.get('title').split(" ")[:2]
        cols_B = PE_B.get('fields')
        data_plot_B = PE_B.get('data')
        data_PE_B = pd.DataFrame(data_plot_B)
        data_PE_B.columns = cols_B
        return data_PE_B, title_B
    
    #畫出最左邊那格的折線圖(殖利率)
    def LinePlot_Y(self):
        self.gView_A.clear()

        data_PE_A = self.GetDF_A()[0]
        data_PE_B = self.GetDF_B()[0]
        
        compare_title = self.GetDF_A()[1][0] + self.GetDF_A()[1][1] + " " + "與" + " " + self.GetDF_B()[1][0] + self.GetDF_B()[1][1]  
        self.compare_title.setText(compare_title)

        day_lst_A = []
        for d in data_PE_A['日期']:
            day = int(d[7:9])
            day_lst_A.append(day)
        
        day_lst_B = []
        for k in data_PE_B['日期']:
            day_B = int(k[7:9])
            day_lst_B.append(day_B)
        
        y_Yield_A = pd.to_numeric(data_PE_A['殖利率(%)'])
        y_Yield_B = pd.to_numeric(data_PE_B['殖利率(%)'])
        if self.cBox_A.isChecked() and self.cBox_B.isChecked():
            line1_Yield_a = self.gView_A.plot(day_lst_A, y_Yield_A, pen = 'r', symbol ='o', symbolBrush = 0.2, name = 'A公司')
            line2_Yield_a = self.gView_A.plot(day_lst_B, y_Yield_B, pen = 'g', symbol ='star', symbolBrush = 0.2, name = 'B公司')
            self.gView_A.addLegend(offset = (20,5),labelTextSize = "9pt")
            self.gView_A.setTitle("殖利率")
        if self.cBox_A.isChecked() and self.cBox_B.isChecked() == False:
            self.gView_A.clear()
            line1_Yield_a = self.gView_A.plot(day_lst_A, y_Yield_A, pen = 'r', symbol ='o', symbolBrush = 0.2, name = 'A公司')
            self.gView_A.addLegend(offset = (20,5),labelTextSize = "9pt")
            self.gView_A.setTitle("殖利率")
        if self.cBox_B.isChecked() and self.cBox_A.isChecked() == False:
            self.gView_A.clear()
            line2_Yield_a = self.gView_A.plot(day_lst_B, y_Yield_B, pen = 'g', symbol ='star', symbolBrush = 0.2, name = 'B公司')
            self.gView_A.addLegend(offset = (20,5),labelTextSize = "9pt")
            self.gView_A.setTitle("殖利率")


    #畫出中間那格的折線圖(本益比)
    def LinePlot_PE(self):
        self.gView_B.clear()

        data_PE_A = self.GetDF_A()[0]
        data_PE_B = self.GetDF_B()[0]

        day_lst_A = []
        for d in data_PE_A['日期']:
            day = int(d[7:9])
            day_lst_A.append(day)

        day_lst_B = []
        for k in data_PE_B['日期']:
            day_B = int(k[7:9])
            day_lst_B.append(day_B)

        y_PE_A = pd.to_numeric(data_PE_A['本益比'])
        y_PE_B = pd.to_numeric(data_PE_B['本益比'])
        if self.cBox_A.isChecked() and self.cBox_B.isChecked():
            line1_PE_a = self.gView_B.plot(day_lst_A, y_PE_A, pen = 'r', symbol ='o', symbolBrush = 0.2, name = 'A公司')
            legend_B = self.gView_B.plot(day_lst_B, y_PE_B, pen = 'g', symbol ='star', symbolBrush = 0.2, name = 'B公司')
            self.gView_B.addLegend(offset = (20,5),labelTextSize = "9pt")
            self.gView_B.setTitle("本益比")
        if self.cBox_A.isChecked() and self.cBox_B.isChecked() == False:
            self.gView_B.clear()
            line1_PE_a = self.gView_B.plot(day_lst_A, y_PE_A, pen = 'r', symbol ='o', symbolBrush = 0.2, name = 'A公司')
            self.gView_B.addLegend(offset = (20,5),labelTextSize = "9pt")
            self.gView_B.setTitle("本益比")
        if self.cBox_B.isChecked() and self.cBox_A.isChecked() == False:
            self.gView_B.clear()
            legend_B = self.gView_B.plot(day_lst_B, y_PE_B, pen = 'g', symbol ='star', symbolBrush = 0.2, name = 'B公司')
            self.gView_B.addLegend(offset = (20,5),labelTextSize = "9pt")
            self.gView_B.setTitle("本益比")


    #畫出右邊那格的折線圖(股價淨值比)
    def LinePlot_PBR(self):
        self.gView_C.clear()

        data_PE_A = self.GetDF_A()[0]
        data_PE_B = self.GetDF_B()[0]

        day_lst_A = []
        for d in data_PE_A['日期']:
            day = int(d[7:9])
            day_lst_A.append(day)
            
        day_lst_B = []
        for k in data_PE_B['日期']:
            day_B = int(k[7:9])
            day_lst_B.append(day_B)

        y_PBR_A = pd.to_numeric(data_PE_A['股價淨值比'])
        y_PBR_B = pd.to_numeric(data_PE_B['股價淨值比'])
        if self.cBox_A.isChecked() and self.cBox_B.isChecked():
            line1_PBR_a = self.gView_C.plot(day_lst_A, y_PBR_A, pen = 'r', symbol ='o', symbolBrush = 0.2, name = 'A公司')
            line1_PBR_a = self.gView_C.plot(day_lst_B, y_PBR_B, pen = 'g', symbol ='star', symbolBrush = 0.2, name = 'B公司')
            self.gView_C.addLegend(offset = (20,5),labelTextSize = "9pt")
            self.gView_C.setTitle("股價淨值比")
        if self.cBox_A.isChecked() and self.cBox_B.isChecked() == False:
            self.gView_C.clear()
            line1_PBR_a = self.gView_C.plot(day_lst_A, y_PBR_A, pen = 'r', symbol ='o', symbolBrush = 0.2, name = 'A公司')
            self.gView_C.addLegend(offset = (20,5),labelTextSize = "9pt")
            self.gView_C.setTitle("股價淨值比")
        if self.cBox_B.isChecked() and self.cBox_A.isChecked() == False:
            self.gView_C.clear()
            line1_PBR_a = self.gView_C.plot(day_lst_B, y_PBR_B, pen = 'g', symbol ='star', symbolBrush = 0.2, name = 'B公司')
            self.gView_C.addLegend(offset = (20,5),labelTextSize = "9pt")
            self.gView_C.setTitle("股價淨值比")
    

    def ExitApp(self):
        self.close()





class AnotherWindow(QWidget):
    # create a customized signal 
    submitted = QtCore.pyqtSignal(str) # "submitted" is like a component name 
    def __init__(self):
        super().__init__()
        uic.loadUi('hw03_trend.ui', self)
        self.setGeometry(400, 80, 800, 600)
         
        # Signal
        self.pBut_exit.setGeometry(0,0,5,5)
        self.pBut_exit.clicked.connect(self.BackMainWin)
        self.gView.scene().sigMouseMoved.connect(self.mouseMoved)

    def passInfo(self, data, date):      #主程式要丟東西到副程式
        self.gView.clear()
        x_lst = []
        for d in data['日期']:
            x_lst.append(pd.to_numeric(d[-2:]))

        y1 = pd.to_numeric(data['收盤價'])
        # print(y1)
        line1 = self.gView.plot(x_lst, y1, pen = 'b', symbol ='x', name = '收盤價') # generates a PlotDataItem
        # pen = pg.mkPen(color=(255, 0, 0), width = 10)
        y2 = pd.to_numeric(data['最高價'])
        y3 = pd.to_numeric(data['最低價'])
        line2 = self.gView.plot(x_lst, y2, pen = 'r', symbol ='o', symbolBrush = 0.2, name = '最高價')
        line3 = self.gView.plot(x_lst, y3, pen = 'y', symbol ='star', symbolBrush = 0.2, name = '最低價')

        legend = self.gView.addLegend()

        # 關聯曲線和圖例
        legend.addItem(line1, '收盤價')
        legend.addItem(line2, '最高價')
        legend.addItem(line3, '最低價')

        # pen2 = pg.mkPen(color=(0, 255, 0), width = 10)
        self.vLine = pg.InfiniteLine(pos = 1, angle=90, movable=False)
        self.hLine = pg.InfiniteLine(pos = 0.2, angle=0, movable=False)
        self.gView.addItem(self.vLine) # add PlotDataItem in PlotWidget 
        self.gView.addItem(self.hLine)
        # plotTitle = 
        self.date = date 
        # self.gView.setTitle(plotTitle)

    def mouseMoved(self, point): # returns the coordinates in pixels with respect to the PlotWidget
        p = self.gView.plotItem.vb.mapSceneToView(point) # convert to the coordinate of the plot
        self.vLine.setPos(p.x()) # set position of the verticle line 畫滑鼠位置的垂直線
        self.hLine.setPos(p.y()) # set position of the horizontal line 畫滑鼠位置的水平線
        plotTitle = "日期：" + self.date[:4] + "/" + self.date[-1:] + "/" + str(int(p.x())) + "  " + "價格：" + str(round(p.y(), 2)) #+ self.lineEdit_year.text()
        # self.lineEdit_x.setText(str(round(p.x(), 4))) 
        # self.lineEdit_cdf.setText(str(round(norm.cdf(p.x()), 4))) 
        self.gView.setTitle(plotTitle)
        
     
    def BackMainWin(self):
        self.close()





def display_message(message):
    dlg = QMessageBox()
    dlg.setWindowTitle("No data")
    dlg.setText(message)
    dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
    buttonY = dlg.button(QMessageBox.StandardButton.Yes)
    buttonY.setText('OK')
    dlg.setIcon(QMessageBox.Icon.Information)
    dlg.exec()
         
def display_msg(message):
    dlgY = QMessageBox()
    dlgY.setWindowTitle("No Company")
    dlgY.setText(message)
    dlgY.setStandardButtons(QMessageBox.StandardButton.Yes)
    button = dlgY.button(QMessageBox.StandardButton.Yes)
    button.setText('OK')
    dlgY.setIcon(QMessageBox.Icon.Information)
    dlgY.exec()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()