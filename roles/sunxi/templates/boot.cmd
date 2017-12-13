setenv kernel_addr 0x46000000
setenv fdt_addr 0x49000000
setenv scratch_addr 0x43200000
setenv vars boot.txt

# this may be overridden in boot.txt
setenv bootdevtype mmc
setenv prefix /boot
setenv bootdev 1
setenv bootpart 1

echo "Loading variables (${prefix}/${vars})"
load ${bootdevtype} ${bootdev}:${bootpart} ${scratch_addr} ${prefix}/${vars}
env import -t ${scratch_addr} ${filesize}

echo "Loading kernel (${prefix}/${kernel})"
ext4load ${bootdevtype} ${bootdev} ${kernel_addr} ${prefix}/${kernel}
echo "Loading FDT (${prefix}/${dtb})"
ext4load ${bootdevtype} ${bootdev} ${fdt_addr} ${prefix}/${dtb}
fdt addr 0x49000000
fdt resize 65536

for overlay_name in ${overlays}; do
	load ${bootdevtype} ${bootdev}:${bootpart} ${scratch_addr} ${prefix}/${overlay_name}.dtbo
	echo "Applying DT overlay (${prefix}/${overlay_name}.dtbo)"
	fdt apply ${scratch_addr}
done

echo "Booting in 5 seconds"
sleep 5
bootz ${kernel_addr} - ${fdt_addr}
