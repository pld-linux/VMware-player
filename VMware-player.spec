# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace utilities
%bcond_with	internal_libs	# internal libs stuff
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%ifarch %{x8664}
%undefine	with_userspace
%endif

%define		ver		3.0.0
%define		buildid	203739
%define		rel		0.1

# point to some working url
%define		download_url	%{nil}

Summary:	VMware player
Summary(pl.UTF-8):	VMware player - wirtualna platforma dla stacji roboczej
Name:		VMware-player
Version:	%{ver}.%{buildid}
Release:	%{rel}
License:	custom, non-distributable
Group:		Applications/Emulators
# https://www.vmware.com/go/downloadplayer/
Source0:	%{download_url}VMware-Player-%{ver}-%{buildid}.i386.bundle
# NoSource0-md5:	1c273da70347a381dc685b5fdf922e7d
NoSource:	0
Source1:	%{download_url}VMware-Player-%{ver}-%{buildid}.x86_64.bundle
# NoSource1-md5:	cf8ac6a75e4fd51a8c9c527a594f5ffc
NoSource:	1
Patch0:		installer.patch
URL:		http://www.vmware.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	libgnomecanvasmm
Requires:	libview >= 0.5.5-2
Requires:	openssl >= 0.9.7
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

%package -n kernel%{_alt_kernel}-misc-vmci
Summary:	VMware Virtual Machine Communication Interface (VMCI)
Summary(pl.UTF-8):	VMCI (Virtual Machine Communication Interface) - interfejs komunikacyjny VMware
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-vmci
Linux kernel module acting as VMware Virtual Machine Communication
Interface (VMCI).

%description -n kernel%{_alt_kernel}-misc-vmci -l pl.UTF-8
Moduł jądra Linuksa będący interfejsem komunikacyjnym VMware (VMCI -
Virtual Machine Communication Interface).

%package -n kernel%{_alt_kernel}-misc-vmblock
Summary:	Kernel module for VMware Player
Summary(pl.UTF-8):	Moduł jądra dla VMware Player
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-vmblock
Kernel modules for VMware Player - vmblock.

%description -n kernel%{_alt_kernel}-misc-vmblock -l pl.UTF-8
Moduły jądra dla VMware Player - vmblock.

%package -n kernel%{_alt_kernel}-misc-vmmon
Summary:	Kernel module for VMware Player
Summary(pl.UTF-8):	Moduł jądra dla VMware Player
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-vmmon
Kernel modules for VMware Player - vmmon.

%description -n kernel%{_alt_kernel}-misc-vmmon -l pl.UTF-8
Moduły jądra dla VMware Player - vmmon.

%package -n kernel%{_alt_kernel}-misc-vmnet
Summary:	Kernel module for VMware Player
Summary(pl.UTF-8):	Moduł jądra dla VMware Player
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-vmnet
Kernel modules for VMware Player - vmnet.

%description -n kernel%{_alt_kernel}-misc-vmnet -l pl.UTF-8
Moduły jądra dla VMware Player - vmnet.

%package -n kernel%{_alt_kernel}-misc-vsock
Summary:	VMware Virtual Socket Family support
Summary(pl.UTF-8):	Obsługa Virtual Socket Family - rodziny gniazd wirtualnych VMware
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires:	kernel%{_alt_kernel}-misc-vmci = %{version}-%{rel}@%{_kernel_ver_str}

%description -n kernel%{_alt_kernel}-misc-vsock
Linux kernel module supporting VMware Virtual Socket Family.

%description -n kernel%{_alt_kernel}-misc-vsock -l pl.UTF-8
Moduł jądra Linuksa obsługujący rodzinę gniazd wirtualnych VMware
(Virtual Socket Family).

%prep
%setup -qcT
%ifarch %{ix86}
export SOURCE=%{SOURCE0}
%endif
%ifarch %{x8664}
export SOURCE=%{SOURCE1}
%endif

# extract installer shell blob
%{__sed} -ne '1,/^exit/{s,$0,$SOURCE,;p}' $SOURCE > install.sh
%{__sed} -i -e "2iSOURCE=$SOURCE" install.sh
%patch0 -p1
chmod a+x install.sh

./install.sh --extract bundles

