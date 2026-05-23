import hid
import pygame
import sys
import ctypes
import os

VENDOR_ID = 0x294B
PRODUCT_ID = 0x1901

pygame.init()
pygame.joystick.init()

BRAVO = pygame.joystick.Joystick(0)
BRAVO.init()
print(f'Found: {BRAVO.get_name()}')
clock = pygame.time.Clock()
device = hid.device()
top_led_status = {
    0:0,
    1:0,
    2:0,
    3:0,
    4:0,
    5:0,
    6:0,
    7:0,
}

def turn_off_led(button):
    print(f'turning off button {button}')
    top_led_status[button] = 0
    device.open(VENDOR_ID, PRODUCT_ID)
    buffer = [0x00, 0x00, 0x00, 0x00, 0x00]
    for btn, status in top_led_status.items():
        if status == 1:
            b_pos = 1 + (btn // 8)
            bi_pos = btn % 8
            buffer[b_pos] |= (1 << bi_pos)

    try:
        device.send_feature_report(bytes(buffer))
    except Exception as e:
        print(f'error: {e}')

def turn_on_led(button):
    print(f'turning on button: {button}')
    top_led_status[button] = 1
    device.open(VENDOR_ID, PRODUCT_ID)
    buffer = [0x00, 0x00, 0x00, 0x00, 0x00]
    for btn, status in top_led_status.items():
        if status == 1:
            b_pos = 1 + (btn // 8)
            bi_pos = btn % 8
            buffer[b_pos] |= (1 << bi_pos)
    byte_pos = 1 + (button // 8)
    if byte_pos >=5:
        return
    try:
        device.send_feature_report(bytes(buffer))
    except Exception as e:
        print(f"Error sending HID report: {e}")
    #device.close()
# try:
running=True
while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                if button < 8:
                    print(f'button pressed: {button} with status {top_led_status[button]}')
                    if top_led_status[button] == 0:
                        turn_on_led(button)
                    else:
                        print(f'button pressed: {button} with status {top_led_status[button]}')
                        turn_off_led(button)
    except KeyboardInterrupt:
        print("exiting")
        device.close()
        pygame.quit()