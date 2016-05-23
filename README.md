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
user@vm$ sudo dnf install -y $(cat build-deps.list)
```

After that, build the rpm:

```
user@vm$ make rpms
```

Then, copy the rpm to your Dom0:
```
user@Dom0$ qvm-run --pass-io <vmname> 'cat /path/to/rpm/x86_64/i3-4.8-3.f20.x86_64.rpm' > i3-4.8-3.f20.x86_64.rpm
```

And finally install it:

```
user@Dom0$ sudo yum localinstall i3-4.8-3.f20.x86_64.rpm
```

Log out, log in again and configure to your needs!

## Contributors
https://github.com/SietsevanderMolen
https://github.com/o-
https://github.com/minad
