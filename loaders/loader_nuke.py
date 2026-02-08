# ba_meta require api 9
from __future__ import annotations

import os
import sys
import babase as ba

# ba_meta export babase.Plugin
class LoaderNuke(ba.Plugin):
    def on_app_running(self):
        try:
            mods_dir = os.path.dirname(__file__)
            version_file = os.path.join(mods_dir, "version.txt")

            if not os.path.exists(version_file):
                ba.screenmessage("❌ version.txt não encontrado", color=(1,0,0))
                return

            with open(version_file, "r") as f:
                version = f.read().strip()

            nuke_dir = os.path.join(mods_dir, "nuke", version)

            if not os.path.isdir(nuke_dir):
                ba.screenmessage("❌ Pasta nuke não encontrada", color=(1,0,0))
                return

            if nuke_dir not in sys.path:
                sys.path.insert(0, nuke_dir)

            import nuke  # importa nuke.py

            ba.screenmessage("☢ Nuke carregado com sucesso", color=(1,0,0))

        except Exception as e:
            ba.screenmessage(f"Erro no loader nuke: {e}", color=(1,0,0))
