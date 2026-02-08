# Released under the MIT License. See LICENSE for details.
#
"""Snippets of code for use by the c++ layer."""
# pylint: disable=missing-function-docstring
from __future__ import annotations

from typing import TYPE_CHECKING
import babase
import bascenev1 as bs
import _bascenev1

if TYPE_CHECKING:
    from typing import Any
    import bascenev1


# =====================================================
# MAIN MENU
# =====================================================
def launch_main_menu_session() -> None:
    assert babase.app.classic is not None
    _bascenev1.new_host_session(
        babase.app.classic.get_main_menu_session()
    )


# =====================================================
# PLAYER ICON
# =====================================================
def get_player_icon(
    sessionplayer: bascenev1.SessionPlayer
) -> dict[str, Any]:
    info = sessionplayer.get_icon_info()
    return {
        'texture': _bascenev1.gettexture(info['texture']),
        'tint_texture': _bascenev1.gettexture(info['tint_texture']),
        'tint_color': info['tint_color'],
        'tint2_color': info['tint2_color'],
    }


# =====================================================
# CHAT FILTER  (/nuke)
# =====================================================
def filter_chat_message(msg: str, client_id: int) -> str | None:
    msg_clean = msg.strip().lower()

    if msg_clean == "/nuke":
        import __main__

        def call_nuke():
            if hasattr(__main__, "nuke"):
                try:
                    __main__.nuke()
                except Exception as e:
                    babase.screenmessage(
                        f"Erro no nuke: {e}",
                        color=(1, 0, 0),
                    )
            else:
                babase.screenmessage(
                    "Nuke não carregado!",
                    color=(1, 0, 0),
                )

        # 🔥 ISSO É O MAIS IMPORTANTE
        bs.pushcall(call_nuke)

        return None  # não mostra /nuke no chat

    return msg


# =====================================================
# LOCAL CHAT
# =====================================================
def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None

    party_window = (
        None if classic.party_window is None
        else classic.party_window()
    )

    if party_window is not None:
        party_window.on_chat_message(msg)
