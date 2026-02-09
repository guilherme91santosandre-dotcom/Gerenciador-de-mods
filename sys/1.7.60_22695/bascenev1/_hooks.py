from __future__ import annotations
from typing import TYPE_CHECKING
import babase
import _bascenev1
import __main__

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
    del client_id  # Unused by default
    return msg


def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None

    # ----------------- intercepta comandos -----------------
    msg_lower = msg.lower().strip()
    try:
        if msg_lower.startswith("/spaz"):
            parts = msg_lower.split()
            character = parts[1] if len(parts) > 1 else "Spaz"
            qtd = int(parts[2]) if len(parts) > 2 else 1
            __main__.Spaz(character, qtd)
            return  # não mostra no chat

        if msg_lower.startswith("/pos"):
            __main__.Pos()
            return  # não mostra no chat
    except Exception as e:
        babase.screenmessage(f"Erro no comando: {e}", color=(1,0,0))

    # ----------------- repassa mensagem normalmente -----------------
    party_window = None if classic.party_window is None else classic.party_window()
    if party_window is not None:
        party_window.on_chat_message(msg)
