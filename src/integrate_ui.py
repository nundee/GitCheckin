# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'integrate.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import git_icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(529, 682)
        icon = QIcon()
        icon.addFile(u":/git-icon/Git-Icon-1788C.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.workItemWidgetFrame = QFrame(Dialog)
        self.workItemWidgetFrame.setObjectName(u"workItemWidgetFrame")
        self.workItemWidgetFrame.setFrameShape(QFrame.StyledPanel)
        self.workItemWidgetFrame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_2.addWidget(self.workItemWidgetFrame)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lvCommits = QListView(self.groupBox)
        self.lvCommits.setObjectName(u"lvCommits")

        self.verticalLayout.addWidget(self.lvCommits)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.labelAvatar = QLabel(Dialog)
        self.labelAvatar.setObjectName(u"labelAvatar")
        self.labelAvatar.setMaximumSize(QSize(32, 32))
        self.labelAvatar.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.labelAvatar)

        self.lineEditIntegrator = QLineEdit(Dialog)
        self.lineEditIntegrator.setObjectName(u"lineEditIntegrator")

        self.horizontalLayout_2.addWidget(self.lineEditIntegrator)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.pbIntegrate = QPushButton(Dialog)
        self.pbIntegrate.setObjectName(u"pbIntegrate")
        self.pbIntegrate.setAutoDefault(False)

        self.horizontalLayoutButtons.addWidget(self.pbIntegrate)

        self.pbCancel = QPushButton(Dialog)
        self.pbCancel.setObjectName(u"pbCancel")
        self.pbCancel.setAutoDefault(False)

        self.horizontalLayoutButtons.addWidget(self.pbCancel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutButtons.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayoutButtons)


        self.retranslateUi(Dialog)
        self.pbIntegrate.clicked.connect(Dialog.accept)
        self.pbCancel.clicked.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Integrate work item", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Intergrable commits", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Integrator", None))
        self.labelAvatar.setText("")
        self.pbIntegrate.setText(QCoreApplication.translate("Dialog", u"Integrate", None))
        self.pbCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

