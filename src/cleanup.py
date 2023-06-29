import os,sys, json, time

LOCKFILE={}

def __ensure_lock():
    if "listpath" not in LOCKFILE:
        if sys.platform.startswith("win"):
            lock_dir=os.getenv("LOCALAPPDATA")
        else:
            lock_dir=os.path.join(os.getenv("HOME"),".local")
        os.makedirs(lock_dir,exist_ok=True)
        LOCKFILE["lockpath"]=os.path.join(lock_dir,".git_cleanup.lockfile")
        LOCKFILE["listpath"]=os.path.join(lock_dir,".git_cleanup.list")


def __get_lock_file():
    __ensure_lock()
    return LOCKFILE.get("lockpath")

def __get_list_file():
    __ensure_lock()
    return LOCKFILE.get("listpath")

def __try_lock():
    try:
        with open(__get_lock_file(), 'x') as lockfile:
            # write the PID of the current process so you can debug
            # later if a lockfile can be deleted after a program crash
            lockfile.write(str(os.getpid()))
            return True
    except IOError:
         # file already exists
        return False

def __unlock():
    os.unlink(__get_lock_file())

def post_cleanup(repo_dir, tmp_branch, stash_commit, pull_req_id):
    try:
        while not __try_lock():
            time.sleep(1)
        with open(__get_list_file(),"+at") as fp:
            data=dict(
                repo=repo_dir,
                branch=tmp_branch,
                stash=stash_commit,
                pull_req=pull_req_id
            )            
            json.dump(data,fp)
            fp.write("\n")
    finally:
        __unlock()

if __name__=="__main__":
    import devops_api, git
    notify_text=[]
    try:
        while not __try_lock():
            time.sleep(1)
        data=[]
        with open(__get_list_file(),"rt") as fp:
            for line in fp.readlines():
                data.append(json.loads(line))
        for task in data:
            repo_dir=task["repo"]
            git.set_repo_dir(repo_dir)
            stash_ref= None
            ok,shelves=git.list_shelves()
            if ok and len(shelves)>0:
                stash_refs = [i for i,s in enumerate(shelves) if s["CommitHash"]==task["stash"]]
                if stash_refs:
                    stash_ref = "stash@{%d}" % stash_refs[0]
                
            branch_exists=git.local_branch_exists(task["branch"])
            if (stash_ref is not None) or branch_exists:
                pr_id=task["pull_req"]
                ok,pr=devops_api.get_pull_request_by_id(pr_id)
                if ok and pr["status"]=="completed":
                    notify_text.append((f"pull request {pr['title']} is completed","info"))
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

    except Exception as ex:
        print(ex)
    finally:
        __unlock()

    if notify_text:
        text_lines = "\n".join([text for (text,_) in notify_text])
        icon = "warn" if any(icon=="warn" for (_,icon) in notify_text) else "info"
        git.git("winnotify","--title","git cleanup", "--text", text_lines, "--icon", icon)
