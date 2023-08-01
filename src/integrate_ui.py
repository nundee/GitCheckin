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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListView, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QVBoxLayout, QWidget)
import git_icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1011, 742)
        font = QFont()
        font.setFamilies([u"Calibri"])
        Dialog.setFont(font)
        icon = QIcon()
        icon.addFile(u":/git-icon/Git-Icon-1788C.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setLineWidth(3)
        self.splitter.setMidLineWidth(1)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setOpaqueResize(False)
        self.splitter.setHandleWidth(10)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.comboBoxDevBranch = QComboBox(self.frame)
        self.comboBoxDevBranch.setObjectName(u"comboBoxDevBranch")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxDevBranch.sizePolicy().hasHeightForWidth())
        self.comboBoxDevBranch.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.comboBoxDevBranch)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)

        self.comboBoxMainBranch = QComboBox(self.frame)
        self.comboBoxMainBranch.setObjectName(u"comboBoxMainBranch")
        sizePolicy1.setHeightForWidth(self.comboBoxMainBranch.sizePolicy().hasHeightForWidth())
        self.comboBoxMainBranch.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.comboBoxMainBranch)


        self.horizontalLayout_4.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.workItemWidgetFrame = QFrame(self.frame)
        self.workItemWidgetFrame.setObjectName(u"workItemWidgetFrame")
        self.workItemWidgetFrame.setFrameShape(QFrame.StyledPanel)
        self.workItemWidgetFrame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_2.addWidget(self.workItemWidgetFrame)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lvCommits = QListView(self.groupBox)
        self.lvCommits.setObjectName(u"lvCommits")
        self.lvCommits.setWordWrap(True)
        self.lvCommits.setSelectionRectVisible(True)

        self.verticalLayout.addWidget(self.lvCommits)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.labelAvatar = QLabel(self.frame)
        self.labelAvatar.setObjectName(u"labelAvatar")
        self.labelAvatar.setMaximumSize(QSize(32, 32))
        self.labelAvatar.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.labelAvatar)

        self.lineEditIntegrator = QLineEdit(self.frame)
        self.lineEditIntegrator.setObjectName(u"lineEditIntegrator")

        self.horizontalLayout_2.addWidget(self.lineEditIntegrator)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.pbIntegrate = QPushButton(self.frame)
        self.pbIntegrate.setObjectName(u"pbIntegrate")
        self.pbIntegrate.setAutoDefault(False)

        self.horizontalLayoutButtons.addWidget(self.pbIntegrate)

        self.pbCancel = QPushButton(self.frame)
        self.pbCancel.setObjectName(u"pbCancel")
        self.pbCancel.setAutoDefault(False)

        self.horizontalLayoutButtons.addWidget(self.pbCancel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutButtons.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayoutButtons)

        self.splitter.addWidget(self.frame)
        self.webEngineView = QWebEngineView(self.splitter)
        self.webEngineView.setObjectName(u"webEngineView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.webEngineView.sizePolicy().hasHeightForWidth())
        self.webEngineView.setSizePolicy(sizePolicy2)
        self.webEngineView.setMinimumSize(QSize(500, 0))
        self.webEngineView.setUrl(QUrl(u"about:blank"))
        self.splitter.addWidget(self.webEngineView)

        self.verticalLayout_3.addWidget(self.splitter)


        self.retranslateUi(Dialog)
        self.pbIntegrate.clicked.connect(Dialog.accept)
        self.pbCancel.clicked.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Integrate work item", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Development branch", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Main branch", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Intergrable commits", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Integrator", None))
        self.labelAvatar.setText("")
        self.pbIntegrate.setText(QCoreApplication.translate("Dialog", u"Integrate", None))
        self.pbCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

