import yaml,json,os,httpx
from functools import cache
from joblib import Memory
from cache_dir import *

memory=Memory(get_cache_dir(), verbose=0)

CONFIG={}

def ensureConfig():
    if not CONFIG:
        cfg_path=os.path.join(os.path.dirname(__file__),"config.yaml")
        with open(cfg_path,'rt') as fp:
            cfg=yaml.safe_load(fp)
            CONFIG.update(cfg)
            CONFIG["auth"]=httpx.BasicAuth(os.getlogin(),CONFIG["token"])

def api_call(cli:str, route:str, method:str="get", body=None, **params):
    ensureConfig()
    project_in_url=bool(params.pop("project_in_url",True))
    proj=CONFIG['project']+'/' if project_in_url else ""
    url=f"{CONFIG['organizationUrl']}{proj}_apis/{cli}/{route}"
    auth=CONFIG["auth"]
    if "api-version" not in params:
        params["api-version"]="6.0"
    with httpx.Client() as client:
        if method=="get":
            rsp = client.get(url, params=params, auth=auth)
        elif method=="post":
            rsp=client.post(url,json=body,params=params, auth=auth)
        elif method=="patch":
            rsp=client.patch(url,json=body,params=params, auth=auth)
        else:
            return False,"unknown method"
        
        ct_e=rsp.charset_encoding

        if ct_e is None:
            ret=rsp.content
        elif "application/json" in rsp.headers.get("Content-Type"):
            ret=rsp.json()
        else:
            ret=rsp.text
        return rsp.is_success,ret    

def git_api_call(route:str, method="get", **params):
    return api_call("git",route, method, **params)
def wit_api_call(route:str, method="get", **params):
    return api_call("wit",route, method, **params)


def get_repos():
    ensureConfig()
    if "repositories" not in CONFIG:
        ok,ret=git_api_call("repositories")
        if ok:
            CONFIG["repositories"] = ret["value"]
    return CONFIG.get("repositories",None)


@cache
def get_repo(name):
    if (repos:=get_repos()) is not None:
        r_list=[r for r in repos if r["name"]==name]
        return r_list[0] if r_list else None

@cache
def get_repo_by_url(url):
    if (repos:=get_repos()) is not None:
        r_list=[r for r in repos if r["webUrl"]==url]
        return r_list[0] if r_list else None


def _get_avatar_(subj_desc):
    params={
        "api-version":"6.0-preview",
        "project_in_url":False
        }

    ok,ret=api_call("GraphProfile","MemberAvatars/"+subj_desc, **params)
    if ok:
        return ret


@memory.cache
def get_identities(name):
    params={
        "api-version":"6.0-preview",
        "project_in_url":False
        }
    ok,ret=api_call("IdentityPicker","Identities",method="post", **params, 
                    body={
                        "query":name,
                        "identityTypes":["user"],
                        "operationScopes":["ims","source"],
                        "options":{"MinResults":5,"MaxResults":400},
                        "properties":["DisplayName", "Mail", "SubjectDescriptor"]
                    }
                )
    if ok:
        identities= ret["results"][0]["identities"]
        for i in identities:
            i["avatar"]=_get_avatar_(i["subjectDescriptor"])
        return identities

def get_my_identity():
    ret= get_identities(os.getlogin())
    return ret[0] if ret else None

def create_pull_request(repo_url, src_branch, target_branch, title, commit_ids, workItem):
    repo=get_repo_by_url(repo_url)
    if repo is None:
        return False,f"unknown repo {repo_url}"
    
    my_id=get_my_identity()
    if my_id is None:
        return False,f"could not get my identity"
    workItemRefs=[{"id":workItem}]
    ok,ret=git_api_call(f"repositories/{repo['id']}/pullrequests",method="post",
                        body={
                            "sourceRefName": "refs/heads/"+src_branch,
                            "targetRefName": "refs/heads/"+target_branch,
                            "title":title,
                            "commits" : [{"id":cid, "workItems":workItemRefs} for cid in commit_ids],
                            "workItemRefs": workItemRefs
                        })
    return ok,ret


def update_pull_request(repo_url, pull_req_id):
    repo=get_repo_by_url(repo_url)
    if repo is None:
        return False,f"unknown repo {repo_url}"
    
    my_id=get_my_identity()
    if my_id is None:
        return False,f"could not get my identity"

    ok,ret=git_api_call(f"repositories/{repo['id']}/pullrequests/{pull_req_id}",method="patch",
                        body={
                            "autoCompleteSetBy":{"id":my_id["localId"]},
                            "completionOptions" : {"deleteSourceBranch" : True}
                        })
    return ok,ret


def get_pull_requests(repo_url, search_crit_params:dict, **params):
    repo=get_repo_by_url(repo_url)
    if repo is None:
        return False,f"unknown repo {repo_url}"
   
    for k,v in search_crit_params.items():
        if not k.startswith("searchCriteria."):
            k = "searchCriteria."+k
        params[k]=v
    ok,ret=git_api_call(f"repositories/{repo['id']}/pullrequests",**params)
    return ok,ret

def get_pull_request_by_id(pull_req_id):
    return git_api_call(f"pullrequests/{pull_req_id}")

if __name__=="__main__":
    import sys
    from pprint import pprint
    TEST_REPO="https://tfs.avl.com/Cameo/CAMEO3/_git/Playground"
    
    def test1():
        pprint(git_api_call("repositories"))

    def test_get_identity():
        obj=get_identities(sys.argv[1] if len(sys.argv)>1 else os.getlogin())
        print(obj)


    def test_my_identity():
        pprint(get_my_identity())

    # def test_create_pull_req():
    #     ok,pr=create_pull_request(TEST_REPO,"dev_test", "development","allo Ales!", 2222)
    #     if ok:
    #         ok,pr_updated=update_pull_request(TEST_REPO,pr["pullRequestId"])
    #         pprint((ok,pr_updated))
    #     else:
    #         pprint(pr)

    def test_get_pull_req(pull_req_id:int = 0):
        if pull_req_id>0:
            pprint(get_pull_request_by_id(pull_req_id))
        else:
            pprint(get_pull_requests(TEST_REPO,{"status":"completed"}))

    #test_my_identity()
    #test_create_pull_req()
    #test_get_pull_req(724)
    test_get_identity()