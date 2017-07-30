# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Image_Analyzer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
        
class Ui_ImageAnalyzer(object):
    

    def setupUi(self, ImageAnalyzer):
        ImageAnalyzer.setObjectName(_fromUtf8("ImageAnalyzer"))
        ImageAnalyzer.resize(640, 480)
        ImageAnalyzer.setStyleSheet(_fromUtf8("QDialog {\n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.317, fx:0.5, fy:0.505773, stop:0 rgba(93, 99, 101, 255), stop:1 rgba(69, 76, 80, 255));\n"
"\n"
"}"))   
        self.frame = QtGui.QWidget(self)
        self.frame.setGeometry(QtCore.QRect(20, 170, 381, 251))
        self.frame.setObjectName(_fromUtf8("frame"))
        figuresize=[12,8]
        self.figure = plt.figure(figsize=(figuresize[0],figuresize[1]))
        self.figure.subplots_adjust(left=0.09,right=0.95,bottom=0.12,top=0.82,hspace=.4, wspace=.06)
        self.figure.suptitle("Analyze the files for the chart", fontsize=12)      
        self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.frame)
        self.canvas.setObjectName(_fromUtf8("canvas"))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        self.frame.setLayout(vbox)        
        self.canvas.draw()
        self.resultLabel = QtGui.QLabel(ImageAnalyzer)
        self.resultLabel.setGeometry(QtCore.QRect(417, 178, 211, 231))
        self.resultLabel.setStyleSheet(_fromUtf8("color:rgb(255, 255, 255);\n"
"font-weight:bold;\n"
"font-size: 17px;"))
        self.resultLabel.setScaledContents(False)
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.resultLabel.setWordWrap(True)
        self.resultLabel.setObjectName(_fromUtf8("resultLabel"))
        self.anamolyBox = QtGui.QGroupBox(ImageAnalyzer)
        self.anamolyBox.setGeometry(QtCore.QRect(20, 10, 611, 80))
        self.anamolyBox.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QRadioButton {\n"
"    color: rgb(255, 255, 255);\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width:                  15px;\n"
"    height:                 15px;\n"
"    border-radius:          7px;\n"
"}\n"
"\n"
"\n"
"QRadioButton::indicator::unchecked {\n"
"    background-color: rgb(247, 247, 247);\n"
"}\n"
"\n"
"QRadioButton::indicator::checked {\n"
"    background-color: rgb(255, 14, 106);\n"
"}\n"
""))
        self.anamolyBox.setObjectName(_fromUtf8("anamolyBox"))
        self.oneClass = QtGui.QRadioButton(self.anamolyBox)
        self.oneClass.setGeometry(QtCore.QRect(20, 40, 161, 23))
        self.oneClass.setStyleSheet(_fromUtf8(""))
        self.oneClass.setChecked(True)
        self.oneClass.setObjectName(_fromUtf8("oneClass"))
        self.robustCovariance = QtGui.QRadioButton(self.anamolyBox)
        self.robustCovariance.setGeometry(QtCore.QRect(190, 40, 181, 23))
        self.robustCovariance.setObjectName(_fromUtf8("robustCovariance"))
        self.mad = QtGui.QRadioButton(self.anamolyBox)
        self.mad.setGeometry(QtCore.QRect(380, 40, 221, 23))
        self.mad.setObjectName(_fromUtf8("mad"))
        self.progressBar = QtGui.QProgressBar(ImageAnalyzer)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(20, 140, 611, 23))
        self.progressBar.setStyleSheet(_fromUtf8("QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(255, 14, 106);\n"
"    width: 20px;\n"
"}"))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.progressBar.setVisible(False)
        self.lineEdit = QtGui.QLineEdit(ImageAnalyzer)
        self.lineEdit.setGeometry(QtCore.QRect(20, 100, 481, 31))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton = QtGui.QPushButton(ImageAnalyzer)
        self.pushButton.setGeometry(QtCore.QRect(510, 100, 121, 31))
        self.pushButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"    border: 2px solid rgb(217, 11, 90);\n"
"    border-radius: 2px;\n"
"    background-color:  rgb(255, 14, 106);\n"
"    min-width: 80px;\n"
"    color: rgb(255, 255, 255);\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:  rgb(217, 11, 90);\n"
"}\n"
"\n"
"QPushButton:flat {\n"
"    border: none; /* no border for a flat push button */\n"
"}\n"
"\n"
"QPushButton:default {\n"
"    border-color: navy; /* make the default button prominent */\n"
"}"))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        
        self.analyze = QtGui.QPushButton(ImageAnalyzer)
        self.analyze.setGeometry(QtCore.QRect(410, 430, 221, 31))
        self.analyze.setStyleSheet(_fromUtf8("QPushButton {\n"
"    border: 2px solid rgb(217, 11, 90);\n"
"    border-radius: 2px;\n"
"    background-color:  rgb(255, 14, 106);\n"
"    min-width: 80px;\n"
"    color: rgb(255, 255, 255);\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:  rgb(217, 11, 90);\n"
"}\n"
"\n"
"QPushButton:flat {\n"
"    border: none; /* no border for a flat push button */\n"
"}\n"
"\n"
"QPushButton:default {\n"
"    border-color: navy; /* make the default button prominent */\n"
"}"))
        self.analyze.setFlat(True)
        self.analyze.setObjectName(_fromUtf8("analyze"))
        
        self.quit = QtGui.QPushButton(ImageAnalyzer)
        self.quit.setGeometry(QtCore.QRect(280, 430, 121, 31))
        self.quit.setStyleSheet(_fromUtf8("QPushButton {\n"
"    border: 2px solid rgb(217, 11, 90);\n"
"    border-radius: 2px;\n"
"    background-color:  rgb(255, 14, 106);\n"
"    min-width: 80px;\n"
"    color: rgb(255, 255, 255);\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:  rgb(217, 11, 90);\n"
"}\n"
"\n"
"QPushButton:flat {\n"
"    border: none; /* no border for a flat push button */\n"
"}\n"
"\n"
"QPushButton:default {\n"
"    border-color: navy; /* make the default button prominent */\n"
"}"))
        self.quit.setFlat(True)
        self.quit.setObjectName(_fromUtf8("quit"))
        

        self.retranslateUi(ImageAnalyzer)
        QtCore.QMetaObject.connectSlotsByName(ImageAnalyzer)

    
    
    def retranslateUi(self, ImageAnalyzer):
        ImageAnalyzer.setWindowTitle(_translate("ImageAnalyzer", "Image Analyzer", None))
        self.resultLabel.setText(_translate("ImageAnalyzer", "Run the analyzer for results", None))
        self.anamolyBox.setTitle(_translate("ImageAnalyzer", "Anamoly Detection Methods", None))
        self.oneClass.setText(_translate("ImageAnalyzer", "One Class SVM", None))
        self.robustCovariance.setText(_translate("ImageAnalyzer", "Robust Covariance", None))
        self.mad.setText(_translate("ImageAnalyzer", "Univariate MAD based", None))
        self.pushButton.setText(_translate("ImageAnalyzer", "Browse", None))
        self.analyze.setText(_translate("ImageAnalyzer", "Analyze", None))
        self.quit.setText(_translate("ImageAnalyzer", "Exit", None))

