%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg tdeio-umountwrapper
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.2
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Progress dialog for safely removing devices in Trinity
Group:		Applications/Utilities
URL:		http://frode.kde.no/misc/tdeio_umountwrapper/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/tdeio/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz
Source1:		media_safelyremove.desktop_tdeio

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

Obsoletes:		trinity-kio-umountwrapper < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-kio-umountwrapper = %{?epoch:%{epoch}:}%{version}-%{release}

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)


BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
Wrapper around tdeio_media_mountwrapper.
Provides a progress dialog for Safely Removing of devices in Trinity.


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%__install -D -m 644 "%{SOURCE1}" %{?buildroot}%{tde_prefix}/share/apps/konqueror/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper
%__install -D -m 644 "%{SOURCE1}" %{?buildroot}%{tde_prefix}/share/apps/d3lphin/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper

%find_lang tdeio_umountwrapper


%post
for f in konqueror d3lphin; do
  update-alternatives --install \
    %{tde_prefix}/share/apps/${f}/servicemenus/media_safelyremove.desktop \
    media_safelyremove.desktop_${f} \
    %{tde_prefix}/share/apps/${f}/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper \
    20
done


%postun
if [ $1 -eq 0 ]; then
  for f in konqueror d3lphin; do
    update-alternatives --remove \
      media_safelyremove.desktop_${f} \
      %{tde_prefix}/share/apps/${f}/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper || :
  done
fi


%files -f tdeio_umountwrapper.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.md
%{tde_prefix}/bin/tdeio_umountwrapper
%{tde_prefix}/share/apps/konqueror/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper
%dir %{tde_prefix}/share/apps/d3lphin
%dir %{tde_prefix}/share/apps/d3lphin/servicemenus
%{tde_prefix}/share/apps/d3lphin/servicemenus/media_safelyremove.desktop_tdeio-umountwrapper

