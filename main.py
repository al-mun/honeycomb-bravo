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

try:
    bartolito = pygame.mixer.Sound("./sounds/bartolito_short.wav")
    moo = pygame.mixer.Sound("./sounds/moo.wav")
    quack = pygame.mixer.Sound("./sounds/quack.wav")
    meh = pygame.mixer.Sound("./sounds/meh.wav")
    wolf = pygame.mixer.Sound("./sounds/wolf.wav")
    dog = pygame.mixer.Sound("./sounds/dog.wav")
    meow = pygame.mixer.Sound("./sounds/moew.wav")
except pygame.error as e:
    print(f'error with song: {e}')
    bartolito = None

# Keep tracking toggle switches and top rows here
led_status = {i: 0 for i in range(48)}

# Hardcoded state specifically for the gear light byte (index 2 of the buffer)
# Starts at 0x00 (all off)
gear_byte = 0x00

def update_hardware():
    global gear_byte
    # Start with a fresh buffer
    buffer = [0x00, 0x00, 0x00, 0x00, 0x00]
    
    # 1. Map all standard toggles and top row buttons from led_status
    for led_id, status in led_status.items():
        if status == 1:
            b_pos = 1 + (led_id // 8)
            bi_pos = i = led_id % 8
            buffer[b_pos] |= (1 << bi_pos)
            
    # 2. Hard-inject our dedicated gear byte into the 3rd position (Index 2)
    buffer[2] |= gear_byte
    
    try:
        device = hid.device()
        device.open(VENDOR_ID, PRODUCT_ID)
        device.send_feature_report(buffer)
        device.close()
    except Exception as e:
        print(f'HID Error: {e}')

def toggle_top_row_led(button):
    led_status[button] = 1 - led_status[button]
    print(f'Toggling top row button {button} to status {led_status[button]}')
    update_hardware()

def set_toggle_switch_lights(button, state):
    toggle_switch_and_lights = {
        32: [14], 33: [14], 34: [21], 35: [15],
        36: [22], 37: [16], 38: [23], 39: [17],
        40: [24], 41: [18], 42: [25], 43: [19],
        44: [26], 45: [20], 46: [27]
    }
    
    if button in toggle_switch_and_lights:
        for light_id in toggle_switch_and_lights[button]:
            led_status[light_id] = state
        update_hardware()

def set_gear_lights(button):
    global gear_byte
    if button == 30:
        print("Gear lights -> ALL GREEN")
        gear_byte = 0x15  # Hardcoded all green bits
        
    elif button == 31:
        print("Gear lights -> ALL RED")
        gear_byte = 0x2A  # Hardcoded all red bits
        
    update_hardware()

def turn_off_all_lights():
    global led_status, gear_byte
    led_status = {i: 0 for i in range(48)}
    gear_byte = 0x00
    update_hardware()

running = True
while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                print(f'Button pressed: {button}')
                
                if button == 0:
                    moo.play()
                    toggle_top_row_led(button)
                if button == 1:
                    quack.play()
                if button == 2:
                    meh.play()
                if button == 3:
                    wolf.play()
                if button == 4:
                    meow.play()
                if button == 5:
                    dog.play()
                if button == 6:
                    bartolito.play
                elif button == 30 or button == 31: 
                    set_gear_lights(button)
                elif 32 <= button <= 46:
                    set_toggle_switch_lights(button, state=1)
                    
            elif event.type == pygame.JOYBUTTONUP:
                button = event.button
                if 32 <= button <= 46:
                    set_toggle_switch_lights(button, state=0)    
                    
    except KeyboardInterrupt:
        print("Exiting...")
        turn_off_all_lights()
        pygame.quit()
        running = False