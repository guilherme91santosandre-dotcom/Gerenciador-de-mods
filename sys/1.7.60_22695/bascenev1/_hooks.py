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
    _bascenev1.new_host_session(
        babase.app.classic.get_main_menu_session()
    )


def get_player_icon(sessionplayer: bascenev1.SessionPlayer) -> dict[str, Any]:
    info = sessionplayer.get_icon_info()
    return {
        'texture': _bascenev1.gettexture(info['texture']),
        'tint_texture': _bascenev1.gettexture(info['tint_texture']),
        'tint_color': info['tint_color'],
        'tint2_color': info['tint2_color'],
    }


def filter_chat_message(msg: str, client_id: int) -> str | None:
    if msg.strip().lower() == "/nuke":

        def run_nuke():
            import __main__

            activity = bs.get_foreground_host_activity()
            if not activity:
                babase.screenmessage(
                    "⚠ Entre em uma partida",
                    color=(1, 0, 0),
                )
                return

            if not hasattr(__main__, "nuke"):
                babase.screenmessage(
                    "❌ Nuke não carregado",
                    color=(1, 0, 0),
                )
                return

            # 🔥 CONTEXTO CORRETO
            with activity.context:
                __main__.nuke()

        # agenda no loop certo
        babase.app.pushcall(run_nuke)

        return None

    return msg


def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None
    party_window = (
        None if classic.party_window is None
        else classic.party_window()
    )
    if party_window is not None:
        party_window.on_chat_message(msg)
