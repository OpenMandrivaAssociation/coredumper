%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Generate a core dump of a running program without crashing
Name:		coredumper
Version:	1.2.1
Release:	9
License:	BSD
Group:		System/Libraries
URL:		http://code.google.com/p/google-coredumper/
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
Provides:	coredumper-devel = %{EVRD}

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
%patch2 -p1

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal; autoconf --force; automake

%serverbuild

export CFLAGS="$CFLAGS -fPIC -DPIC"

%configure2_5x --disable-static

%make CFLAGS="$CFLAGS -fPIC -DPIC"

#%%check
#make check

%install
%makeinstall_std

# cleanup
rm -rf %{buildroot}%{_datadir}/doc

%files -n %{libname}
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/lib*.so.*

%files -n %{develname}
%doc examples
%{_libdir}/lib*.so
%{_includedir}/google/*
%{_mandir}/man3/*


%changelog
* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-8mdv2011.0
+ Revision: 627771
- don't force the usage of automake1.7

* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-7mdv2011.0
+ Revision: 617417
- the mass rebuild of 2010.0 packages

* Sun Oct 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-6mdv2010.0
+ Revision: 453536
- disable make check for now
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - patch 1: fix build
    - rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.2.1-4mdv2009.0
+ Revision: 266538
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon May 12 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-3mdv2009.0
+ Revision: 206218
- don't obsolete itself... (duh!)

* Mon May 12 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-2mdv2009.0
+ Revision: 206194
- rebuild

* Sat May 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-1mdv2009.0
+ Revision: 205382
- 1.2.1
- rediffed P0
- fix devel package naming

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires obsoletes buildprereq

* Mon Apr 23 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1-1mdv2008.0
+ Revision: 17401
- 1.1
- rebuild


* Fri Jul 14 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-2mdv2007.0
- rebuild

* Sun Jun 12 2005 Oden Eriksson <oeriksson@mandriva.com> 0.2-1mdk
- 0.2
- rediff P0

* Sat Mar 19 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.1-3mdk
- make it actually work and run the tests
- use a new P0

* Sat Mar 19 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.1-2mdk
- use the %%mkrel macro
- do not own the %%{_includedir}/google directory

* Fri Mar 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.1-1mdk
- initial package
- used bits of the provided spec file
- added P0 (shlib-with-non-pic-code)

