# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'face.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1080, 968)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(130, 620, 831, 61))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.openButton = QPushButton(self.layoutWidget)
        self.openButton.setObjectName(u"openButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openButton.sizePolicy().hasHeightForWidth())
        self.openButton.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(15)
        self.openButton.setFont(font)
        self.openButton.setStyleSheet(u"border-image: url(:/images/img/\u6253\u5f00\u6444\u50cf\u5934.png);")

        self.horizontalLayout.addWidget(self.openButton)

        self.horizontalSpacer = QSpacerItem(127, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.recogButton = QPushButton(self.layoutWidget)
        self.recogButton.setObjectName(u"recogButton")
        sizePolicy.setHeightForWidth(self.recogButton.sizePolicy().hasHeightForWidth())
        self.recogButton.setSizePolicy(sizePolicy)
        self.recogButton.setFont(font)
        self.recogButton.setStyleSheet(u"border-image: url(:/images/img/\u4eba\u8138\u8bc6\u522b.png);")

        self.horizontalLayout.addWidget(self.recogButton)

        self.horizontalSpacer_2 = QSpacerItem(127, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.saveButton = QPushButton(self.layoutWidget)
        self.saveButton.setObjectName(u"saveButton")
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setFont(font)
        self.saveButton.setStyleSheet(u"border-image: url(:/images/img/\u4fdd\u5b58.png);")

        self.horizontalLayout.addWidget(self.saveButton)

        self.horizontalSpacer_3 = QSpacerItem(127, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.inputButton = QPushButton(self.layoutWidget)
        self.inputButton.setObjectName(u"inputButton")
        sizePolicy.setHeightForWidth(self.inputButton.sizePolicy().hasHeightForWidth())
        self.inputButton.setSizePolicy(sizePolicy)
        self.inputButton.setFont(font)
        self.inputButton.setStyleSheet(u"border-image: url(:/images/img/\u6570\u636e\u91c7\u96c6.png);")

        self.horizontalLayout.addWidget(self.inputButton)

        self.horizontalSpacer_4 = QSpacerItem(127, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.queryButton = QPushButton(self.layoutWidget)
        self.queryButton.setObjectName(u"queryButton")
        sizePolicy.setHeightForWidth(self.queryButton.sizePolicy().hasHeightForWidth())
        self.queryButton.setSizePolicy(sizePolicy)
        self.queryButton.setFont(font)
        self.queryButton.setStyleSheet(u"border-image: url(:/images/img/\u67e5\u8be2.png);")

        self.horizontalLayout.addWidget(self.queryButton)

        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setGeometry(QRect(250, 10, 581, 91))
        font1 = QFont()
        font1.setPointSize(40)
        font1.setBold(False)
        self.titleLabel.setFont(font1)
        self.titleLabel.setStyleSheet(u"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 0), stop:0.52 rgba(0, 0, 0, 0), stop:0.565 rgba(82, 121, 76, 33), stop:0.65 rgba(159, 235, 148, 64), stop:0.721925 rgba(255, 238, 150, 129), stop:0.77 rgba(255, 128, 128, 204), stop:0.89 rgba(191, 128, 255, 64), stop:1 rgba(0, 0, 0, 0));")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.faceLabel = QLabel(self.centralwidget)
        self.faceLabel.setObjectName(u"faceLabel")
        self.faceLabel.setGeometry(QRect(60, 110, 541, 461))
        self.faceLabel.setStyleSheet(u"border-image: url(:/images/img/z.jpg);")
        self.queryTableWidget = QTableWidget(self.centralwidget)
        self.queryTableWidget.setObjectName(u"queryTableWidget")
        self.queryTableWidget.setGeometry(QRect(120, 700, 851, 241))
        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setGeometry(QRect(640, 500, 381, 61))
        self.statusLabel.setFont(font)
        self.nameLineEdit = QLineEdit(self.centralwidget)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.nameLineEdit.setGeometry(QRect(730, 200, 291, 61))
        self.nameLineEdit.setFont(font)
        self.numLineEdit = QLineEdit(self.centralwidget)
        self.numLineEdit.setObjectName(u"numLineEdit")
        self.numLineEdit.setGeometry(QRect(730, 300, 291, 61))
        self.numLineEdit.setFont(font)
        self.jointimeLineEdit = QLineEdit(self.centralwidget)
        self.jointimeLineEdit.setObjectName(u"jointimeLineEdit")
        self.jointimeLineEdit.setGeometry(QRect(730, 400, 291, 61))
        self.jointimeLineEdit.setFont(font)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(640, 200, 81, 61))
        self.label.setFont(font)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(640, 300, 81, 61))
        self.label_2.setFont(font)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(640, 400, 91, 61))
        self.label_3.setFont(font)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(620, 100, 421, 471))
        self.timeLabel = QLabel(self.groupBox)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setGeometry(QRect(20, 20, 381, 51))
        font2 = QFont()
        font2.setPointSize(12)
        self.timeLabel.setFont(font2)
        self.openGroupBox = QGroupBox(self.centralwidget)
        self.openGroupBox.setObjectName(u"openGroupBox")
        self.openGroupBox.setGeometry(QRect(130, 610, 61, 71))
        self.openGroupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(320, 610, 61, 71))
        self.groupBox_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(509, 609, 71, 71))
        self.groupBox_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(709, 610, 61, 71))
        self.groupBox_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.groupBox_6 = QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(899, 610, 61, 71))
        self.groupBox_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.groupBox_6.raise_()
        self.groupBox_5.raise_()
        self.groupBox_4.raise_()
        self.groupBox_3.raise_()
        self.openGroupBox.raise_()
        self.groupBox.raise_()
        self.layoutWidget.raise_()
        self.titleLabel.raise_()
        self.faceLabel.raise_()
        self.queryTableWidget.raise_()
        self.statusLabel.raise_()
        self.nameLineEdit.raise_()
        self.numLineEdit.raise_()
        self.jointimeLineEdit.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.openButton.setText("")
        self.recogButton.setText("")
        self.saveButton.setText("")
        self.inputButton.setText("")
        self.queryButton.setText("")
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"ZP\u8003\u52e4\u7cfb\u7edf", None))
        self.faceLabel.setText("")
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"\u8003\u52e4\u72b6\u6001\uff1a", None))
        self.nameLineEdit.setText("")
        self.numLineEdit.setText("")
        self.jointimeLineEdit.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u59d3\u540d\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u5de5\u53f7\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5165\u5751\u65f6\u95f4\uff1a", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u4fe1\u606f\u663e\u793a", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u65f6\u95f4\uff1a", None))
        self.openGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u8bc6\u522b", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u91c7\u96c6", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2", None))
    # retranslateUi

