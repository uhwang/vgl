from pathlib import Path, PurePath

def create_folder(path):
    p = Path(path)
    if p.exists() == False:
        try:
            Path.mkdir(path)
        except Exception as e:
            print("... Error: can't create %s"%path)
            return False
            
    return True