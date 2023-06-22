import yaml,json,os,httpx
from base64 import b64encode

CONFIG={}

def ensureConfig():
    if not CONFIG:
        cfg_path=os.path.join(os.path.dirname(__file__),"config.yaml")
        with open(cfg_path,'rt') as fp:
            cfg=yaml.safe_load(fp)
            CONFIG.update(cfg)
            CONFIG["auth"]=httpx.BasicAuth(os.getlogin(),CONFIG["token"])

def api_call(cli:str, route:str, method:str, body=None, **params):
    ensureConfig()
    params["api-version"]="6.0"
    with httpx.Client() as client:
        url=f"{CONFIG['organizationUrl']}/{CONFIG['project']}/_apis/{cli}/{route}"
        auth=CONFIG["auth"]
        if method=="get":
            rsp = client.get(url, params=params, auth=auth)
        elif method=="post":
            rsp=client.post(url,json=body,params=params, auth=auth)
        else:
            return False,"unknown method"
        return rsp.is_success,rsp.json()    

def git_api_call(route:str, method="get", **params):
    return api_call("git",route, method, **params)
def wit_api_call(route:str, method="get", **params):
    return api_call("wit",route, method, **params)

if __name__=="__main__":
    from pprint import pprint
    pprint(git_api_call("repositories"))
