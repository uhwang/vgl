from pathlib import Path, PurePath

def create_folder(path):
    p = Path(path)
    if p.exists() == False:
        try:
            p.mkdir()
        except Exception as e:
            print("... Error: %s\n... Fail to create %s"%
                 (e,path))
            return False
            
    return True