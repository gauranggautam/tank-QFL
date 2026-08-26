"""
lc.py

Control a LabVIEW experiment window using pywinauto + pyautogui.

Button naming convention:
    btn0  -> scroll click position
    btn1  -> some button
    btn2  -> ...
    btn9  -> some button (you can add more)

Typical usage from another script:

    import lc as lv

    # Once at the start of a sequence:
    lv.focus_maximiser()   # focuses LabVIEW window and caches rect

    # Then you can click many times with minimal overhead:
    lv.click_button("btn1")
    lv.click_scroll("btn0", times=20)
    lv.click_scroll_then_button("btn0", "btn5", scroll_clicks=3)
"""

from pywinauto.application import Application
import pyautogui
import time

# ================== USER CONFIG ==================

# Keywords that must appear in the LabVIEW window title.
# Robust to changes in session number and V number, e.g.:
#   "LabScan V1 Session 3; MicroPL_V4.xml"
#   "LabScan V1 Session 5; MicroPL_V7.xml"
WINDOW_KEYWORDS = ["LabScan", "MicroPL_V", ".xml"]

# Logical click spots: name -> (dx, dy) offset from window top-left
BUTTON_OFFSETS = {
    "btn0": (419, 1029),  # scroll
    "btn1": (420, 86),
    "btn2": (266, 608),
    "btn3": (258, 635),
    "btn4": (144, 417),
    "btn5": (268, 695),
    "btn6": (285, 715),
    "btn7": (171, 943),
    "btn8": (268, 669),
    "btn9": (339, 841),
    # add "btn10": (...) if needed
}

# =================================================

# cached window rect after focus_maximiser()
_LAST_RECT = None


# ---------- Core window helpers ----------

def debug_list_windows():
    """Print all LabVIEW window titles to help adjust matching."""
    app = Application(backend="win32").connect(path="LabVIEW.exe")
    for w in app.windows():
        print("  -", w.window_text())


def _get_window():
    """
    Connect to LabVIEW and return the experiment window
    by searching for WINDOW_KEYWORDS in the title.
    """
    app = Application(backend="win32").connect(path="LabVIEW.exe")
    candidates = []
    for w in app.windows():
        title = w.window_text()
        if all(k in title for k in WINDOW_KEYWORDS):
            candidates.append((title, w))

    if not candidates:
        raise RuntimeError(
            f"No LabVIEW window matched keywords {WINDOW_KEYWORDS}."
        )

    _, win = candidates[0]
    return win


def focus_maximiser(maximize=False):
    """
    Focus the LabVIEW experiment window and cache its rectangle.

    Call this ONCE at the start of your script or sequence, e.g.:
        lv.focus_maximiser()

    If maximize=True, it will restore+maximize the window once.
    """
    global _LAST_RECT
    win = _get_window()
    win.set_focus()
    if maximize:
        try:
            win.restore()
        except Exception:
            pass
        try:
            win.maximize()
        except Exception:
            pass
    rect = win.rectangle()
    _LAST_RECT = rect
    return win, rect


def get_cached_rect():
    """Return the cached rect. Requires focus_maximiser() to have been called."""
    if _LAST_RECT is None:
        raise RuntimeError("No cached rect. Call focus_maximiser() first.")
    return _LAST_RECT


# ---------- Low-level click helpers ----------

def _click_absolute(x, y, move_duration=0.0):
    """Move the mouse to absolute (x, y) and click."""
    pyautogui.moveTo(x, y, duration=move_duration)
    pyautogui.click()


def click_offset(rect, dx, dy, move_duration=0.0):
    """
    Click at a position defined by an offset (dx, dy) from the top-left of rect.
    """
    x = rect.left + dx
    y = rect.top + dy
    _click_absolute(x, y, move_duration=move_duration)


# ---------- High-level button interface ----------

def click_button(name, move_duration=0.0):
    """
    Click a logical button defined in BUTTON_OFFSETS by its name.

    Requires focus_maximiser() to have been called earlier.

    Example:
        click_button("btn1")
        click_button("btn5")
    """
    if name not in BUTTON_OFFSETS:
        raise ValueError(
            f"Button '{name}' not found in BUTTON_OFFSETS. "
            f"Run calibrate_point('{name}') first and add the offset."
        )

    rect = get_cached_rect()
    dx, dy = BUTTON_OFFSETS[name]
    click_offset(rect, dx, dy, move_duration=move_duration)


