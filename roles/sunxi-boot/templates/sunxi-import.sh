#!/bin/bash
# {{ ansible_managed }}

VERSION=$1
SUFFIX=$2
DTB="{{ sunxi_dt }}.dtb"

if [ -z "$VERSION" ]
then
	echo "version missing"
	exit 1
fi

if [ -z "$SUFFIX" ]
then
	echo "suffix missing"
	exit 1
fi

MODULES="/lib/modules/${VERSION}"
MODULES_BACKUP="${MODULES}.backup"
MODULES_REMOTE="{{ sunxi_mountpoint }}/modules/lib/modules/${VERSION}"
KPATH_REMOTE="{{ sunxi_mountpoint}}/${VERSION}"

if [ ! -d "$MODULES_REMOTE" -o ! -d "$KPATH_REMOTE" ]
then
	echo "$MODULES_REMOTE or $KPATH_REMOTE does not exist"
	exit 1
fi

# Remove backup
if [ -e "${MODULES_BACKUP}" ]
then
	echo "Removing old backup"
	sudo rm -rf "${MODULES_BACKUP}"
fi

# Backup
if [ -e "${MODULES}" ]
then
	echo "Backupping current modules dir"
	sudo mv "${MODULES}" "${MODULES_BACKUP}"
fi

# Sync modules
echo "Synchronizing ${MODULES_REMOTE}/ with ${MODULES}/"
sudo rsync -xa --delete ${MODULES_REMOTE}/ ${MODULES}/
# copy kernel
echo "Copying kernel and DTB"
sudo cp ${KPATH_REMOTE}/arch/arm/boot/zImage /boot/zImage${SUFFIX}
# copy DTB
sudo cp ${KPATH_REMOTE}/arch/arm/boot/dts/${DTB} /boot/opi.dtb${SUFFIX}
