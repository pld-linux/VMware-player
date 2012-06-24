# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# without SMP kernel modules
%bcond_without	userspace	# don't build userspace utilities
%bcond_with	kernel24	# build kernel24 modules (disable kernel26)
%bcond_with	internal_libs	# internal libs stuff
%bcond_with	verbose		# verbose build (V=1)
#
%include	/usr/lib/rpm/macros.perl
%if %{with kernel24}
%define         _kernelsrcdir		/usr/src/linux-2.4
%endif

%ifarch %{x8664}
%undefine	with_userspace
%endif
#
%define		_ver	1.0.2
%define		_build	29634
%define		_rel	0.1
%define		_urel	104
%define		_ccver	%(rpm -q --qf "%{VERSION}" gcc)
#
Summary:	VMware player
Summary(pl):	VMware player - wirtualna platforma dla stacji roboczej
Name:		VMware-player
Version:	%{_ver}.%{_build}
Release:	%{_rel}
License:	custom, non-distributable
Group:		Applications/Emulators
Source0:	http://download3.vmware.com/software/vmplayer/%{name}-%{_ver}-%{_build}.tar.gz
# NoSource0-md5:c2b781e450c9c0b51820ca6b428d9773
Source1:	http://knihovny.cvut.cz/ftp/pub/vmware/vmware-any-any-update%{_urel}.tar.gz
# Source1-md5:	8cba16d3f6b3723b43d555a5f7cbf850
Source2:	%{name}.init
Source3:	%{name}-vmnet.conf
Source4:	%{name}.png
Source5:	%{name}.desktop
Source6:	%{name}-nat.conf
Source7:	%{name}-dhcpd.conf
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-run_script.patch
NoSource:	0
URL:		http://www.vmware.com/
BuildRequires:	gcc-c++
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	libgnomecanvasmm
Requires:	libview >= 0.5.5-2
Conflicts:	kernel(vmmon) < %{version}-%{_rel}
Conflicts:	kernel(vmmon) > %{version}-%{_rel}
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles %{_libdir}/vmware/lib/.*\.so.*

%description
VMware Player Virtual Platform is a thin software layer that allows
multiple guest operating systems to run concurrently on a single
standard PC, without repartitioning or rebooting, and without
significant loss of performance.

%description -l pl
VMware Player Virtual Platform to cienka warstwa oprogramowania
pozwalaj�ca na jednoczesne dzia�anie wielu go�cinnych system�w
operacyjnych na jednym zwyk�ym PC, bez repartycjonowania ani
rebootowania, bez znacznej utraty wydajno�ci.

%package debug
Summary:	VMware debug utility
Summary(pl):	Narz�dzie VMware do odpluskwiania
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}

%description debug
VMware debug utility.

%description debug -l pl
Narz�dzie VMware do odpluskwiania.

%package help
Summary:	VMware Player help files
Summary(pl):	Pliki pomocy dla VMware Player
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}
Requires:	mozilla

%description help
VMware Player help files.

%description help -l pl
Pliki pomocy dla VMware Player.

%package networking
Summary:	VMware networking utilities
Summary(pl):	Narz�dzia VMware do obs�ugi sieci
Group:		Applications/Emulators
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Obsoletes:	VMware-Player-samba
Conflicts:	kernel(vmnet) < %{version}-%{_rel}
Conflicts:	kernel(vmnet) > %{version}-%{_rel}

%description networking
VMware networking utilities.

%description networking -l pl
Narz�dzia VMware do obs�ugi sieci.

%package samba
Summary:	VMware SMB utilities
Summary(pl):	Narz�dzia VMware do SMB
Group:		Applications/Emulators
Requires:	%{name} = %{version}-%{release}

%description samba
VMware SMB utilities.

%description samba -l pl
Narz�dzia VMware do SMB.

%package -n kernel%{_alt_kernel}-misc-vmmon
Summary:	Kernel module for VMware Player
Summary(pl):	Modu� j�dra dla VMware Player
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(vmmon) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-misc-vmmon
Kernel modules for VMware Player - vmmon.

