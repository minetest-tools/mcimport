#!/bin/bash

# shell wrapper around mcimport.py
# meant to assist users and provide an easy way to select input and output folders, and
# assure that the python script runs from the correct location.

cd `dirname $0`

if [ ! -f map_content.txt ]; then
	zenity --info --text "Unable to locate \"map_content.txt\" file - this is a critical error, and this program is unable to continue."
	exit 1
fi

while true; do
	IN=`cd ~/.minecraft/saves; zenity --file-selection --directory --filename="New World"`
	if [ "`basename "$IN"`" == "level.dat" ]; then
		IN="`dirname "$IN"`"
	fi
	if [ ! -d "$IN" ]; then
		zenity --info --text "The chosen entry \"$IN\" is not a folder. Try selecting a folder that has a \"level.dat\" file inside."
		exit 1
	fi
	break
done

OUT=`zenity --entry --entry-text="$(basename "$IN")" --text="Type the output name of the converted world:"`

if [ -d "${HOME}/.minetest/worlds/$OUT" ]; then
	if ! `zenity --question --title="Overwrite existing world?" --text="The world \"$OUT\" already exists, do you want to overwrite it?" --default-cancel`; then
		exit 1
	fi
	rm -rf "${HOME}/.minetest/worlds/$OUT"
fi

zenity --info --width=800 --title="Conversion in progress" --text="The conversion is now running and make take a *very* long time to finish. Do not be alarmed by output lines that show \"Unknown Minecraft Block\" messages, this is normal and can usually be ignored without issues. You can safely close this window." &

python3 mcimport.py "$IN" "${HOME}/.minetest/worlds/$OUT"

