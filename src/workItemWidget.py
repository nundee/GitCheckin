from qworkitem_ui import Ui_workItemWidget, QWidget
from PySide6.QtCore import Signal, Slot,QCoreApplication, QObject

from dataclasses import dataclass
@dataclass
class WorkItemModel:
    WorkItem:int
    WorkItemDescription:str

import workitems

class MySignals(QObject):
    workItemChanged=Signal(WorkItemModel)

class WorkItemWidget(Ui_workItemWidget):

    def __init__(self, parent: QWidget):
        self.setupUi(parent)
        self.data = WorkItemModel(WorkItem=-1, WorkItemDescription=None)
        self.lineEditWorkItem.editingFinished.connect(self.workItemChangedCB)
        self.signals=MySignals(parent)

    def setWorkItem(self, workItem:int):
        if workItem>0:
            self.data.WorkItem=workItem
            self.lineEditWorkItem.setText(str(self.data.WorkItem))
            self.lineEditWorkItem.editingFinished.emit()

    @Slot()
    def workItemChangedCB(self):
        try:
            wiId=int(self.lineEditWorkItem.text())
            self.labelWorkItemDesc.setText(f'<span style="color:blue">*fetching work item ...*</span>')
            QCoreApplication.processEvents()
            rsp=list(workitems.get_work_items(wiId))[0]
            is_error=False
            if isinstance(rsp,str):
                is_error=True
                title=rsp
            else:
                self.data.WorkItem=wiId
                title=rsp["fields"]["System.Title"]
        except:
            is_error=True
            title="Please enter a valid work item"

        if title:
            self.data.WorkItemDescription=title
            color="red" if is_error else "green"
            self.labelWorkItemDesc.setText(f'<span style="color:{color}">{title}</span>')

        self.signals.workItemChanged.emit(self.data)

if __name__=="__main__":
    from PySide6.QtWidgets import QApplication

    app=QApplication()
    w=QWidget()
    wiw=WorkItemWidget(w)
    w.show()
    app.exec()