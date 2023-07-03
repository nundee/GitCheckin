__all__ = ["post_cleanup"]

import os,sys, json, time
from cache_dir import *
LOCKFILE={}

def _ensure_lock():
    if "listpath" not in LOCKFILE:
        lock_dir=get_cache_dir()
        LOCKFILE["lockpath"]=os.path.join(lock_dir,".git_cleanup.lockfile")
        LOCKFILE["listpath"]=os.path.join(lock_dir,".git_cleanup.list")

def _get_lock_file():
    _ensure_lock()
    return LOCKFILE.get("lockpath")

def _get_list_file():
    _ensure_lock()
    return LOCKFILE.get("listpath")

def _try_lock():
    try:
        with open(_get_lock_file(), 'x') as lockfile:
            # write the PID of the current process so you can debug
            # later if a lockfile can be deleted after a program crash
            lockfile.write(str(os.getpid()))
            return True
    except IOError:
         # file already exists
        return False

def _unlock():
    os.unlink(_get_lock_file())

def post_cleanup(repo_dir, tmp_branch, stash_commit, pull_req_id):
    try:
        while not _try_lock():
            time.sleep(1)
        with open(_get_list_file(),"+at") as fp:
            data=dict(
                repo=repo_dir,
                branch=tmp_branch,
                stash=stash_commit,
                pull_req=pull_req_id
            )            
            json.dump(data,fp)
            fp.write("\n")
    finally:
        _unlock()

if __name__=="__main__":
    import devops_api, git
    notify_text=[]
    try:
        while not _try_lock():
            time.sleep(1)
        data=[]
        with open(_get_list_file(),"rt") as fp:
            for line in fp.readlines():
                data.append(json.loads(line))
        delete_list=[]
        for i_task,task in enumerate(data):
            repo_dir=task["repo"]
            git.set_root_dir(repo_dir)
            stash_ref= None
            shelves=git.list_shelves()
            if len(shelves)>0:
                stash_ref = git.find_shelve_ref(task["stash"])
            branch_exists=git.local_branch_exists(task["branch"])
            if (stash_ref is not None) or branch_exists:
                pr_id=task["pull_req"]
                ok,pr=devops_api.get_pull_request_by_id(pr_id)
                pr_status=pr["status"]
                if ok and pr_status in ("completed", "abandoned"):
                    notify_text.append((f"pull request {pr['title']} is {pr_status}","info"))
                    if branch_exists:
                        ok,ret=git.git("branch", "-D", task["branch"])
                        if ok:
                            notify_text.append((f'deleted {task["branch"]}', 'info'))
                        else:
                            notify_text.append((ret,'warn'))
                    if stash_ref is not None:
                        ok,ret=git.git("stash", "drop", stash_ref)
                        if ok:
                            notify_text.append((f'droped shelve {stash_ref}', 'info'))
                        else:
                            notify_text.append((ret,'warn'))
                else:
                    print(f"the status of pull request {pr_id} is {pr_status}")
            else:
                print("nothing to do for task ",task)
                delete_list.append(i_task)

        if delete_list:
            delete_list.reverse()
            for i in delete_list:
                del data[i]
            with open(_get_list_file(),"wt") as fp:
                for x in data:
                    json.dump(x,fp)
                    fp.write(os.linesep)

    except Exception as ex:
        print(ex)
    finally:
        _unlock()

    if notify_text:
        text_lines = "\n".join([text for (text,_) in notify_text])
        icon = "warn" if any(icon=="warn" for (_,icon) in notify_text) else "info"
        git.git("winnotify","--title","git cleanup", "--text", text_lines, "--icon", icon)
