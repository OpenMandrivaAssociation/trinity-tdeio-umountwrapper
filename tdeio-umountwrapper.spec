#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg tdeio-umountwrapper
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.2
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Progress dialog for safely removing devices in Trinity
Group:		Applications/Utilities
URL:		http://frode.kde.no/misc/tdeio_umountwrapper/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/tdeio/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz
Source1:		media_safelyremove.desktop_tdeio

BuildRequires:  cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

Obsoletes:		trinity-kio-umountwrapper < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-kio-umountwrapper = %{?epoch:%{epoch}:}%{version}-%{release}

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
Wrapper around tdeio_media_mountwrapper.
Provides a progress dialog for Safely Removing of devices in Trinity.


##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
  -DSHARE_INSTALL_PREFIX="%{tde_datadir}" \
  -DLIB_INSTALL_DIR="%{tde_libdir}" \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DWITH_GCC_VISIBILITY=ON \
  \
  -DBUILD_ALL=ON \
  -DBUILD_DOC=ON \
  -DBUILD_TRANSLATIONS=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

%__install -D -m 644 "%{SOURCE1}" %{?buildroot}%{tde_datadir}/apps/konqueror/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper
%__install -D -m 644 "%{SOURCE1}" %{?buildroot}%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper

%find_lang tdeio_umountwrapper


%post
for f in konqueror d3lphin; do
  update-alternatives --install \
    %{tde_datadir}/apps/${f}/servicemenus/media_safelyremove.desktop \
    media_safelyremove.desktop_${f} \
    %{tde_datadir}/apps/${f}/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper \
    20
done


%postun
if [ $1 -eq 0 ]; then
  for f in konqueror d3lphin; do
    update-alternatives --remove \
      media_safelyremove.desktop_${f} \
      %{tde_datadir}/apps/${f}/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper || :
  done
fi


%files -f tdeio_umountwrapper.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.md
%{tde_bindir}/tdeio_umountwrapper
%{tde_datadir}/apps/konqueror/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper
%dir %{tde_datadir}/apps/d3lphin
%dir %{tde_datadir}/apps/d3lphin/servicemenus
%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper

