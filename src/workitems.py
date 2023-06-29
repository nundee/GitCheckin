from devops_api import wit_api_call,cache

@cache
def get_work_items(id_or_text):
    try:
        wiId = int(id_or_text)
        success,rsp=wit_api_call("workitems", method="get", ids=wiId, fields=','.join(["System.Id","System.Title"]))
    except:
        if id_or_text:
            whereClause = f"[System.Title] contains '{id_or_text}'"
        else:
            col="[System.ChangedDate]"
            count=500
            whereClause = f"{col} >= @Today-{count} ORDER BY {col} DESC"
        req_body=dict(
            query=f"SELECT [System.Id], [System.Title], {col} FROM WorkItems WHERE {whereClause}"
        )
        success,rsp=wit_api_call("wiql", method="post", body=req_body)
        if success:
            ids=[str(wi['id']) for wi in rsp['workItems']]
            success,rsp=wit_api_call("workitems", method="get", ids=','.join(ids), fields=','.join(["System.Id","System.Title"]))
    
    if success:
        for wi in rsp['value']:
            yield wi
    else:        
        if msg:=rsp.get('value', None) is None:
           msg=rsp.get('message', None)             
        if msg is None:
            msg="unknown error"
        yield msg



if __name__=='__main__':
    from pprint import pprint
    for wi in get_work_items(2222):
        pprint(wi)