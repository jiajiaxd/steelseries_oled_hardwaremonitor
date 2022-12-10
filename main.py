from PIL import Image, ImageFont, ImageDraw
from easyhid import Enumeration
from time import sleep
import signal
import sys
import LibreHardwareMonitorAPI as LHM

# Stores an enumeration of all the connected USB HID devices
en = Enumeration()
# print(en.show())
# Return a list of devices based on the search parameters / Hardcoded to Apex 7
devices = en.find(vid=0x1038, pid=0x1610, interface=1)
if not devices:
    devices = en.find(vid=0x1038, pid=0x1618, interface=1)
if not devices:
    print("No devices found, exiting.")
    sys.exit(0)
# Use first device found with vid/pid
dev = devices[0]
dev.open()
im = Image.new('1', (128, 40))
draw = ImageDraw.Draw(im)

monitor = LHM.HWMonitor(LHM.init_librehardwaremonitor())

a = 0.0
while True:
    # use a truetype font
    interval = 1
    a += interval
    t = 5
    draw.rectangle([(0, 0), (128, 40)], fill=0)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 12)

    data = monitor.get_hardware_brief_information()
    if a <= t:
        draw.text((0, 0), 'CPU Load: {:2.0f}%'.format(data.get('CPU_Load')), font=font, fill=255)
        draw.text((0, 12), "CPU Power: {:4.0f}W".format(data.get('CPU_Power')), font=font, fill=255)
        draw.text((0, 24), "CPU Temp: {:4.0f}°C".format(data.get('CPU_Temperature')), font=font, fill=255)
    elif t < a <= 2 * t:
        draw.text((0, 0), 'GPU Load: {:2.0f}%'.format(data.get('GPU_Core_Load')), font=font, fill=255)
        draw.text((0, 12), "GPU Power: {:4.0f}W".format(data.get('GPU_Power')), font=font, fill=255)
        draw.text((0, 24), "GPU Temp: {:4.0f}°C".format(data.get('GPU_Temperature')), font=font, fill=255)
    if a == 2 * t:
        a = 0

    data = im.tobytes()
    # Set up feature report package
    data = bytearray([0x61]) + data + bytearray([0x00])
    dev.send_feature_report(data)
    sleep(interval)

dev.close()
