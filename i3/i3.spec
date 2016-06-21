%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/i3
%endif

Name:           i3
Version:        4.12
Release:        3%{?dist}
Epoch:          1000
Summary:        Improved tiling window manager
License:        BSD
URL:            http://i3wm.org
Source0:        http://i3wm.org/downloads/%{name}-%{version}.tar.bz2
Source1:        %{name}-logo.svg
Patch0:         0001-Show-qubes-domain-in-non-optional-colored-borders.patch

BuildRequires:  asciidoc
BuildRequires:  bison
BuildRequires:  cairo-devel
BuildRequires:  flex
BuildRequires:  libX11-devel
BuildRequires:  libev-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  pango-devel
BuildRequires:  pcre-devel
# TODO: Testsuites
#BuildRequires:  perl(strict)
#BuildRequires:  perl(warnings)
#BuildRequires:  perl(Pod::Usage)
#BuildRequires:  perl(Cwd)
#BuildRequires:  perl(File::Temp)
#BuildRequires:  perl(Getopt::Long)
#BuildRequires:  perl(POSIX)
#BuildRequires:  perl(TAP::Harness)
#BuildRequires:  perl(TAP::Parser)
#BuildRequires:  perl(TAP::Parser::Aggregator)
#BuildRequires:  perl(Time::HiRes)
#BuildRequires:  perl(IO::Handle)
#BuildRequires:  perl(AnyEvent::Util)
#BuildRequires:  perl(AnyEvent::Handle)
#BuildRequires:  perl(AnyEvent::I3)
#BuildRequires:  perl(X11::XCB::Connection)
#BuildRequires:  perl(Carp)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Data::Dumper::Names)
BuildRequires:  startup-notification-devel
BuildRequires:  xcb-proto
BuildRequires:  xcb-util-cursor-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xmlto
%ifnarch s390 s390x
BuildRequires:  xorg-x11-drv-dummy
%endif
BuildRequires:  yajl-devel

Requires:       dmenu
Requires:       dzen2
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# TODO - CHECK THIS - we're building in a different vm, so we can't rely on the perl version
# 5.18.4 should be available to fc20
#Requires:       perl(:MODULE_COMPAT_5.18.4)
Recommends:     rxvt-unicode
Recommends:     xorg-x11-apps
Requires:       xorg-x11-fonts-misc

%description
Key features of i3 are correct implementation of XrandR, horizontal and vertical
columns (think of a table) in tiling. Also, special focus is on writing clean,
readable and well documented code. i3 uses xcb for asynchronous communication
with X11, and has several measures to be very fast.

Please be aware that i3 is primarily targeted at advanced users and developers.

%package        doc
Summary:        Documentation for %{name}
BuildRequires:  doxygen
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
Asciidoc and doxygen generated documentations for %{name}.

%prep
%setup -q
%patch0 -p1

# Drop /usr/bin/env lines in those which will be installed to %%_bindir.
find . -maxdepth 1 -type f -name "i3*" -exec sed -i -e '1s;^#!/usr/bin/env perl;#!/usr/bin/perl;' {} + -print

# 1. Drop dwarf-2, -g3 in CFLAGS recommended by gcc maintainer. Since upstream
# uses -pipe and -g only, we can safely ignore these, but ldflags needs
# override still.
# 2. Preserve the timestamps.
sed -i -e 's|LDFLAGS ?=|override LDFLAGS +=|g' \
       -e 's|INSTALL=.*|INSTALL=install -p|g' \
       common.mk

%build
%make_build CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}" V=1
%make_build -C man V=1
%make_build -C docs V=1

doxygen pseudo-doc.doxygen
mv pseudo-doc/html pseudo-doc/doxygen

%install
%make_install

