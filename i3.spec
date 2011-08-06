Name:           i3
Version:        4.0.1
Release:        1%{?dist}
Summary:        Improved tiling window manager
Group:          User Interface/Desktops
License:        BSD
URL:            http://i3wm.org
Source0:        http://i3wm.org/downloads/%{name}-%{version}.tar.bz2
Source1:        %{name}-logo.svg
Source2:        fedora-%{name}-%{version}-common.mk

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  xcb-util-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-proto
BuildRequires:  libev-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libX11-devel
BuildRequires:  yajl-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  asciidoc

Requires:       rxvt-unicode
Requires:       xorg-x11-apps
Requires:       dmenu
Requires:       xorg-x11-fonts-misc
Requires:       dzen2


%description
Key features of i3 are correct implementation of XrandR, horizontal and vertical
columns (think of a table) in tiling. Also, special focus is on writing clean, 
readable and well documented code. i3 uses xcb for asynchronous communication
with X11, and has several measures to be very fast.

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
%setup -q

cp %{SOURCE2} %{_builddir}/%{name}-%{version}/

sed \
    -e 's|include $(TOPDIR)/common.mk|include $(TOPDIR)/fedora-%{name}-%{version}-common.mk|g' \
    -i Makefile

sed \
    -e 's|PUTINOPTFLAGSHERE|%{optflags}|g' \
    -e 's|PUTININCLUDEDIRHERE|%{_includedir}|g' \
    -e 's|PUTINPREFIXHERE|%{_prefix}|g' \
    -e 's|PUTINSYSCONFDIRHERE|%{_sysconfdir}|g' \
    -i fedora-%{name}-%{version}-common.mk


%build
make %{?_smp_mflags} V=1

cd man; make %{?_smp_mflags} V=1
cd ../docs; make %{?_smp_mflags} V=1

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
%doc GOALS LICENSE RELEASE-NOTES-%{version}
%{_bindir}/%{name}*
%{_includedir}/%{name}/*
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/welcome
%config(noreplace) %{_sysconfdir}/%{name}/config.keycodes
%{_datadir}/xsessions/%{name}.desktop
%{_mandir}/man*/%{name}*
%{_datadir}/pixmaps/%{name}-logo.svg


%files doc
%defattr(-,root,root,-)
%doc docs/*.{html,png} pseudo-doc/doxygen/


%changelog
* Mon Aug 01 2011 Simon Wesp <cassmodiah@fedoraproject.org> - 4.0.1-1
- New upstream release

* Sun Jul 31 2011 Simon Wesp <cassmodiah@fedoraproject.org> -4.0-1
- New upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.e-6.bf2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 19 2011 Simon Wesp <cassmodiah@fedoraproject.org> - 3.e-5.bf2
- New upstream release

* Tue Jan 11 2011 Simon Wesp <cassmodiah@fedoraproject.org> - 3.e-4.bf1
- rebuild against newest libev

* Wed Jun 09 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 3.e-3.bf1
- New upstream release (3.e-bf1)

* Fri Apr 16 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 3.e-2
- Rebuild

* Tue Mar 30 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 3.e-1
- New upstream release

* Sat Mar 20 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d.bf1-4.20100320git
- Update to current git

* Wed Feb 03 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d.bf1-4
- Some bugfixes (sync with upstream)

* Wed Jan 06 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d.bf1-3
- Add Missing R: xorg-x11-fonts-misc
- Add i3-logo as SOURCE1 and install it to DATADIR/pixmaps

* Sun Dec 27 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d.bf1-2
- Add missing Requires for a functional minimal (not comfortable) i3-system.
- Build manpages and add them to main-pkg
- Build doxygen generated documentation and add them to the doc subpackage

* Fri Dec 25 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d.bf1-1
- Correct version-tag (Thanks to Michael Schwendt)
- Add more documentation (generated with asciidoc)

* Fri Dec 25 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d-bf1_1
- New upstream release

* Wed Dec 02 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d-1
- Package build for Fedora
