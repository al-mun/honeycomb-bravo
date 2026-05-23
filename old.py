import hid
import pygame
import sys

VENDOR_ID = 0x294B
PRODUCT_ID = 0x1901

pygame.init()
pygame.joystick.init()

try:
    BRAVO = pygame.joystick.Joystick(0)
    BRAVO.init()
    print(f'Found: {BRAVO.get_name()}')
except:
    print("couldn't find the controller")
    pygame.quite()
    exit()

try:
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    print('device opened')
except Exception as e:
    print(f'failed to open HID connection: {e}')
    pygame.quit()
    exit()

def turn_on_led(button):
    print('made it here')
    buffer = [0x00, 0x00, 0x00, 0x00, 0x00]
    byte_pos = 1 + (button // 8)
    bit_pos = button % 8
    buffer[byte_pos] |= (1 << bit_pos)
    try:
        print('trying to turn on light')
        print(device)
        device.send_feature_report(bytes(buffer))
    except Exception as e:
        print(f"Error sending HID report: {e}")
try:
    running=True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    button = event.button
                    print(button)
                    if button == 0:
                        turn_on_led(button)
                    print(f'button pressed: {button}')

        except KeyboardInterrupt:
            print("exiting")
            device.close()
            pygame.quit()
except KeyboardInterrupt:
    print("exiting")
    device.close()
    pygame.quit()
finally:
    try:
        device.close()
        print("closing connection")
    except Exception:
        pass
        pygame.quit()