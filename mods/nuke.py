# ba_meta require api 9
from __future__ import annotations

import babase
import bascenev1 as bs
import bascenev1lib.actor.bomb as bombmod

# ba_meta export babase.Plugin
class NuclearBombPlugin(babase.Plugin):
    """☢ Nuclear Bomb API Plugin"""

    def on_app_running(self):
        # expõe a função globalmente pro hook chamar
        babase.app.nuke = self.nuke

        print("☢ NuclearBombPlugin carregado")
        print("Use via hook: babase.app.nuke(...)")

    # ==================================================
    # FUNÇÃO QUE O HOOK VAI CHAMAR
    # ==================================================
    def nuke(
        self,
        seconds: int = 5,
        mode: str = "normal",
        radius: float = 12000.0
    ) -> None:

        activity = bs.get_foreground_host_activity()
        if not activity:
            print("⚠ Nenhuma partida ativa")
            return

        blast_types = {
            "normal": "normal",
            "tnt": "tnt",
            "ice": "ice",
            "impact": "impact"
        }

        mode = mode.lower()
        if mode not in blast_types:
            print("⚠ Tipo inválido:", mode)
            return

        def explode():
            act = bs.get_foreground_host_activity()
            if not act:
                return

            babase.screenmessage("☢ IMPACTO NUCLEAR ☢", color=(1, 0, 0))

            with act.context:
                for p in act.players:
                    if not p.actor or not p.actor.node:
                        continue

                    bombmod.Blast(
                        position=p.actor.node.position,
                        blast_radius=radius,
                        blast_type=blast_types[mode],
                        source_player=None
                    )
                    p.actor.handlemessage(bs.DieMessage())

        # contagem
        def countdown(t: int):
            if t > 0:
                babase.screenmessage(
                    f"☢ BOMBA NUCLEAR EM {t}s",
                    color=(1, 0.5, 0)
                )
                bs.timer(1.0, bs.Call(countdown, t - 1))
            else:
                explode()

        countdown(seconds)
