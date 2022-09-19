from gpiozero import PWMOutputDevice
from gpiozero import CPUTemperature
import time
import os
import signal
import sys

# Raspberry Pi Fan Controler pi
RPI_FAN_PIN = 18

# Time delay per check
PERIOD_S = 10

PID_FILE = "/tmp/PiFanController.pid"

def _save_my_pid(filename):
    with open(filename, "w+") as f:
        f.write(str(os.getpid()))
        f.flush()
        pass
    pass

def _remove_my_pid(filename):
    os.remove(filename)
    pass

step_down_counter = 0
last_temp = 0
def fanValConvert(temp):
    global step_down_counter
    global last_temp

    if step_down_counter > 0 and temp <= last_temp:
        print("Step down in %d seconds" % (step_down_counter * PERIOD_S))
        step_down_counter -= 1
        return -1

    last_temp = temp

    if temp < 35:
        step_down_counter = 0
        return 0.0
    if temp < 50:
        step_down_counter = 3
        return 0.3
    if temp < 55:
        step_down_counter = 6
        return 0.4
    if temp < 60:
        step_down_counter = 6
        return 0.6
    if temp < 65:
        step_down_counter = 12
        return 0.8
    if temp < 70:
        step_down_counter = 16
        return 0.9
    step_down_counter = 24
    return 1.0


def signals_handler(signum, frame):
    print('Signal handler called with signal ' + str(signum))
    _remove_my_pid(PID_FILE)
    sys.exit(signum)

if __name__ == "__main__":
    print("Register signal handler")
    signal.signal(signal.SIGINT , signals_handler)

    _save_my_pid(PID_FILE)

    piFan = PWMOutputDevice(RPI_FAN_PIN)
    cpuTemp = CPUTemperature()

    while True:
        temp = cpuTemp.temperature
        print("CPU Temp: {} C".format(temp))

        fanVal = fanValConvert(temp)

        if fanVal > 0:
            print("Fan Value: {}".format(fanVal))
            piFan.value = fanVal
        else:
            # In step down counter
            pass

        time.sleep(PERIOD_S)
        pass
    pass
