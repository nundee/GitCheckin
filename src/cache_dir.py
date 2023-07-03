__all__ = ["get_cache_dir"]

import sys,os
_CACHE_DIR_ = []

def get_cache_dir():
    if not _CACHE_DIR_:
        if sys.platform.startswith("win"):
            cache_dir=os.getenv("LOCALAPPDATA")
        else:
            cache_dir=os.path.join(os.getenv("HOME"),".local")
        _CACHE_DIR_.append(os.path.join(cache_dir,"git"))
        os.makedirs(_CACHE_DIR_[0],exist_ok=True)
    return _CACHE_DIR_[0]

