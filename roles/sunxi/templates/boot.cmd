echo Loading zImage
ext4load mmc {{ sunxi_mmc }} 0x46000000 boot/zImage${devsuffix}
echo Loading FDT blob
ext4load mmc {{ sunxi_mmc }} 0x49000000 boot/opi.dtb${devsuffix}
if test -n ${devsuffix}
then
	echo Unsetting devsuffix, reboot proofing
	setenv devsuffx
	saveenv
fi

setenv patchaddr 0x43200000
setenv patchscript /boot/patch.scr
if test -e mmc {{ sunxi_mmc }} ${patchscript}
then
	echo Found patch script, running it
	load mmc {{ sunxi_mmc }} ${patchaddr} ${patchscript}
	source ${patchaddr}
fi

echo All done, booting in 3 seconds
sleep 3
bootz 0x46000000 - 0x49000000
