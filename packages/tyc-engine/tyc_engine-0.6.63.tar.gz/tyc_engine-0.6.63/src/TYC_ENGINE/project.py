import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "templates" / "project"

def cre_prj(name: str):
    target = Path.cwd() / name
    if target.exists():
        print(f"❌ Project '{name}' already exists")
        return
    shutil.copytree(TEMPLATE_DIR, target)
    print(f"✅ Project '{name}' created")
