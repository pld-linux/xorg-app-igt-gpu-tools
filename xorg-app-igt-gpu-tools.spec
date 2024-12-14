Summary:	Tools for Intel DRM driver
Summary(pl.UTF-8):	Narzędzia do sterownika Intel DRM
Name:		xorg-app-igt-gpu-tools
Version:	1.30
Release:	1
License:	MIT
Group:		X11/Applications
Source0:	https://xorg.freedesktop.org/archive/individual/app/igt-gpu-tools-%{version}.tar.xz
# Source0-md5:	10706e68a57f464408d309ae74bec5e2
URL:		http://intellinuxgraphics.org/
BuildRequires:	alsa-lib-devel
BuildRequires:	bison
BuildRequires:	cairo-devel >= 1.17.2
BuildRequires:	curl-devel
# rst2man
BuildRequires:	docutils
# libdw
BuildRequires:	elfutils-devel
BuildRequires:	flex
# -std=gnu11
BuildRequires:	gcc >= 6:4.7
BuildRequires:	glib2-devel >= 2.0
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	gsl-devel
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	json-c-devel
BuildRequires:	kmod-devel
BuildRequires:	libdrm-devel >= 2.4.92
BuildRequires:	libunwind-devel
BuildRequires:	meson >= 0.47.2
BuildRequires:	ninja >= 1.5
BuildRequires:	peg
BuildRequires:	pixman-devel >= 0.36.0
BuildRequires:	pkgconfig
BuildRequires:	procps-devel >= 1:3.3
BuildRequires:	python3-devel >= 1:3.0
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xmlrpc-c-client-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libpciaccess-devel >= 0.10
BuildRequires:	xorg-proto-dri2proto-devel >= 2.6
BuildRequires:	xorg-util-util-macros >= 1.16
BuildRequires:	xz
Requires:	cairo >= 1.17.2
Requires:	libdrm >= 2.4.92
Requires:	xorg-lib-libXrandr >= 1.3
Requires:	xorg-lib-libpciaccess >= 0.10
Obsoletes:	xorg-app-intel-gpu-tools < 1.23
# libunwind is required
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64 hppa ia64 mips ppc ppc64 sh tilegx
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# igt_ioctl symbol is function pointer, not plain function
%define		skip_post_check_so	libxe_oa.so.*

%description
This is a collection of tools for development and testing of the Intel
DRM driver.

%description -l pl.UTF-8
Ten pakiet zawiera zestaw narzędzi do rozwijania i testowania
sterownika Intel DRM.

%package devel
Summary:	Header files for i915 perf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki i915 perf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libdrm-devel >= 2.4.92

%description devel
Header files for i915 perf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki i915 perf.

%prep
%setup -q -n igt-gpu-tools-%{version}

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' tools/intel-gfx-fw-info

%build
%meson build \
	-Dchamelium=enabled

%ninja_build -C build

# install fails without prebuilt docs
%ninja_build -C build igt-gpu-tools-doc

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# tests
%{__rm} \
	$RPM_BUILD_ROOT%{_bindir}/code_cov_* \
	$RPM_BUILD_ROOT%{_datadir}/igt-gpu-tools/{README,*.testlist}
%{__rm} -r $RPM_BUILD_ROOT%{_libexecdir}/igt-gpu-tools

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING MAINTAINERS NEWS README.md
%attr(755,root,root) %{_bindir}/amd_hdmi_compliance
%attr(755,root,root) %{_bindir}/dpcd_reg
%attr(755,root,root) %{_bindir}/gputop
%attr(755,root,root) %{_bindir}/i915-perf-*
%attr(755,root,root) %{_bindir}/igt_comms_decoder
%attr(755,root,root) %{_bindir}/igt_results
%attr(755,root,root) %{_bindir}/igt_resume
%attr(755,root,root) %{_bindir}/igt_runner
%attr(755,root,root) %{_bindir}/igt_stats
%attr(755,root,root) %{_bindir}/intel-gfx-fw-info
%attr(755,root,root) %{_bindir}/intel_*
%attr(755,root,root) %{_bindir}/lsgpu
%attr(755,root,root) %{_bindir}/power
%attr(755,root,root) %{_bindir}/msm_dp_compliance
%attr(755,root,root) %{_bindir}/xe-perf-*
%attr(755,root,root) %{_libdir}/libi915_perf.so.1.5
%attr(755,root,root) %{_libdir}/libigt.so.0
%attr(755,root,root) %{_libdir}/libxe_oa.so.1.5
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_bindir}/intel-gen4asm
%attr(755,root,root) %{_bindir}/intel-gen4disasm
%attr(755,root,root) %{_bindir}/intel-gpu-overlay
%{_pkgconfigdir}/intel-gen4asm.pc
%endif
%dir %{_datadir}/igt-gpu-tools
%{_datadir}/igt-gpu-tools/registers
%{_datadir}/igt-gpu-tools/blacklist*.txt
%{_datadir}/igt-gpu-tools/*.blocklist.txt
%{_datadir}/igt-gpu-tools/*.png
%{_gtkdocdir}/igt-gpu-tools
%{_mandir}/man1/intel_*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libi915_perf.so
%attr(755,root,root) %{_libdir}/libigt.so
%attr(755,root,root) %{_libdir}/libxe_oa.so
%{_includedir}/i915-perf
%{_includedir}/xe-oa
%{_pkgconfigdir}/i915-perf.pc
%{_pkgconfigdir}/xe-oa.pc
