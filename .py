import lc as lv
import time
def acqandor():
    lv.click_scroll(name="btn1", times=50, delay=0.01, move_duration=0.1)
    lv.click_scroll(name="btn0", times=38, delay=0.01, move_duration=0.1)
    lv.click_button(name="btn2", move_duration=0.1) #apds off
    time.sleep(0.5)
    lv.click_button(name="btn3", move_duration=0.1) #FW
    time.sleep(0.5)
    lv.click_button(name="btn4", move_duration=0.1) #FW450t0420
    time.sleep(0.5)
    lv.click_button(name="btn5", move_duration=0.1) #DetectorSwitch
    time.sleep(0.5)
    lv.click_button(name="btn6", move_duration=0.1) #D toSpectro
    time.sleep(8)
    lv.click_button(name="btn7", move_duration=0.1) #Andoracq
    return lv
def revertandor():
    lv.click_button(name="btn5", move_duration=0.1) #DetectorSwitch
    time.sleep(0.5)
    lv.click_button(name="btn8", move_duration=0.1) #D toAPDs
    time.sleep(5)
    lv.click_button(name="btn3", move_duration=0.1) #FW
    time.sleep(0.5)
    lv.click_button(name="btn9", move_duration=0.1) #FW420t0450
    time.sleep(0.5)
    lv.click_button(name="btn2", move_duration=0.1)#apds back-on
    return lv


