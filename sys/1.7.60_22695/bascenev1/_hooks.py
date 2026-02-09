# Released under the MIT License. See LICENSE for details.
#
"""Snippets of code for use by the c++ layer."""
# (most of these are self-explanatory)
# pylint: disable=missing-function-docstring
from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import bascenev1 as bs
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


def filter_chat_message(msg: str, client_id: int) -> str | None:
    """
    Hook do chat.
    ClientID -1 = host
    """

    # só o host pode usar comandos
    if client_id != -1:
        return msg

    if not msg.startswith('/'):
        return msg

    args = msg[1:].split()
    if not args:
        return None

    cmd = args[0].lower()

    try:
        from SpazBotPlugin import SpazBotPlugin
        plugin = SpazBotPlugin.get_instance()

        # /spaz Zoe 3
        if cmd == 'spaz':
            character = args[1] if len(args) > 1 else 'Spaz'
            qtd = int(args[2]) if len(args) > 2 else 1
            plugin.Spaz(character=character, qtd=qtd)
            return None

        # /pos
        if cmd == 'pos':
            plugin.Pos()
            return None

        # /clear
        if cmd == 'clear':
            plugin.Spaz(character='clear')
            return None

        # /statico
        if cmd == 'statico':
            plugin.Spaz(character='statico')
            return None

        # /pula
        if cmd == 'pula':
            plugin.Spaz(character='pula')
            return None

        # /molesto
        if cmd == 'molesto':
            plugin.Spaz(character='molesto')
            return None

    except Exception as e:
        print(f'[HOOK ERROR] {e}')

    return None


def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None
    party_window = (
        None if classic.party_window is None else classic.party_window()
    )

    if party_window is not None:
        party_window.on_chat_message(msg)
