# Released under the MIT License. See LICENSE for details.
from __future__ import annotations

import babase
import bascenev1 as bs
import _bascenev1

def launch_main_menu_session() -> None:
    assert babase.app.classic is not None
    _bascenev1.new_host_session(babase.app.classic.get_main_menu_session())

def get_player_icon(sessionplayer: bascenev1.SessionPlayer) -> dict[str, object]:
    info = sessionplayer.get_icon_info()
    return {
        'texture': _bascenev1.gettexture(info['texture']),
        'tint_texture': _bascenev1.gettexture(info['tint_texture']),
        'tint_color': info['tint_color'],
        'tint2_color': info['tint2_color'],
    }

def filter_chat_message(msg: str, client_id: int) -> str | None:
    """Intercept chat commands and call the SpazBotPlugin."""

    # only host (-1) runs commands
    if client_id != -1:
        return msg

    text = msg.strip()
    if not text.startswith("/"):
        return msg

    parts = text[1:].split()
    if not parts:
        return None

    cmd = parts[0].lower()

    try:
        from spazbot import SpazBotPlugin

        plugin = SpazBotPlugin.get_instance()

        if cmd == "spaz":
            character = parts[1] if len(parts) > 1 else "Spaz"
            qtd = int(parts[2]) if len(parts) > 2 else 1
            plugin.Spaz(character=character, qtd=qtd)
            return None

        if cmd == "pos":
            plugin.Pos()
            return None

        if cmd == "clear":
            plugin.Spaz(character="clear")
            return None

        if cmd == "statico":
            plugin.Spaz(character="statico")
            return None

        if cmd == "pula":
            plugin.Spaz(character="pula")
            return None

        if cmd == "molesto":
            plugin.Spaz(character="molesto")
            return None

    except Exception as e:
        print(f"[HOOK ERROR] {e}")

    return None

def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    if classic is None:
        return
    party_window = None if classic.party_window is None else classic.party_window()
    if party_window is not None:
        party_window.on_chat_message(msg)