cd bundles/vmware-player-app/lib/modules
%{__tar} xf source/vmblock.tar
%{__tar} xf source/vmci.tar
%{__tar} xf source/vmmon.tar
%{__tar} xf source/vmnet.tar
%{__tar} xf source/vsock.tar
mv vmmon-only/linux/driver.c{,.dist}
mv vmnet-only/hub.c{,.dist}
mv vmnet-only/driver.c{,.dist}
rm -rf binary # unusable
cd -

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%if 0
# build our local install.sh
# grab offsets
%{__sed} -ne "/^### Offsets ###/,/^### End offsets/{s,\$0,\$SOURCE,;p}" blob.sh > install.sh
# grab product name
%{__grep} ^PRODUCT_NAME= blob.sh >> install.sh
# install set_lengths function
%{__sed} -ne "/^set_lengths/,/^}/p" blob.sh >> install.sh
cat <<'EOF' >> install.sh
set_lengths $SOURCE
dd if="$SOURCE" ibs=$LAUNCHER_SIZE obs=1024 skip=1 | tar xz
dd if="$SOURCE" ibs=$SKIP_BYTES obs=1024 skip=1 | tar xz
EOF
sh -x install.sh

sed -e "s,@@VMWARE_INSTALLER@,$(PWD)/install," install/vmware-installer/bootstrap > install/bootstrap
. install/bootstrap
%endif

%build
%if %{with kernel}
cd bundles/vmware-player-app/lib/modules

%build_kernel_modules -C vmblock-only -m vmblock SRCROOT=$PWD VM_KBUILD=26 VM_CCVER=%{cc_version}
%build_kernel_modules -C vmci-only -m vmci SRCROOT=$PWD VM_KBUILD=26 VM_CCVER=%{cc_version}
%build_kernel_modules -C vmmon-only -m vmmon SRCROOT=$PWD VM_KBUILD=26 VM_CCVER=%{cc_version} <<'EOF'
if grep -q "^CONFIG_PREEMPT_RT=y$" o/.config; then
	sed -e '/pollQueueLock/s/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(pollQueueLock)/' \
		-e '/timerLock/s/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(timerLock)/' \
	linux/driver.c.dist > linux/driver.c
else
	cat linux/driver.c.dist > linux/driver.c
fi
EOF

%build_kernel_modules -C vmnet-only -m vmnet SRCROOT=$PWD VM_KBUILD=26 VM_CCVER=%{cc_version} <<'EOF'
if grep -q "^CONFIG_PREEMPT_RT=y$" o/.config; then
	sed -e 's/SPIN_LOCK_UNLOCKED/SPIN_LOCK_UNLOCKED(vnetHubLock)/' \
		 hub.c.dist > hub.c
	sed -e 's/RW_LOCK_UNLOCKED/RW_LOCK_UNLOCKED(vnetPeerLock)/' \
		driver.c.dist > driver.c
else
	cat hub.c.dist > hub.c
	cat driver.c.dist > driver.c
fi
EOF

cp -a vmci-only/Module.symvers vsock-only
%build_kernel_modules -C vsock-only -m vsock SRCROOT=$PWD VM_KBUILD=26 VM_CCVER=%{cc_version} -c
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with kernel}
%install_kernel_modules -m bundles/vmware-player-app/lib/modules/vmblock-only/vmblock -d misc
%install_kernel_modules -m bundles/vmware-player-app/lib/modules/vmci-only/vmci -d misc
%install_kernel_modules -m bundles/vmware-player-app/lib/modules/vmmon-only/vmmon -d misc
%install_kernel_modules -m bundles/vmware-player-app/lib/modules/vmnet-only/vmnet -d misc
%install_kernel_modules -m bundles/vmware-player-app/lib/modules/vsock-only/vsock -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-vmblock
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmblock
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vmci
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmci
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vmmon
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmmon
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vmnet
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vmnet
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-misc-vsock
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-vsock
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-vmblock
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmblock.ko*

%files -n kernel%{_alt_kernel}-misc-vmci
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmci.ko*

%files -n kernel%{_alt_kernel}-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmmon.ko*

%files -n kernel%{_alt_kernel}-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmnet.ko*

%files -n kernel%{_alt_kernel}-misc-vsock
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vsock.ko*
%endif
