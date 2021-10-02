#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace utilities
%bcond_with	internal_libs	# internal libs stuff
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		ver		16.1.2
%define		buildid		17966106
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
Source0:	%{download_url}VMware-Player-%{ver}-%{buildid}.x86_64.bundle
# NoSource0-md5:	f50090a394730f20c0ae9c715e56f6ed
NoSource:	0
Patch0:		installer.patch
URL:		https://www.vmware.com/products/workstation-player.html
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	atk
Requires:	cairo
Requires:	cairomm
Requires:	curl-libs >= 7.19.7-2
Requires:	expat
Requires:	fontconfig-libs
Requires:	freetype
Requires:	glib2
Requires:	glibmm
Requires:	gtk+2
Requires:	gtkmm
Requires:	gtkmm-atk
Requires:	libaio
Requires:	libarchive
Requires:	libart_lgpl
Requires:	libgcc
Requires:	libpng
Requires:	librsvg
Requires:	libsexy
Requires:	libsexymm
Requires:	libsigc++
Requires:	libstdc++
Requires:	libview >= 0.5.5-2
Requires:	libxml2
Requires:	openssl >= 0.9.7
Requires:	pango
Requires:	pangomm
Requires:	xorg-lib-libXau
Requires:	xorg-lib-libXcomposite
Requires:	xorg-lib-libXcursor
Requires:	xorg-lib-libXdamage
Requires:	xorg-lib-libXdmcp
Requires:	xorg-lib-libXfixes
Requires:	xorg-lib-libXft
Requires:	xorg-lib-libXinerama
Requires:	xorg-lib-libXrandr
Requires:	xorg-lib-libXrender
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles %{_libdir}/vmware/lib/.*\.so.*
%define		skip_post_check_so	.*%{_libdir}/vmware/lib/.*

%define		debug_package	%{nil}

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
Obsoletes:	VMware-player-samba < 2.0

%description networking
VMware networking utilities.

%description networking -l pl.UTF-8
Narzędzia VMware do obsługi sieci.

%package -n kernel%{_alt_kernel}-misc-vmmon
Summary:	VMware Virtual Machine Monitor kernel module
Summary(pl.UTF-8):	Moduł jądra VMware Virtual Machine Monitor - monitor maszyny wirtualnej
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-vmmon
VMware Virtual Machine Monitor kernel module.

%description -n kernel%{_alt_kernel}-misc-vmmon -l pl.UTF-8
Moduł jądra VMware Virtual Machine Monitor - monitor maszyny
wirtualnej.

%package -n kernel%{_alt_kernel}-misc-vmnet
Summary:	VMware Virtual Networking Driver kernel module
Summary(pl.UTF-8):	Moduł jądra VMware Virtual Networking Driver - sterownik sieciowy maszyny wirtualnej
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-vmnet
VMware Virtual Networking Driver.

%description -n kernel%{_alt_kernel}-misc-vmnet -l pl.UTF-8
Moduł jądra VMware Virtual Networking Driver - sterownik sieciowy
maszyny wirtualnej.

%prep
%setup -qcT

export SOURCE=%{SOURCE0}

# extract installer shell blob
%{__sed} -ne '1,/^exit/{s,$0,$SOURCE,;p}' $SOURCE > install.sh
%{__sed} -i -e "2iSOURCE=$SOURCE" install.sh
%patch0 -p1
chmod a+x install.sh

./install.sh --extract bundles

cd bundles/vmware-vmx/lib/modules
%{__tar} xf source/vmmon.tar
%{__tar} xf source/vmnet.tar
cd -

%build
%if %{with kernel}
cd bundles/vmware-vmx/lib/modules

%build_kernel_modules -C vmmon-only -m vmmon SRCROOT=$PWD VM_KBUILD=yes

%build_kernel_modules -C vmnet-only -m vmnet SRCROOT=$PWD VM_KBUILD=yes

cd ../../../..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m bundles/vmware-vmx/lib/modules/vmmon-only/vmmon -d misc
%install_kernel_modules -m bundles/vmware-vmx/lib/modules/vmnet-only/vmnet -d misc
%endif

