from __future__ import annotations
import babase
import _bascenev1
import __main__  # acessa funções do SpazMod.py

def launch_main_menu_session() -> None:
    assert babase.app.classic is not None
    _bascenev1.new_host_session(babase.app.classic.get_main_menu_session())

def get_player_icon(sessionplayer) -> dict:
    info = sessionplayer.get_icon_info()
    return {
        'texture': _bascenev1.gettexture(info['texture']),
        'tint_texture': _bascenev1.gettexture(info['tint_texture']),
        'tint_color': info['tint_color'],
        'tint2_color': info['tint2_color'],
    }

def filter_chat_message(msg: str, client_id: int) -> str | None:
    del client_id  # não usado

    # -----------------------------
    # /spaz chama SpazMod.Spaz()
    # -----------------------------
    if msg.startswith("/spaz"):
        try:
            parts = msg.split()
            if len(parts) == 2 and parts[1].lower() == "all":
                __main__.Spaz("all")
            else:
                qtd = int(parts[1]) if len(parts) > 1 else 1
                tipo = parts[2] if len(parts) > 2 else "Spaz"
                __main__.Spaz(tipo, qtd)
        except Exception as e:
            print("Erro /spaz:", e)
        return None

    # -----------------------------
    # /pos chama SpazMod.Pos()
    # -----------------------------
    if msg.startswith("/pos"):
        try:
            __main__.Pos()
        except Exception as e:
            print("Erro /pos:", e)
        return None

    return msg  # mensagens normais continuam

def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    if classic is None:
        return
    party_window = None if classic.party_window is None else classic.party_window()
    if party_window:
        party_window.on_chat_message(msg)
