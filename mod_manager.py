import os
import shutil
import subprocess

# ===== CONFIG =====
GAME_SYS_PATH = "/Intents"
MODS_PATH = "/sdcard/BombSquad/mods"
GIT_PATH = "/home/userland/bombsquad-git"
VERSION_FILE = f"{GIT_PATH}/VERSION.txt"

# ===== FUNÇÕES =====
def get_game_version():
    # Detecta versão pelo sys real
    for d in os.listdir(GAME_SYS_PATH):
        if "_" in d:
            return d
    return None

def get_saved_version():
    if not os.path.exists(VERSION_FILE):
        return None
    with open(VERSION_FILE) as f:
        return f.read().strip()

def wipe_old_scripts():
    targets = ["babase", "bascenev1", "bauiv1", "bacommon"]
    for t in targets:
        path = os.path.join(MODS_PATH, t)
        if os.path.exists(path):
            shutil.rmtree(path)

def git_update():
    subprocess.run(["git", "fetch"], cwd=GIT_PATH)
    subprocess.run(["git", "reset", "--hard", "origin/main"], cwd=GIT_PATH)

def install_new(version):
    src = f"{GIT_PATH}/sys/{version}"
    for folder in ["babase", "bascenev1", "bauiv1", "bacommon"]:
        shutil.copytree(
            f"{src}/{folder}",
            f"{MODS_PATH}/{folder}"
        )

# ===== MAIN =====
game_version = get_game_version()
saved_version = get_saved_version()

if game_version != saved_version:
    print("🔄 Atualização detectada")
    wipe_old_scripts()
    git_update()
    install_new(game_version)
    with open(VERSION_FILE, "w") as f:
        f.write(game_version)
else:
    print("✅ Scripts atualizados")
