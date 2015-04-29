#!/usr/bin/python

import sys
import platform
import time
import usb.core
import usb.util

DOWN = 0x01
UP = 0x02
LEFT = 0x04
RIGHT = 0x08
FIRE = 0x10
STOP = 0x20

MOTOR = 0x02
LED = 0x03

Launcher = None


def usage():
    print("============ USAGE =============")
    print("missile.py [command] [value]")
    print("commands: right, left, up, down, fire, sleep, park, led")


def init():
    global Launcher
    Launcher = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if Launcher is None:
        raise ValueError('Missile device not found')

    # Detach usb HID
    if "Linux" == platform.system():
        try:
            Launcher.detach_kernel_driver(0)
        except Exception:
            pass  # already done :)

    Launcher.set_configuration()


def send(cmd):
    Launcher.ctrl_transfer(0x21, 0x09, 0, 0, [MOTOR, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


def led(cmd):
    Launcher.ctrl_transfer(0x21, 0x09, 0, 0, [LED, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


def move(cmd, duration_ms):
    send(cmd)
    time.sleep(duration_ms / 1000.0)
    send(STOP)


def execute(cmd, value):
    cmd = cmd.lower()

    if cmd == "right":
        move(RIGHT, value)
    elif cmd == "left":
        move(LEFT, value)
    elif cmd == "up":
        move(UP, value)
    elif cmd == "down":
        move(DOWN, value)
    elif cmd == "park":
        move(DOWN, 2000)
        move(LEFT, 8000)
    elif cmd == "sleep":
        time.sleep(value / 1000.0)
    elif cmd == "led":
        if value == 0:
            led(0x00)
        else:
            led(0x01)
    elif cmd == "fire":
        if value < 1 or value > 4:
            value = 1
        time.sleep(0.5)
        for i in range(value):
            send(FIRE)
            time.sleep(4.5)
    else:
        print("Error: Unknown command: '%s'" % cmd)


def main(args):
    if len(args) < 2:
        usage()
        sys.exit(1)

    init()

    command = args[1]
    value = 0
    if len(args) > 2:
        value = int(args[2])
    execute(command, value)


if __name__ == '__main__':
    main(sys.argv)