%description -n kernel%{_alt_kernel}-misc-vmmon -l pl
Modu�y j�dra dla VMware Player - vmmon.

%package -n kernel%{_alt_kernel}-misc-vmnet
Summary:	Kernel module for VMware Player
Summary(pl):	Modu� j�dra dla VMware Player
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(vmnet) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-misc-vmnet
Kernel modules for VMware Player - vmnet.

%description -n kernel%{_alt_kernel}-misc-vmnet -l pl
Modu�y j�dra dla VMware Player - vmnet.

%package -n kernel%{_alt_kernel}-smp-misc-vmmon
Summary:	SMP kernel module for VMware Player
Summary(pl):	Modu� j�dra SMP dla VMware Player
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel(vmmon) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-smp-misc-vmmon
SMP kernel modules fov VMware Player - vmmon-smp.

%description -n kernel%{_alt_kernel}-smp-misc-vmmon -l pl
Modu�y j�dra SMP dla VMware Player - vmmon-smp.

%package -n kernel%{_alt_kernel}-smp-misc-vmnet
Summary:	SMP kernel module for VMware Player
Summary(pl):	Modu� j�dra SMP dla VMware Player
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel(vmnet) = %{version}-%{_rel}

%description -n kernel%{_alt_kernel}-smp-misc-vmnet
SMP kernel module for VMware Player - vmnet-smp.

%description -n kernel%{_alt_kernel}-smp-misc-vmnet -l pl
Modu�y j�dra SMP dla VMware Player - vmnet-smp.

%package -n kernel24-misc-vmmon
Summary:	Kernel module for VMware Player
Summary(pl):	Modu� j�dra dla VMware Player
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(vmmon) = %{version}-%{_rel}

%description -n kernel24-misc-vmmon
Kernel modules for VMware Player - vmmon.

%description -n kernel24-misc-vmmon -l pl
Modu�y j�dra dla VMware Player - vmmon.

%package -n kernel24-misc-vmnet
Summary:	Kernel module for VMware Player
Summary(pl):	Modu� j�dra dla VMware Player
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(vmnet) = %{version}-%{_rel}

%description -n kernel24-misc-vmnet
Kernel modules for VMware Player - vmnet.

%description -n kernel24-misc-vmnet -l pl
Modu�y j�dra dla VMware Player - vmnet.

%package -n kernel24-smp-misc-vmmon
Summary:	SMP kernel module for VMware Player
Summary(pl):	Modu� j�dra SMP dla VMware Player
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel(vmmon) = %{version}-%{_rel}

%description -n kernel24-smp-misc-vmmon
SMP kernel modules fov VMware Player - vmmon-smp.

%description -n kernel24-smp-misc-vmmon -l pl
Modu�y j�dra SMP dla VMware Player - vmmon-smp.

%package -n kernel24-smp-misc-vmnet
Summary:	SMP kernel module for VMware Player
Summary(pl):	Modu� j�dra SMP dla VMware Player
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel(vmnet) = %{version}-%{_rel}

%description -n kernel24-smp-misc-vmnet
SMP kernel module for VMware Player - vmnet-smp.

%description -n kernel24-smp-misc-vmnet -l pl
Modu�y j�dra SMP dla VMware Player - vmnet-smp.

%prep
%setup -q -n vmware-player-distrib -a1
cd vmware-any-any-update%{_urel}
tar xf vmmon.tar
tar xf vmnet.tar
cp -a vmmon-only{,.clean}
cp -a vmnet-only{,.clean}
sed -e 's/filter x86_64%/filter x86_64% amd64% ia64%/' \
	-i vmnet-only.clean/Makefile.kernel
cd -

%build
sed -i 's:vm_db_answer_LIBDIR:VM_LIBDIR:g;s:vm_db_answer_BINDIR:VM_BINDIR:g' bin/vmplayer

