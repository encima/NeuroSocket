#!/bin/bash 

xprop -id $(xprop -root _NET_ACTIVE_WINDOW | cut -d ' ' -f 5) _EoNT_WM_NAME WM_CLASS
