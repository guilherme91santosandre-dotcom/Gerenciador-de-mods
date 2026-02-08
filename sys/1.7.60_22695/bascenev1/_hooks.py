# Released under the MIT License. See LICENSE for details.
#
"""Snippets of code for use by the c++ layer."""
# (most of these are self-explanatory)
# pylint: disable=missing-function-docstring
from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import bascenev1 as bs

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
    """Intercepta comandos no chat."""
    del client_id  # ignorado por enquanto

    # Checa se o comando é /nuke
    if msg.strip().lower() == "/nuke":
        # Tenta chamar a função nuke se ela existir no __main__
        try:
            import __main__
            if hasattr(__main__, "nuke"):
                __main__.nuke()
                babase.screenmessage("☢ Comando /nuke ativado!", color=(1, 0, 0))
            else:
                babase.screenmessage("⚠ Função nuke() não encontrada!", color=(1, 1, 0))
        except Exception as e:
            babase.screenmessage(f"Erro ao executar /nuke: {e}", color=(1, 0, 0))
        return None  # não mostra o /nuke no chat

    return msg  # todas as outras mensagens seguem normalmente


def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None
    party_window = None if classic.party_window is None else classic.party_window()
    if party_window is not None:
        party_window.on_chat_message(msg)
