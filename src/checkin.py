import git, devops_api,  workitems
from datetime import datetime

from pydantic import BaseModel

class FileStatus(BaseModel):
    raw_entry:str

    @property
    def Name(self):
        return self.raw_entry[3:]
    
    @property
    def Status(self):
        s = self.raw_entry[:2]
        return ' U' if s=='??' else s

    def __str__(self) -> str:
        return self.Status + '   '+ self.Name

    def __repr__(self) -> str:
        return str(self)


class CheckinModel(BaseModel):
    Comment:str
    WorkItem:int
    WorkItemDescription:str
    PendingChanges:list[FileStatus]
    CheckinItems:list[FileStatus]


def showGui(data:CheckinModel):
    from PySide6 import QtCore, QtGui, QtWidgets
    from PySide6.QtCore import Qt, QCoreApplication
    from PySide6.QtWidgets import QApplication, QDialog
    from PySide6.QtCore import Slot
    from checkin_ui import Ui_Dialog

    class FileView(QtCore.QAbstractListModel):
        def __init__(self, f_list:list[FileStatus]=[]):
                super().__init__()
                self.f_list = f_list

        def data(self, index, role):
            if role == Qt.DisplayRole:
                f=self.f_list[index.row()]
                return str(f)
            elif role == Qt.ForegroundRole:
                status = self.f_list[index.row()].Status[1]
                if status=='U':
                    return QtGui.QColor("green")
                elif status=='M':
                    return QtGui.QColor("blue")
                elif status=='D':
                    return QtGui.QColor("red")
            elif role == Qt.FontRole:
                status = self.f_list[index.row()].Status[1]
                if status=='D':
                    font=QtGui.QFont()
                    font.setStrikeOut(True)
                    return font

        def rowCount(self, index):
            return len(self.f_list)


    class CheckinDialog(QDialog):
        def __init__(self) -> None:
            super().__init__(None)
            ui=Ui_Dialog()
            self.ui=ui
            ui.setupUi(self)
            if data.Comment:
                ui.textEditComment.setPlainText(data.Comment)
            if data.WorkItem>0:
                ui.lineEditWorkItem.setText(str(data.WorkItem))
            if data.WorkItemDescription:
                ui.labelWorkItemDesc.setText(f'<span style="color:green">{data.WorkItemDescription}</span>')
            ui.listViewPendingChanges.setModel(FileView(data.PendingChanges))
            ui.listViewCheckinItems.setModel(FileView(data.CheckinItems))

            ui.bIncludeSelected.clicked.connect(self.includeSelected)
            ui.bIncludeAll.clicked.connect(self.includeAll)
            ui.bExcludeSelected.clicked.connect(self.excludeSelected)
            ui.bExcludeAll.clicked.connect(self.excludeAll)

            ui.lineEditWorkItem.editingFinished.connect(self.workItemChanged)
            ui.textEditComment.textChanged.connect(self.commentChanged)

        def notifyChanges(self):
            self.ui.listViewPendingChanges.model().layoutChanged.emit()
            self.ui.listViewCheckinItems.model().layoutChanged.emit()

        @Slot()
        def commentChanged(self):
            data.Comment=self.ui.textEditComment.toPlainText()

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
                    data.WorkItem=wiId
                    title=rsp["fields"]["System.Title"]
                    comment=self.ui.textEditComment.toPlainText()
                    if not comment:
                        self.ui.textEditComment.setPlainText(title)
            except:
                is_error=True
                title="Please enter a valid work item"

            if title:
                color="red" if is_error else "green"
                self.ui.labelWorkItemDesc.setText(f'<span style="color:{color}">{title}</span>')

        @Slot()
        def includeSelected(self):
            items = [data.PendingChanges[i.row()] for i in self.ui.listViewPendingChanges.selectedIndexes()]
            for i in items:
                data.CheckinItems.append(i)
                data.PendingChanges.remove(i)
            self.notifyChanges()

        @Slot()
        def includeAll(self):
            data.CheckinItems+=data.PendingChanges
            data.PendingChanges.clear()
            self.notifyChanges()

        @Slot()
        def excludeSelected(self):
            items = [data.CheckinItems[i.row()] for i in self.ui.listViewCheckinItems.selectedIndexes()]
            for i in items:
                data.PendingChanges.append(i)
                data.CheckinItems.remove(i)
            self.notifyChanges()

        @Slot()
        def excludeAll(self):
            data.PendingChanges+=data.CheckinItems
            data.CheckinItems.clear()
            self.notifyChanges()


    qapp=QApplication()
    app = CheckinDialog()
    return app.exec()



