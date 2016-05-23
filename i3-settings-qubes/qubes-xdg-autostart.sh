autostart_etc=${XDG_CONFIG_DIRS-/etc/xdg}/autostart
autostart_home=${XDG_CONFIG_HOME-~/.config}/autostart

shopt -s nullglob
for i in $autostart_etc/*.desktop $autostart_home/*.desktop; do
    if ! grep -q "OnlyShowIn=" "$i"; then
        $(grep "Exec=" "$i" | sed 's/Exec=//') &
    fi
done
