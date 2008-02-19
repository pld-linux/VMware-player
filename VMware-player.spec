#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace utilities
%bcond_with	internal_libs	# internal libs stuff
%bcond_with	verbose		# verbose build (V=1)
#
%include	/usr/lib/rpm/macros.perl

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%ifarch %{x8664}
%undefine	with_userspace
%endif
#
%define		ver		2.0.2
%define		buildid	59824
%define		urel	115
%define		ccver	%(rpm -q --qf '%{V}' gcc)
%define		_rel	0.13
#
Summary:	VMware player
Summary(pl.UTF-8):	VMware player - wirtualna platforma dla stacji roboczej
Name:		VMware-player
Version:	%{ver}.%{buildid}
Release:	%{_rel}
License:	custom, non-distributable
Group:		Applications/Emulators
Source0:	http://download3.vmware.com/software/vmplayer/%{name}-%{ver}-%{buildid}.i386.tar.gz
# NoSource0-md5:	0c108db615943d71b78f18826611acce
NoSource:	0
Source1:	http://download3.vmware.com/software/vmplayer/%{name}-%{ver}-%{buildid}.x86_64.tar.gz
# NoSource1-md5:	f59a77f3e3b8e87591eff605c4bbb796
NoSource:	1
Source2:	http://knihovny.cvut.cz/ftp/pub/vmware/vmware-any-any-update%{urel}.tar.gz
# Source2-md5:	ab33ff7a799fee77f0f4ba5667cd4b9a
Source3:	%{name}-vmnet.conf
Source4:	%{name}.png
Source5:	%{name}.desktop
Source6:	%{name}-nat.conf
Source7:	%{name}-dhcpd.conf
Source8:	%{name}.init
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-run_script.patch
URL:		http://www.vmware.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	libgnomecanvasmm
Requires:	libview >= 0.5.5-2
Requires:	openssl >= 0.9.7
Requires(post,postun):	desktop-file-utils
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles %{_libdir}/vmware/lib/.*\.so.*

%description
VMware Player Virtual Platform is a thin software layer that allows
multiple guest operating systems to run concurrently on a single
standard PC, without repartitioning or rebooting, and without
significant loss of performance.

%description -l pl.UTF-8
VMware Player Virtual Platform to cienka warstwa oprogramowania
pozwalająca na jednoczesne działanie wielu gościnnych systemów
operacyjnych na jednym zwykłym PC, bez repartycjonowania ani
rebootowania, bez znacznej utraty wydajności.

%package debug
Summary:	VMware debug utility
Summary(pl.UTF-8):	Narzędzie VMware do odpluskwiania
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}

%description debug
VMware debug utility.

%description debug -l pl.UTF-8
Narzędzie VMware do odpluskwiania.

%package help
Summary:	VMware Player help files
Summary(pl.UTF-8):	Pliki pomocy dla VMware Player
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}

%description help
VMware Player help files.

%description help -l pl.UTF-8
Pliki pomocy dla VMware Player.

%package networking
Summary:	VMware networking utilities
Summary(pl.UTF-8):	Narzędzia VMware do obsługi sieci
Group:		Applications/Emulators
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Obsoletes:	VMware-Player-samba

%description networking
VMware networking utilities.

%description networking -l pl.UTF-8
Narzędzia VMware do obsługi sieci.

%package -n kernel%{_alt_kernel}-misc-vmmon
Summary:	Kernel module for VMware Player
Summary(pl.UTF-8):	Moduł jądra dla VMware Player
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vmmon) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-misc-vmmon
Kernel modules for VMware Player - vmmon.

%description -n kernel%{_alt_kernel}-misc-vmmon -l pl.UTF-8
Moduły jądra dla VMware Player - vmmon.

%package -n kernel%{_alt_kernel}-misc-vmnet
Summary:	Kernel module for VMware Player
Summary(pl.UTF-8):	Moduł jądra dla VMware Player
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vmnet) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-misc-vmnet
Kernel modules for VMware Player - vmnet.

%description -n kernel%{_alt_kernel}-misc-vmnet -l pl.UTF-8
Moduły jądra dla VMware Player - vmnet.

