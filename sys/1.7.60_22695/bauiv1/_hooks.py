# Released under the MIT License. See LICENSE for details.
#
"""Safe hooks for BombSquad mods - disables broken buttons."""
from __future__ import annotations

import logging
import inspect
from typing import TYPE_CHECKING

import _bauiv1

if TYPE_CHECKING:
    import babase
    import bauiv1


def empty_call() -> None:
    pass


def _root_ui_button_press(rootuitype: "bauiv1.UIV1AppSubsystem.RootUIElement") -> None:
    """Call a UI button if it exists, else ignore."""
    import babase

    ui = getattr(babase.app, "ui_v1", None)
    if ui is None:
        return
    call = ui.root_ui_calls.get(rootuitype)
    if call is not None:
        call()


# --------------------------
# Buttons that are safe to use
# --------------------------
def root_ui_account_button_press() -> None:
    empty_call()


def root_ui_inbox_button_press() -> None:
    empty_call()


def root_ui_settings_button_press() -> None:
    empty_call()


def root_ui_achievements_button_press() -> None:
    empty_call()


# --------------------------
# Disable buttons that crash (store, tickets, etc)
# --------------------------
def root_ui_store_button_press() -> None:
    # Disabled to prevent crash
    empty_call()


def root_ui_ticket_icon_press() -> None:
    empty_call()


def root_ui_get_tokens_button_press() -> None:
    empty_call()


def root_ui_tokens_meter_press() -> None:
    empty_call()


def root_ui_trophy_meter_press() -> None:
    empty_call()


def root_ui_level_icon_press() -> None:
    empty_call()


def root_ui_menu_button_press() -> None:
    empty_call()


def root_ui_back_button_press() -> None:
    try:
        _bauiv1.root_ui_back_press()
    except Exception:
        pass


def root_ui_squad_button_press() -> None:
    empty_call()


def root_ui_inventory_button_press() -> None:
    empty_call()


def root_ui_chest_slot_0_press() -> None:
    empty_call()


def root_ui_chest_slot_1_press() -> None:
    empty_call()


def root_ui_chest_slot_2_press() -> None:
    empty_call()


def root_ui_chest_slot_3_press() -> None:
    empty_call()


# --------------------------
# Utility functions
# --------------------------
def quit_window(quit_type: "babase.QuitType") -> None:
    from babase import app

    if getattr(app, "classic", None) is None:
        logging.exception("Classic not present.")
        return

    app.classic.quit_window(quit_type)


def show_url_window(address: str) -> None:
    from babase import app

    if getattr(app, "classic", None) is None:
        logging.exception("Classic not present.")
        return

    app.classic.show_url_window(address)


def double_transition_out_warning() -> None:
    """Called if a widget is set to transition out twice."""
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_line_number = caller_frame.lineno
    logging.warning(
        "ContainerWidget was set to transition out twice;"
        " this often implies buggy code (%s line %s).\n"
        "Generally you should check _root_widget.transitioning_out and do nothing if True.",
        caller_filename,
        caller_line_number,
    )