%if %{with userspace}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/vmware,%{_prefix}/lib/cups/filter,%{_datadir}/{appdata,mime/packages},%{_desktopdir},%{_pixmapsdir},%{_iconsdir},%{_sysconfdir}/{cups,thnuclnt,vmware}}

install bundles/vmware-network-editor/lib/libvmware-netcfg.so/libvmware-netcfg.so $RPM_BUILD_ROOT%{_libdir}

# TODO: ovftool?

#cp -p bundles/vmware-player/lib/share/pixmaps/*.png $RPM_BUILD_ROOT%{_pixmapsdir}

install bundles/vmware-player-app/bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p bundles/vmware-player-app/etc/cups/* $RPM_BUILD_ROOT%{_sysconfdir}/cups
cp -p bundles/vmware-player-app/extras/.thnumod $RPM_BUILD_ROOT%{_sysconfdir}/thnuclnt
cp -p bundles/vmware-player-app/extras/thnucups $RPM_BUILD_ROOT%{_prefix}/lib/cups/filter
cp -pr bundles/vmware-player-app/lib/* $RPM_BUILD_ROOT%{_libdir}/vmware
cp -pr bundles/vmware-player-app/share/appdata/* $RPM_BUILD_ROOT%{_datadir}/appdata
%{__sed} -e 's,@@BINARY@@,%{_bindir}/vmplayer,' bundles/vmware-player-app/share/applications/vmware-player.desktop >$RPM_BUILD_ROOT%{_desktopdir}/vmware-player.desktop
cp -pr bundles/vmware-player-app/share/icons/hicolor $RPM_BUILD_ROOT%{_iconsdir}
cp -pr bundles/vmware-player-app/share/mime/packages/* $RPM_BUILD_ROOT%{_datadir}/mime/packages
for f in vmplayer vmware-enter-serial vmware-setup-helper licenseTool vmware-{mount,fuseUI,app-control,zenity} ; do
	ln -sf appLoader $RPM_BUILD_ROOT%{_libdir}/vmware/bin/$f
done
ln -s ../%{_lib}/vmware/bin/vmware-mount $RPM_BUILD_ROOT%{_bindir}/vmware-mount
ln -s ../%{_lib}/vmware/bin/vmware-netcfg $RPM_BUILD_ROOT%{_bindir}/vmware-netcfg
ln -s ../%{_lib}/vmware/bin/vmware-fuseUI $RPM_BUILD_ROOT%{_bindir}/vmware-fuseUI
ln -s ../%{_lib}/vmware/bin/appLoader $RPM_BUILD_ROOT%{_bindir}/vmrest

install -D bundles/vmware-player-setup/vmware-config $RPM_BUILD_ROOT%{_libdir}/vmware/setup/vmware-config

install bundles/vmware-usbarbitrator/bin/vmware-usbarbitrator $RPM_BUILD_ROOT%{_libdir}/vmware/bin

install bundles/vmware-vmx/bin/* $RPM_BUILD_ROOT%{_bindir}
install bundles/vmware-vmx/sbin/* $RPM_BUILD_ROOT%{_sbindir}
cp -pr bundles/vmware-vmx/lib/* $RPM_BUILD_ROOT%{_libdir}/vmware
install -d $RPM_BUILD_ROOT%{_libdir}/vmware/{modules,roms}
cp -p bundles/vmware-vmx/extra/modules.xml $RPM_BUILD_ROOT%{_libdir}/vmware/modules
cp -pr bundles/vmware-vmx/roms/* $RPM_BUILD_ROOT%{_libdir}/vmware/roms
for f in vmware-{modonfig,modconfig-console,gksu,vmblock-fuse} ; do
	ln -sf appLoader $RPM_BUILD_ROOT%{_libdir}/vmware/bin/$f
done

%endif

%clean
rm -rf $RPM_BUILD_ROOT

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
# bin/vmware-vmx SUID
# %{_sbindir}/vmware-authd SUID
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-vmmon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmmon.ko*

%files -n kernel%{_alt_kernel}-misc-vmnet
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/vmnet.ko*
%endif
