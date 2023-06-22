from subprocess import Popen,PIPE
import asyncio

ERROR_PREFIX = "__error__: "

def git(command, *args, **kwargs):
    cmd_line_args=['git', command]+list(args)
    for k,v in kwargs.items():
        cmd_line_args.append(f"--{k}={v}")
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


def status():
    return git('status', '--porcelain')


PRETTY_FORMAT=[
    ("CommitHash","%H"),
    ("Subject","%s"),
    ("ParentHashes","%P"),
    ("AuthorName","%an"),
    ("AuthorDate","%aD"),
    ("RefNames","%d")
]

FIELD_SEP=">>|<<"
P_FORMAT = FIELD_SEP.join(a for _,a in PRETTY_FORMAT)


def parseLogLine(line):
    return dict((k,v) for (k,_),v in zip(PRETTY_FORMAT,line.split(FIELD_SEP)))

def log(*args, **kwargs):
    for line in git('log', *args, pretty=P_FORMAT, **kwargs):
        if line.startswith(ERROR_PREFIX):
            yield dict(Error=line[len(ERROR_PREFIX):])
        else:
            yield parseLogLine(line)

if __name__=="__main__":
    from pprint import pprint
    def main():
        for line in status():
            print (line)
        for commit in log():
            if "Error" in commit:
                pprint(commit)
            elif " #1" in commit["Subject"]:
                pprint(commit)

    main()
