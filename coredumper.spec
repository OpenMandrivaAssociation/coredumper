%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Generate a core dump of a running program without crashing
Name:		coredumper
Version:	1.2.1
Release:	11
License:	BSD
Group:		System/Libraries
Url:		https://code.google.com/p/google-coredumper/
Source0:	http://google-coredumper.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:		coredumper-libtool_fixes.diff
Patch1:		coredumper-1.2.1-fix-build.diff
Patch2:		coredumper-1.2.1-rosa-buildfix.patch
BuildRequires:	autoconf2.5
BuildRequires:	automake
# gdb is needed by make check
BuildRequires:	gdb

%description
The coredumper library can be compiled into applications to create
core dumps of the running program, without termination. It
supports both single- and multi-threaded core dumps, even if the
kernel doesn't natively support for multi-threaded core files.

#----------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Generate a core dump of a running program without crashing
Group:		System/Libraries

%description -n	%{libname}
The coredumper library can be compiled into applications to create
core dumps of the running program, without termination. It
supports both single- and multi-threaded core dumps, even if the
kernel doesn't natively support for multi-threaded core files.

%files -n %{libname}
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/lib%{name}.so.*

#----------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Generate a core dump of a running program without crashing
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	coredumper-devel = %{EVRD}

%description -n	%{devname}
The coredumper library can be compiled into applications to create
core dumps of the running program, without termination. It
supports both single- and multi-threaded core dumps, even if the
kernel doesn't natively support for multi-threaded core files.

This package contains static and debug libraries and header
files for developing applications that use the coredumper library.

%files -n %{devname}
%doc examples
%{_libdir}/lib%{name}.so
%{_includedir}/google/*
%{_mandir}/man3/*

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0 -b .libtool
%patch1 -p0 -b .tv
%patch2 -p1

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force
aclocal
autoconf --force
automake --add-missing

%serverbuild

export CFLAGS="$CFLAGS -fPIC -DPIC"

%configure2_5x --disable-static

%make CFLAGS="$CFLAGS -fPIC -DPIC"

%install
%makeinstall_std

# cleanup
rm -rf %{buildroot}%{_datadir}/doc

