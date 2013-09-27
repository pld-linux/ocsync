# TODO:
# * Add subpackage and complile time flags for plugin packages:
#   * smb backend
# * Package documentation
Summary:	A user level bidirectional client only file synchronizer (owncloud version)
Name:		ocsync
Version:	0.90.2
Release:	0.1
License:	GPL v2
Group:		Libraries
Source0:	http://download.owncloud.com/download/%{name}-%{version}.tar.bz2
# Source0-md5:	c2a8a19289e4d7e7e8eebf8304ac39bd
URL:		http://www.csync.org
BuildRequires:	check
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	iniparser-devel
BuildRequires:	libstdc++-devel
BuildRequires:	neon-devel
BuildRequires:	sqlite3-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ocsync is the ownCloud version of csync. csync is an implementation of
a file synchronizer which provides the feature of roaming home
directories for Linux clients.

%package owncloud
Summary:	Plugin files for using ownCloud backend with libraries %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description owncloud
ocsync is a csync version which is temporarily maintained by the
ownCloud community to support the ownCloud client. csync is an
implementation of a file synchronizer which provides the feature of
roaming home directories for Linux clients. csync makes use of
libsmbclient in Samba/Windows environments.

%package devel
Summary:	Development header files and libraries for %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development header files and libraries for %{name}

%prep
%setup -q

%build
if test ! -e "build"; then
	%{__mkdir} build
fi

cd build

%cmake \
	-DCMAKE_C_FLAGS:STRING="%{optflags}" \
	-DCMAKE_CXX_FLAGS:STRING="%{optflags}" \
	-DCMAKE_SKIP_RPATH=ON \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DPREFIX=%{_prefix} \
	-DSYSCONFDIR=%{_sysconfdir} \
	$RPM_BUILD_ROOT/%{name}-%{version} \
	..

%{__make}
%{__make} doc

cd ..

%install
rm -rf $RPM_BUILD_ROOT

cd build

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING INSTALL README
%config(noreplace) %{_sysconfdir}/ocsync/ocsync.conf
%config(noreplace) %{_sysconfdir}/ocsync/ocsync_exclude.conf
%attr(755,root,root) %{_bindir}/ocsync
%dir %{_sysconfdir}/ocsync
%attr(755,root,root) %{_libdir}/libocsync.so.*.*.*
%ghost %{_libdir}/libocsync.so.0
%dir %{_libdir}/ocsync-0
%{_mandir}/man1/ocsync.1*

%files owncloud
%defattr(644,root,root,755)
%{_libdir}/ocsync-0/ocsync_owncloud.so
%{_libdir}/libhttpbflib.a

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libocsync.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
