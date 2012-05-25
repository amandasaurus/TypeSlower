#!/bin/sh

do_it() {
    # need error checking there. We should also restrict which device gets
    # deactivated, by checking other properties.
    keyboard_ids="$(xinput list | sed -rn 's/.*id=([0-9]+).*slave\s+keyboard.*/\1/p')"

    for keyboard_id in $keyboard_ids; do
        # 121 is "Device Active".
        # use xinput watch-props $device_id to see some properties.
        xinput set-prop $keyboard_id 136 $1;
    done;
}
# you maybe don't want to exit in case of failure there.
echo "turning off"
do_it 0
echo "should be off"
sleep 5
echo "should be on"
do_it 1

