from dataclasses import dataclass, field
import json,os
import re
#from pydantic import BaseModel
from datetime import datetime

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
        msg = "%s #%d" % (self.Title,self.WorkItems[-1])
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
        cherry_picked=re.findall(r'CherryPickedFrom:\s*([0-9a-f])')
        if cherry_picked:
            self.CherryPickedFrom=cherry_picked
        self.Title=title
        self.Body=body
        self.WorkItems=workItems

    @staticmethod
    def parse(text:str):
        commit=Commit()
        obj = dict((k,v) for (k,_),v in zip(PRETTY_FORMAT,text.split(FIELD_SEP)))
        commit.Author = obj["Author"]
        commit.Date = datetime.fromtimestamp(int(obj["Date"]))
        commit.ParentHashes=obj["ParentHashes"].split()
        commit.parseSubject(obj["Subject"])

        del obj["Subject"]

        return Commit(**obj)


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
