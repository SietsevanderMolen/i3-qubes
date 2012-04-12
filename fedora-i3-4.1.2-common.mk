INSTALL=install -p
PREFIX=PUTINPREFIXHERE
SYSCONFDIR=PUTINSYSCONFDIRHERE
TERM_EMU=xterm
GIT_VERSION:=4.0.1
VERSION:=4.0.1
cflags_for_lib = $(shell pkg-config --silence-errors --cflags $(1))
ldflags_for_lib = $(shell pkg-config --exists $(1) && pkg-config --libs $(1) || echo -l$(2))

CFLAGS += PUTINOPTFLAGSHERE -std=c99 -std=gnu99
CFLAGS += -IPUTININCLUDEDIRHERE
CFLAGS += -IPUTININCLUDEDIRHERE/libev
CFLAGS += -Wunused-result
CFLAGS += -Wunused-value
CFLAGS += -Iinclude
CFLAGS += $(call cflags_for_lib, xcb-keysyms)
ifeq ($(shell pkg-config --exists xcb-util || echo 1),1)
CPPFLAGS += -DXCB_COMPAT
CFLAGS += $(call cflags_for_lib, xcb-atom)
CFLAGS += $(call cflags_for_lib, xcb-aux)
else
CFLAGS += $(call cflags_for_lib, xcb-util)
endif
CFLAGS += $(call cflags_for_lib, xcb-icccm)
CFLAGS += $(call cflags_for_lib, xcb-xinerama)
CFLAGS += $(call cflags_for_lib, xcb-randr)
CFLAGS += $(call cflags_for_lib, xcb)
CFLAGS += $(call cflags_for_lib, xcursor)
CFLAGS += $(call cflags_for_lib, x11)
CFLAGS += $(call cflags_for_lib, yajl)
CFLAGS += $(call cflags_for_lib, libev)
CFLAGS += $(call cflags_for_lib, libpcre,pcre)
CFLAGS += $(call cflags_for_lib, libstartup-notification-1.0)
CPPFLAGS += -DI3_VERSION=\"${GIT_VERSION}\"
CPPFLAGS += -DSYSCONFDIR=\"${SYSCONFDIR}\"
CPPFLAGS += -DTERM_EMU=\"$(TERM_EMU)\"

LIBS += -lm
LIBS += -L $(TOPDIR)/libi3 -li3
LIBS += $(call ldflags_for_lib, xcb-event, xcb-event)
LIBS += $(call ldflags_for_lib, xcb-keysyms, xcb-keysyms)
ifeq ($(shell pkg-config --exists xcb-util || echo 1),1)
LIBS += $(call ldflags_for_lib, xcb-atom, xcb-atom)
LIBS += $(call ldflags_for_lib, xcb-aux, xcb-aux)
else
LIBS += $(call ldflags_for_lib, xcb-util)
endif
LIBS += $(call ldflags_for_lib, xcb-icccm, xcb-icccm)
LIBS += $(call ldflags_for_lib, xcb-xinerama, xcb-xinerama)
LIBS += $(call ldflags_for_lib, xcb-randr, xcb-randr)
LIBS += $(call ldflags_for_lib, xcb, xcb)
LIBS += $(call ldflags_for_lib, xcursor, Xcursor)
LIBS += $(call ldflags_for_lib, x11, X11)
LIBS += $(call ldflags_for_lib, yajl, yajl)
LIBS += $(call ldflags_for_lib, libev, ev)
LIBS += $(call ldflags_for_lib, libpcre,pcre)
LIBS += $(call ldflags_for_lib, libstartup-notification-1.0)

# Please test if -Wl,--as-needed works on your platform and send me a patch.
# it is known not to work on Darwin (Mac OS X)
#ifneq (,$(filter Linux GNU GNU/%, $(UNAME)))
#LDFLAGS += -Wl,--as-needed
#endif

CFLAGS += -idirafter $(TOPDIR)/yajl-fallback

#ifneq (,$(filter Linux GNU GNU/%, $(UNAME)))
#CPPFLAGS += -D_GNU_SOURCE
#endif

.PHONY: install clean dist distclean

