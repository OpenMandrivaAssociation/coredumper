%define name	coredumper
%define version 0.2

%define major 0
%define libname	%mklibname %{name} %{major}

Summary:	Generate a core dump of a running program without crashing
Name:		%{name}
Version:	%{version}
Release:	%mkrel 2
License:	BSD
Group:		Development/Libraries
Group:		System/Libraries
URL:		http://goog-coredumper.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/goog-coredumper/%{name}-%{version}.tar.bz2
Patch0:		coredumper-0.2-libtool_fixes.diff
BuildPrereq:	autoconf2.5
BuildPrereq:	automake1.7
# gdb is needed by make check
BuildRequires:	gdb
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The coredumper library can be compiled into applications to create
core dumps of the running program, without termination. It
supports both single- and multi-threaded core dumps, even if the
kernel doesn't natively support for multi-threaded core files.

%package -n	%{libname}
Summary:	Generate a core dump of a running program without crashing
Group:		System/Libraries

%description -n	%{libname}
The coredumper library can be compiled into applications to create
core dumps of the running program, without termination. It
supports both single- and multi-threaded core dumps, even if the
kernel doesn't natively support for multi-threaded core files.

%package -n	%{libname}-devel
Summary:	Generate a core dump of a running program without crashing
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	coredumper-devel = %{version}
Provides:	libcoredumper-devel = %{version}
Obsoletes:	coredumper-devel libcoredumper-devel

%description -n	%{libname}-devel
The coredumper library can be compiled into applications to create
core dumps of the running program, without termination. It
supports both single- and multi-threaded core dumps, even if the
kernel doesn't natively support for multi-threaded core files.

This package contains static and debug libraries and header
files for developing applications that use the coredumper library.


%prep

%setup -q
%patch0 -p0 -b .libtool

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force && aclocal-1.7 && autoconf --force && automake-1.7

%serverbuild

export CFLAGS="$CFLAGS -fPIC -DPIC"

%configure2_5x

%make CFLAGS="$CFLAGS -fPIC -DPIC"

make check

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std


# cleanup
rm -rf %{buildroot}%{_prefix}/doc

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc examples
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_includedir}/google/*

