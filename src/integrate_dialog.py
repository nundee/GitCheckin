from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QModelIndex, Slot
from PySide6.QtWidgets import QApplication, QDialog,QComboBox, QCompleter, QStyledItemDelegate, QStyle

from integrate_ui import Ui_Dialog
from workItemWidget import WorkItemWidget, WorkItemModel
from devops_api import get_identities
from models import Commit, IntegrateModel
import git

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


class CommitView(QtCore.QAbstractListModel):
    def __init__(self):
            super().__init__()           
            self.commits =  []
            self.texts=[]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.commits[index.row()], self.texts[index.row()]
            #return self.commits[index.row()].toMarkdown()

    def rowCount(self, index):
        return len(self.commits)


    def setData(self,commit_list:list[Commit]):
        def mkTD(commit:Commit):
            td=QtGui.QTextDocument()
            #td.setMarkdown(commit.toMarkdown())#, QtGui.QTextDocument.MarkdownFeature.MarkdownDialectCommonMark)
            td.setHtml(commit.toHtml())
            return td

        self.commits=commit_list
        self.texts = [mkTD(c) for c in self.commits]
        self.layoutChanged.emit()




class CommitDelegate(QStyledItemDelegate):
    oddColor=QtGui.QColor("lightcyan")
    selectedColor=QtGui.QColor("lightgray")
    def paint(self, painter: QtGui.QPainter, option, index: QModelIndex) -> None:
        _, td=index.data()
        painter.save()
        self.initStyleOption(option,index)
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, self.selectedColor)
        elif index.row() % 2 == 1:
            painter.fillRect(option.rect, self.oddColor)
        painter.translate(option.rect.x(),option.rect.y())
        td.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index: QModelIndex):
        _, td=index.data()
        sz=td.size().toSize()
        return sz

class IntegrateDialog(QDialog):
    def __init__(self, iModel:IntegrateModel, parent=None) -> None:
        super().__init__(parent)
        ui=Ui_Dialog()
        self.iModel=iModel
        self.ui=ui
        ui.setupUi(self)
        self._selectBranches()
        self.workItem=WorkItemWidget(ui.workItemWidgetFrame)
        self.workItem.signals.workItemChanged.connect(self.onWorkitemChanged)
        self.ui.pbSearchCommits.clicked.connect(self.searchCommits)
        self.commitModel=CommitView()
        self.ui.lvCommits.setModel(self.commitModel)
        self.ui.lvCommits.setItemDelegate(CommitDelegate())
        self.ui.lvCommits.selectionModel().selectionChanged.connect(self.onCommitClicked)
        #self.ui.lvCommits.clicked.connect(self.onCommitClicked)
        self.userModel=UserView()
        self.completer = QCompleter(self)
        self.completer.setModel(self.userModel)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        ui.lineEditIntegrator.setCompleter(self.completer)
        ui.lineEditIntegrator.textChanged.connect(self.onIntegraterChanged)
        self.workItem.setWorkItem(iModel.WorkItem)


    def _selectBranches(self):
        def selectBranch(cb:QComboBox,branches:list[str],branch_candidates:list[str]):
            cb.setModel(model:=QtCore.QStringListModel(branches))
            for branch in branch_candidates:
                if branch:
                    try:
                        cb.setCurrentIndex(branches.index(branch))
                        return cb.currentIndex()
                    except ValueError:
                        pass
            return 0

        selectBranch(self.ui.comboBoxDevBranch,git.remote_branches(),[self.iModel.DevBranch])
        selectBranch(self.ui.comboBoxMainBranch,git.local_branches(),[self.iModel.MainBranch, "main","master"])

    @Slot(WorkItemModel)
    def onWorkitemChanged(self,wi):
        self.iModel.WorkItem=wi.WorkItem
        
    @Slot(WorkItemModel)
    def searchCommits(self):
        cb=self.ui.comboBoxDevBranch
        self.iModel.DevBranch=cb.model().stringList()[cb.currentIndex()]
        cb=self.ui.comboBoxMainBranch
        self.iModel.MainBranch=cb.model().stringList()[cb.currentIndex()]
        local_branch = self.iModel.CherryPickBranch
        if not local_branch:
            local_branch = self.iModel.MainBranch
        commits,errors=git.get_commits_related_to_work_item(self.iModel.WorkItem,local_branch,self.iModel.DevBranch)
        self.iModel.Commits=commits
        self.commitModel.setData(commits)
        self.ui.labelCommitSearch.setText(f'<span style="color:blue"><b>{len(commits)} commits found</b></span>')
        self.ui.lvCommits.selectionModel().setCurrentIndex(self.commitModel.index(0),QtCore.QItemSelectionModel.SelectionFlag.Select)

    @Slot()
    def onCommitClicked(self):
        index:QModelIndex = self.ui.lvCommits.selectionModel().currentIndex()
        commit,_ = index.data()
        url=f"{git.get_remote_url()}/commit/{commit.Hash}?refName=refs%2Fheads%2F{self.iModel.DevBranch}"
        print("open", url)
        self.ui.webEngineView.setUrl(url)

    @Slot()
    def onIntegraterChanged(self):
        text= self.ui.lineEditIntegrator.text().strip()
        if len(text)<3:
            return
        user = [u for u in self.userModel.user_list if u["displayName"]==text]
        if user:
            user=user[0]
            self.iModel.Integrator=user["localId"]
            pix=user["pixmap"]
            self.ui.labelAvatar.setPixmap(pix)
        else:
            text=text.split(",")[0].strip()
            self.userModel.set_partial_text(text)


def showGui(model:IntegrateModel):
    _=QApplication()
    app = IntegrateDialog(model)
    return app.exec()


if __name__=="__main__":
    import re,sys
    git.set_root_dir(r'C:\CAMEO\CAMEO_Cumulus')
    ok,currentBranch=git.get_current_branch_name()
    model=IntegrateModel()#WorkItem=19832)
    if currentBranch.startswith("tmp_integrate_"):
        m = re.search(r'\btmp_integrate_(\d+)_',currentBranch)
        if m:
            model.WorkItem=int(m[1])
            model.CherryPickBranch=currentBranch
        else:
            git.log_error("cannot not work on this branch")
            sys.exit(-1)


    try:
        showGui(model)
    finally:
        git.git("switch", currentBranch)
