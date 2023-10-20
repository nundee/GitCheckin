from devops_api import wit_api_call,cache

def _get_work_items(id_or_text):
    try:
        wiId = int(id_or_text)
        success,rsp=wit_api_call("workitems", method="get", ids=wiId, fields=','.join(["System.Id","System.Title"]))
    except:
        col="[System.ChangedDate]"
        if id_or_text:
            whereClause = f"[System.Title] contains '{id_or_text}'"
        else:
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

@cache
def get_work_items(id_or_text):
    return list(_get_work_items(id_or_text))

if __name__=='__main__':
    import sys
    import argparse
    import git
    parser = argparse.ArgumentParser(
        prog="git workitems",
        description="work item utility"
        )

    parser.add_argument("-w", "--work-item", type=int, default=-1)
    parser.add_argument("--show", action="store_true", default=False)
    parser.add_argument("--show-commits", action="store_true", default=False)
    parser.add_argument("--find-deps", action="store_true", default=False)
    parser.add_argument("-q", "--query", type=str, default="", help="a string to query for in the work item titles")

    argv=git.apply_common_args(sys.argv[1:])
    args=parser.parse_args(argv)

    def abort_err(text):
        git.log_error(text)
        sys.exit(-1)

    ok,currBranch=git.get_current_branch_name()
    if not ok:
        abort_err(currBranch)

    try:

        if args.show:
            if args.work_item>0:
                search_arg=args.work_item
            elif len(args.query)>0:
                search_arg=args.query
            else:
                abort_err("'show' sub command needs an work item or a search word")
            for wi in get_work_items(search_arg):
                print(f"{wi['id']}: {wi['fields']['System.Title']}")

        #elif args.show_commits:
        #    git.li
        elif args.find_deps:
            if git.local_branch_exists("master"):
                master="master"
            elif git.local_branch_exists("main"):
                master="main"
            wi_graph=git.list_non_integrated_work_items(master,"origin/"+currBranch)
            if args.work_item<=0:
                print(wi_graph)
            else:
                if args.work_item in wi_graph:
                    print(wi_graph["args.work_item"])
            
    finally:
        git.git("switch", currBranch)
