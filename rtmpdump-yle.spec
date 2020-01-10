
%define name	rtmpdump-yle
%define version	1.3.1
%define rel	1

%define build_crypto 0

%bcond_with plf

%if %with plf
%define build_crypto 1
%define distsuffix plf
%endif

%if !%build_crypto
%define notice This version does not contain RTMPE / RTMPS / SWF verification support.
%else
%if %with plf
%define notice This package is in PLF because it contains support for the RTMPE protocol \
which some people may consider to be a DRM protection mechanism.
%else
%define notice %nil
%endif
%endif

Summary:	YLE Areena stream downloader
Name:		%{name}
Version:	%{version}
Release:	%mkrel %rel
URL:		http://users.tkk.fi/~aajanki/rtmpdump-yle/
Source:		http://users.tkk.fi/~aajanki/rtmpdump-yle/%name-%version.tar.gz
Patch0:		rtmpdump-yle-system-json.patch
License:	GPLv2+
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	zlib-devel
%if %build_crypto
BuildRequires:	openssl-devel
%endif
BuildRequires:	libjson-devel

%description
RTMPDump-YLE (also known as yle-dl) is a commandline program for
retrieving video and audio files from Finnish YLE Areena.
RTMPDump-Yle can also handle live radio and TV broadcasts.

You can download files from YLE Areena for private use only.

%notice
RTMPE/RTMPS/SWF-verification is not needed for YLE Areena.

%prep
%setup -q
%autopatch -p1

for file in README* ChangeLog* TODO; do
	iconv -f ISO-8859-15 -t UTF-8 -o $file.new $file
	mv -f $file.new $file
done

%build
# there already is a generic shared librtmp package, thus
# we build the library statically:
%make XCFLAGS="%optflags" LDFLAGS="%ldflags" SHARED=no prefix=%{_prefix} \
%if !%build_crypto
	CRYPTO=
%endif
# empty line

%install
rm -rf %{buildroot}
%makeinstall_std prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir} SHARED=no
rm %{buildroot}%{_libdir}/librtmp.a

# remove stuff that is already in main rtmpdump package
rm %{buildroot}%{_libdir}/pkgconfig/librtmp.pc
rm %{buildroot}%{_includedir}/librtmp/*.h
rm %{buildroot}%{_sbindir}/rtmp{gw,srv,suck}
rm %{buildroot}%{_mandir}/man3/librtmp.3*
rm %{buildroot}%{_mandir}/man8/rtmpgw.8*
rm %{buildroot}%{_mandir}/man1/rtmpdump.1*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.fi README.yle ChangeLog* TODO
%{_bindir}/rtmpdump-yle
%{_bindir}/yle-dl


%changelog
* Fri Nov 26 2010 Jani Välimaa <wally@mandriva.org> 1.3.1-1mdv2011.0
+ Revision: 601579
- new version 1.3.1
- drop upstream applied patch

  + Anssi Hannula <anssi@mandriva.org>
    - fix grammar in description

* Sat Sep 04 2010 Anssi Hannula <anssi@mandriva.org> 1.2.4-1mdv2011.0
+ Revision: 575853
- initial Mandriva release

