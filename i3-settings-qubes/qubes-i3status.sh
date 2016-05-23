#!/bin/bash

WIFI_VM="sys-net"

json() {
    if [[ -n "$3" ]]; then
        echo -n "{\"name\":\"$1\",\"color\":\"$3\",\"full_text\":\"$2\"},"
    else
        echo -n "{\"name\":\"$1\",\"full_text\":\"$2\"},"
    fi
}

status_net() {
    local net=$(qvm-run $WIFI_VM -p 'iwconfig; ifconfig' 2>/dev/null)
    local ssid=$(echo "$net" | perl -ne 'print $1 if /ESSID:"(.*)"/')
    if [[ -n $ssid ]]; then
        local quality=$(echo "$net" | perl -ne 'print "$1 " if /Quality=([^ ]+)/')
        json wifi "W: $quality$ssid"
    fi
    local ip=$(echo "$net" | perl -ne 'if (/^[w|e]/../^$/) { print $1 if /inet ([^ ]+)/ }')
    [[ -n $ip ]] && json ip "I: $ip"
}

status_time() {
    local time=$(date '+%F %T')
    echo -n "{\"name\":\"time\",\"full_text\":\"$time\"}" # last entry
}

status_bat() {
    local bat_now=$(cat /sys/class/power_supply/BAT0/energy_now 2>/dev/null)
    local bat_full=$(cat /sys/class/power_supply/BAT0/energy_full_design 2>/dev/null)
    if [[ -n "$bat_full" ]]; then
        local bat=$((100*bat_now/bat_full))

        local ac=''
        local color='#00ff00'
        if [[ $(cat /sys/class/power_supply/AC/online) == '1' ]]; then
            ac=' AC'
        elif ((bat < 25)); then
            color='#ff0000'
        elif ((bat < 50)); then
            color='#ffff00'
        fi

        json bat "B: $bat%$ac" "$color"
    fi
}

status_load() {
    local load=$(uptime)
    load=${load/#*load average: }
    load=${load%,*,*}
    json load "$load"
}

status_qubes() {
    local qubes=$(qvm-ls 2>/dev/null | grep ' \* ' | wc -l)
    json qubes "$qubes Q"
}

status_disk() {
    local disk=`df -h / | tail -n 1 | awk '{print $4}'`
    json disk "D: $disk"
}

main() {
    echo '{"version":1}'
    echo '['
    echo '[]'
    local n
    for ((n=0; ; ++n)); do
        if (( n % 10 == 0 )); then
            local qubes=$(status_qubes)
            local net=$(status_net)
            local disk=$(status_disk)
            local bat=$(status_bat)
            local load=$(status_load)
        fi
        local time=$(status_time)
        echo ",[$qubes$net$disk$bat$load$time]"
        sleep 1
    done
}

main
