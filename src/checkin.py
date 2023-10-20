import git, devops_api,  workitems
from datetime import datetime
from models import CheckinModel,FileStatus

def showGui(data:CheckinModel):
    from PySide6 import QtCore, QtGui
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


    _=QApplication()
    app = CheckinDialog()
    return app.exec()



if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(
        prog="git checkin",
        description="check in pending changes to azure dev ops"
        )

    parser.add_argument("-w", "--work-item", type=int, default=0)
    parser.add_argument("-c", "--comment", type=str, default="")
    parser.add_argument("--no-pull", action="store_true", default=False)

    argv=git.apply_common_args(sys.argv[1:])
    args,checkin_list=parser.parse_known_args(argv)

    ok,currentBranch=git.get_current_branch_name()
    if not ok:
        git.log_error(currentBranch)
        sys.exit(-1)

    def abort():
        git.git("switch",currentBranch)
        sys.exit(-1)

    def check_error(ret_tuple):
        ok,_=ret_tuple
        if not ok:
            abort()
        return ret_tuple


    if not args.no_pull:
        # make a pull
        git.log_info("try to pull from origin ...")
        check_error(git.git("pull"))

    # get the actual status
    _,status_list=check_error(git.status())

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
    git.log_info("try shelve changes ...")
    changes=[f.Name for f in data.CheckinItems]
    _, stash_commit=check_error(git.shelve(f"Gated checkin {datetime.now()} [{data.WorkItem}] ## {data.Comment}", changes))

    # create temp branch 
    tmp_branchName=f"tmp_{data.WorkItem}_{stash_commit.Hash}"
    git.log_info("create and switch to temporary branch "+tmp_branchName)
    ok,_ = git.git("checkout","-b",tmp_branchName)
    if not ok:
        git.git("switch",currentBranch)
        git.log_info("unshelve the last change")
        git.unshelve_last(drop=True)
        abort()

    git.log_info("unshelve the last change")
    ok,_=git.unshelve_last(drop=False)
    if not ok:
        git.log_info("switch back to dev")
        ok,ret=git.git("switch",currentBranch)
        if ok:
            git.log_info("unshelve the last change")
            git.unshelve_last(drop=True)
        abort()

    # commit changes
    git.log_info("commit changes to temp branch")
    ok,msg=git.git("add", "--", *changes)
    commit = git.Commit(Subject=data.Comment)
    commit.parseSubject()
    commit.WorkItems+=[data.WorkItem]
    ok,msg=git.git("commit", "-m", commit.asCommitMessage())
    #if not git.is_clean_working_tree():
    #    abort()
    check_error(git.git("fetch","-q", "origin"))
    ok,msg=check_error(git.git("push","-u", "origin", f"{tmp_branchName}:{tmp_branchName}" ))
    ok,msg=check_error(git.git("fetch","-q", "origin", tmp_branchName ))
    ok,msg=check_error(git.git("checkout", tmp_branchName ))
    
    git.log_info("get the created commit")
    lastCommit=list(git.parse_log("-n", "1"))[0]

    git.git("switch",currentBranch)

    # create pull request
    remote_url=git.get_remote_url()
    git.log_info(f"remote url is {remote_url}")
    git.log_info("create pull request ...")
    ok,pr=check_error(devops_api.create_pull_request(remote_url,
                                         tmp_branchName,currentBranch,
                                         data.Comment,
                                         data.WorkItem,
                                         [lastCommit.Hash]                                         
                                         ))
    ok,pr=check_error(devops_api.update_pull_request(remote_url,pr["pullRequestId"],auto_complete=True))

    from cleanup import post_cleanup
    post_cleanup(git.get_root_dir(),tmp_branchName,stash_commit.Hash,pr["pullRequestId"])

    from webbrowser import open_new_tab
    git.log_info("I will redirect you to the devops web page. Please have a look at your pull request")
    open_new_tab(f'{remote_url}/pullrequest/{pr["pullRequestId"]}')
