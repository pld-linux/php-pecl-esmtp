# TODO
# - fix build (see %%build)
# - crashes for me:
# # gdb --args php -r 'echo "11\n";'
#[...]
#Program received signal SIGSEGV, Segmentation fault.
#0xb7f4732e in _zval_ptr_dtor () from /usr/lib/libphp_common-5.0.5.so
#(gdb) bt
#0  0xb7f4732e in _zval_ptr_dtor () from /usr/lib/libphp_common-5.0.5.so
#1  0xb7fd7dbb in zm_shutdown_esmtp () from /usr/lib/php/esmtp.so
#2  0xb7f56478 in module_destructor () from /usr/lib/libphp_common-5.0.5.so
#3  0xb7f59268 in zend_hash_clean () from /usr/lib/libphp_common-5.0.5.so
#4  0xb7f5930c in zend_hash_graceful_reverse_destroy () from /usr/lib/libphp_common-5.0.5.so
#5  0xb7f51cd6 in zend_shutdown () from /usr/lib/libphp_common-5.0.5.so
#6  0xb7f1491e in php_module_shutdown () from /usr/lib/libphp_common-5.0.5.so
#7  0x0804acc9 in main ()
#(gdb)
%define		php_name	php%{?php_suffix}
%define		modname	esmtp
%define		status		alpha
Summary:	%{modname} - ESMTP client extension
Summary(pl.UTF-8):	%{modname} - klient ESMTP
Name:		%{php_name}-pecl-%{modname}
Version:	0.3.1
Release:	3.1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	e1db69e1b05efd0bf7f5c7d0b6b3255f
Patch0:		php-pecl-%{modname}-pthreads.patch
Patch1:		php-pecl-%{modname}-dlfcn.patch
URL:		http://pecl.php.net/package/esmtp/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	fix-crash
BuildRequires:	libesmtp-devel >= 1.0.3r1
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Obsoletes:	php-pear-%{modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Esmtp is a wrapper for SMTP client library based on the libESMTP
library (http://www.stafford.uklinux.net/libesmtp/). You can use it to
send messages using internal SASL, and external/openssl SSL support.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie esmtp to wrapper dla biblioteki klienckiej SMTP bazowanej
na libESMTP. Może być użyte do wysłania wiadomości z użyciem
wewnętrznego mechanizmu SASL czy za pomocą SSL z użyciem zewnętrznej
biblioteki openssl.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
%patch0 -p1

%build
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
%{__patch} -p1 < %{PATCH1}
%configure
%{__make} \
	CFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS NOTES TODO
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
