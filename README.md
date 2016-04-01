# i3-qubes
Qubes OS rpm for i3 4.8

You'll find the full installation instructions and more information on https://sietse.no/i3-wm-in-qubes-os

## To install, follow these steps:

First, clone the repository in a vm (if needed, install git first):

```
user@vm$ git clone https://github.com/SietsevanderMolen/i3-qubes.git
```

Then make sure all dependencies are installed:

```
user@vm$ sudo dnf install fedpkg asciidoc bison doxygen flex libX11-devel libXcursor-devel libxcb-devel libxkbfile-devel pango-devel perl startup-notification-devel xcb-proto xcb-util-cursor-devel xcb-util-devel xcb-util-keysyms-devel xcb-util-wm-devel xmlto yajl-devel
```

After that, compile the rpm:

```
user@vm$ fedpkg --dist f20 local --builddir ~/rpmbuild
```

Then, copy the rpm to your Dom0:
```
user@Dom0$ qvm-run --pass-io <vmname> 'cat /home/user/rpmbuild/x86_64/i3-4.8-3.f20.x86_64.rpm' > i3-4.8-3.f20.x86_64.rpm
```

And finally install it:

```
user@Dom0$ sudo yum localinstall i3-4.8-3.f20.x86_64.rpm
```

Log out, log in again and configure to your needs!
