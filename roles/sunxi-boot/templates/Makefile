.PHONY: all

all: dtbs scrs

dtbs: $(patsubst %.dtso,%.dtbo,$(wildcard *.dtso))
scrs: $(patsubst %.cmd,%.scr,$(wildcard *.cmd))

%.dtbo: %.dtso
	dtc -I dts -O dtb -o $@ -b0 -@ $<

%.scr: %.cmd
	mkimage -C none -A {{ sunxi_mkimage_arch }} -T script -d $< $@
