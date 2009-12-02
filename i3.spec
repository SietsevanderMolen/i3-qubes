Name:           i3
Version:        3.d
Release:        1%{?dist}
Summary:        Improved tiling window manager

Group:          User Interface/Desktops
License:        BSD
URL:            http://i3.zekjur.net
Source0:        http://i3.zekjur.net/downloads/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  xcb-util-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-proto
BuildRequires:  libev-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libX11-devel
BuildRequires:  bison
BuildRequires:  flex


%description
Key features of i3 are correct implementation of Xinerama (workspaces are 
assigned to virtual screens, i3 does the right thing when attaching new 
monitors), XrandR support (not done yet), horizontal and vertical columns 
(think of a table) in tiling. Also, special focus is on writing clean, readable 
and well documented code. i3 uses xcb for asynchronous communication with X11, 
and has several measures to be very fast.

Please be aware that i3 is primarily targeted at advanced users and developers.


%prep
%setup -q

#####          I M P O R T A N T         #####
##### !!!! TO CHECK ON EVERY UPDATE !!!! #####
# correct path of libev inclusion, honor optflags and clear double mention.
sed -e 's|CFLAGS += -Wunused|CFLAGS += -I/usr/include/libev|g' \
    -e 's|CFLAGS += -Wall|CFLAGS += %{optflags}|g' \
    -e 's|CFLAGS += -pipe|CFLAGS += |g' \
    -i common.mk
##############################################


%build
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc GOALS LICENSE TODO
%{_bindir}/%{name}
%{_bindir}/%{name}-input
%{_bindir}/%{name}-msg
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/config
%{_sysconfdir}/%{name}/welcome
%{_datadir}/xsessions/%{name}.desktop


%changelog
* Wed Dec 02 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d-1
- Package build for Fedora
