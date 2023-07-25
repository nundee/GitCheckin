# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qworkitem.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_workItemWidget(object):
    def setupUi(self, workItemWidget):
        if not workItemWidget.objectName():
            workItemWidget.setObjectName(u"workItemWidget")
        workItemWidget.resize(400, 91)
        self.verticalLayout = QVBoxLayout(workItemWidget)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.label = QLabel(workItemWidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)

        self.lineEditWorkItem = QLineEdit(workItemWidget)
        self.lineEditWorkItem.setObjectName(u"lineEditWorkItem")

        self.horizontalLayout.addWidget(self.lineEditWorkItem)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.labelWorkItemDesc = QLabel(workItemWidget)
        self.labelWorkItemDesc.setObjectName(u"labelWorkItemDesc")
        self.labelWorkItemDesc.setMinimumSize(QSize(0, 60))
        self.labelWorkItemDesc.setTextFormat(Qt.MarkdownText)
        self.labelWorkItemDesc.setWordWrap(True)
        self.labelWorkItemDesc.setMargin(3)

        self.verticalLayout.addWidget(self.labelWorkItemDesc)


        self.retranslateUi(workItemWidget)

        QMetaObject.connectSlotsByName(workItemWidget)
    # setupUi

    def retranslateUi(self, workItemWidget):
        workItemWidget.setWindowTitle(QCoreApplication.translate("workItemWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("workItemWidget", u"Work item:", None))
        self.labelWorkItemDesc.setText("")
    # retranslateUi