def click_scroll(name="btn0", times=1, delay=0.0, move_duration=0.0):
    """
    Click a 'scroll' button (e.g. btn0) multiple times.

    Requires focus_maximiser() to have been called earlier.

    Example:
        click_scroll("btn0", times=20)
    """
    if name not in BUTTON_OFFSETS:
        raise ValueError(f"Scroll button '{name}' not found in BUTTON_OFFSETS.")

    rect = get_cached_rect()
    dx, dy = BUTTON_OFFSETS[name]

    for _ in range(times):
        click_offset(rect, dx, dy, move_duration=move_duration)
        if delay > 0:
            time.sleep(delay)


def click_scroll_then_button(
    scroll_name="btn0",
    button_name="btn1",
    scroll_clicks=1,
    move_duration=0.0,
    delay_after_scroll=0.0,
):
    """
    1) Use cached rect from focus_maximiser()
    2) Click 'scroll_name' position N times
    3) Click 'button_name'

    Both names must exist in BUTTON_OFFSETS.
    """
    if scroll_name not in BUTTON_OFFSETS or button_name not in BUTTON_OFFSETS:
        raise ValueError(
            f"Missing offsets for scroll '{scroll_name}' or button '{button_name}'. "
            f"Run calibrate_point(name) and update BUTTON_OFFSETS."
        )

    rect = get_cached_rect()

    # Click scroll position multiple times
    sdx, sdy = BUTTON_OFFSETS[scroll_name]
    for _ in range(scroll_clicks):
        click_offset(rect, sdx, sdy, move_duration=move_duration)
        if delay_after_scroll > 0:
            time.sleep(delay_after_scroll)

    # Click the final button
    bdx, bdy = BUTTON_OFFSETS[button_name]
    click_offset(rect, bdx, bdy, move_duration=move_duration)


# ---------- Calibration helpers ----------

def calibrate_point(name):
    """
    Calibrate one named point (button or scroll spot).

    Steps:
      1. Call focus_maximiser() BEFORE this (to cache rect).
      2. Move your mouse to the EXACT position for this 'name'.
      3. Press Ctrl+C in the terminal.
      4. It prints the (dx, dy) offset for BUTTON_OFFSETS.

    Example:
        focus_maximiser()
        calibrate_point("btn3")
    """
    rect = get_cached_rect()
    print(f"[CALIBRATE] Move your mouse to the desired '{name}' click location.")
    print("[CALIBRATE] Press Ctrl+C in this terminal when ready.\n")

    try:
        while True:
            x, y = pyautogui.position()
            dx = x - rect.left
            dy = y - rect.top
            msg = f"ABS(x={x}, y={y})  OFFSET(dx={dx}, dy={dy})"
            print(msg, end="\r")
            time.sleep(0.1)
    except KeyboardInterrupt:
        dx = x - rect.left
        dy = y - rect.top
        print("\n[CALIBRATE] Final offset for name '%s': (dx=%d, dy=%d)" % (name, dx, dy))
        print("[CALIBRATE] Add this line to BUTTON_OFFSETS:")
        print(f'    "{name}": ({dx}, {dy}),')
        return dx, dy


def calibrate_many(names):
    """
    Calibrate a list of button/spot names one-by-one.

    Example:
        focus_maximiser()
        calibrate_many(["btn0", "btn1", ..., "btn9"])
    """
    for n in names:
        print(f"\n========== Calibrating '{n}' ==========")
        calibrate_point(n)


# ---------- Example main (optional) ----------

if __name__ == "__main__":
    # Example calibration flow:
    # 1. Run: python lc.py
    # 2. In another terminal or after editing, do:
    #       focus_maximiser()
    #       calibrate_many([...])
    #
    # Or just import this module and call functions manually.
    print(
        "Import this module and use:\n"
        "  focus_maximiser, debug_list_windows,\n"
        "  calibrate_point, calibrate_many,\n"
        "  click_button, click_scroll, click_scroll_then_button."
    )
