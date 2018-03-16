echo FDT Fixups, loading and resizing FDT
fdt addr 0x49000000
fdt resize

echo Enabling UART1
fdt set /soc/serial@01c28400 status okay
echo Enabling UART2
fdt set /soc/serial@01c28800 status okay
echo Enabling UART3
fdt set /soc/serial@01c28c00 status okay

echo Enabling I2C0
fdt set /soc/i2c@01c2ac00 status okay
echo Enabling I2C1
fdt set /soc/i2c@01c2b000 status okay

echo Aliasing Ethernet0
fdt set /aliases ethernet0 /soc/ethernet@1c30000

echo Adding SID
fdt mknode /soc eeprom@1c14000
fdt set /soc/eeprom@1c14000 compatible allwinner,sun4i-a10-sid
fdt set /soc/eeprom@1c14000 reg <0x01c14000 0x234>
fdt set /soc/eeprom@1c14000 '#address-cells' <1>
fdt set /soc/eeprom@1c14000 '#size-cells' <1>

{% include "patch_" + inventory_hostname + ".cmd" ignore missing %}
