---
title: playlist-converter 
categories:
date:   2018-12-20 10:34:02
---

this script will read the file locations from a playlist and  

* 	create a new timestamp-named folder either in a specified location or the users $HOME path 
* 	copy the mp3 files to the newly created folder 
* 	set all files to the same volume level 
* 	write a new playlist of relative pathnames to the directory

setting the volume is done by way of [mp3gain](https://www.mankier.com/1/mp3gain)'s "-r" and "-d" flag. Afaics the default base value would be 89db, so 
~~~
mp3gain -r -d6
~~~
would be 89db +6db = 95db


## script
~~~bash
#!/bin/bash
OLDIFS=$IFS
IFS='
'

printf "looking for mp3gain... "
command -v mp3gain || (printf "this script depends on mp3gain, which is not present on this computer. exiting\n" && exit 0)


if [[ -z $@ ]]; then
echo "usage: pass a playlist as first parameter and a destination basepath as optional second parameter" && exit 1
fi

defaultdir=$HOME
arg1=$(file -b $1)
arg2=$(file -b ${2:-$HOME})
colr='\033[0;34m'
off='\033[0m'


if [[ ( ${arg1,,} != *playlist* ) || ( ${arg1,,} == error* ) ]]; then
echo "please pass a valid playlist as first argument"
exit 1
fi

if [[ -z $2 ]]; then
echo "you can specify a destination path as second parameter... defaulting to ${HOME}" 
fi

pllist=$(/usr/bin/basename $1)
tstamp=$(date +%Y_%j_%H%M%S)
destpth=${2:-$HOME}
destin=${destpth%/}/00_playlists_normalized/"${pllist%.*}"-"${tstamp}"

read -n 1 -p $'normalize \e[34m'"${1}"$'\e[0m'" in "$'\e[34m'"${destin}"$'\e[0m'" [y/n]" yn
	case "$yn" in
		[Yy] ) printf "\n";;
		* ) printf "\n" && exit 0;;
	esac

printf "creating a destination directory at ${colr}${destin}${off}... "
mkdir -p $destin && printf "ok\n"

printf "copying files to ${colr}${destin}${off}..."
for mp3_file in $(grep "^[^#]" $1 | sed 's/\r$//'); do cp $mp3_file $destin; done && printf "ok\n"

printf "${colr}applying uniform gain${off}\n"
mp3gain -r -c -k ${destin}/*mp3

printf "rewriting playlist for normalized directory to${colr}${destin}/playlist_${tstamp}.m3u${off}...\n"
for i in $(grep "^[^#]" $1); do echo ${i##/*/} >> $destin/playlist_${tstamp}.m3u; done && printf "ok \n"

IFS=$OLDIFS
~~~

[save as](https://raw.githubusercontent.com/gestos/keuch/master/code_box/bourne/list2norm)
