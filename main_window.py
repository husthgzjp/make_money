# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(848, 560)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(110, 40, 141, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 210, 93, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(400, 10, 431, 481))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(120, 280, 93, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 280, 93, 51))
        self.pushButton_5.setObjectName("pushButton_5")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(230, 280, 115, 19))
        self.radioButton.setObjectName("radioButton")
        self.buttonGroup = QtWidgets.QButtonGroup(Form)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(230, 310, 115, 19))
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName("radioButton_2")
        self.buttonGroup.addButton(self.radioButton_2)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(0, 100, 221, 91))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 30, 93, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_6.setGeometry(QtCore.QRect(110, 30, 93, 51))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 350, 91, 51))
        self.pushButton_7.setObjectName("pushButton_7")

        self.retranslateUi(Form)
        self.pushButton_2.clicked.connect(Form.click_shuabao)
        self.pushButton.clicked.connect(Form.tst_adb)
        self.pushButton_3.clicked.connect(Form.click_jukandian)
        self.pushButton_4.clicked.connect(Form.df_xw)
        self.pushButton_5.clicked.connect(Form.restart_jukandian)
        self.pushButton_6.clicked.connect(Form.df_xsp)
        self.pushButton_7.clicked.connect(Form.click_xuexi)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "初始化设备"))
        self.pushButton_2.setText(_translate("Form", "刷宝赚钱"))
        self.pushButton_3.setText(_translate("Form", "聚看点赚钱"))
        self.pushButton_5.setText(_translate("Form", "重启聚看点"))
        self.radioButton.setText(_translate("Form", "看推荐"))
        self.radioButton_2.setText(_translate("Form", "看视频"))
        self.groupBox.setTitle(_translate("Form", "东方头条"))
        self.pushButton_4.setText(_translate("Form", "看新闻"))
        self.pushButton_6.setText(_translate("Form", "看小视频"))
        self.pushButton_7.setText(_translate("Form", "学习强国"))

