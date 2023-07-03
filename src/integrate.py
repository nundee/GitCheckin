import git
import os,re


def get_commits_related_to_work_item(workItem:int, branch=None, remote=False):
    commits = []
    errors=[]
    if not branch:
        ok,branch = git.get_current_branch_name()
        if not ok:
            git.log_error(branch)
            return [],[branch]
    if remote:
        branch="origin/"+branch
        if not git.remote_branch_exists(branch):           
            error=f"remote {branch} does not exist"
            git.log_error(error)
            return [],[error]
    elif not git.local_branch_exists(branch):
        error=f"local {branch} does not exist"
        git.log_error(error)
        return [],[error]

    for obj in git.parse_log(branch):
        if isinstance(obj,git.ParseError):
            errors.append(obj.ErrorMessage)
        elif len(obj.ParentHashes)>1 and  workItem in obj.WorkItems:
            commits.append(obj)
    return commits,errors


def get_cherry_picked_from(commit:git.Commit):
    if commit.Body:
        hashes=re.findall(r'CherryPickedFrom:([0-9a-f]+)\b',commit.Body)
        return hashes[-1] if hashes else None

def get_integrable_commits(workItem:int, dev_branch="development", main_branch="main"):
    dev_commits,_=get_commits_related_to_work_item(workItem,dev_branch, remote=True)
    main_branch_commits,_=get_commits_related_to_work_item(workItem,main_branch, remote=False)
    cherry_picked_commits = list(filter(None,[get_cherry_picked_from(c) for c in main_branch_commits]))
    relevant_dev_commits = [c for c in dev_commits if c.Hash not in cherry_picked_commits]
    return relevant_dev_commits


def create_cherry_pick_commit(commit:git.Commit):
    cherry_pick = git.Commit(
                    Title=commit.Title, 
                    Body= commit.Body,
                    WorkItems=commit.WorkItems,
                    CherryPickedFrom=commit.Hash)
    return cherry_pick

if __name__ == "__main__":
    from rich import print
    git.set_root_dir(r'C:\CAMEO\CAMEO_Cumulus')
    git.set_verbose(False)
    git.log_info("fetch origin")
    git.git("fetch", "origin","development")
    git.log_info("get integrable commits ...")
    commits = get_integrable_commits(19832,dev_branch="development", main_branch="master")
    for x in commits:
        c=create_cherry_pick_commit(x)
        print(c.asCommitMessage())
        #print(x.AbbrevHash, x.Date, x.Title, x.WorkItems)
