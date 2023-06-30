import sys,os
from subprocess import Popen,PIPE, run as run_process

ERROR_PREFIX = "__error__: "

def log_error(msg):
    print(msg,file=sys.stderr)


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
    if OPTIONS["verbose"]:
        print(cmd_line_args)
    return cmd_line_args



def g_git(command, *args, **kwargs):
    cmd_line_args=__prepare_cmd(command,*args,**kwargs)
    with Popen(cmd_line_args,stdout=PIPE, stderr=PIPE) as proc:        
        while True:
            buf=proc.stdout.readline()
            if buf:
                yield buf.decode("utf8").rstrip('\r\n')
            else:
                break
        errs = proc.stderr.readlines()
        ret=proc.wait()
        #print("ret=",ret)
        if ret != 0:
            for buf in errs:
                yield ERROR_PREFIX + buf.decode("utf8").rstrip('\r\n')


def git(command, *args, **kwargs):
    cmd_line_args=__prepare_cmd(command,*args,**kwargs)
    p=run_process(cmd_line_args,capture_output=True)
    if p.returncode:
        return False, p.stderr.decode('utf8')
    else:
        return True, [s.decode('utf8') for s in p.stdout.splitlines() if len(s)]

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


FIELD_SEP=">>|<<"
PRETTY_FORMAT=[
    ("CommitHash","%H"),
    ("Subject","%B"),
    ("ParentHashes","%P"),
    ("AuthorName","%an"),
    ("AuthorDate","%aD"),
    ("RefNames","%d")
]
P_FORMAT = FIELD_SEP.join(a for _,a in PRETTY_FORMAT)


def __parseLogLine(line):
    return dict((k,v) for (k,_),v in zip(PRETTY_FORMAT,line.split(FIELD_SEP)))

def list_shelves(*args):
    ok,lines=git("stash", "list", *args, pretty=P_FORMAT)
    if ok:
        return True, [__parseLogLine(l) for l in lines]
    else:
        return False,lines

def shelve(message,changes):
    ok, msg=git("stash","push","--include-untracked", 
                "--message", message, 
                "--", *changes)
    if not ok:
        return False,msg
    ok,shelves = list_shelves("-n", "1")
    return (True,shelves[0]) if ok else (False,shelves)

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

def log(*args, **kwargs):
    for line in g_git('log', *args, pretty=P_FORMAT, **kwargs):
        if line.startswith(ERROR_PREFIX):
            yield dict(Error=line[len(ERROR_PREFIX):])
        else:
            yield __parseLogLine(line)

if __name__=="__main__":
    from pprint import pprint
    def main():
        print("current branch is", get_current_branch_name())
        print("status")
        for line in status():
            print (line)
        # for commit in log():
        #     if "Error" in commit:
        #         pprint(commit)
        #     elif " #1" in commit["Subject"]:
        #         pprint(commit)

    main()
