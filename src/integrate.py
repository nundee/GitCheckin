import git
import os,re
from models import IntegrateModel
from datetime import datetime
from rich import print




# def get_cherry_picked_from(commit:git.Commit):
#     if commit.Body:
#         hashes=re.findall(r'CherryPickedFrom:([0-9a-f]+)\b',commit.Body)
#         return hashes[-1] if hashes else None

# def get_integrable_commits(workItem:int, dev_branch="origin/development", main_branch="main"):
#     relevant_commits,_ = get_commits_related_to_work_item(workItem,main_branch, dev_branch)
#     return relevant_commits
    #dev_commits,_=get_commits_related_to_work_item(workItem,dev_branch, remote=True)
    #main_branch_commits,_=get_commits_related_to_work_item(workItem,main_branch, remote=False)
    #cherry_picked_commits = list(filter(None,[get_cherry_picked_from(c) for c in main_branch_commits]))
    #relevant_dev_commits = [c for c in dev_commits if c.Hash not in cherry_picked_commits]
    #return relevant_dev_commits


def integrate_work_item(model:IntegrateModel):
    ok,currentBranch=git.get_current_branch_name()
    if not ok:
        git.log_error(currentBranch)
        sys.exit(-1)

    tmp_branchName=f"tmp_integrate_{model.WorkItem}_{datetime.now().strftime('%Y_%m_%H_%M_%S')}"

    def abort():
        ok,_=git.git("switch",currentBranch)
        if ok:
            git.git("branch", "-D", tmp_branchName)
        sys.exit(-1)

    def check_error(ret_tuple):
        if not ret_tuple[0]:
            abort()
        return ret_tuple

    #git.log_info("fetch origin")
    #origin,devBranch=model.DevBranch.split('/',maxsplit=2)
    commits = sorted(model.Commits,key=lambda c:c.Date)
    git.log_info("create and switch to temporary branch "+tmp_branchName)
    check_error(git.git("checkout","-b",tmp_branchName))
    for x in commits:
        check_error(git.git("cherry-pick","-x", x.Hash))
    
    git.git("switch",currentBranch)
    return 0


if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(
        prog="git checkin",
        description="check in pending changes to azure dev ops"
        )

    parser.add_argument("-w", "--work-item", type=int, default=-1)
    #parser.add_argument("--no-pull", action="store_true", default=False)
    parser.add_argument("-v", "--verbose", action="store_true", default=True)

    args=parser.parse_args(sys.argv[1:])

    git.set_verbose(args.verbose)

    from integrate_dialog import showGui
  
    model=IntegrateModel(WorkItem=args.work_item)
    ok,currentBranch=git.get_current_branch_name()
    if not ok:
        git.log_error(currentBranch)
        sys.exit(-1)
    try:
        if not showGui(model):
            sys.exit(-1)
        sys.exit(integrate_work_item(model))
    finally:
        git.git("switch", currentBranch)
        