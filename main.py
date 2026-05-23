import hid
import pygame
import time

VENDOR_ID = 0x294B
PRODUCT_ID = 0x1901

pygame.init()
pygame.joystick.init()
BRAVO = pygame.joystick.Joystick(0)
BRAVO.init()

print(f'Found: {BRAVO.get_name()}')


top_led_status = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
    21: 0,
    22: 0,
    23: 0,
    24: 0,
    25: 0,
    26: 0,
    27: 0,
    28: 0,
    29: 0,
    30: 0,
    31: 0,
    32: 0,
    33: 0,
    34: 0,
    35: 0,
    36: 0,
    37: 0,
    38: 0,
    39: 0,
    40: 0,
    41: 0,
    42: 0,
    43: 0,
    44: 0,
    45: 0,
    46: 0
}

switch_lights = {
    ## button: light
    30: [8,10,12],
    31: [9,11,13],
    33: [14],
    34: [21],
    35: [15],
    36: [22],
    37: [16],
    38: [23],
    39: [17],
    40: [24],
    41: [18],
    42: [25],
    43: [19],
    44: [26],
    45: [20],
    46: [27]
}

def turn_on_switch_lights(button):
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    light = switch_lights[button]
    for light in switch_lights[button]:

        buffer = [0x00, 0x00, 0x00, 0x00, 0x00]
        b_pos = 1 + (light // 8)
        bi_pos = light % 8
        buffer[b_pos] |= (1 << bi_pos)
        try:
            device.send_feature_report(buffer)
        except Exception as e:
            print(f'error: {e}')

def build_buffer(button):
    buffer = [0x00, 0x00, 0x00, 0x00, 0x00]
    for button, status in top_led_status.items():
        if status == 1:
            b_pos = 1 + (button // 8)
            bi_pos = button % 8
            buffer[b_pos] |= (1 << bi_pos)
            print(f'bit {button}: buffer = {buffer}')
    return buffer 

def testing_buffer():
    for i in range(8,27):
        buffer = [0x00, 0x00, 0x00, 0x00, 0x00]
        b_pos = 1 + (i // 8)
        bi_pos = i % 8
        buffer[b_pos] |= (1<< bi_pos)
        device = hid.device()
        device.open(VENDOR_ID, PRODUCT_ID)
        try:
            print(f'testing button: {i}')
            device.send_feature_report(buffer)
            time.sleep(2)
        except Exception as e:
            print(f'error: {e}')

def turn_off_led(button):
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    print(f'turning off button {button}')
    top_led_status[button] = 0
    try:
        device.send_feature_report(build_buffer())
    except Exception as e:
        print(f'error: {e}')

def turn_on_led(button):
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    print(f'turning on button: {button}')
    top_led_status[button] = 1
    try:
        device.send_feature_report(build_buffer(button))
    except Exception as e:
        print(f'error: {e}')
def turn_off_all_lights():
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    buffer = [0x00, 0x00, 0x00, 0x00, 0x00]
    device.send_feature_report(buffer)
    device.close()

running = True
while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                print(f'button pressed: {button}')
                # if button <= 6:
                if top_led_status[button] == 0:
                    turn_on_led(button)
                elif top_led_status[button] == 1:
                    turn_off_led(button)
                # elif button >=30 and button <=46:
                #     turn_on_switch_lights(button)
                    #testing_buffer()
    except KeyboardInterrupt:
        print("exiting")
        turn_off_all_lights()
        pygame.quit()