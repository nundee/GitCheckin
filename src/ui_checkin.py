# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'checkinDdgSsl.ui'
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
    QDialog, QDialogButtonBox, QHBoxLayout, QLabel,
    QLineEdit, QListView, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(401, 452)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEditComment = QLineEdit(Dialog)
        self.lineEditComment.setObjectName(u"lineEditComment")

        self.horizontalLayout_4.addWidget(self.lineEditComment)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label)

        self.comboBoxWorkItems = QComboBox(Dialog)
        self.comboBoxWorkItems.setObjectName(u"comboBoxWorkItems")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxWorkItems.sizePolicy().hasHeightForWidth())
        self.comboBoxWorkItems.setSizePolicy(sizePolicy1)
        self.comboBoxWorkItems.setEditable(True)

        self.horizontalLayout_3.addWidget(self.comboBoxWorkItems)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.bExcludeSelected = QPushButton(Dialog)
        self.bExcludeSelected.setObjectName(u"bExcludeSelected")

        self.horizontalLayout.addWidget(self.bExcludeSelected)

        self.bExcludeAl = QPushButton(Dialog)
        self.bExcludeAl.setObjectName(u"bExcludeAl")

        self.horizontalLayout.addWidget(self.bExcludeAl)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listViewCheckinItems = QListView(Dialog)
        self.listViewCheckinItems.setObjectName(u"listViewCheckinItems")
        self.listViewCheckinItems.setSelectionMode(QAbstractItemView.MultiSelection)

        self.verticalLayout.addWidget(self.listViewCheckinItems)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.bIncludeSelected = QPushButton(Dialog)
        self.bIncludeSelected.setObjectName(u"bIncludeSelected")

        self.horizontalLayout_2.addWidget(self.bIncludeSelected)

        self.bIncludeAll = QPushButton(Dialog)
        self.bIncludeAll.setObjectName(u"bIncludeAll")

        self.horizontalLayout_2.addWidget(self.bIncludeAll)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.listViewPendingChanges = QListView(Dialog)
        self.listViewPendingChanges.setObjectName(u"listViewPendingChanges")

        self.verticalLayout.addWidget(self.listViewPendingChanges)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Check in changes", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Comment:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Work item:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Check in items", None))
        self.bExcludeSelected.setText(QCoreApplication.translate("Dialog", u"Exclude selected", None))
        self.bExcludeAl.setText(QCoreApplication.translate("Dialog", u"Exclude All", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Pending changes", None))
        self.bIncludeSelected.setText(QCoreApplication.translate("Dialog", u"Include selected", None))
        self.bIncludeAll.setText(QCoreApplication.translate("Dialog", u"Include All", None))
    # retranslateUi

