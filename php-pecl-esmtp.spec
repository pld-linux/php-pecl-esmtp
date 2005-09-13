%define		_modname	esmtp
%define		_status		alpha
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - ESMTP client extension
Summary(pl):	%{_modname} - klient ESMTP
Name:		php-pecl-%{_modname}
Version:	0.3.1
Release:	2.1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	e1db69e1b05efd0bf7f5c7d0b6b3255f
Patch0:		%{name}-pthreads.patch
Patch1:		%{name}-dlfcn.patch
URL:		http://pecl.php.net/package/esmtp/
BuildRequires:	libesmtp-devel >= 1.0.3r1
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.238
%requires_php_extension
Requires:	%{_sysconfdir}/conf.d
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Esmtp is a wrapper for SMTP client library based on the libESMTP
library (http://www.stafford.uklinux.net/libesmtp/). You can use it to
send messages using internal SASL, and external/openssl SSL support.

In PECL status of this extension is: %{_status}.

%description -l pl
Rozszerzenie esmtp to wrapper dla biblioteki klienckiej SMTP bazowanej
na libESMTP. Mo¿e byæ u¿yte do wys³ania wiadomo¶ci z u¿yciem
wewnêtrznego mechanizmu SASL czy za pomoc± SSL z u¿yciem zewnêtrznej
biblioteki openssl.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
cd %{_modname}-%{version}
%patch0 -p1

%build
cd %{_modname}-%{version}
phpize

# i have no damn clue, how to fix it "properly", but it's causing
# shell syntax error and therefore dlfcn.h header is undetected:
#configure:5021: result: no
#configure:5047: checking dlfcn.h usability
#configure:5060: gcc -c -g -O2 -pthread  conftest.c >&5
#configure:5066: $? = 0
#configure:5070: test -z
#./configure: syntax error: `||' unexpected
#configure:5073: $? = 1
# so, therefore the patch.
patch -p1 < %{PATCH1}
%configure
%{__make} \
	CFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL,NOTES,TODO}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
