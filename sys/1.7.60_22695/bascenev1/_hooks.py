# ba_meta require api 9
# pylint: disable=missing-function-docstring
from __future__ import annotations

import babase

import _bascenev1

def launch_main_menu_session() -> None:
    assert babase.app.classic is not None
    _bascenev1.new_host_session(babase.app.classic.get_main_menu_session())

def get_player_icon(sessionplayer) -> dict[str, any]:
    info = sessionplayer.get_icon_info()
    return {
        'texture': _bascenev1.gettexture(info['texture']),
        'tint_texture': _bascenev1.gettexture(info['tint_texture']),
        'tint_color': info['tint_color'],
        'tint2_color': info['tint2_color'],
    }

def filter_chat_message(msg: str, client_id: int) -> str | None:
    del client_id
    return msg

def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None
    party_window = None if classic.party_window is None else classic.party_window()
    if party_window is not None:
        party_window.on_chat_message(msg)

# ---------------- Comando /update ----------------

def handle_update_command(msg: str, client_id: int) -> None:
    """
    Comando /update: Mostra na tela que o update do sys/mod está funcionando.
    """
    if msg.strip().lower() == "/update":
        # Mostra a mensagem na tela
        local_chat_message("⚡ Update do sys funcionando! ✅")
        # Aqui você pode chamar funções de atualização real se quiser:
        # ex: GerenciadorSys().atualizar_sys()
