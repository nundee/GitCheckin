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

with open(os.path.join(os.path.dirname(__file__),"commitViewTemplate.html"),'rt') as fp:
    htmlTemplate=Template(fp.read())

@dataclass
class Commit:
    Hash:str = ""
    Subject:str = ""
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
        wi='Related work items: #' + str(self.WorkItems[-1])
        msg=self.Subject
        if wi not in msg:
            msg += (os.linesep+os.linesep+wi)
        return msg

    def parseSubject(self):      
        workItems = re.findall(r'#(\d+)\b',self.Subject)
        if not workItems:
            workItems = re.findall(r'_(\d+)_',self.Subject)

        if workItems:
            workItems = list(set(int(w) for w in workItems))
        m=re.search(r'\(cherry\spicked\sfrom\scommit\s([0-9a-f]+)\)',self.Subject)
        if m:
            self.CherryPickedFrom=m[1]

        self.WorkItems=workItems

    @staticmethod
    def parse(text:str):
        commit=Commit()
        obj = dict((k,v) for (k,_),v in zip(PRETTY_FORMAT,text.split(FIELD_SEP)))
        commit.Hash = obj["Hash"]
        commit.Author = obj["Author"]
        commit.Date = datetime.fromtimestamp(int(obj["Date"]))
        commit.ParentHashes=obj["ParentHashes"].split()
        commit.Subject=obj["Subject"]
        commit.parseSubject()

        return commit

    def toHtml(self):
        sep='\r\n\r\n'
        if sep in self.Subject:
            title,body=self.Subject.split(sep,maxsplit=1)
        else:
            sep='\n\n'
            if sep in self.Subject:
                title,body=self.Subject.split(sep,maxsplit=1)
            else:
                title,body=self.Subject.strip(),""
        return htmlTemplate.substitute(
            Title=title,
            Body=body,
            WorkItem=self.WorkItems[-1],
            Author=self.Author,
            Date=self.Date,
            Hash = self.Hash
        )


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
    MainBranch:str = ""
    DevBranch:str = "origin/development"
    CherryPickBranch:str = ""
    Integrator:str = ""