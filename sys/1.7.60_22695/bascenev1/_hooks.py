# Released under the MIT License. See LICENSE for details.
#
"""Mod de Chuva de Bombas"""
# pylint: disable=missing-function-docstring
from __future__ import annotations

import babase
import bascenev1
import _bascenev1
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

# ----------------------------------------------------------
# Variáveis globais do mod
# ----------------------------------------------------------
bomba_pos = (0, 0, 0)  # posição alvo
bomba_default_tipo = "normal"
bomba_default_qtd = 10

# ----------------------------------------------------------
# Funções de chat
# ----------------------------------------------------------
def filter_chat_message(msg: str, client_id: int) -> str | None:
    """Intercepta mensagens e executa comandos /bomba e /pos"""
    global bomba_pos, bomba_default_tipo, bomba_default_qtd

    # Comando /Pos X Y Z
    if msg.lower().startswith("/pos"):
        try:
            parts = msg.split()
            x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
            bomba_pos = (x, y, z)
            babase.screenmessage(f"Posição definida: {bomba_pos}", color=(0,1,1))
            return None
        except Exception:
            babase.screenmessage("Uso correto: /Pos X Y Z", color=(1,0,0))
            return None

    # Comando /Bomba quantidade tipo
    if msg.lower().startswith("/bomba"):
        try:
            parts = msg.split()
            qtd = int(parts[1]) if len(parts) > 1 else bomba_default_qtd
            tipo = parts[2].upper() if len(parts) > 2 else bomba_default_tipo
            babase.screenmessage(f"Lançando {qtd} bombas tipo {tipo}!", color=(1,0,0))
            babase.pushcall(lambda: chuva_bombas(qtd, tipo, bomba_pos))
            return None
        except Exception:
            babase.screenmessage("Uso correto: /Bomba quantidade tipo", color=(1,0,0))
            return None

    return msg

def local_chat_message(msg: str) -> None:
    """Mostra mensagem localmente"""
    classic = babase.app.classic
    if classic is not None and classic.party_window is not None:
        classic.party_window().on_chat_message(msg)

# ----------------------------------------------------------
# Função principal de chuva de bombas
# ----------------------------------------------------------
def chuva_bombas(qtd: int, tipo: str, pos: tuple[float, float, float]):
    """Cria explosões no local definido"""
    assert babase.app.classic is not None
    for i in range(qtd):
        # Pequeno atraso entre as bombas
        babase.timer(i * 0.3, lambda: spawn_bomba(tipo, pos))

def spawn_bomba(tipo: str, pos: tuple[float, float, float]):
    """Spawn de uma bomba específica"""
    assert babase.app.classic is not None
    bomb_kwargs: dict[str, Any] = {
        "position": (pos[0], pos[1] + 5, pos[2]),  # cai do alto
        "velocity": (0, -5, 0),
    }

    # Diferentes tipos de bomba
    if tipo == "TNT":
        bomb_type = "tnt"
    elif tipo == "ICY":
        bomb_type = "ice"
    else:
        bomb_type = "normal"

    # Spawn usando bascenev1
    bscene = babase.app.classic._get_game_roots()[0]
    if hasattr(bscene, "spawn_player_bomb"):
        # se existir o método do jogo
        bscene.spawn_player_bomb(bomb_type, **bomb_kwargs)
    else:
        # fallback: cria uma explosão visual
        babase.apptimer(0, lambda: babase.explosion(pos[0], pos[1], pos[2], scale=1.0))

# ----------------------------------------------------------
# Inicialização
# ----------------------------------------------------------
babase.app.bind_chat_message_filter(filter_chat_message)
