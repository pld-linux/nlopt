#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

Summary:	Library for nonlinear optimization
Summary(pl.UTF-8):	Biblioteka do nieliniowej optymalizacji
Name:		nlopt
Version:	2.7.1
Release:	0.1
License:	LGPL v2.1, MIT
Group:		Libraries
#Source0Download: https://github.com/stevengj/nlopt/releases
Source0:	https://github.com/stevengj/nlopt/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ed1a3000a1c8c248d51df126dfcfaa78
Patch0:		python.patch
URL:		https://nlopt.readthedocs.io
BuildRequires:	cmake >= 3.2
BuildRequires:	guile
BuildRequires:	libstdc++-devel
BuildRequires:	octave
BuildRequires:	python3-devel
BuildRequires:	swig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NLopt is a free/open-source library for nonlinear optimization,
providing a common interface for a number of different free
optimization routines available online as well as original
implementations of various other algorithms.

%description -l pl.UTF-8
Biblioteka do nieliniowej optymalizacji

%package devel
Summary:	Development files for NLopt
Summary(pl.UTF-8):	Pliki programistyczne biblioteki NLopt
License:	AGPL v3+ and BSD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for NLopt.

%description devel -l pl
Pliki programistyczne biblioteki NLopt.

%package -n python3-nlopt
Summary:	Python 3 bindings for NLopt
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki NLopt
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-nlopt
Python 3 bindings for NLopt

%description -n python3-nlopt -l pl.UTF-8
Wiązania Pythona 3 do biblioteki NLopt

%package -n guile-nlopt
Summary:	Guile bindings for NLopt
Summary(pl.UTF-8):	Wiązania Guile do biblioteki NLopt
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n guile-nlopt
Guile bindings for NLopt

%description -n guile-nlopt -l pl.UTF-8
Wiązania Guile do biblioteki NLopt

%package -n octave-nlopt
Summary:	Octave interface for NLopt
Summary(pl.UTF-8):	Interfejs Octave do biblioteki NLopt
Group:		Applications/Math
Requires:	%{name} = %{version}-%{release}

%description -n octave-nlopt
Octave interface for NLopt

%description -n octave-nlopt -l pl.UTF-8
Interfejs Octave do biblioteki NLopt

%prep
%setup -q
%patch0 -p1

%build
mkdir build
cd build
%cmake .. \
	-DNLOPT_MATLAB=OFF \
	-DNLOPT_TESTS=%{?with_tests:ON}%{?!with_tests:OFF}

%{__make}
%{?with_tests:%{__make} test ARGS=--output-on-failure}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py3_sitedir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYRIGHT NEWS.md README.md TODO
%attr(755,root,root) %{_libdir}/libnlopt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnlopt.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnlopt.so
%{_includedir}/nlopt.h*
%{_libdir}/cmake/nlopt
%{_pkgconfigdir}/nlopt.pc
%{_mandir}/man3/nlopt*.3*

%files -n python3-nlopt
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_nlopt.so
%{py3_sitedir}/nlopt.py

%files -n guile-nlopt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/guile/3.0/extensions/nlopt_guile.so
%{_datadir}/guile/site/3.*/nlopt.scm

%files -n octave-nlopt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/octave/*/site/oct/x86_64-pld-linux-gnu/nlopt_optimize.oct
%{_datadir}/octave/*/site/m/*.m
