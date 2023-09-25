import sys
from subprocess import Popen,PIPE, run as run_process
from models import ERROR_PREFIX, P_FORMAT,LOG_SEP, LOG_SEP_LEN, Commit, ParseError
from rich import print

def log_info(msg):
    print(f"[cyan]{msg}[/cyan]",file=sys.stderr)
def log_error(msg):
    print(f"[red]{msg}[/red]",file=sys.stderr)


OPTIONS=dict(
    verbose=True,
    root_dir=None
)

def get_root_dir():
    p=run_process(["git","rev-parse", "--show-toplevel" ],capture_output=True)
    if p.returncode:
        return None
    else:
        return p.stdout.decode('utf8').strip()

def set_root_dir(dir):
    OPTIONS["root_dir"]=dir
def set_verbose(val:bool):
    OPTIONS["verbose"]=val


def __prepare_cmd(command, *args, **kwargs):
    cmd_line_args=['git']
    root_dir=OPTIONS.get("root_dir",None)
    if root_dir is None:
        root_dir=get_root_dir()
        set_root_dir(root_dir)
    if root_dir is None:
        log_error("not a git repository")
        sys.exit(-1)
    cmd_line_args += ["-C", root_dir, command, *args]
    for k,v in kwargs.items():
        cmd_line_args.append(f"--{k}={v}")
    print(f"[grey46][i]{' '.join(cmd_line_args)}[/i][/grey46]")
    return cmd_line_args



def check_res(t):
    if not t[0]:
        log_error(t[1])
        raise Exception(t[1])
    return t


def _g_git(command, *args, **kwargs):
    cmd_line_args=__prepare_cmd(command,*args,**kwargs)
    with Popen(cmd_line_args,stdout=PIPE, stderr=PIPE) as proc:        
        while True:
            buf=proc.stdout.readline()
            if buf:
                line = buf.decode("utf8").rstrip('\r\n')
                yield line
            else:
                break
        errs = proc.stderr.readlines()
        ret=proc.wait()
        #print("ret=",ret)
        if ret != 0:
            for buf in errs:
                err=buf.decode("utf8").rstrip('\r\n')
                print(f"[red]{err}[/red]")
                yield ERROR_PREFIX + err


def git(command, *args, **kwargs):
    cmd_line_args=__prepare_cmd(command,*args,**kwargs)
    p=run_process(cmd_line_args,capture_output=True)
    if p.returncode:
        err = p.stderr.decode('utf8')
        log_error(err)
        return False, err
    else:
        out=p.stdout.decode('utf8')
        if OPTIONS.get("verbose",False):
            print(f":right_arrow: [gold3][i]{out}[/i][/gold3]:white_check_mark:")
        else:
            print(":white_check_mark:")
        return True, out.splitlines()

def status():
    return git('status', '--porcelain')


def get_current_branch_name():
    ok,res = git("symbolic-ref", "--short", "-q", "HEAD")
    return ok, (res[0] if ok else res)

def enumerate_refs(*which_ref, sort=False, short_format=True):
    args={}
    if short_format:
        args["format"]='%(refname:short)'
    if sort:
        args["sort"]='refname'
    refs=["refs/"+r for r in which_ref]
    ok,ret = git("for-each-ref", *refs,**args)
    return ret if ok else []

def local_branches():
    return enumerate_refs("heads")

def remote_branches():
    return enumerate_refs("remotes")

def all_branches():
    return enumerate_refs("remotes","heads")
def all_tags():
    return enumerate_refs("tags")


def is_clean_working_tree():
    ok,msg=git("rev-parse", "--verify", "HEAD")
    if not ok:
        log_error(msg)
        return False
    ok,msg=git("update-index", "-q", "--ignore-submodules", "--refresh")
    if not ok:
        log_error(msg)
        return False

    # Check for unstaged changes
    ok,msg= git("diff-files", "--quiet", "--ignore-submodules")
    if not ok:
        log_error(msg)
        return False

    # Check for Uncommited changes
    #ok,msg=git("diff-index", "--cached", "--quiet", "--ignore-submodules HEAD --")
    #if not ok:
    #    log_error(msg)
    #    return False

    return True


def local_branch_exists(branchName):
    branches=enumerate_refs(f"heads/{branchName}")
    return len(branches) > 0 and (branches[0]==branchName)

def remote_branch_exists(branchName):
    branches=enumerate_refs(f"remotes/{branchName}")
    return len(branches) > 0 and (branches[0]==branchName)

def get_remote_url():
    ok,ret=git("config","--get", "remote.origin.url")
    if ok:
        return ret[0]
#
# Checks whether branch1 is successfully merged into branch2
#
def is_branch_merged_into(branch1,branch2):
    ok,merge_hash = git("merge-base",branch1, branch2)
    ok,base_hash =  git("rev-parse", branch1)
	# If the hashes are equal, the branches are merged.
    return merge_hash[0] == base_hash[0]


def list_shelves(*args) -> list[ParseError|Commit]:
    return list(g_parse_log(_g_git("stash", "list", *args, pretty=P_FORMAT)))

def shelve(message,changes):
    ok, msg=git("stash","push","--include-untracked", 
                "--message", message, 
                "--", *changes)
    if not ok:
        return False,msg
    shelves = list_shelves("-n", "1")
    return (True,shelves[0]) if shelves else (False,shelves)

def unshelve_last(drop=False):
    if drop:
        return git("stash", "pop")
    else:
        return git("stash", "apply")

def find_shelve_ref(commit_hash):
    ok,lines=git("stash", "list", pretty="%gd %H")
    if not ok:
        return None 
    refs = [r for r,h in [line.split() for line in lines] if h==commit_hash]
    return refs[0] if refs else None