mkdir -p %{buildroot}%{_mandir}/man1/
install -Dpm0644 man/*.1 \
        %{buildroot}%{_mandir}/man1/

mkdir -p %{buildroot}%{_datadir}/pixmaps/
install -Dpm0644 %{SOURCE1} \
        %{buildroot}%{_datadir}/pixmaps/

%check
%ifnarch s390 s390x
# TODO: with xorg dummy to test the package.
#cd testcases/ && ./complete-run.pl -p 1
%endif

%files
%doc RELEASE-NOTES-%{version}
%license LICENSE
%{_bindir}/%{name}*
%{_includedir}/%{name}/
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/config.keycodes
%{_datadir}/xsessions/%{name}.desktop
%{_datadir}/xsessions/%{name}-with-shmlog.desktop
%{_mandir}/man*/%{name}*
%{_datadir}/pixmaps/%{name}-logo.svg
%{_datadir}/applications/%{name}.desktop

%files doc
%doc docs/*.{html,png} pseudo-doc/doxygen/

%changelog
* Mon Mar 07 2016 Christian Dersch <lupinix@mailbox.org> - 4.12-3
- Fixed mispelled dependency i3status

* Sun Mar 06 2016 Christian Dersch <lupinix@mailbox.org> - 4.12-2
- Added BR: cairo-devel to enable new rendering implementation

* Sun Mar 06 2016 Christian Dersch <lupinix@mailbox.org> - 4.12-1
- Upgrade to version 4.12

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Christian Dersch <lupinix@mailbox.org> - 4.11-1
- new version

* Tue Sep 08 2015 Christopher Meng <rpm@cicku.me> - 4.10.4-1
- Update to 4.10.4

* Fri Aug 14 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 4.10.3-3
- Fix typo in spec file

* Fri Aug 14 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 4.10.3-2
- Add Recommends for i3-status
- Move Requires for rxvt-unicode and xorg-x11-apps to Recommends

* Thu Aug 13 2015 Martin Preisler <mpreisle@redhat.com> - 4.10.3-1
- Update to 4.10.3 (#1248840)
- Added Getopt::Long perl build dep

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.10.2-2
- Perl 5.22 rebuild

* Sun May 17 2015 Björn Esser <bjoern.esser@gmail.com> - 4.10.2-1
- Update to 4.10.2 (#1206967)

* Sun Mar 08 2015 Christopher Meng <rpm@cicku.me> - 4.9.1-1
- Update to 4.9.1

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.8-5
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 04 2014 Dan Horák <dan[at]danny.cz> - 4.8-3
- no xorg-x11-drv-* on s390(x)

* Wed Jun 25 2014 Christopher Meng <rpm@cicku.me> - 4.8-2
- Bugfix: don't focus unmapped container on manage(regression)

* Sat Jun 21 2014 Christopher Meng <rpm@cicku.me> - 4.8-1
- Update to 4.8

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Martin Preisler <mpreisle@redhat.com> - 4.7.2-1
- New upstream release

* Thu Aug 08 2013 Simon Wesp <cassmodiah@fedoraproject.org> - 4.6-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.5.1-2
- Perl 5.18 rebuild

* Thu Mar 21 2013 Simon Wesp <cassmodiah@fedoraproject.org> - 4.5.1-1
- New upstream release

* Tue Mar 12 2013 Simon Wesp <cassmodiah@fedoraproject.org> - 4.5-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Martin Preisler <mpreisle@redhat.com> - 4.4-1
- update to 4.4

* Wed Oct 31 2012 Felix Wiedemann <felix.wiedemann@online.de> - 4.3-1
- update to 4.3
- enabled support for pango

* Mon Aug 20 2012 Adam Jackson <ajax@redhat.com> 4.2-3
- Rebuild for new xcb-util soname

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Martin Preisler <mpreisle@redhat.com> - 4.2-1
- update to 4.2

* Mon Mar 26 2012 Tom Callaway <spot@fedoraproject.org> - 4.1.2-1
- update to 4.1.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 4.0.1-2
- Rebuild for libyajl soname bump

* Mon Aug 01 2011 Simon Wesp <cassmodiah@fedoraproject.org> - 4.0.1-1
- New upstream release

* Sun Jul 31 2011 Simon Wesp <cassmodiah@fedoraproject.org> -4.0-1
- New upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.e-6.bf2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Simon Wesp <cassmodiah@fedoraproject.org> - 3.e-5.bf2
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