%prep
%setup -q -n vmware-player-distrib -a2
cd vmware-any-any-update%{urel}
tar xf vmmon.tar
tar xf vmnet.tar
cp -a vmmon-only{,.clean}
cp -a vmnet-only{,.clean}
sed -e 's/filter x86_64%/filter x86_64% amd64% ia64%/' \
	-i vmnet-only.clean/Makefile.kernel
cd -

%patch0 -p1
%patch1 -p1

# will never use these
rm -f lib/libconf/lib/gtk-2.0/2.10.0/engines/*.a
rm -f lib/libconf/lib/gtk-2.0/2.10.0/immodules/*.a
rm -f lib/libconf/lib/gtk-2.0/2.10.0/loaders/*.a
rm -f lib/libconf/lib/pango/1.5.0/modules/*.a

%{__sed} -i -e 's#/build/.*/libconf/#%{_libdir}/vmware/libconf/#' \
	lib/libconf/etc/gtk-2.0/{gdk-pixbuf.loaders,gtk.immodules} \
	lib/libconf/etc/pango/{pango.modules,pangorc}

# typo?
%{__sed} -i -e 's#/etc/pango/pango/pangox.aliases#/etc/pango/pangox.aliases#' \
	lib/libconf/etc/pango/pangorc

%build
sed -i 's:vm_db_answer_LIBDIR:VM_LIBDIR:g;s:vm_db_answer_BINDIR:VM_BINDIR:g' bin/vmplayer

cd vmware-any-any-update%{urel}
chmod u+w ../lib/bin/vmware-vmx ../lib/bin-debug/vmware-vmx ../bin/vmnet-bridge

# hack until new any-any-update version available
sed -i -e 's/#define.*VMMON_VERSION_V6.*/#define VMMON_VERSION_V6		(167 << 16 | 0)/g' vmmon-only.clean/include/iocontrols_compat.h

%if %{with kernel}
rm -rf built
mkdir built

for mod in vmmon vmnet ; do
	for cfg in %{?with_dist_kernel:dist}%{!?with_dist_kernel:nondist}; do
		if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
			exit 1
		fi
		rm -rf $mod-only
		cp -a $mod-only.clean $mod-only
		cd $mod-only
		install -d o/include/linux
		ln -sf %{_kernelsrcdir}/config-$cfg o/.config
		ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
		ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
	if grep -q "^CONFIG_PREEMPT_RT=y$" o/.config; then
		sed -e '/pollQueueLock/s/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(pollQueueLock)/' \
			-e '/timerLock/s/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(timerLock)/' \
			-i ../vmmon-only/linux/driver.c
		sed -e 's/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(vnetHubLock)/' \
			-i ../vmnet-only/hub.c
		sed -e 's/RW_LOCK_UNLOCKED/RW_LOCK_UNLOCKED(vnetPeerLock)/' \
			-i ../vmnet-only/driver.c
	fi
	%if %{with dist_kernel}
		%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
	%else
		install -d o/include/config
		touch o/include/config/MARKER
		ln -sf %{_kernelsrcdir}/scripts o/scripts
		%endif
		%{__make} -C %{_kernelsrcdir} modules \
			VMWARE_VER=VME_V5 \
			SRCROOT=$PWD \
			M=$PWD O=$PWD/o \
			VM_KBUILD=26 \
			%{?with_verbose:V=1} \
			VM_CCVER=%{ccver}
		mv -f $mod.ko ../built/$mod-$cfg.ko
		cd -
	done
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/{nat,dhcpd} \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware/{bin,lib,share/pixmaps} \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_pixmapsdir} \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/var/run/vmware
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
echo "options vmmon vmversion=16" > $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{name}-vmmon.conf

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

cd vmware-any-any-update%{urel}/built
install vmmon* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vmmon.ko
install vmnet* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vmnet.ko
cd -
%endif

%if %{with userspace}
install %{SOURCE8} $RPM_BUILD_ROOT/etc/rc.d/init.d/vmnet
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/nat/nat.conf
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases
touch $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases~