def g_parse_log(_generator):
    log_text=[]
    for line in _generator:
        if line.startswith(ERROR_PREFIX):
            yield ParseError(ErrorMessage=line[len(ERROR_PREFIX):])
        if line.endswith(LOG_SEP):
            log_text.append(line[:-LOG_SEP_LEN])
            text="\n".join(log_text)
            log_text.clear()
            yield Commit.parse(text)
        else:
            log_text.append(line)


def parse_log(*args, **kwargs):
    return g_parse_log(_g_git('log', *args, pretty=P_FORMAT, **kwargs))

def get_changed_files(commit_hash):
    return git("diff-tree","--no-commit-id", "--name-only", "-r", commit_hash)


def check_branches(localBranch, remoteBranch, do_check=True):
    if not localBranch:
        _,localBranch = check_res(get_current_branch_name())
    if not remote_branch_exists(remoteBranch):           
        raise Exception(f"remote {remoteBranch} does not exist")
    elif not local_branch_exists(localBranch):
        raise Exception(f"local {localBranch} does not exist")
    origin,devBranch=remoteBranch.split('/',maxsplit=1)
    if do_check:
        check_res(git("switch",devBranch))
        check_res(git("fetch", origin,devBranch))
    check_res(git("switch",localBranch))
    if do_check and not is_clean_working_tree():
        raise Exception("the working tree is not clean")
    if do_check and not localBranch.startswith("tmp_"):
        check_res(git("pull"))


def list_non_integrated_commits(localBranch, remoteBranch, do_check=True, include_files=False):
    errors:list[str]=[]
    commits:list[Commit]=[]
    try:
        check_branches(localBranch,remoteBranch,do_check)
        already_cherry_picked=set(c.CherryPickedFrom for c in parse_log() if c.CherryPickedFrom)
        commits = list(c for c in parse_log(f'{localBranch}...{remoteBranch}', '--no-merges', '--right-only', '--cherry-pick') if c.Hash not in already_cherry_picked)
        if include_files:
            for c in commits:
                _,c.Files=get_changed_files(c.Hash)
    except Exception as ex:
        errors.append(str(ex))
    return commits,errors


def find_commit_deps(commit:Commit, all_commits:dict[str,Commit]):
    deps:list[Commit]=[]
    files=set(commit.Files)
    c=commit
    while c and c.ParentHashes:
        c=all_commits.get(c.ParentHashes[0], None)
        if c is not None and any(f in files for f in c.Files):
            deps.append(c)
            files.update(c.Files)
    return deps

def list_non_integrated_work_items(localBranch, remoteBranch, do_check=True):
    wi_graph={}
    commits,errors = list_non_integrated_commits(localBranch,remoteBranch,do_check, include_files=True)
    if errors:
        for err in errors:
            log_error(err)
        return wi_graph

    commit_table = dict((c.Hash,c) for c in commits)
    graph:dict[Commit,list[Commit]]={}
    for commit in commits:
        deps=find_commit_deps(commit,commit_table)
        if deps:
            graph[commit]=deps

    for commit in commits:
        for wi in commit.WorkItems:
            wi_deps=wi_graph.get(wi,[])
            if not wi_deps:
                wi_graph[wi] = wi_deps
            deps = graph.get(commit,None)
            if deps:
                for c in deps:
                    wi_deps+=c.WorkItems
            
    return wi_graph

def get_commits_related_to_work_item(workItem:int, localBranch, remoteBranch, do_check=True):
    commits:list[Commit] = []
    errors:list[str]=[]
    try:
        check_branches(localBranch,remoteBranch,do_check)

        grep_rx = r'(#%d\b|_%d_)' % (workItem,workItem)
        already_cherry_picked=set(c.CherryPickedFrom for c in parse_log('-E', grep=grep_rx) if c.CherryPickedFrom)

        for obj in parse_log(f'{localBranch}...{remoteBranch}', '--no-merges', '--right-only', '--cherry-pick', '-E', grep=grep_rx):
            if isinstance(obj,ParseError):
                errors.append(obj.ErrorMessage)
            elif workItem in obj.WorkItems and obj.Hash not in already_cherry_picked:
                commits.append(obj)
    except Exception as ex:
        errors.append(str(ex))

    return commits,errors



if __name__=="__main__":
    set_root_dir(r'C:\CAMEO\CAMEO_Cumulus')
    set_verbose(False)
    currBranch=get_current_branch_name()[1]
    print("current branch is", get_current_branch_name()[1])
    print("status")
    for line in status()[1]:
        print (line)

    def test_shelves():
        for commit in list_shelves():
            print(commit)

    def test_parse_log():
        for commit in parse_log("-n", "6"):
            print(commit)


    def test_non_integrated_commits():
        commits,errors=list_non_integrated_commits("master", "origin/development", do_check=False, include_files=False)
        for err in errors:
            log_error(err)
        if commits:
            commits = sorted(commits,key=lambda c:c.Date)
            for c in commits:
                if c.WorkItems:
                    print(c)

    def test_list_work_items():
        w_items=list_non_integrated_work_items("master", "origin/development", do_check=False)
        print("work items:", w_items)


    def test_work_item_commits(work_item:int):
        commits,errors=get_commits_related_to_work_item(work_item,"master", "origin/development", do_check=False)
        commits = sorted(commits,key=lambda c:c.Date)
        for commit in commits:
            print(commit)
            ok,files=get_changed_files(commit.Hash)
            #if ok:
            #    print("Files changed")
            #    print(files)
        for err in errors:
            print(err)


    try:
        #test_non_integrated_commits()
        test_list_work_items()
        #test_work_item_commits(int(sys.argv[1]))
    finally:
        git("switch",currBranch)