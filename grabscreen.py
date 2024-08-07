import mss
import mss.tools
import numpy as np
import cv2

def screenshot():
    with mss.mss() as sct:
        monitor_number = 0
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }
        output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)
        output=np.array(sct_img)
        output=cv2.cvtColor(output,cv2.COLOR_RGBA2BGR)
        return output