cp -a lib/share/icons/hicolor/* $RPM_BUILD_ROOT%{_iconsdir}/hicolor

install lib/share/pixmaps/* $RPM_BUILD_ROOT%{_libdir}/vmware/share/pixmaps
install doc/EULA $RPM_BUILD_ROOT%{_libdir}/vmware/share/EULA.txt

install bin/*-* $RPM_BUILD_ROOT%{_bindir}
install lib/bin/vmware-vmx $RPM_BUILD_ROOT%{_libdir}/vmware/bin
install lib/lib/libvmwarebase.so.0/libvmwarebase.so.0 $RPM_BUILD_ROOT%{_libdir}
install lib/lib/libvmwareui.so.0/libvmwareui.so.0 $RPM_BUILD_ROOT%{_libdir}

cp -r	lib/{bin-debug,config,help*,messages,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

cat > $RPM_BUILD_ROOT%{_sysconfdir}/vmware/locations <<EOF
VM_BINDIR=%{_bindir}
VM_LIBDIR=%{_libdir}/vmware
EOF

%if %{with internal_libs}
install bin/vmplayer $RPM_BUILD_ROOT%{_bindir}
install lib/bin/vmplayer $RPM_BUILD_ROOT%{_libdir}/vmware/bin
cp -a	lib/lib/* $RPM_BUILD_ROOT%{_libdir}/vmware/lib
cp -a	lib/libconf $RPM_BUILD_ROOT%{_libdir}/vmware
%else
install lib/bin/vmplayer $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}/vmware/lib/lib{crypto,ssl}.so.0.9.7
ln -s %{_libdir}/libcrypto.so.0.9.7 $RPM_BUILD_ROOT%{_libdir}/vmware/lib/libcrypto.so.0.9.7/libcrypto.so.0.9.7
ln -s %{_libdir}/libssl.so.0.9.7 $RPM_BUILD_ROOT%{_libdir}/vmware/lib/libssl.so.0.9.7/libssl.so.0.9.7
%endif

# remove not needed files
rm -rf $RPM_BUILD_ROOT%{_bindir}/vmware-{config,uninstall}.pl $RPM_BUILD_ROOT%{_iconsdir}/hicolor/index.theme
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%if %{with internal_libs}
gdk-pixbuf-query-loaders %{_libdir}/vmware/libconf/lib/gtk-2.0/2.10.0/loaders/*.so \
	> %{_libdir}/vmware/libconf/etc/gtk-2.0/gdk-pixbuf.loaders
gtk-query-immodules-2.0 %{_libdir}/vmware/libconf/lib/gtk-2.0/2.10.0/immodules/*.so \
	> %{_libdir}/vmware/libconf/etc/gtk-2.0/gtk.immodules
pango-querymodules %{_libdir}/vmware/libconf/lib/pango/1.5.0/modules/*.so \
	> %{_libdir}/vmware/libconf/etc/pango/pango.modules
%endif

%postun
%update_icon_cache hicolor

%post networking
/sbin/chkconfig --add vmnet
%service vmnet restart "VMware networking service"

%preun networking
if [ "$1" = "0" ]; then
	%service vmnet stop
	/sbin/chkconfig --del vmnet
fi

%post	-n kernel%{_alt_kernel}-misc-vmmon
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmmon
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vmnet
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmnet
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc doc/* lib/configurator/vmnet-{dhcpd,nat}.conf
%dir %{_sysconfdir}/vmware
%{_sysconfdir}/vmware/locations
%attr(755,root,root) %{_bindir}/vmplayer
%attr(755,root,root) %{_bindir}/vmware-acetool
%attr(755,root,root) %{_bindir}/vm-support
%attr(755,root,root) %{_libdir}/libvmwarebase.so.*
%attr(755,root,root) %{_libdir}/libvmwareui.so.*
%dir %{_libdir}/vmware
%dir %{_libdir}/vmware/bin
# warning: SUID !!!
%attr(4755,root,root) %{_libdir}/vmware/bin/vmware-vmx
%dir %{_libdir}/vmware/lib
%{_libdir}/vmware/config
%if %{with internal_libs}
%attr(755,root,root) %{_libdir}/vmware/bin/vmplayer
%attr(755,root,root) %{_libdir}/vmware/lib/lib*
%attr(755,root,root) %{_libdir}/vmware/lib/wrapper-gtk24.sh

%dir %{_libdir}/vmware/libconf
%dir %{_libdir}/vmware/libconf/etc
%{_libdir}/vmware/libconf/etc/fonts
%{_libdir}/vmware/libconf/etc/gtk-2.0
%{_libdir}/vmware/libconf/etc/pango
%dir %{_libdir}/vmware/libconf/lib
%dir %{_libdir}/vmware/libconf/lib/gtk-2.0
%dir %{_libdir}/vmware/libconf/lib/gtk-2.0/2.10.0
%dir %{_libdir}/vmware/libconf/lib/gtk-2.0/2.10.0/engines
%attr(755,root,root) %{_libdir}/vmware/libconf/lib/gtk-2.0/2.10.0/engines/*.so
%dir %{_libdir}/vmware/libconf/lib/gtk-2.0/2.10.0/immodules
%attr(755,root,root) %{_libdir}/vmware/libconf/lib/gtk-2.0/2.10.0/immodules/*.so
%dir %{_libdir}/vmware/libconf/lib/gtk-2.0/2.10.0/loaders
%attr(755,root,root) %{_libdir}/vmware/libconf/lib/gtk-2.0/2.10.0/loaders/*.so
%dir %{_libdir}/vmware/libconf/lib/pango
%dir %{_libdir}/vmware/libconf/lib/pango/1.5.0
%dir %{_libdir}/vmware/libconf/lib/pango/1.5.0/modules
%attr(755,root,root) %{_libdir}/vmware/libconf/lib/pango/1.5.0/modules/*.so
%else
# package old openssl (buggy but needed to work)
%dir %{_libdir}/vmware/lib/libcrypto.so.0.9.7
%attr(755,root,root) %{_libdir}/vmware/lib/libcrypto.so.0.9.7/libcrypto.so.0.9.7
%dir %{_libdir}/vmware/lib/libssl.so.0.9.7
%attr(755,root,root) %{_libdir}/vmware/lib/libssl.so.0.9.7/libssl.so.0.9.7
%endif
%dir %{_libdir}/vmware/messages
%lang(en) %{_libdir}/vmware/messages/en
%lang(ja) %{_libdir}/vmware/messages/ja
%{_libdir}/vmware/share
%{_libdir}/vmware/xkeymap
%attr(1777,root,root) %dir /var/run/vmware
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_pixmapsdir}/*.png
%{_desktopdir}/%{name}.desktop

%files debug
%defattr(644,root,root,755)
%dir %{_libdir}/vmware/bin-debug
# warning: SUID !!!
%attr(4755,root,root) %{_libdir}/vmware/bin-debug/vmware-vmx

%files help
%defattr(644,root,root,755)
%{_libdir}/vmware/help*

%files networking
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet.conf
%attr(754,root,root) /etc/rc.d/init.d/vmnet
%attr(755,root,root) %{_bindir}/vmnet-bridge
%attr(755,root,root) %{_bindir}/vmnet-detect
%attr(755,root,root) %{_bindir}/vmnet-dhcpd
%attr(755,root,root) %{_bindir}/vmnet-natd
%attr(755,root,root) %{_bindir}/vmnet-netifup
%attr(755,root,root) %{_bindir}/vmnet-sniffer
%attr(755,root,root) %{_bindir}/vmware-ping
%dir %{_sysconfdir}/vmware/vmnet8
%dir %{_sysconfdir}/vmware/vmnet8/dhcpd
%dir %{_sysconfdir}/vmware/vmnet8/nat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/nat/nat.conf
%verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases*

%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-vmmon
%defattr(644,root,root,755)
%{_sysconfdir}/modprobe.d/%{name}-vmmon.conf
/lib/modules/%{_kernel_ver}/misc/vmmon.ko*

%files -n kernel%{_alt_kernel}-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmnet.ko*

%endif
