# Released under the MIT License. See LICENSE for details.
#
"""Hooks do BombSquad com filtro de comando /nuke"""
# pylint: disable=missing-function-docstring
from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import _bascenev1

if TYPE_CHECKING:
    from typing import Any
    import bascenev1


# ================= FUNÇÕES BÁSICAS =================
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


# ================= FILTRO DE CHAT =================
def filter_chat_message(msg: str, client_id: int) -> str | None:
    """Intercepta mensagens do chat e filtra comandos."""
    del client_id  # Ignora o ID do cliente, não usado aqui

    # Comando /nuke
    if msg.lower().startswith("/nuke"):
        try:
            import nuke  # importa o plugin Nuke
            # executa nuke()
            nuke.nuke()
        except Exception as e:
            babase.screenmessage(f"Erro ao executar nuke: {e}", color=(1, 0, 0))
        return None  # não mostra a mensagem no chat

    return msg  # deixa passar qualquer outra mensagem normal


# ================= CHAT LOCAL =================
def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None
    party_window = None if classic.party_window is None else classic.party_window()

    if party_window is not None:
        party_window.on_chat_message(msg)
