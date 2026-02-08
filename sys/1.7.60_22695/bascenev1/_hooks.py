# Released under the MIT License. See LICENSE for details.
#
"""Snippets of code for use by the c++ layer."""
# pylint: disable=missing-function-docstring
from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import bascenev1 as bs
import bascenev1lib.actor.bomb as bombmod
import _bascenev1

if TYPE_CHECKING:
    from typing import Any
    import bascenev1


def launch_main_menu_session() -> None:
    assert babase.app.classic is not None
    _bascenev1.new_host_session(babase.app.classic.get_main_menu_session())


def get_player_icon(sessionplayer: bascenev1.SessionPlayer) -> dict[str, Any]:
    info = sessionplayer.get_icon_info()
    return {
        'texture': _bascenev1.gettexture(info['texture']),
        'tint_texture': _bascenev1.gettexture(info['tint_texture']),
        'tint_color': info['tint_color'],
        'tint2_color': info['tint2_color'],
    }


# =========================
# Chat e Comandos
# =========================
_original_filter_chat_message = None  # Vai guardar o filtro antigo

def filter_chat_message(msg: str, client_id: int) -> str | None:
    global _original_filter_chat_message
    if _original_filter_chat_message is None:
        # inicializa o original se ainda não tiver
        from _hooks import filter_chat_message as original
        _original_filter_chat_message = original

    # Comando /nuke
    if msg.lower().startswith("/nuke"):
        args = msg.split()
        mode = args[1] if len(args) > 1 else "normal"
        nuke(mode=mode)
        return None  # não exibe no chat

    # chama o filtro original
    return _original_filter_chat_message(msg, client_id)


def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None
    party_window = None if classic.party_window is None else classic.party_window()
    if party_window is not None:
        party_window.on_chat_message(msg)


# =========================
# Função Nuclear Bomb
# =========================
def nuke(seconds=5, mode="normal", radius=12000.0):
    """Executa a bomba nuclear."""
    texts = {
        "portugues": {
            "count": "☢ BOMBA NUCLEAR EM",
            "boom": "💥 IMPACTO NUCLEAR 💥",
            "author": "MOD FEITO POR NOTASNOIN2",
            "need_match": "⚠ Você precisa estar em uma partida ⚠"
        }
    }
    t = texts["portugues"]
    activity = bs.get_foreground_host_activity()
    if not activity:
        babase.screenmessage(t["need_match"], color=(1,0,0))
        return

    blast_map = {"normal": "normal", "tnt": "tnt", "icy": "ice", "impact": "impact"}
    mode = blast_map.get(mode.lower(), "normal")

    def countdown(time_left: int):
        act = bs.get_foreground_host_activity()
        if not act:
            return
        if time_left > 0:
            msg = f"{t['count']} {time_left}s"
            print(msg)
            babase.screenmessage(msg, color=(1,0.5,0))
            bs.timer(1.0, bs.Call(countdown, time_left - 1))
        else:
            explode()

    def explode():
        act = bs.get_foreground_host_activity()
        if not act:
            return
        print(t["boom"])
        print(t["author"])
        babase.screenmessage(t["boom"], color=(1,0,0))
        babase.screenmessage(t["author"], color=(1,1,1))
        try:
            bs.getsound('aliFall').play()
        except Exception:
            print("⚠ Som 'aliFall' não encontrado")

        with act.context:
            for p in act.players:
                if not p.actor or not p.actor.node:
                    continue
                bombmod.Blast(
                    position=p.actor.node.position,
                    blast_radius=radius,
                    blast_type=mode,
                    source_player=None
                )
                p.actor.handlemessage(bs.DieMessage())

    countdown(int(seconds))
