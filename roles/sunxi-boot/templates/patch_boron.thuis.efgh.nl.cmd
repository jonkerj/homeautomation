echo Attaching BME280
fdt mknode /soc/i2c@01c2b000 pressure@77
fdt set /soc/i2c@01c2b000/pressure@77 compatible bosch,bme280
fdt set /soc/i2c@01c2b000/pressure@77 reg <0x77>
echo Attaching Si7020
fdt mknode /soc/i2c@01c2b000 humid@40
fdt set /soc/i2c@01c2b000/humid@40 compatible silabs,si7020
fdt set /soc/i2c@01c2b000/humid@40 reg <0x40>