cd vmware-any-any-update%{_urel}
chmod u+w ../lib/bin/vmware-vmx ../lib/bin-debug/vmware-vmx ../bin/vmnet-bridge

%if %{with kernel}
rm -rf built
mkdir built

%if %{without kernel24}
for mod in vmmon vmnet ; do
	for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
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
			VM_CCVER=%{_ccver}
		mv -f $mod.ko ../built/$mod-$cfg.ko
		cd -
	done
done

%else
for mod in vmmon vmnet ; do
	rm -rf $mod-only
	tar xf ../lib/modules/source/$mod.tar
	cd $mod-only
sed -i s/'^HEADER_DIR.*'/'HEADER_DIR = \%{_prefix}\/src\/linux-2.4\/include'/ Makefile
	sed -i s/'^BUILD_DIR.*'/'BUILD_DIR = .'/ Makefile

%if %{with smp}
	%{__make} \
		VM_KBUILD=no VMWARE_VER=VME_V5 \
		M=$PWD O=$PWD CC=%{kgcc} \
		INCLUDES="%{rpmcflags} -I. -D__KERNEL_SMP=1 -D__SMP__ -I%{_kernelsrcdir}/include"
	if [ -e $mod-xxx-* ]; then
		mv -f $mod-xxx-* ../built/$mod-smp.o
	else
		mv -f driver-*/$mod-xxx-* ../built/$mod-smp.o
	fi

	%{__make} VM_KBUILD=no clean
%endif
	%{__make} \
		VM_KBUILD=no VMWARE_VER=VME_V5 \
		M=$PWD O=$PWD CC=%{kgcc} \
		INCLUDES="%{rpmcflags} -I. -I%{_kernelsrcdir}/include"
	if [ -e $mod-xxx-* ]; then
		mv -f $mod-xxx-* ../built/$mod.o
	else
		mv -f driver-*/$mod-xxx-* ../built/$mod.o
	fi

	cd ..
done
%endif # kernel24

%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware \
	$RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/{nat,dhcpd} \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_libdir}/vmware/{bin,share/pixmaps} \
	$RPM_BUILD_ROOT%{_mandir} \
	$RPM_BUILD_ROOT%{_pixmapsdir} \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/var/run/vmware
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

cd vmware-any-any-update%{_urel}

%if %{without kernel24}
install built/vmmon-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vmmon.ko
install built/vmnet-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vmnet.ko
%if %{with smp} && %{with dist_kernel}
install built/vmmon-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/vmmon.ko
install built/vmnet-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/vmnet.ko
%endif

%else
install built/vmmon.o \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vmmon.o
install built/vmnet.o \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/vmnet.o
%if %{with smp} && %{with dist_kernel}
install built/vmmon-smp.o \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/vmmon.o
install built/vmnet-smp.o \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/vmnet.o
%endif

%endif

cd -
%endif

