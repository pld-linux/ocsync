Summary:	A user level bidirectional client only file synchronizer (owncloud version)
Name:		ocsync
Version:	0.80.0
Release:	0.1
License:	GPL v2
Group:		Developer/Libraries
Source0:	http://download.owncloud.com/download/%{name}-%{version}.tar.bz2
# Source0-md5:	db46cdb4c710a607dfc062ed0a413b35
URL:		http://www.csync.org
BuildRequires:	cmake
BuildRequires:	check
BuildRequires:	doxygen
BuildRequires:	gcc-c++
BuildRequires:	iniparser-devel
BuildRequires:	neon-devel
BuildRequires:	sqlite3-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ocsync is the ownCloud version of csync. csync is an implementation of 
a file synchronizer which provides the feature of roaming home directories 
for Linux clients.

%package owncloud
Summary:	Plugin files for using ownCloud backend with libraries %{name}
Group:		Developer/Libraries
Requires:	%{name} = %{version}

%description owncloud
ocsync is a csync version which is temporarily maintained by the ownCloud
community to support the ownCloud client. csync is an implementation of a 
file synchronizer which provides the feature of roaming home directories 
for Linux clients. csync makes use of libsmbclient in Samba/Windows environments.

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

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING INSTALL README
%config(noreplace) %{_sysconfdir}/ocsync/ocsync.conf
%config(noreplace) %{_sysconfdir}/ocsync/ocsync_exclude.conf
%attr(755,root,root) %{_bindir}/ocsync
%dir %{_sysconfdir}/ocsync
%{_libdir}/libocsync.so.*
%dir %{_libdir}/ocsync-0
%{_mandir}/man1/ocsync.1.gz

%files owncloud
%defattr(644,root,root,755)
%{_libdir}/ocsync-0/ocsync_owncloud.so
%{_libdir}/libhttpbflib.a
