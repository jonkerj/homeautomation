#!/bin/sh
# {{ ansible_managed }}

CONTROLDIR="/sys/class/gpio/gpio{{ sunxi_reboot_gpio}}"

echo 0 > $CONTROLDIR/value
sleep 1
echo 1 > $CONTROLDIR/value
