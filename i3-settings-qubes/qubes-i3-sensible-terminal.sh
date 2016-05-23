#!/bin/bash

run_terminal='
for t in $TERMINAL urxvt rxvt terminator Eterm aterm xterm gnome-terminal roxterm xfce4-terminal; do
    which $t > /dev/null 2>&1 && exec $t;
done
'

get_id() {
    local id=$(xprop -root _NET_ACTIVE_WINDOW)
    echo ${id##* } # extract id
}

get_vm() {
    local id=$(get_id)
    local vm=$(xprop -id $id | grep '_QUBES_VMNAME(STRING)')
    local vm=${vm#*\"} # extract vmname
    echo ${vm%\"*} # extract vmname
}

main() {
    local vm=$(get_vm)
    if [[ -n "$vm" ]]; then
        qvm-run "$vm" "bash -c '$run_terminal'"
    else # run terminal in dom0
        exec bash -c "$run_terminal"
    fi
}

main
