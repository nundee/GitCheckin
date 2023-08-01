from dataclasses import dataclass, field
import os
import re
from datetime import datetime
from string import Template

ERROR_PREFIX = "__error__: "

FIELD_SEP = ">>|<<"
LOG_SEP = ">>end<<"
LOG_SEP_LEN = len(LOG_SEP)

PRETTY_FORMAT=[
    ("Hash","%H"),
    ("Subject","%B"),
    ("ParentHashes","%P"),
    ("Author","%an"),
    ("Date","%at")
    #("RefNames","%d")
]
P_FORMAT = FIELD_SEP.join(a for _,a in PRETTY_FORMAT) + LOG_SEP

@dataclass
class ParseError:
    ErrorMessage:str = ""


htmlTemplate=Template('''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" />
<style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: "\2610"; }
li.checked::marker { content: "\2612"; }
</style>
</head>
<body style=" font-family:'Calibri'; font-size:9pt;">
<h2 style=" color:#0000ff;"> ${Title} </h2>
<p> ${Body} </p>
<ul>
<li> Work item: <b> ${WorkItem} </b></li>
<li> Author: <b><span style=" color:#008000;"> ${Author} </span></b></li>
<li> Date: <b><span style=" color:#008000;"> ${Date} </span></b></li>
<li> Commit hash: <b> ${Hash} </b></li>
</ul>
</body></html>
''')


@dataclass
class Commit:
    Hash:str = ""
    Title:str = ""
    Body:object  = None
    ParentHashes:list[str] = field(default_factory=list)
    Author:str  = ""
    Date:datetime = None
    WorkItems:list[int] = field(default_factory=list)
    CherryPickedFrom:str=None
    #RefNames:

    @property
    def AbbrevHash(self):
        return self.Hash[:8]

    def asCommitMessage(self):
        wi=' #%d' % self.WorkItems[-1]
        msg=self.Title
        if not msg.endswith(wi):
            msg += wi
        if self.Body:
            msg += (os.linesep+os.linesep+self.Body)
        if self.CherryPickedFrom:
            msg += (os.linesep+os.linesep+"CherryPickedFrom:"+self.CherryPickedFrom)
        return msg

    def parseSubject(self, text:str):
        subj = text.strip().splitlines()
        title = ""
        body = None
        k=-1
        for i,line in enumerate(subj):
            if len(line)>0:
                title+=line
            else:
                k=i+1
                break
        
        workItems = re.findall(r'#(\d+)\b',title)

        if k>0 and k < (len(subj)-1):
            body="\n".join(subj[k:])
            workItems+=re.findall(r'#(\d+)\b',body)

        if workItems:
            workItems = list(set(int(w) for w in workItems))
        if body:
            m=re.search(r'\s*CherryPickedFrom:\s*([0-9a-f]+)\b',body)
            if m:
                self.CherryPickedFrom=m[0]
                s,e=m.span()
                body=body[:s]+body[e:]

        self.Title=title
        self.Body=body
        self.WorkItems=workItems

    @staticmethod
    def parse(text:str):
        commit=Commit()
        obj = dict((k,v) for (k,_),v in zip(PRETTY_FORMAT,text.split(FIELD_SEP)))
        commit.Hash = obj["Hash"]
        commit.Author = obj["Author"]
        commit.Date = datetime.fromtimestamp(int(obj["Date"]))
        commit.ParentHashes=obj["ParentHashes"].split()
        commit.parseSubject(obj["Subject"])

        return commit

    def toHtml(self):
        return htmlTemplate.substitute(
            Title=self.Title,
            Body=str(self.Body) if self.Body else '',
            WorkItem=self.WorkItems[-1],
            Author=self.Author,
            Date=self.Date,
            Hash = self.Hash
        )


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


@dataclass
class FileStatus:
    raw_entry:str

    @property
    def Name(self):
        return self.raw_entry[3:]
    
    @property
    def Status(self):
        s = self.raw_entry[:2]
        return ' U' if s=='??' else s

    def __str__(self) -> str:
        return self.Status + '   '+ self.Name

    def __repr__(self) -> str:
        return str(self)

@dataclass
class CheckinModel:
    Comment:str
    WorkItem:int
    WorkItemDescription:str
    PendingChanges:list[FileStatus]
    CheckinItems:list[FileStatus]

@dataclass
class IntegrateModel:
    WorkItem:int = -1
    Commits:list[Commit] = field(default_factory=list)
    MainBranch:str = "main"
    DevBranch:str = "development"
    Integrator:str = ""