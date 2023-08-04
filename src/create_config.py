import yaml,os

file_name=os.path.join(os.path.dirname(__file__),"config.yaml")
if not os.path.exists(file_name):
    with open(file_name,"wt") as fp:
        cfg_obj=dict(
            token="please_replace_me_with_a_valid_token",
            organizationUrl = "https://tfs.avl.com/Cameo/",
            project = "CAMEO3"
        )
        yaml.safe_dump(cfg_obj,fp)
