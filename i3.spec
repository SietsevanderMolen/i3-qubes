%global upstream_version 3.d-bf1

Name:           i3
Version:        3.d.bf1
Release:        4%{?dist}
Summary:        Improved tiling window manager

Group:          User Interface/Desktops
License:        BSD
URL:            http://i3.zekjur.net
Source0:        http://i3.zekjur.net/downloads/%{name}-%{upstream_version}.tar.bz2
Source1:        %{name}-logo.svg
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Fix bindings using the cursor keys in default config
Patch0: %{name}-%{upstream_version}-6de212f7eec993346d24af5333ceedfe7849a2f6.patch
# Bugfix: Don’t put dock clients into floating mode (Thanks xeen)
Patch1: %{name}-%{upstream_version}-9dce0818378feefe0aa7844f51f48e03a01607dc.patch
# We don’t have DLOG yet in master branch (Thanks ccount)
Patch2: %{name}-%{upstream_version}-4c87170494cbdd680cb4b128dd60fcdaac995609.patch
# Remove superfluous #include <assert.h> (Thanks badboy)
Patch3: %{name}-%{upstream_version}-8adce413f5f92bd8e4c485ee61ff6b8448cd2058.patch
# Bugfix: Containers could lose their snap state (Thanks Atsutane)
Patch4: %{name}-%{upstream_version}-505eaaf3490c21de00e636d012f513f4334ed5c3.patch
# Bugfix: Use ev_loop_new instead of ev_default_loop because the latter one blocks SIGCHLD (Thanks Ciprian)
Patch5: %{name}-%{upstream_version}-86b0dab7ea8b0252fe30506b08074f4ef4798219.patch
# Bugfix: if a font provides no per-char info for width, fall back to the default (Thanks Ciprian)
Patch6: %{name}-%{upstream_version}-d1a0e930a8698deb32d8356bc13403fdd86e2b78.patch
# Use LOG instead of DLOG (next branch feature only)
Patch7: %{name}-%{upstream_version}-1dcb4a39fd676441c30ce5614c2ae6082114837d.patch
# bugfix: lexer: return to INITIAL state (Thanks dirkson)
Patch8: %{name}-%{upstream_version}-aaf46bfc55dccf57962ac12d804b6886620c20fc.patch
# Bugfix: Don’t leak IPC socket to launched processes
Patch9: %{name}-%{upstream_version}-f399c3ef9d0db8c95113b242e0c69498cf077669.patch

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

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

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
%config(noreplace) %{_sysconfdir}/%{name}/welcome
%{_datadir}/xsessions/%{name}.desktop
%{_mandir}/man1/%{name}*
%{_datadir}/pixmaps/%{name}-logo.svg


%files doc
%defattr(-,root,root,-)
%doc docs/*.{html,png} pseudo-doc/doxygen/


%changelog
* Wed Feb 03 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 3.d.bf1-4
- Some bugfixes (sync with upstream)
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=6de212f7eec993346d24af5333ceedfe7849a2f6
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=aaf46bfc55dccf57962ac12d804b6886620c20fc
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=1dcb4a39fd676441c30ce5614c2ae6082114837d
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=d1a0e930a8698deb32d8356bc13403fdd86e2b78
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=86b0dab7ea8b0252fe30506b08074f4ef4798219
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=505eaaf3490c21de00e636d012f513f4334ed5c3
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=8adce413f5f92bd8e4c485ee61ff6b8448cd2058
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=4c87170494cbdd680cb4b128dd60fcdaac995609
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=9dce0818378feefe0aa7844f51f48e03a01607dc
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=f399c3ef9d0db8c95113b242e0c69498cf077669
- Add Patch http://code.stapelberg.de/git/i3/commit/?id=d1a0e930a8698deb32d8356bc13403fdd86e2b78

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
