from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtGui import QPixmap
import pyqtgraph as pg
from scipy.stats import norm
from scipy.stats import chi2
import numpy as np
import pandas as pd
import sys, os
from pathlib import Path
 
  
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
            return QtGui.QColor('#d8ffdb')
 
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


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('hw_tabpages.ui', self)
        self.tabWidget.setCurrentIndex(0)
        self.setWindowTitle('An application with multiple pages')
        # self.pdfcdf_status = 1
        # page 1
        self.folderPath = ""
        self.count = 0
        # page 2
        self.pdfcdf_status = 1
        self.pdfcdf_plot('PDF')
        self.label_up_mu.setText('Upper Bound')
        self.label_up_sigma.setText('Upper Bound')
        self.label_low_mu.setText('Lower Bound')
        self.label_low_sigma.setText('Lower Bound')
        self.label_mu.setText('mu')
        self.label_sigma.setText('sigma')
        self.lineEdit_mu.show()
        self.lineEdit_up_mu.show()
        self.lineEdit_low_mu.show()
        self.vSlider_mu.show()
        # page 3
        self.table = self.tableView
        
        win = self.graphWidget_plot
        self.plt1 = win.addPlot()
        win.nextRow()
        self.plt2 = win.addPlot()

        # Signals_Page1
        self.Button_first.clicked.connect(self.showImgFirst)
        self.Button_pre.clicked.connect(self.showImgPre)
        self.Button_next.clicked.connect(self.showImgNext)
        self.Button_last.clicked.connect(self.showImgLast)
        self.actionOpen_folder_2.triggered.connect(self.openFolder)
        self.count = 0
        # Signals_Page2
        self.cBox_distribution.addItems(['Normal', 'chi2'])
        self.cBox_distribution.currentIndexChanged.connect(self.pdfcdf_plot)
        self.cBox_distribution.currentIndexChanged.connect(self.para_change)
        self.checkBox_grid.stateChanged.connect(self.gridOn)
        self.lineEdit_x.returnPressed.connect(self.comp_pdf)
        self.lineEdit_pro.returnPressed.connect(self.comp_invpdf)
        self.lineEdit_mu.textChanged.connect(self.pdfcdf_plot)
        self.lineEdit_sigma.textChanged.connect(self.pdfcdf_plot)
        self.vSlider_mu.valueChanged.connect(self.sliderMove_mu)
        self.vSlider_mu.sliderMoved.connect(self.sliderMove_mu)
        self.vSlider_sigma.valueChanged.connect(self.sliderMove_sigma)
        self.vSlider_sigma.sliderMoved.connect(self.sliderMove_sigma)
        self.rButton_pdf.toggled.connect(self.pdfcdf_clicked)
        self.rButton_cdf.toggled.connect(self.pdfcdf_clicked)
        # Signals_Page3
        self.actionOpen_file.triggered.connect(self.fileOpen)
        self.cBox_var1.currentIndexChanged.connect(self.update_plt1)
        self.cBox_var1.currentIndexChanged.connect(self.update_plt2)
        self.cBox_var2.currentIndexChanged.connect(self.update_plt1)
        self.cBox_var2.currentIndexChanged.connect(self.update_plt2)
        self.pButton_exit.clicked.connect(self.dialogBox)
        self.actionExit_2.triggered.connect(self.close)

       
    # Slots_page1
    def openFolder(self):
        self.folderPath = QFileDialog.getExistingDirectory(self, "Open folder","../")       
        self.picName = os.listdir(self.folderPath)
        self.label_img.setPixmap(QPixmap(self.folderPath +'/'+self.picName[0]))

    def showImgFirst(self):
        self.label_img.setPixmap(QPixmap(self.folderPath +'/'+ self.picName[0]))  
        # self.count == 0
        self.label_title.setText(self.picName[0].split('.')[-2]) # set Label text
        
    def showImgLast(self):
        self.label_img.setPixmap(QPixmap(self.folderPath +'/'+ self.picName[len(self.picName)-1])) 
        self.label_title.setText(self.picName[len(self.picName)-1].split('.')[-2])

    def showImgNext(self):
        if self.count == len(self.picName) - 1:
            self.count = 0
        else :
            self.count += 1
        self.label_img.setPixmap(QPixmap(self.folderPath +'/'+ self.picName[self.count]))
        self.label_title.setText(self.picName[self.count].split('.')[-2])

    def showImgPre(self):
        if self.count == 0:
            self.count = len(self.picName) - 1
        else:
            self.count -= 1
        self.label_img.setPixmap(QPixmap(self.folderPath +'/'+ self.picName[self.count]))
        self.label_title.setText(self.picName[self.count].split('.')[-2])
   

    # Slots_page2
    def pdfcdf_plot(self, t):
        self.graphWidget.clear() 
        if self.cBox_distribution.currentText() == 'Normal':
            x = np.linspace(-10, 10, 1000)
            mu = int(self.lineEdit_mu.text())
            sigma = int(self.lineEdit_sigma.text())
            if t == 'PDF':
                y = norm.pdf(x, mu, sigma)
            else :
                y = norm.cdf(x, mu, sigma)
            pen = pg.mkPen(color=(200, 180, 200), width = 5) 
            self.graphWidget.plot(x, y, pen = pen, name = 'Demo')
            self.graphWidget.setBackground('w')
            styles = {'color':'green', 'font-size':'10px'}
            self.graphWidget.setLabel('left', 'Y', **styles)
            self.graphWidget.setLabel('bottom', 'X', **styles)
        
        else:
            x = np.linspace(0, 8, 1000)
            n = int(self.lineEdit_sigma.text())
            if t == 'PDF':
                y = chi2.pdf(x, n)
            else :
                y = chi2.cdf(x, n)

            pen = pg.mkPen(color=(200, 180, 200), width = 5) 
            self.graphWidget.plot(x, y, pen = pen, name = 'Demo')
            self.graphWidget.setBackground('w')
            styles = {'color':'green', 'font-size':'10px'}
            self.graphWidget.setLabel('left', 'Y', **styles)
            self.graphWidget.setLabel('bottom', 'X', **styles)


    def para_change(self):
        if self.cBox_distribution.currentText() == 'Normal':
            self.label_up_mu.setText('Upper Bound')
            self.label_up_sigma.setText('Upper Bound')
            self.label_low_mu.setText('Lower Bound')
            self.label_low_sigma.setText('Lower Bound')
            self.label_mu.setText('mu')
            self.label_sigma.setText('sigma')
            self.lineEdit_mu.show()
            self.lineEdit_up_mu.show()
            self.lineEdit_low_mu.show()
            self.vSlider_mu.show()
        else:
            self.label_up_mu.setText('')
            self.label_low_mu.setText('')
            self.label_mu.setText('')
            self.label_sigma.setText('df')
            self.lineEdit_up_mu.hide()
            self.lineEdit_mu.hide()
            self.lineEdit_low_mu.hide()
            self.vSlider_mu.hide()


    def pdfcdf_clicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.pdfcdf_status = -self.pdfcdf_status
            self.pdfcdf_plot(radioBtn.text())


    def sliderMove_mu(self):
        self.lineEdit_mu.setText(str(round(self.vSlider_mu.value(),4)))
        if self.pdfcdf_status == 1:
            self.pdfcdf_plot('PDF')
        else :
            self.pdfcdf_plot('CDF')


    def sliderMove_sigma(self):
        self.lineEdit_sigma.setText(str(round(self.vSlider_sigma.value(),4)))
        if self.pdfcdf_status == 1:
            self.pdfcdf_plot('PDF')
        else :
            self.pdfcdf_plot('CDF')

    def comp_pdf(self):
        if self.cBox_distribution.currentText() == 'Normal':
            cdf = norm.cdf(float(self.lineEdit_x.displayText()), float(self.lineEdit_mu.displayText()), float(self.lineEdit_sigma.displayText())) 
            self.lineEdit_pro.setText(str(round(cdf, 4)))
        else: 
            cdf = chi2.cdf(float(self.lineEdit_x.displayText()), df = float(self.lineEdit_sigma.displayText())) 
            self.lineEdit_pro.setText(str(round(cdf, 4)))
 
    def comp_invpdf(self):
        if self.cBox_distribution.currentText() == 'Normal':
            x = norm.ppf(float(self.lineEdit_pro.displayText()), float(self.lineEdit_mu.displayText()), float(self.lineEdit_sigma.displayText())) 
            self.lineEdit_x.setText(str(round(x,4)))
        else:
            x = chi2.ppf(float(self.lineEdit_pro.displayText()), df = float(self.lineEdit_sigma.displayText())) 
            self.lineEdit_x.setText(str(round(x,4)))

    def gridOn(self, s):    
        if s == 2: 
            self.graphWidget.showGrid(x = True, y = True)   
        else:
            self.graphWidget.showGrid(x = False, y = False)  
       
 
    # Slots_page3
    def fileOpen(self):
        home_dir = str(Path.home())
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            "", "EXCEL files (*.xlsx *.xls);;Text files (*.txt);;Images (*.png *.xpm *.jpg)")
        # print(fname[0])
        if fname[0]:
            self.df = pd.read_excel(fname[0], index_col = None, header = 0)
            self.model = TableModel(self.df)
            self.table.setModel(self.model)
 
            self.label_var.setText(str(self.df.shape[1]))
            self.label_num.setText(str(self.df.shape[0]))
            self.label_name.setText(str(fname[0]))
            self.cBox_var1.clear()
            self.cBox_var1.addItems(self.df.columns)
            self.cBox_var2.clear()
            self.cBox_var2.addItems(self.df.columns)
            self.update_plt1()
            self.update_plt2()

    def update_plt1(self):
        self.cBox_var1.currentText() == self.df.columns[0]
        self.plt1.clear()
        y, x = np.histogram(self.df[self.cBox_var1.currentText()])
            # self.plt1.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        barItem = pg.BarGraphItem(x = x[0:len(y)-1], height = y, width = (x.max()-x.min())/len(x), brush=(107,200,224))
        self.plt1.addItem(barItem)
        self.plt1.setTitle(self.cBox_var1.currentText())
 
    def update_plt2(self):
        if self.cBox_var2.currentText() != "":
            self.plt2.clear()
            if isinstance(self.df[self.cBox_var1.currentText()][0], str) or isinstance(self.df[self.cBox_var2.currentText()][0], str) :
                self.plt2.setLabel('bottom',"")   
                self.plt2.setLabel('left',"")
                self.plt2.setTitle(self.cBox_var1.currentText() + ' and ' +self.cBox_var2.currentText())
                return
            else :
                self.plt2.plot(self.df[self.cBox_var1.currentText()], self.df[self.cBox_var2.currentText()], pen=None, symbol='o', symbolSize=5)
                self.plt2.setLabel('bottom',self.cBox_var1.currentText())   
                self.plt2.setLabel('left',self.cBox_var2.currentText())   
                self.plt2.setTitle(self.cBox_var1.currentText() + ' and ' +self.cBox_var2.currentText())

    def dialogBox(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("確認離開視窗")
        dlg.setText("確定要離開這個 App")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        buttonY = dlg.button(QMessageBox.StandardButton.Yes)
        buttonY.setText('確定')
        buttonY = dlg.button(QMessageBox.StandardButton.No)
        buttonY.setText('取消')
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()
 
        if button == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            print("No!")    


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()