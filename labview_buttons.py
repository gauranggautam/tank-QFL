"""
lc.py

Control a LabVIEW experiment window using pywinauto + pyautogui.

Button naming convention:
    btn0  -> scroll click position
    btn1  -> some button
    btn2  -> ...
    ...
    btn10 -> some button

Typical usage:

    import labview_buttons as lv

    # ONE TIME: calibrate positions
    lv.calibrate_many(["btn0", "btn1", "btn2", ..., "btn10"])

    # After pasting offsets into BUTTON_OFFSETS:
    lv.click_button("btn1")
    lv.click_scroll("btn0", times=20)
    lv.click_scroll_then_button("btn0", "btn5", scroll_clicks=3)
"""

from pywinauto.application import Application
import pyautogui
import time

# ================== USER CONFIG ==================

# Exact title of your LabVIEW experiment window
WINDOW = "LabScan V1 Session 3; MicroPL_V4.xml"

# Logical click spots: name -> (dx, dy) offset from window top-left
# Fill this after running calibrate_point / calibrate_many.
BUTTON_OFFSETS = {
    # Example after calibration (you will fill this):
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
}

# How long to pause after focus/maximize, in seconds
FOCUS_DELAY = 0.1

# =================================================


# ---------- Core window helpers ----------

def _get_window():
    """Connect to LabVIEW and return the experiment window."""
    app = Application(backend="win32").connect(path="LabVIEW.exe")
    win = app.window(title=WINDOW)
    return win


def focus_and_maximize():
    """
    Focus and maximize the LabVIEW experiment window.
    Returns (window, rect).
    """
    win = _get_window()
    win.set_focus()
    #time.sleep(0.1)
    #time.sleep(0.1)
    #win.maximize()
    time.sleep(FOCUS_DELAY)
    rect = win.rectangle()
    #print(f"[INFO] Window rect: left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}")
    return win, rect


def get_rect():
    """Get the current rectangle of the experiment window (no maximize)."""
    win = _get_window()
    rect = win.rectangle()
    print(f"[INFO] Window rect: left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}")
    return win, rect


# ---------- Low-level click helpers ----------

def _click_absolute(x, y, move_duration=0.1):
    """Move the mouse to absolute (x, y) and click."""
    pyautogui.moveTo(x, y, duration=move_duration)
    pyautogui.click()


def click_offset(rect, dx, dy, move_duration=0.1):
    """
    Click at a position defined by an offset (dx, dy) from the top-left of the window rect.
    """
    x = rect.left + dx
    y = rect.top + dy
    _click_absolute(x, y, move_duration=move_duration)


# ---------- High-level button interface ----------

def click_button(name, move_duration=0.1):
    """
    Click a logical button defined in BUTTON_OFFSETS by its name.

    Example:
        click_button("btn1")
        click_button("btn5")
    """
    if name not in BUTTON_OFFSETS:
        raise ValueError(
            f"Button '{name}' not found in BUTTON_OFFSETS. "
            f"Run calibrate_point('{name}') first and add the offset."
        )

    win, rect = focus_and_maximize()
    dx, dy = BUTTON_OFFSETS[name]
    #print(f"[INFO] Clicking '{name}' at offset dx={dx}, dy={dy}")
    click_offset(rect, dx, dy, move_duration=move_duration)


def click_scroll(name="btn0", times=1, delay=0.1, move_duration=0.1):
    """
    Click a 'scroll' button (e.g. btn0) multiple times.

    Example:
        click_scroll("btn0", times=20)
    """
    if name not in BUTTON_OFFSETS:
        raise ValueError(f"Scroll button '{name}' not found in BUTTON_OFFSETS.")

    win, rect = focus_and_maximize()
    dx, dy = BUTTON_OFFSETS[name]

    for i in range(times):
        #print(f"[INFO] Scroll click {i+1}/{times} at dx={dx}, dy={dy}")
        click_offset(rect, dx, dy, move_duration=move_duration)
        time.sleep(delay)


def click_scroll_then_button(
    scroll_name="btn0",
    button_name="btn1",
    scroll_clicks=1,
    move_duration=0.1,
    delay_after_scroll=0.3,
):
    """
    1) Focus + maximize window
    2) Click 'scroll_name' position N times
    3) Click 'button_name'

    Both names must exist in BUTTON_OFFSETS.
    """
    missing = [n for n in (scroll_name, button_name) if n not in BUTTON_OFFSETS]
    if missing:
        raise ValueError(
            f"Missing offsets for: {missing}. "
            f"Run calibrate_point(name) and update BUTTON_OFFSETS."
        )

    win, rect = focus_and_maximize()

    # Click scroll position multiple times
    sdx, sdy = BUTTON_OFFSETS[scroll_name]
    for i in range(scroll_clicks):
        #print(f"[INFO] Scroll click {i+1}/{scroll_clicks} at dx={sdx}, dy={sdy}")
        click_offset(rect, sdx, sdy, move_duration=move_duration)
        time.sleep(delay_after_scroll)

    # Click the final button
    bdx, bdy = BUTTON_OFFSETS[button_name]
    print(f"[INFO] Clicking button '{button_name}' at dx={bdx}, dy={bdy}")
    click_offset(rect, bdx, bdy, move_duration=move_duration)


# ---------- Calibration helpers ----------

def calibrate_point(name):
    """
    Calibrate one named point (button or scroll spot).

    Steps:
      1. LabVIEW window is focused + maximized.
      2. Move your mouse to the EXACT position for this 'name'.
      3. Press Ctrl+C in the terminal.
      4. It prints the (dx, dy) offset for BUTTON_OFFSETS.

    Example:
        calibrate_point("btn3")
    """
    win, rect = focus_and_maximize()
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
        calibrate_many(["btn0", "btn1", ..., "btn10"])
    """
    for n in names:
        print(f"\n========== Calibrating '{n}' ==========")
        calibrate_point(n)


# ---------- Example main (optional) ----------

if __name__ == "__main__":
    # ONE-TIME CALIBRATION EXAMPLE:
    # 1. Uncomment this block.
    # 2. Run:  python labview_clicker.py
    # 3. For each name:
    #       - Window will maximize
    #       - Move mouse to that button/spot
    #       - Press Ctrl+C
    #       - Copy printed offset line into BUTTON_OFFSETS above
    #
    #names_to_calibrate = [
    #     "btn0",  # scroll
    #     "btn1",   #scollup
    #     "btn2",   #apdswitch
    #     "btn3",   #filterwheel
    #     "btn4",   #FW450to420
    #     "btn5",   #Detector
    #     "btn6",   #D:APDtoSpectro
    #     "btn7",   #AcquireAndor(set_settings)
    #     "btn8",   #D:SpectrotoAPD
    #     "btn9",   #FW420to450
    #     "btn10",  
    #]
    #calibrate_many(names_to_calibrate)

    print("Import this module and use: calibrate_point, calibrate_many, click_button, click_scroll, click_scroll_then_button.")
