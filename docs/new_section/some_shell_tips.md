---
layout: post
title: some shell tips
categories: bash screen
date: 2019-01-03 21:12:24
---

## gnu screen caption line and scrolling

while I'm revisiting my shell and screen startup files, I try to solve a thing that I always found annoying but never bothered to look it up.  
First, a look at my `.screenrc` file:

``` bash 
startup_message off	# no welcome message when screen starts 
shell $SHELL	# start bash as a non-login shell (shell -$SHELL would start a login shell)
shelltitle "$ |bash"	# show name of currently running program as title in the terminal
attrcolor b ".I"	# I really don't know anymore
defhstatus "(^Et) | $USER@^EH"	# show name of current program in window list
hardstatus off	# suppress status messages ("bell in window 0")
caption always "%{= wk} %-w%{= KW} [%n %t ] %{-}%+w %= %{= wg} %C%a"	# generates a status line at the bottom of the window 
bindkey "^[Od" prev  # ctrl-left moves to previous window
bindkey "^[Oc" next  # ctrl-right moves to next window
term screen-256color # gives access to all colors on 256-color terminals
termcapinfo xterm* ti@:te@	# this enables using the scrollbar of the terminal window	and mouse scrolling
``` 

with this configuration, I can scroll up the terminal window (eg to view some output), but whenever the time in the `caption` changes, the scroll buffer will return to the bottom of the terminal because of the change in the caption line  
to avoid this, one can use screens "copy mode". The `caption` will stay in the foreground, while you can use the arrow keys to move up and down through the terminal output.

```
Ctrl+A Esc to go in copy mode.
Then use arrows or PageUp/PageDown to move through the scroll buffer.
To exit copy mode, just hit Esc.
```

