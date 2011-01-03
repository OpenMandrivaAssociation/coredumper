%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Generate a core dump of a running program without crashing
Name:		coredumper
Version:	1.2.1
Release:	%mkrel 8
License:	BSD
Group:		System/Libraries
URL:		http://code.google.com/p/google-coredumper/
Source0:	http://google-coredumper.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:		coredumper-libtool_fixes.diff
Patch1:		coredumper-1.2.1-fix-build.diff
BuildRequires:	autoconf2.5
BuildRequires:	automake
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

%package -n	%{develname}
Summary:	Generate a core dump of a running program without crashing
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	coredumper-devel = %{version}
Provides:	libcoredumper-devel = %{version}
Obsoletes:	coredumper-devel
Obsoletes:	%{mklibname coredumper -d 0}

%description -n	%{develname}
The coredumper library can be compiled into applications to create
core dumps of the running program, without termination. It
supports both single- and multi-threaded core dumps, even if the
kernel doesn't natively support for multi-threaded core files.

This package contains static and debug libraries and header
files for developing applications that use the coredumper library.


%prep

%setup -q
%patch0 -p0 -b .libtool
%patch1 -p0 -b .tv

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal; autoconf --force; automake

%serverbuild

export CFLAGS="$CFLAGS -fPIC -DPIC"

%configure2_5x

%make CFLAGS="$CFLAGS -fPIC -DPIC"

#%%check
#make check

%install
rm -rf %{buildroot}

%makeinstall_std

# cleanup
rm -rf %{buildroot}%{_datadir}/doc

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc examples
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_includedir}/google/*
%{_mandir}/man3/*
