# Released under the MIT License. See LICENSE for details.
#
"""Snippets of code for use by the c++ layer."""
# (most of these are self-explanatory)
# pylint: disable=missing-function-docstring
from __future__ import annotations

from typing import TYPE_CHECKING
import random
import babase
import bascenev1 as bs
import _bascenev1

if TYPE_CHECKING:
    from typing import Any
    import bascenev1

# =====================================================
# MENU E ÍCONES
# =====================================================
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


# =====================================================
# NUKE
# =====================================================
NUKE_ACTIVE = False

def start_nuke(duration: int, bombs_per_drop: int = 1, bomb_type: str = "NORMAL") -> None:
    """Inicia a queda de bombas no mapa"""
    global NUKE_ACTIVE
    activity = bs.get_foreground_host_activity()
    if activity is None:
        return

    NUKE_ACTIVE = True

    bomb_map = {
        "NORMAL": "normal",
        "TNT": "tnt",
        "ICE": "ice",
        "IMPACT": "impact",
    }
    bomb_type = bomb_map.get(bomb_type.upper(), "normal")

    def drop_bombs():
        if not NUKE_ACTIVE:
            return
        for _ in range(bombs_per_drop):
            pos = (
                random.uniform(-6, 6),
                random.uniform(8, 12),
                random.uniform(-6, 6),
            )
            bs.Bomb(position=pos, velocity=(0, -5, 0), bomb_type=bomb_type).autoretain()

    bs.Timer(0.5, drop_bombs, repeat=True)

    def stop_nuke():
        global NUKE_ACTIVE
        NUKE_ACTIVE = False
        bs.screenmessage("☢ NUKE FINALIZADO", color=(1, 0, 0))

    bs.Timer(duration, stop_nuke)
    bs.screenmessage(f"☢ NUKE INICIADO: {duration}s | {bombs_per_drop}x | {bomb_type.upper()}", color=(1, 0, 0))


# =====================================================
# CHAT
# =====================================================
def filter_chat_message(msg: str, client_id: int) -> str | None:
    del client_id  # Não usado

    # Comando /nuke
    if msg.lower().startswith("/nuke"):
        try:
            parts = msg.split()
            duration = int(parts[1]) if len(parts) > 1 else 10
            bombs_per_drop = int(parts[2]) if len(parts) > 2 else 1
            bomb_type = parts[3] if len(parts) > 3 else "NORMAL"
            start_nuke(duration, bombs_per_drop, bomb_type)
        except Exception:
            bs.screenmessage("Uso: /nuke <segundos> [quantidade] [tipo]", color=(1,0,0))
        return None  # Não mostra o comando no chat

    return msg  # Outras mensagens continuam normalmente


def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None
    party_window = None if classic.party_window is None else classic.party_window()
    if party_window is not None:
        party_window.on_chat_message(msg)
