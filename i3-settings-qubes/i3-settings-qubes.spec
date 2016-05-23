%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/i3-settings-qubes
%endif

Name:       i3-settings-qubes
Version:    0.1
Release:    1%{?dist}
Summary:    Default i3 settings for Qubes

Group:      User Interface/Desktops
License:    GPLv2+
URL:        http://www.qubes-os.org/
Source0:    i3.config
Source1:    i3.config.keycodes
Source2:    qubes-i3-sensible-terminal.sh
Source3:    qubes-i3status.sh
Source4:    qubes-xdg-autostart.sh

Requires:   i3
Requires:   xautolock
Requires:   i3lock

%description
%{summary}

%prep

%build


%install
install -m 644 -D %{SOURCE0} %{buildroot}%{_sysconfdir}/i3/config
install -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/i3/config.keycodes
install -m 755 -D %{SOURCE2} %{buildroot}%{_sbindir}/qubes-i3-sensible-terminal.sh
install -m 755 -D %{SOURCE3} %{buildroot}%{_sbindir}/qubes-i3status.sh
install -m 755 -D %{SOURCE4} %{buildroot}%{_sbindir}/qubes-xdg-autostart.sh

%files
%{_sysconfdir}/i3/config
%{_sysconfdir}/i3/config.keycodes
%{_sbindir}/qubes-i3-sensible-terminal.sh
%{_sbindir}/qubes-i3status.sh
%{_sbindir}/qubes-xdg-autostart.sh

%changelog
