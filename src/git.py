import sys
from subprocess import Popen,PIPE, run as run_process
from commit_model import ERROR_PREFIX, P_FORMAT, Commit, ParseError, g_parse_log

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
    if OPTIONS.get("verbose",False):
        print(f"[grey46][i]{' '.join(cmd_line_args)}[/i][/grey46]")
    return cmd_line_args



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
        print(f":red_circle:[red]  {err}[/red]")
        return False, err
    else:
        out=p.stdout.decode('utf8')
        if OPTIONS.get("verbose",False):
            print(f":right_arrow: [gold3][i]{out}[/i][/gold3]")
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
    ok,msg=git("diff-index", "--cached", "--quiet", "--ignore-submodules HEAD --")
    if not ok:
        log_error(msg)
        return False

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


def parse_log(*args, **kwargs):
    return g_parse_log(_g_git('log', *args, pretty=P_FORMAT, **kwargs))

if __name__=="__main__":
    from pprint import pprint
    def main():
        set_root_dir(r'C:\CAMEO\CAMEO_Cumulus')
        print("current branch is", get_current_branch_name())
        print("status")
        for line in status()[1]:
            print (line)
        
        # for commit in list_shelves():
        #     pprint(commit)


        for commit in parse_log("-n", "6"):
            pprint(commit)

    main()
