# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnaliseDeFaturamento.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import sys
from os.path import dirname,relpath,join
import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from tkinter import Tk
from tkinter.filedialog import askopenfilename


class Ui_Prediction(object):
    def setupUi(self, Prediction):
        Prediction.setObjectName("Prediction")
        Prediction.resize(716, 611)
        self.centralwidget = QtWidgets.QWidget(Prediction)
        self.centralwidget.setObjectName("centralwidget")
        self.arquivoInput = QtWidgets.QPushButton(self.centralwidget)
        self.arquivoInput.setGeometry(QtCore.QRect(590, 90, 111, 31))
        self.arquivoInput.setObjectName("arquivoInput")
        self.arimaBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.arimaBtn.setGeometry(QtCore.QRect(590, 220, 82, 17))
        self.arimaBtn.setObjectName("arimaBtn")
        self.linearBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.linearBtn.setGeometry(QtCore.QRect(590, 250, 121, 17))
        self.linearBtn.setObjectName("linearBtn")
        self.desvPad = QtWidgets.QRadioButton(self.centralwidget)
        self.desvPad.setGeometry(QtCore.QRect(590, 270, 111, 41))
        self.desvPad.setObjectName("desvPad")
        self.predictBtn = QtWidgets.QPushButton(self.centralwidget)
        self.predictBtn.setGeometry(QtCore.QRect(600, 390, 75, 23))
        self.predictBtn.setObjectName("predictBtn")
        self.txt_predicao = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_predicao.setGeometry(QtCore.QRect(10, 550, 561, 20))
        self.txt_predicao.setObjectName("txt_predicao")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 301, 31))
        self.label.setObjectName("label")
        self.txt_atual = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_atual.setGeometry(QtCore.QRect(360, 40, 211, 31))
        self.txt_atual.setObjectName("txt_atual")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(360, 10, 111, 20))
        self.label_2.setObjectName("label_2")
        self.aritmeticalMean = QtWidgets.QRadioButton(self.centralwidget)
        self.aritmeticalMean.setGeometry(QtCore.QRect(590, 310, 131, 17))
        self.aritmeticalMean.setObjectName("aritmeticalMean")
        self.meanWeighted = QtWidgets.QRadioButton(self.centralwidget)
        self.meanWeighted.setGeometry(QtCore.QRect(590, 340, 121, 17))
        self.meanWeighted.setObjectName("meanWeighted")
        self.nRows_spbox = QtWidgets.QSpinBox(self.centralwidget)
        self.nRows_spbox.setGeometry(QtCore.QRect(600, 40, 61, 31))
        self.nRows_spbox.setObjectName("nRows_spbox")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(570, 190, 151, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(580, 180, 141, 16))
        self.label_3.setObjectName("label_3")
        self.inputView = QtWidgets.QTableWidget(self.centralwidget)
        self.inputView.setGeometry(QtCore.QRect(10, 90, 561, 451))
        self.inputView.setObjectName("inputView")
        self.inputView.setColumnCount(4)
        self.inputView.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.inputView.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.inputView.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.inputView.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.inputView.setHorizontalHeaderItem(3, item)
        Prediction.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Prediction)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 716, 21))
        self.menubar.setObjectName("menubar")
        Prediction.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Prediction)
        self.statusbar.setObjectName("statusbar")
        Prediction.setStatusBar(self.statusbar)

        self.retranslateUi(Prediction)
        QtCore.QMetaObject.connectSlotsByName(Prediction)
        self.arquivoInput.clicked.connect(self.openfile)
        self.predictBtn.clicked.connect(self.predicao)

    def openfile(self):
        #findpath
        Tk().withdraw()
        path = askopenfilename()
        self.all_data = pd.read_csv(path, sep = ';')
        #fileload to table
        numColumn = self.nRows_spbox.value()
        if numColumn == 0: numRows = len(self.all_data.index)
        else: numRows = numColumn
        self.inputView.setColumnCount(len(self.all_data.columns))
        self.inputView.setRowCount(numRows)
        self.inputView.setHorizontalHeaderLabels(self.all_data.columns)
        for i in range(numRows):
            for j in range(len(self.all_data.columns)):
                self.inputView.setItem(i,j,QTableWidgetItem(str(self.all_data.iat[i,j])))
        self.inputView.resizeColumnsToContents()
        self.inputView.resizeRowsToContents()
        soma_vendas = str('R$%0.02f' %sum(self.all_data['Vendas']))
        self.txt_atual.setText(soma_vendas)

    def predicao(self):
        df = self.all_data
        if self.aritmeticalMean.isChecked() == True:
            media = df['Vendas'].mean()
            predicao = "O número de vendas predito através da média aritimética é de {}".format(str(int(media)))
            self.txt_predicao.setText(predicao)
        elif self.desvPad.isChecked()==True:
            media = df['Vendas'].mean()
            desvio = df['Vendas'].std()
            coe_var = (desvio/media)*100
            predicao = "Segundo o Desvio Padrão, um total de vendas de {}% é esperado".format(coe_var)
            self.txt_predicao.setText(predicao)
        elif self.meanWeighted.isChecked()==True:
            listaMP = np.transpose((np.array([df['Vendas'].tail(12), [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]])))
            df_ult = pd.DataFrame(listaMP, columns=['Vendas', 'Pesos'])
            df_ult['Ponderado'] = df_ult['Vendas'] * df_ult['Pesos']
            med_ponderada = df_ult['Ponderado'].sum() / df_ult['Pesos'].sum()
            predicao = "Segundo a média Ponderada, um total de vendas de {} é esperado".format(str(int(med_ponderada)))
            self.txt_predicao.setText(predicao)
        elif self.arimaBtn.isChecked() == True:
            model = ARIMA(df['Vendas'], order=(1, 1, 1))
            model_fit = model.fit()
            yhat = model_fit.predict(len(df['Vendas']), len(df['Vendas']) + 5, typ='levels')
            pred = np.array(yhat)
            predicao = "Segundo o ARIMA, um total de vendas de {} é esperado".format(str(int(pred[0])))
            self.txt_predicao.setText(predicao)
        elif self.linearBtn.isChecked() == True:
            model = AutoReg(df['Vendas'], lags=2)
            model_fit = model.fit()
            yhat = model_fit.predict(len(df['Vendas']), len(df['Vendas']) + 5)
            pred = np.array(yhat)
            predicao = "Predição utilizando Time Series baseado em Regressão Linear é: {}" .format(str(int(pred[0])))
            self.txt_predicao.setText(predicao)




    def retranslateUi(self, Prediction):
        _translate = QtCore.QCoreApplication.translate
        Prediction.setWindowTitle(_translate("Prediction", "MainWindow"))
        self.arquivoInput.setText(_translate("Prediction", "Arquivo"))
        self.arimaBtn.setText(_translate("Prediction", "ARIMA"))
        self.linearBtn.setText(_translate("Prediction", "Regressão Linear"))
        self.desvPad.setText(_translate("Prediction", "DesvPad"))
        self.predictBtn.setText(_translate("Prediction", "Predizer"))
        self.label.setText(_translate("Prediction", "Predição de Faturamento"))
        self.label_2.setText(_translate("Prediction", "Total de Vendas"))
        self.aritmeticalMean.setText(_translate("Prediction", "Média"))
        self.meanWeighted.setText(_translate("Prediction", "Média Ponderada"))
        self.label_3.setText(_translate("Prediction", "Selecione o tipo de Predição"))
        item = self.inputView.horizontalHeaderItem(0)
        item.setText(_translate("Prediction", "Data"))
        item = self.inputView.horizontalHeaderItem(1)
        item.setText(_translate("Prediction", "Vendas"))
        item = self.inputView.horizontalHeaderItem(2)
        item.setText(_translate("Prediction", "Mes"))
        item = self.inputView.horizontalHeaderItem(3)
        item.setText(_translate("Prediction", "Ano"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Prediction = QtWidgets.QMainWindow()
    ui = Ui_Prediction()
    ui.setupUi(Prediction)
    Prediction.show()
    sys.exit(app.exec_())
