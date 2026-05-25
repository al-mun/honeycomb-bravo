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


led_status = {
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
    46: 0,
}

gear_lights = {
    30: [8,10,12],
    31: [9,11,13]
}

toggle_switch_and_lights = {
    ## button: light
    30: [8,10,12],
    31: [9,11,13],
    32: [14],
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

def build_buffer():
    buffer = [0x00, 0x00, 0x00, 0x00, 0x00]
    for btn, status in led_status.items():
        if status == 1:
            b_pos = 1 + (btn // 8)
            bi_pos = btn % 8
            buffer[b_pos] |= (1 << bi_pos)
            print(f'buffer = {buffer}')
    return buffer #for turning light off

def toggle_switch_lights(button):
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    light = toggle_switch_and_lights[button]
    for light in toggle_switch_and_lights[button]:
        buffer = [0x00, 0x00, 0x00, 0x00, 0x00]
        b_pos = 1 + (light // 8)
        bi_pos = light % 8
        buffer[b_pos] |= (1 << bi_pos)
        print(buffer)
        try:
            device.send_feature_report(buffer)
        except Exception as e:
            print(f'error: {e}')

def turn_on_gear_lights(button):
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    
    print(f'turning on gear lights: {button}')
    led_status[button] = 1
    if button == 30:
        device.send_feature_report([0x00, 0x00, 0x15, 0x00, 0x00]) # all green
    if button == 31:
        device.send_feature_report([0x00, 0x00, 0x2A, 0x00, 0x00]) # all red
        # device.send_feature_report([0x00, 0x00, 0x01, 0x00, 0x00]) # left green
        # device.send_feature_report([0x00, 0x00, 0x05, 0x00, 0x00]) #top, left green
        # device.send_feature_report([0x00, 0x00, 0x02, 0x00, 0x00]) #left red
        # device.send_feature_report([0x00, 0x00, 0x04, 0x00, 0x00]) #top  green
        # device.send_feature_report([0x00, 0x00, 0x06, 0x00, 0x00]) #top  green left red
        # device.send_feature_report([0x00, 0x00, 0x07, 0x00, 0x00]) #top  green left orange
        # device.send_feature_report([0x00, 0x00, 0x08, 0x00, 0x00]) #top  red
        # device.send_feature_report([0x00, 0x00, 0x09, 0x00, 0x00]) #top red left greeen
        # device.send_feature_report([0x00, 0x00, 0x10, 0x00, 0x00]) # right green
        # device.send_feature_report([0x00, 0x00, 0x11, 0x00, 0x00]) # left right green
        # device.send_feature_report([0x00, 0x00, 0x12, 0x00, 0x00]) # left red right green
        # device.send_feature_report([0x00, 0x00, 0x13, 0x00, 0x00]) # left orange right green
        # device.send_feature_report([0x00, 0x00, 0x14, 0x00, 0x00]) # top green right green
        # device.send_feature_report([0x00, 0x00, 0x15, 0x00, 0x00]) # all green
        # device.send_feature_report([0x00, 0x00, 0x16, 0x00, 0x00]) # top green left red right green
        # device.send_feature_report([0x00, 0x00, 0x17, 0x00, 0x00]) # top green left orange right green
        # device.send_feature_report([0x00, 0x00, 0x18, 0x00, 0x00]) # top red right green
        # device.send_feature_report([0x00, 0x00, 0x19, 0x00, 0x00]) # top red right green left green
        # device.send_feature_report([0x00, 0x00, 0x20, 0x00, 0x00]) # right red
        # device.send_feature_report([0x00, 0x00, 0x21, 0x00, 0x00]) # right red left green
        # device.send_feature_report([0x00, 0x00, 0x22, 0x00, 0x00]) # right red left red
        # device.send_feature_report([0x00, 0x00, 0x23, 0x00, 0x00]) # right red left orange
        # device.send_feature_report([0x00, 0x00, 0x24, 0x00, 0x00]) # top green right red
        # device.send_feature_report([0x00, 0x00, 0x25, 0x00, 0x00]) # top green left green right red
        # device.send_feature_report([0x00, 0x00, 0x26, 0x00, 0x00]) # top green left green right red
        # device.send_feature_report([0x00, 0x00, 0x27, 0x00, 0x00]) # top green left orange right red
        # device.send_feature_report([0x00, 0x00, 0x28, 0x00, 0x00]) # top red right red
        # device.send_feature_report([0x00, 0x00, 0x29, 0x00, 0x00]) # top red left green right red
        # device.send_feature_report([0x00, 0x00, 0x30, 0x00, 0x00]) # right orange
        # device.send_feature_report([0x00, 0x00, 0x31, 0x00, 0x00]) # right orange left green
        # device.send_feature_report([0x00, 0x00, 0x32, 0x00, 0x00]) # left red right orange
        # device.send_feature_report([0x00, 0x00, 0x33, 0x00, 0x00]) # left orange right orange
        # device.send_feature_report([0x00, 0x00, 0x34, 0x00, 0x00]) # top green right orange
        # device.send_feature_report([0x00, 0x00, 0x35, 0x00, 0x00]) # top green left green right orange
        # device.send_feature_report([0x00, 0x00, 0x36, 0x00, 0x00]) # top green left red right orange
        # device.send_feature_report([0x00, 0x00, 0x37, 0x00, 0x00]) # top green left orange right orange
        # device.send_feature_report([0x00, 0x00, 0x38, 0x00, 0x00]) # top red right orange
        # device.send_feature_report([0x00, 0x00, 0x39, 0x00, 0x00]) # top red right orange left green
    # else:
    #     try:
    #         device.send_feature_report(buffers[0])
    #         device.send_feature_report(buffers[2])
    #         device.send_feature_report(buffers[3])
    #     except Exception as e:
    #         print(f'error: {e}')

def turn_on_top_led(button):
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    print(f'turning on button: {button}')
    led_status[button] = 1
    try:
        device.send_feature_report(build_buffer())
    except Exception as e:
        print(f'error: {e}')

def turn_off_led(button):
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    print(f'turning off button {button}')
    led_status[button] = 0
    try:
        device.send_feature_report(build_buffer())
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
                if button < 8:
                    if led_status[button] == 0:
                        turn_on_top_led(button)     #top row buttons
                    elif led_status[button] == 1:
                        turn_off_led(button)
                elif button >=32 and button <=46: # toggle switches
                    toggle_switch_lights(button)
                elif button >=30 and button <=31: #gear lights
                    #toggle_switch_lights(button)
                    turn_on_gear_lights(button)
                    #testing_buffer()
                # elif button == 30:
                #     turn_on_gear_lights()
    except KeyboardInterrupt:
        print("exiting")
        turn_off_all_lights()
        pygame.quit()