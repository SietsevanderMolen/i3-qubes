%global upstream_version 3.d-bf1

Name:           i3
Version:        3.d.bf1
Release:        3%{?dist}
Summary:        Improved tiling window manager

Group:          User Interface/Desktops
License:        BSD
URL:            http://i3.zekjur.net
Source0:        http://i3.zekjur.net/downloads/%{name}-%{upstream_version}.tar.bz2
Source1:        %{name}-logo.svg
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  xcb-util-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-proto
BuildRequires:  libev-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libX11-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  asciidoc
Requires:       rxvt-unicode
Requires:       xorg-x11-apps
Requires:       dmenu
Requires:       xorg-x11-fonts-misc


%description
Key features of i3 are correct implementation of Xinerama (workspaces are 
assigned to virtual screens, i3 does the right thing when attaching new 
monitors), XrandR support (not done yet), horizontal and vertical columns 
(think of a table) in tiling. Also, special focus is on writing clean, readable 
and well documented code. i3 uses xcb for asynchronous communication with X11, 
and has several measures to be very fast.

Please be aware that i3 is primarily targeted at advanced users and developers.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildRequires:  doxygen
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}


%description doc
Asciidoc and doxygen generated documentations for %{name}.


%prep
%setup -q -n %{name}-%{upstream_version}

sed -e 's|CFLAGS += -Wunused|CFLAGS += -I/usr/include/libev|g' \
    -e 's|CFLAGS += -Wall|CFLAGS += %{optflags}|g' \
    -e 's|CFLAGS += -pipe|CFLAGS += |g' \
    -i common.mk


%build
make %{?_smp_mflags}

cd man; make %{?_smp_mflags}
cd ../docs; make %{?_smp_mflags}

cd ..
doxygen pseudo-doc.doxygen
mv pseudo-doc/html pseudo-doc/doxygen


%install
rm -rf %{buildroot}

make install \
     DESTDIR=%{buildroot} \
     INSTALL="install -p"

mkdir -p %{buildroot}/%{_mandir}/man1/
install -Dpm0644 man/*.1 \
        %{buildroot}/%{_mandir}/man1/

mkdir -p %{buildroot}/%{_datadir}/pixmaps/
install -Dpm0644 %{SOURCE1} \
        %{buildroot}/%{_datadir}/pixmaps/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc GOALS LICENSE RELEASE-NOTES-%{upstream_version}
%{_bindir}/%{name}*
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/config
%config %{_sysconfdir}/%{name}/welcome
%{_datadir}/xsessions/%{name}.desktop
%{_mandir}/man1/%{name}*
%{_datadir}/pixmaps/%{name}-logo.svg


%files doc
%defattr(-,root,root,-)
%doc docs/*.{html,png} pseudo-doc/doxygen/


%changelog
* Wed Jan 06 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d.bf1-3
- Add Missing R: xorg-x11-fonts-misc
- Add i3-logo as SOURCE1 and install it to DATADIR/pixmaps

* Sun Dec 27 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d.bf1-2
- Add missing Requires for a functional minimal (not comfortable) i3-system. (The requirements provides functions which are used in the standard configfile)
- Build manpages and add them to main-pkg
- Build doxygen generated documentation and add them to the documentation subpackage

* Fri Dec 25 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d.bf1-1
- Correct version-tag (https://www.redhat.com/archives/fedora-devel-list/2009-December/msg01102.html) Thank you Michael
- Add more documentation (generated with asciidoc)

* Fri Dec 25 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d-bf1_1
- New upstream release

* Wed Dec 02 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d-1
- Package build for Fedora
