from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QModelIndex, Slot
from PySide6.QtWidgets import QApplication, QDialog, QCompleter

from integrate_ui import Ui_Dialog
from devops_api import get_identities, get_my_identity

class UserView(QtCore.QAbstractListModel):
    def __init__(self):
            super().__init__()           
            self.user_list =  []
            self.ids=set()
            self.partial_text=""
            self.partial_text_changed=False

    def set_partial_text(self, text):
        if text != self.partial_text:
            self.partial_text=text
            self.partial_text_changed=True
            #self.layoutChanged.emit()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            f=self.user_list[index.row()]
            return f["displayName"]
        elif role == Qt.DecorationRole:
            f=self.user_list[index.row()]
            if (pix:=f.get("pixmap",None)) is None:
                pix=QtGui.QPixmap()
                pix.loadFromData(f["avatar"])
                f["pixmap"]=pix
            return QtGui.QIcon(pix)
        elif role == Qt.EditRole:
            f=self.user_list[index.row()]
            return f["displayName"]

    def rowCount(self, index):
        return len(self.user_list)

    def canFetchMore(self, index):
        return len(self.user_list) < 200

    def fetchMore(self, index):
        if self.partial_text_changed:
            new_list=get_identities(self.partial_text)
            if new_list:
                self.partial_text_changed=False
                start=len(self.ids)
                new_list=[u for u in new_list if u["localId"] not in self.ids]
                self.beginInsertRows(QModelIndex(), start, min(200,start + len(new_list)))
                
                for u in new_list:
                    self.user_list.append(u)
                    self.ids.add(u["localId"])

                self.endInsertRows()

class IntegrateDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        ui=Ui_Dialog()
        self.ui=ui
        ui.setupUi(self)
        self.model=UserView()
        self.completer = QCompleter(self)
        self.completer.setModel(self.model)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        ui.lineEditIntegrator.setCompleter(self.completer)
        ui.lineEditIntegrator.textChanged.connect(self.onIntegraterChanged)

    @Slot()
    def onIntegraterChanged(self):
        text= self.ui.lineEditIntegrator.text().strip()
        if len(text)<3:
            return
        user = [u for u in self.model.user_list if u["displayName"]==text]
        if user:
            pix=user[0]["pixmap"]
            self.ui.labelAvatar.setPixmap(pix)
        else:
            text=text.split(",")[0].strip()
            self.model.set_partial_text(text)


if __name__=="__main__":
    _=QApplication()
    app = IntegrateDialog()
    app.exec()
