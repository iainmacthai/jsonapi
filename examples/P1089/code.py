# SPDX-FileCopyrightText: 2020 ladyada, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import alarm
import supervisor
import alarm
from adafruit_magtag.magtag import MagTag

# Change this to the hour you want to check the data at, for us its 8pm
# local time (eastern), which is 20:00 hrs
DAILY_UPDATE_HOUR = 20

# Set up where we'll be fetching data from
DATA_SOURCE = "https://iainmacthai.github.io/jsonapi/examples/P1089/P1089_ls_cables_korea.json"

CLIENT_LOCATION = ['client']
CABLE6TYPE_LOCATION = ['cable6', 'cable_type']
CABLE6SIZE_LOCATION = ['cable6', 'cable_size']
CABLE6FACTKP_LOCATION = ['cable6', 'kp', 'factory_final_kp']
CABLE6INNOKP_LOCATION = ['cable6', 'kp', 'innovatum_final_kp']
CABLE6STATUS_LOCATION = ['cable6', 'status']

magtag = MagTag(
    url=DATA_SOURCE,
    json_path=(CLIENT_LOCATION, CABLE6TYPE_LOCATION,
               CABLE6SIZE_LOCATION, CABLE6FACTKP_LOCATION,
               CABLE6INNOKP_LOCATION, CABLE6STATUS_LOCATION),
)


# CLIENT
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.pcf",
    text_position=(10, 15),
    text_transform=lambda x: "Client: {}".format(x),
)
# CABLE 6 TYPE
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.pcf",
    text_position=(10, 35),
    text_transform=lambda x: "Cable Type:   {:,}".format(x),
)
# CABLE 6 SIZE
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.pcf",
    text_position=(10, 55),
    text_transform=lambda x: "Cable Size:   {:,}".format(x),
)
# CABLE 6 FACT KP
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.pcf",
    text_position=(10, 75),
    text_transform=lambda x: "Factory KP:   {:,}".format(x),
)
# CABLE 6 INNO KP
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.pcf",
    text_position=(10, 95),
    text_transform=lambda x: "Innovatum KP:   {:,}".format(x),
)
# CABLE 6 STATUS
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.pcf",
    text_position=(10, 115),
    text_transform=lambda x: "Cable Status:   {:,}".format(x),
)

# updated time
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.pcf",
    text_position=(245, 30),
    line_spacing=0.75,
    is_data=False
)


magtag.peripherals.neopixels.brightness = 0.1
magtag.peripherals.neopixel_disable = False # turn on lights
magtag.peripherals.neopixels.fill(0x0F0000) # red!

magtag.get_local_time()
try:
    now = time.localtime()
    print("Now: ", now)

    # display the current time since its the last-update
    updated_at = "%d/%d\n%d:%02d" % now[1:5]
    magtag.set_text(updated_at, 6, False)

    # get data from the Covid Tracking Project
    value = magtag.fetch()
    print("Response is", value)

    # OK we're done!
    magtag.peripherals.neopixels.fill(0x000F00) # greten
except (ValueError, RuntimeError) as e:
    print("Some error occured, trying again later -", e)

time.sleep(2) # let screen finish updating

# we only wanna wake up once a day, around the event update time:
event_time = time.struct_time((now[0], now[1], now[2],
                               DAILY_UPDATE_HOUR, 0, 0,
                               -1, -1, now[8]))
# how long is that from now?
remaining = time.mktime(event_time) - time.mktime(now)
if remaining < 0:             # ah its aready happened today...
    remaining += 24 * 60 * 60 # wrap around to the next day
remaining_hrs = remaining // 3660
remaining_min = (remaining % 3600) // 60
print("Gonna zzz for %d hours, %d minutes" % (remaining_hrs, remaining_min))

# Turn it all off and go to bed till the next update time
magtag.exit_and_deep_sleep(remaining)
