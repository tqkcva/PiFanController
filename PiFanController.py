from gpiozero import PWMOutputDevice
from gpiozero import CPUTemperature
import time
import os

# Raspberry Pi Fan Controler pi
RPI_FAN_PIN = 18

# Time delay per check
PERIOD_S = 5

def _save_my_pid(filename="/tmp/PiFanController.pid"):
    with open(filename, "w+") as f:
        f.write(str(os.getpid()))
        f.flush()
        pass
    pass

def fanVal(temp):
    if temp < 50:
        return 0.0
    if temp < 60:
        return 0.2
    if temp < 70:
        return 0.5
    if temp < 80:
        return 0.8
    return 1.0

if __name__ == "__main__":
    piFan = PWMOutputDevice(RPI_FAN_PIN)
    cpuTemp = CPUTemperature()

    _save_my_pid()

    while True:
        temp = cpuTemp.temperature
        val = fanVal(temp)
        print("CPU Temp: {} C".format(temp))
        print("Fan Value: {}".format(val))
        piFan.value = val

        time.sleep(PERIOD_S)
        pass
    pass
