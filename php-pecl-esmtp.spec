%define		_modname	esmtp
%define		_status		alpha

Summary:	%{_modname} - ESMTP client extension
Summary(pl):	%{_modname} - klient ESMTP
Name:		php-pecl-%{_modname}
Version:	0.3.1
Release:	2
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	e1db69e1b05efd0bf7f5c7d0b6b3255f
URL:		http://pecl.php.net/package/esmtp/
BuildRequires:	libesmtp-devel >= 1.0.3r1
BuildRequires:	libtool
BuildRequires:	php-devel >= 3:5.0.0
Requires:	php-common >= 3:5.0.0
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
Esmtp is a wrapper for SMTP client library based on the libESMTP library
(http://www.stafford.uklinux.net/libesmtp/). You can use it to send messages
using internal SASL, and external/openssl SSL support.

In PECL status of this extension is: %{_status}.

%description -l pl
Rozszerzenie esmtp to wrapper dla biblioteki klienckiej SMTP bazowanej
na libESMTP. Mo¿e byæ u¿yte do wys³ania wiadomo¶ci z u¿yciem
wewnêtrznego mechanizmu SASL czy za pomoc± SSL z u¿yciem zewnêtrznej
biblioteki openssl.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make} \
	CFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL,NOTES,TODO}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
