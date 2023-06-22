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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QComboBox,
    QDialog, QDialogButtonBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(419, 519)
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(9)
        font.setStyleStrategy(QFont.PreferAntialias)
        Dialog.setFont(font)
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
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEditComment = QLineEdit(self.widget)
        self.lineEditComment.setObjectName(u"lineEditComment")

        self.horizontalLayout_4.addWidget(self.lineEditComment)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label)

        self.comboBoxWorkItems = QComboBox(self.widget)
        self.comboBoxWorkItems.setObjectName(u"comboBoxWorkItems")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxWorkItems.sizePolicy().hasHeightForWidth())
        self.comboBoxWorkItems.setSizePolicy(sizePolicy1)
        self.comboBoxWorkItems.setEditable(True)

        self.horizontalLayout_3.addWidget(self.comboBoxWorkItems)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.groupBox = QGroupBox(self.widget)
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

        self.splitter.addWidget(self.widget)
        self.widget1 = QWidget(self.splitter)
        self.widget1.setObjectName(u"widget1")
        self.verticalLayout_4 = QVBoxLayout(self.widget1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.widget1)
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

        self.buttonBox = QDialogButtonBox(self.widget1)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_4.addWidget(self.buttonBox)

        self.splitter.addWidget(self.widget1)

        self.verticalLayout_5.addWidget(self.splitter)


        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.close)
        self.buttonBox.accepted.connect(Dialog.accept)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Check in changes", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Comment:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Work item:", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Checkin items", None))
        self.bExcludeSelected.setText(QCoreApplication.translate("Dialog", u" Exclude selected ", None))
        self.bExcludeAll.setText(QCoreApplication.translate("Dialog", u"Exclude All", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Pending changes", None))
        self.bIncludeSelected.setText(QCoreApplication.translate("Dialog", u" Include selected ", None))
        self.bIncludeAll.setText(QCoreApplication.translate("Dialog", u"Include All", None))
    # retranslateUi

