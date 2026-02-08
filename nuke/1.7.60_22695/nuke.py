# ba_meta require api 9

from __future__ import annotations

import __main__
import babase
import bascenev1 as bs
import bascenev1lib.actor.bomb as bombmod


# ba_meta export babase.Plugin
class NuclearBombPlugin(babase.Plugin):
    """☢ Nuclear Bomb Mod"""

    def on_app_running(self):
        # expõe a função no console
        __main__.nuke = self.nuke

        print('☢ NUCLEAR BOMB MOD')
        print('MOD FEITO POR NOTASNOIN2')
        print('Digite: nuke() no console ou /nuke no chat')

        babase.screenmessage(
            '☢ Nuclear Bomb Mod carregado',
            color=(1, 0, 0)
        )

    # ======================================================
    # COMANDO PRINCIPAL
    # ======================================================
    def nuke(
        self,
        seconds: int | None = 5,
        mode: str = "normal",
        radius: float = 12000.0,
        language: str = "portugues",
    ):

        texts = {
            "portugues": {
                "count": "☢ BOMBA NUCLEAR EM",
                "boom": "💥 IMPACTO NUCLEAR 💥",
                "author": "MOD FEITO POR NOTASNOIN2",
                "need_match": "⚠ Você precisa estar em uma partida ⚠",
            },
            "english": {
                "count": "☢ NUCLEAR BOMB IN",
                "boom": "💥 NUCLEAR IMPACT 💥",
                "author": "MOD MADE BY NOTASNOIN2",
                "need_match": "⚠ You must be in a match ⚠",
            },
        }

        lang = language.lower()
        if lang not in texts:
            lang = "portugues"

        t = texts[lang]

        activity = bs.get_foreground_host_activity()
        if not activity:
            babase.screenmessage(t["need_match"], color=(1, 1, 0))
            return

        blast_map = {
            "normal": "normal",
            "tnt": "tnt",
            "icy": "ice",
            "impact": "impact",
        }

        mode = mode.lower()
        if mode not in blast_map:
            print("Tipo inválido")
            return

        # ================= CONTAGEM =================
        def countdown(time_left: int):
            act = bs.get_foreground_host_activity()
            if not act:
                return

            if time_left > 0:
                msg = f'{t["count"]} {time_left}s'
                babase.screenmessage(msg, color=(1, 0.5, 0))
                bs.timer(1.0, bs.Call(countdown, time_left - 1))
            else:
                explode()

        # ================= EXPLOSÃO =================
        def explode():
            act = bs.get_foreground_host_activity()
            if not act:
                return

            babase.screenmessage(t["boom"], color=(1, 0, 0))
            babase.screenmessage(t["author"], color=(1, 1, 1))

            try:
                bs.getsound('aliFall').play()
            except Exception:
                pass

            for p in act.players:
                if not p.actor or not p.actor.node:
                    continue

                bombmod.Blast(
                    position=p.actor.node.position,
                    blast_radius=radius,
                    blast_type=blast_map[mode],
                    source_player=None,
                )

                p.actor.handlemessage(bs.DieMessage())

        countdown(int(seconds))