copy mode tip from [TeChn4K/superuser](https://superuser.com/a/801452)  
explanations for all screenrc commands can be found at [aperiodic](http://aperiodic.net/screen/commands:start)  
very useful blogpost for understanding the caption/hardstatus strings at [kilobitspersecond](https://www.kilobitspersecond.com/2014/02/10/understanding-gnu-screens-hardstatus-strings/)

<a href="/images/screen1.png" target="_blank"><img class="thumbnail" src="/images/screen1.png" width="200" /></a>
<a href="/images/screen2.png" target="_blank"><img class="thumbnail" src="/images/screen2.png" width="200" /></a>

## dircolors and environment sourcing

Since I rarely have an editor instance opened indirectly via the system's environment, I found out by chance that my $EDITOR variable was set to `/usr/bin/nano` instead of `/usr/bin/vim`.  
So I wanted to find out, where that variable was sourced from. In this case, I'm working on a systemd-free gentoo machine and apparently the common way to set default environment variables in gentoo is putting an appropriate file into `/etc/env.d/`.  
So, `grep -ir editor /etc/env.d/` should either come up with a file that can be edited to the appropriate value or one can create a new file. Files are numbered, which determines the order in which they'll be read. So in this case, I created `/etc/env.d/99editor`, containing only one line that says `EDITOR="/usr/bin/vim"`.  
To merge this change into your $ENV, you'll need to run `env-update` and it will be written to `/etc/profile.env`.   
Now, to have a detailed look into $ENV and find out which variables get sourced from where and when, I found a most useful [tip from Stephane Chazelas](https://unix.stackexchange.com/a/154971/109617) on stackexchange. Running
```bash
PS4='+$BASH_SOURCE> ' BASH_XTRACEFD=7 bash -xl 7>&2
```
will tell you in all detail in which order the environment is sourced and which files set which variables. It's also a good occasion to read up again on the various `.bashrc, .bash_profile, /etc/profile` and what have you other files that are involved in the shell environment buildup. Of course I didn't ;).  
But while I'm at it I want to get rid of the annoying default `DIRCOLS` that don't mix with my terminal background at last...  
As `equery u rxvt-unicode` tells me:
```openrc
 * Found these USE flags for x11-terms/rxvt-unicode-9.21:
  U I
	 + + 256-color            : Enable 256 color support
```
that I have 256 colors, I should at least use some of those that can be read from a light background. So, first thing to do:
go to [FLOZz](https://misc.flogisoft.com/bash/tip_colors_and_formatting#colors2), save and run that script (and of course grok all the nice info he has on terminal colours).  next  
`dircolors -p > ~/.dir_colors` (filename is arbitrary)  
to create a file that you can modify and which will be sourced into $ENV in the future. edit the file to your liking.  
I found [seebis solarized dircolors](https://github.com/seebi/dircolors-solarized/blob/master/dircolors.256dark) somewhat instructional. The notation for 256 colors differs from the standard shell escape codes. The notation is for example `00;38;5;34` or `01;48;5;255` where:

* 00; or 01; is for normal or bold 
* 38; or 48; is for foreground or background
* 5; (don't really know, probably the identifier for the 256-colorscheme)
* the last number is the actual colour code as displayed by [FLOZz's script](https://misc.flogisoft.com/bash/tip_colors_and_formatting#colors2)

once the editing is done execute  
`eval "$(dircolors -b ~/.dir_colors)"`  
to have bash use the new colours. To make this permanent, put that command in one of the environment files (see above links to read up which one suites best... I've put it into ~/.bashrc which in turn is sourced by ~/.bash_profile).  
As I don't like coloured file extensions but care only about the files with special permissions, my ~/.dir_colors looks pretty dull:
```bash
Configuration file for dircolors, a utility to help you set the
LS_COLORS environment variable used by GNU ls with the --color option.

Copyright (C) 1996-2017 Free Software Foundation, Inc.
Copying and distribution of this file, with or without modification,
are permitted provided the copyright notice and this notice are preserved.

TERM Eterm
TERM ansi
TERM *color*
TERM con[0-9]*x[0-9]*
TERM cons25
TERM console
TERM cygwin
TERM dtterm
TERM gnome
TERM hurd
TERM jfbterm
TERM konsole
TERM kterm
TERM linux
TERM linux-c
TERM mlterm
TERM putty
TERM rxvt*
TERM screen*
TERM st
TERM terminator
TERM tmux*
TERM vt100
TERM xterm*

NORMAL 00	# no color code at all
FILE 00	# regular file: use no color at all
RESET 0		# reset to "normal" color
DIR 01;38;5;26	# directory
LINK 01;36	# symbolic link.  (If you set this to 'target' instead of a
                # numerical value, the color is as for the file pointed to.)
MULTIHARDLINK 00	# regular file with more than one link
FIFO 40;33	# pipe
SOCK 01;35	# socket
DOOR 01;35	# door
BLK 40;33;01	# block device driver
CHR 40;33;01	# character device driver
ORPHAN 01;05;37;41  # symlink to nonexistent file, or non-stat'able file ...
MISSING 01;05;37;41 # ... and the files they point to
SETUID 37;41	# file that is setuid (u+s)
SETGID 30;43	# file that is setgid (g+s)
CAPABILITY 30;41	# file with capability
STICKY_OTHER_WRITABLE 30;42 # dir that is sticky and other-writable (+t,o+w)
OTHER_WRITABLE 34;42 # dir that is other-writable (o+w) and not sticky
STICKY 37;44	# dir with the sticky bit set (+t) and not other-writable

 This is for files with execute permission:
EXEC 00;38;5;34

 Or if you want to colorize scripts even if they do not have the
 executable bit actually set.
.sh  01;32
.csh 01;32
```
Links:  
gentoo handbook: [environment variables](https://wiki.gentoo.org/wiki/Handbook:X86/Working/EnvVar)  
ubuntu manpages [1](http://manpages.ubuntu.com/manpages/disco/man1/dircolors.1.html), [5](http://manpages.ubuntu.com/manpages/disco/man5/dir_colors.5.html)
