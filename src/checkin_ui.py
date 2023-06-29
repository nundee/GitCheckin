# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'checkin.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListView, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSplitter, QVBoxLayout, QWidget)
import git_icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(419, 624)
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(9)
        font.setStyleStrategy(QFont.PreferAntialias)
        Dialog.setFont(font)
        icon = QIcon()
        icon.addFile(u":/git-icon/Git-Icon-1788C.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    /*background-color: #dadbde;*/\n"
"    min-width: 80px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	border: 1px;\n"
"	border-color: navy; \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #dadbde;\n"
"}\n"
"\n"
"\n"
"QPushButton:flat {\n"
"    border: none; /* no border for a flat push button */\n"
"}\n"
"\n"
"QPushButton:default {\n"
"    border: 1px;\n"
"    border-color: navy; /* make the default button prominent */\n"
"}")
        self.verticalLayout_5 = QVBoxLayout(Dialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setFrameShape(QFrame.NoFrame)
        self.splitter.setLineWidth(5)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.setHandleWidth(10)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.textEditComment = QPlainTextEdit(self.layoutWidget)
        self.textEditComment.setObjectName(u"textEditComment")
        self.textEditComment.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout_4.addWidget(self.textEditComment)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label)

        self.lineEditWorkItem = QLineEdit(self.layoutWidget)
        self.lineEditWorkItem.setObjectName(u"lineEditWorkItem")

        self.horizontalLayout_3.addWidget(self.lineEditWorkItem)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.labelWorkItemDesc = QLabel(self.layoutWidget)
        self.labelWorkItemDesc.setObjectName(u"labelWorkItemDesc")
        self.labelWorkItemDesc.setTextFormat(Qt.MarkdownText)
        self.labelWorkItemDesc.setWordWrap(True)
        self.labelWorkItemDesc.setMargin(3)

        self.verticalLayout_3.addWidget(self.labelWorkItemDesc)

        self.groupBox = QGroupBox(self.layoutWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bExcludeSelected = QPushButton(self.groupBox)
        self.bExcludeSelected.setObjectName(u"bExcludeSelected")
        self.bExcludeSelected.setFlat(False)

        self.horizontalLayout.addWidget(self.bExcludeSelected)

        self.bExcludeAll = QPushButton(self.groupBox)
        self.bExcludeAll.setObjectName(u"bExcludeAll")
        self.bExcludeAll.setFlat(False)

        self.horizontalLayout.addWidget(self.bExcludeAll)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listViewCheckinItems = QListView(self.groupBox)
        self.listViewCheckinItems.setObjectName(u"listViewCheckinItems")
        self.listViewCheckinItems.setSelectionMode(QAbstractItemView.MultiSelection)

        self.verticalLayout.addWidget(self.listViewCheckinItems)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.layoutWidget1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.bIncludeSelected = QPushButton(self.groupBox_2)
        self.bIncludeSelected.setObjectName(u"bIncludeSelected")
        self.bIncludeSelected.setFlat(False)

        self.horizontalLayout_2.addWidget(self.bIncludeSelected)

        self.bIncludeAll = QPushButton(self.groupBox_2)
        self.bIncludeAll.setObjectName(u"bIncludeAll")
        self.bIncludeAll.setFlat(False)

        self.horizontalLayout_2.addWidget(self.bIncludeAll)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.listViewPendingChanges = QListView(self.groupBox_2)
        self.listViewPendingChanges.setObjectName(u"listViewPendingChanges")
        self.listViewPendingChanges.setSelectionMode(QAbstractItemView.MultiSelection)

        self.verticalLayout_2.addWidget(self.listViewPendingChanges)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.splitter.addWidget(self.layoutWidget1)

        self.verticalLayout_5.addWidget(self.splitter)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.bCheckin = QPushButton(Dialog)
        self.bCheckin.setObjectName(u"bCheckin")

        self.horizontalLayout_5.addWidget(self.bCheckin)

        self.bCancel = QPushButton(Dialog)
        self.bCancel.setObjectName(u"bCancel")

        self.horizontalLayout_5.addWidget(self.bCancel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)


        self.retranslateUi(Dialog)
        self.bCheckin.clicked.connect(Dialog.accept)
        self.bCancel.clicked.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Check in changes", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Comment:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Work item:", None))
        self.labelWorkItemDesc.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Checkin items", None))
        self.bExcludeSelected.setText(QCoreApplication.translate("Dialog", u" Exclude selected ", None))
        self.bExcludeAll.setText(QCoreApplication.translate("Dialog", u"Exclude All", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Pending changes", None))
        self.bIncludeSelected.setText(QCoreApplication.translate("Dialog", u" Include selected ", None))
        self.bIncludeAll.setText(QCoreApplication.translate("Dialog", u"Include All", None))
        self.bCheckin.setText(QCoreApplication.translate("Dialog", u"Check in", None))
        self.bCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

