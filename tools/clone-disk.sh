#!/bin/sh

# Clone/backup hard disk

sudo dd if=/dev/sdc of=/dev/sdd bs=16M conv=noerror,sync status=progress