if __name__ == "__main__":
    import sys,os
    import argparse
    from pprint import pprint
    parser = argparse.ArgumentParser(
        prog="git checkin",
        description="check in pending changes to azure dev ops"
        )

    parser.add_argument("-w", "--work-item", type=int, default=0)
    parser.add_argument("-c", "--comment", type=str, default="")
    parser.add_argument("--no-pull", action="store_true", default=False)
    parser.add_argument("-q", "--quiet", action="store_true", default=False)

    args,checkin_list=parser.parse_known_args(sys.argv[1:])

    verbose=not args.quiet
    git.OPTIONS["verbose"]=verbose
    log = pprint if verbose else lambda x: None

    ok,currentBranch=git.get_current_branch_name()
    if not ok:
        git.log_error(currentBranch)
        sys.exit(-1)

    def abort():
        git.git("switch",currentBranch)
        sys.exit(-1)

    def check_error(ret_tuple, do_exit=True, log_output=True):
        ok,msg=ret_tuple
        if not ok:
            git.log_error(msg)
            if do_exit:abort()
        elif log_output:
            log(msg)
        return ret_tuple


    if not args.no_pull:
        # make a pull
        log("try to pull from origin ...")
        check_error(git.git("pull"))

    # get the actual status
    _,status_list=check_error(git.status(),log_output=False)

    data = CheckinModel(
        Comment=args.comment, 
        WorkItem=args.work_item,
        WorkItemDescription="",
        PendingChanges=[],
        CheckinItems=[])
    
    for f in status_list:
        f_status=FileStatus(raw_entry=f)
        if f_status.Name in checkin_list:
            data.CheckinItems.append(f_status)
        else:
            data.PendingChanges.append(f_status)

    if data.WorkItem>0:
        try:
            rsp=list(workitems.get_work_items(data.WorkItem))[0]
            if isinstance(rsp,str):
                data.WorkItem=0
                git.log_error(rsp)
            else:
                data.WorkItemDescription=rsp["fields"]["System.Title"]
        except:
            data.WorkItem=0
            git.log_error("invalid work item")


    if data.WorkItemDescription and not data.Comment:
        data.Comment=data.WorkItemDescription

    if data.WorkItem<=0 or len(data.CheckinItems)<1:        
        if not showGui(data):
            abort()

    # stash changes
    log("try shelve changes ...")
    changes=[f.Name for f in data.CheckinItems]
    _, stash_commit=check_error(git.shelve(f"Gated checkin [{data.WorkItem}] {datetime.now()}", changes))

    # create temp branch 
    tmp_branchName=f"tmp_{data.WorkItem}_{stash_commit['CommitHash']}"
    ok,_ = check_error(git.git("checkout","-b",tmp_branchName),do_exit=False)
    if not ok:
        git.git("switch",currentBranch)
        log("unshelve the last change")
        git.unshelve_last(drop=True)
        abort()

    ok,_=check_error(git.unshelve_last(drop=False), do_exit=False)
    if not ok:
        ok,ret=check_error(git.git("switch",currentBranch), do_exit=False)
        if ok:
            log("unshelve the last change")
            git.unshelve_last(drop=True)
        abort()

    # commit changes
    ok,msg=check_error(git.git("add", "--", *changes), do_exit=False)
    ok,msg=check_error(git.git("commit", "-m", data.Comment+" #"+str(data.WorkItem)), do_exit=False)
    #if not git.is_clean_working_tree():
    #    abort()
    check_error(git.git("fetch","-q", "origin"))
    ok,msg=check_error(git.git("push","-u", "origin", f"{tmp_branchName}:{tmp_branchName}" ))
    ok,msg=check_error(git.git("fetch","-q", "origin", tmp_branchName ))
    ok,msg=check_error(git.git("checkout", tmp_branchName ))
    
    lastCommit=list(git.log("-n", "1"))[0]

    git.git("switch",currentBranch)

    # create pull request
    remote_url=git.get_remote_url()
    log(f"remote url is {remote_url}")
    ok,pr=check_error(devops_api.create_pull_request(remote_url,
                                         tmp_branchName,currentBranch,
                                         data.Comment,
                                         [lastCommit["CommitHash"]],
                                         data.WorkItem
                                         ),
                                         log_output=False)
    ok,pr=check_error(devops_api.update_pull_request(remote_url,pr["pullRequestId"]))

    import cleanup
    cleanup.post_cleanup(os.getcwd(),tmp_branchName,stash_commit["CommitHash"],pr["pullRequestId"])

    import webbrowser
    webbrowser.open_new_tab(f'{remote_url}/pullrequest/{pr["pullRequestId"]}')