%if %{with userspace}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/vmnet
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/nat/nat.conf
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases
touch $RPM_BUILD_ROOT%{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases~

install lib/share/pixmaps/* $RPM_BUILD_ROOT%{_libdir}/vmware/share/pixmaps
install lib/share/EULA.txt $RPM_BUILD_ROOT%{_libdir}/vmware/share

install bin/*-* $RPM_BUILD_ROOT%{_bindir}
install lib/bin/vmware-vmx $RPM_BUILD_ROOT%{_libdir}/vmware/bin

cp -r	lib/{bin-debug,config,help*,messages,xkeymap} \
	$RPM_BUILD_ROOT%{_libdir}/vmware

cat > $RPM_BUILD_ROOT%{_sysconfdir}/vmware/locations <<EOF
VM_BINDIR=%{_bindir}
VM_LIBDIR=%{_libdir}/vmware
EOF

%if %{with internal_libs}
install bin/vmplayer $RPM_BUILD_ROOT%{_bindir}
install lib/bin/vmplayer $RPM_BUILD_ROOT%{_libdir}/vmware/bin
cp -r	lib/lib $RPM_BUILD_ROOT%{_libdir}/vmware
cp -r	lib/libconf $RPM_BUILD_ROOT%{_libdir}/vmware
%else
install lib/bin/vmplayer $RPM_BUILD_ROOT%{_bindir}
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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

%post	-n kernel%{_alt_kernel}-smp-misc-vmmon
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-misc-vmmon
%depmod %{_kernel_ver}smp

%post	-n kernel%{_alt_kernel}-smp-misc-vmnet
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-misc-vmnet
%depmod %{_kernel_ver}smp

%post	-n kernel24-misc-vmmon
%depmod %{_kernel_ver}

%postun -n kernel24-misc-vmmon
%depmod %{_kernel_ver}

%post	-n kernel24-misc-vmnet
%depmod %{_kernel_ver}

%postun -n kernel24-misc-vmnet
%depmod %{_kernel_ver}

%post	-n kernel24-smp-misc-vmmon
%depmod %{_kernel_ver}smp

%postun -n kernel24-smp-misc-vmmon
%depmod %{_kernel_ver}smp

%post	-n kernel24-smp-misc-vmnet
%depmod %{_kernel_ver}smp

%postun -n kernel24-smp-misc-vmnet
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc doc/* lib/configurator/vmnet-{dhcpd,nat}.conf
%dir %{_sysconfdir}/vmware
%{_sysconfdir}/vmware/locations
%attr(755,root,root) %{_bindir}/vmplayer
%dir %{_libdir}/vmware
%dir %{_libdir}/vmware/bin
# warning: SUID !!!
%attr(4755,root,root) %{_libdir}/vmware/bin/vmware-vmx
%{_libdir}/vmware/config
%if %{with internal_libs}
%attr(755,root,root) %{_libdir}/vmware/bin/vmware
%dir %{_libdir}/vmware/lib
%{_libdir}/vmware/lib/lib*
%attr(755,root,root) %{_libdir}/vmware/lib/wrapper-gtk24.sh
%endif
%dir %{_libdir}/vmware/messages
%lang(ja) %{_libdir}/vmware/messages/ja
%{_libdir}/vmware/share
%{_libdir}/vmware/xkeymap
%attr(1777,root,root) %dir /var/run/vmware
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
%attr(755,root,root) %{_bindir}/vmnet-dhcpd
%attr(755,root,root) %{_bindir}/vmnet-natd
%attr(755,root,root) %{_bindir}/vmnet-netifup
%attr(755,root,root) %{_bindir}/vmnet-sniffer
%attr(755,root,root) %{_bindir}/vmware-ping
%dir %{_sysconfdir}/vmware/vmnet8
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/nat/nat.conf
%verify(not md5 mtime size) %{_sysconfdir}/vmware/vmnet8/dhcpd/dhcpd.leases*

%if 0
%files samba
%defattr(644,root,root,755)
%doc lib/configurator/vmnet-smb.conf
%attr(755,root,root) %{_bindir}/vmware-nmbd
%attr(755,root,root) %{_bindir}/vmware-smbd
%attr(755,root,root) %{_bindir}/vmware-smbpasswd
%attr(755,root,root) %{_bindir}/vmware-smbpasswd.bin
%{_libdir}/vmware/smb
%endif
%endif

%if %{with kernel}
%if %{without kernel24}
%files -n kernel%{_alt_kernel}-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmmon.ko*

%files -n kernel%{_alt_kernel}-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmnet.ko*

%if %{with smp} && %{with dist_kernel}
%files	-n kernel%{_alt_kernel}-smp-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/vmmon.ko*

%files	-n kernel%{_alt_kernel}-smp-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/vmnet.ko*
%endif

%else
%files -n kernel24-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmmon.o*

%files -n kernel24-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmnet.o*

%if %{with smp} && %{with dist_kernel}
%files	-n kernel24-smp-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/vmmon.o*

%files	-n kernel24-smp-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/vmnet.o*
%endif

%endif

%endif
