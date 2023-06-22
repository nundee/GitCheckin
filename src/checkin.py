from typing import Optional
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import Slot
from checkin_ui import Ui_Dialog
import git,workitems


class FileModel(object):
    def __init__(self, text) -> None:
        self.name=text[3:]
        self.status=text[:2]
        if self.status=="??":
            self.status=" U"

    def __str__(self) -> str:
        return self.status + '   '+ self.name

    def __repr__(self) -> str:
        return str(self)

class FileView(QtCore.QAbstractListModel):
    def __init__(self, flist=[]):
            super().__init__()
            self.flist = flist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            f=self.flist[index.row()]
            return str(f)
        elif role == Qt.ForegroundRole:
            status = self.flist[index.row()].status[1]
            if status=='U':
                return QtGui.QColor("green")
            elif status=='M':
                return QtGui.QColor("blue")
            elif status=='D':
                return QtGui.QColor("red")
        elif role == Qt.FontRole:
            status = self.flist[index.row()].status[1]
            if status=='D':
                font=QtGui.QFont()
                font.setStrikeOut(True)
                return font

    def rowCount(self, index):
        return len(self.flist)


class CheckinApp(QDialog):
    def __init__(self, pendingChanges) -> None:
        super().__init__(None)
        ui=Ui_Dialog()
        self.ui=ui
        ui.setupUi(self)
        self.pendingChanges=pendingChanges
        self.checkinItems=[]
        self.workItem=None
        ui.listViewPendingChanges.setModel(FileView(self.pendingChanges))
        ui.listViewCheckinItems.setModel(FileView(self.checkinItems))

        ui.bIncludeSelected.clicked.connect(self.includeSelected)
        ui.bIncludeAll.clicked.connect(self.includeAll)
        ui.bExcludeSelected.clicked.connect(self.excludeSelected)
        ui.bExcludeAll.clicked.connect(self.excludeAll)

        ui.lineEditWorkItem.editingFinished.connect(self.workItemChanged)

    def notifyChanges(self):
        self.ui.listViewPendingChanges.model().layoutChanged.emit()
        self.ui.listViewCheckinItems.model().layoutChanged.emit()

    @Slot()
    def workItemChanged(self):
        try:
            wiId=int(self.ui.lineEditWorkItem.text())
            self.ui.labelWorkItemDesc.setText(f'<span style="color:blue">*fetching work item ...*</span>')
            QCoreApplication.processEvents()
            rsp=list(workitems.get_work_items(wiId))[0]
            is_error=False
            if isinstance(rsp,str):
                is_error=True
                title=rsp
            else:
                title=rsp["fields"]["System.Title"]
        except:
            is_error=True
            title="Please enter a valid work item"

        if title:
            color="red" if is_error else "green"
            self.ui.labelWorkItemDesc.setText(f'<span style="color:{color}">{title}</span>')

    @Slot()
    def includeSelected(self):
        items = [self.pendingChanges[i.row()] for i in self.ui.listViewPendingChanges.selectedIndexes()]
        for i in items:
            self.checkinItems.append(i)
            self.pendingChanges.remove(i)
        self.notifyChanges()

    @Slot()
    def includeAll(self):
        self.checkinItems+=self.pendingChanges
        self.pendingChanges.clear()
        self.notifyChanges()

    @Slot()
    def excludeSelected(self):
        items = [self.checkinItems[i.row()] for i in self.ui.listViewCheckinItems.selectedIndexes()]
        for i in items:
            self.pendingChanges.append(i)
            self.checkinItems.remove(i)
        self.notifyChanges()

    @Slot()
    def excludeAll(self):
        self.pendingChanges+=self.checkinItems
        self.checkinItems.clear()
        self.notifyChanges()


if __name__ == "__main__":
    import sys
    pendingChanges=[FileModel(line) for line in git.status()]
    qapp=QApplication(sys.argv)
    app = CheckinApp(pendingChanges)
    ret=app.exec()
    # Run the main Qt loop
    if ret:
        print(app.checkinItems)
