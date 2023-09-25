import git
import os,re
from models import IntegrateModel
import devops_api
from datetime import datetime
from rich import print
from rich.markdown import Markdown
from rich.prompt import Prompt


cherry_pick_prompt='''
# Possible actions
- **stop**  :  *Stop the current commit and continue with manual conflict resolving*
- **skip**  :  *Skip the current commit and continue with the rest of the sequence*
- **abort** :  *Cancel the operation and return to the pre-sequence state*
'''

def integrate_work_item(model:IntegrateModel, currentBranch):
    if not currentBranch:
        ok,currentBranch=git.get_current_branch_name()
        if not ok:
            git.log_error(currentBranch)
            sys.exit(-1)

    time_stamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    is_temp_branch=currentBranch.startswith("tmp_integrate_")
    if is_temp_branch:
        tmp_branchName=currentBranch
    else:
        tmp_branchName=f"tmp_integrate_{model.WorkItem}_{time_stamp}"

    def abort():
        if not is_temp_branch:
            ok,_=git.git("switch",currentBranch)
            if ok:
                git.git("branch", "-D", tmp_branchName)
        sys.exit(-1)

    def check_error(ret_tuple):
        if not ret_tuple[0]:
            abort()
        return ret_tuple

    commits = sorted(model.Commits,key=lambda c:c.Date)
    
    if not is_temp_branch:
        git.log_info("create and switch to temporary branch "+tmp_branchName)
        check_error(git.git("checkout","-b",tmp_branchName))
    else:
        check_error(git.git("fetch","-q", "origin"))
    for x in commits:
        ok,_=git.git("cherry-pick","--allow-empty", "-x", x.Hash)
        if not ok:
            print(Markdown(cherry_pick_prompt))
            action=Prompt.ask("What do you want me to do?", choices=['stop','skip','abort'])
            if action=="stop":
                sys.exit(-1)
            else:
                git.git("cherry-pick",'--'+action)
                if action=="abort":
                    abort()


    if not git.remote_branch_exists(tmp_branchName):
        check_error(git.git("push","-u", "origin", f"{tmp_branchName}:{tmp_branchName}" ))
    check_error(git.git("fetch","-q", "origin", tmp_branchName ))
    check_error(git.git("checkout", tmp_branchName ))

    # if we got here then is all right
    # create pull request
    remote_url=git.get_remote_url()
    git.log_info(f"remote url is {remote_url}")
    git.log_info("create pull request ...")
    ok,pr=check_error(devops_api.create_pull_request(remote_url,
                                         tmp_branchName,model.MainBranch,
                                         f"Integrate work item {model.WorkItem} into {model.MainBranch}. Created on {time_stamp}",
                                         model.WorkItem,
                                         reviewer_ids=[model.Integrator]
                                         ))
    ok,pr=check_error(devops_api.update_pull_request(remote_url,pr["pullRequestId"],auto_complete=False, delete_source_branch=True))

    from cleanup import post_cleanup
    post_cleanup(git.get_root_dir(),tmp_branchName,"",pr["pullRequestId"])

    from webbrowser import open_new_tab
    git.log_info("I will redirect you to the devops web page. Please have a look at your pull request")
    open_new_tab(f'{remote_url}/pullrequest/{pr["pullRequestId"]}')

    if is_temp_branch:
        _,devBranch = model.DevBranch.split("/", maxsplit=1)
        git.git("switch",devBranch)
    else:
        git.git("switch",currentBranch)
    return 0


if __name__ == "__main__":

    #git.set_root_dir(r'C:\CAMEO\CAMEO_Cumulus')

    import sys
    import argparse
    parser = argparse.ArgumentParser(
        prog="git integrate",
        description="integrate a work item to azure dev ops"
        )

    parser.add_argument("-w", "--work-item", type=int, default=-1)
    #parser.add_argument("--no-pull", action="store_true", default=False)
    parser.add_argument("-v", "--verbose", action="store_true", default=False)

    args=parser.parse_args(sys.argv[1:])

    git.set_verbose(args.verbose)

    from integrate_dialog import showGui
  
    model=IntegrateModel(WorkItem=args.work_item)
    ok,currentBranch=git.get_current_branch_name()   
    if not ok:
        git.log_error(currentBranch)
        sys.exit(-1)
    git.log_info("current branch is: "+currentBranch)
    if currentBranch.startswith("tmp_integrate_"):
        m = re.search(r'\btmp_integrate_(\d+)_',currentBranch)
        if m:
            model.WorkItem=int(m[1])
            model.CherryPickBranch=currentBranch
        else:
            git.log_error("cannot not work on this branch")
            sys.exit(-1)

    try:
        if not showGui(model):
            sys.exit(-1)
        sys.exit(integrate_work_item(model,currentBranch))
    finally:
        git.git("switch", currentBranch)
        