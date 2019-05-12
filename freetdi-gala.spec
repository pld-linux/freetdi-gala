# NOTE: "gala" package name was already occupied, so project name prefix was added.
#
# Conditional build:
%bcond_without	tests		# unit tests
#
Summary:	C++ graph implementation
Summary(pl.UTF-8):	Implementacja grafów w C++
Name:		freetdi-gala
# release "0" has some bugs/got some later improvements (conditional stx, DESTDIR support etc.), use post-0 snapshot
%define	gitref	19bcf7614c428f2b27f005d154aa546f96f83c74
%define	snap	20181110
Version:	0
Release:	1.%{snap}.1
License:	GPL v3+
Group:		Libraries
#Source0Download; https://github.com/freetdi/gala/releases
#Source0:	https://github.com/freetdi/gala/archive/%{version}/gala-%{version}.tar.gz
Source0:	https://github.com/freetdi/gala/archive/%{gitref}/gala-%{snap}.tar.gz
# Source0-md5:	0f7fdff6ad63092419919a880f7469d5
Patch0:		gala-int128.patch
Patch1:		gala-boost.patch
URL:		https://github.com/freetdi/gala
%if %{with tests}
BuildRequires:	boost-devel
BuildRequires:	libstdc++-devel >= 6:4.7
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gala is a C++ graph implementation inspired by boost/BGL, but with low
level access. You choose the containers and data types and get full
access - at your own risk.

%description -l pl.UTF-8
gala to implementacja grafów zainspirowana przez boost/EGL, ale z
niskopoziomowym dostępem. Można wybrać dowolne kontenery i typy
danych, mając do nich pełny dostęp - na własną odpowiedzialność.

%package devel
Summary:	C++ graph implementation
Summary(pl.UTF-8):	Implementacja grafów w C++
Group:		Development/Libraries
Requires:	libstdc++-devel >= 6:4.7

%description devel
gala is a C++ graph implementation inspired by boost/BGL, but with low
level access. You choose the containers and data types and get full
access - at your own risk.

%description devel -l pl.UTF-8
gala to implementacja grafów zainspirowana przez boost/EGL, ale z
niskopoziomowym dostępem. Można wybrać dowolne kontenery i typy
danych, mając do nich pełny dostęp - na własną odpowiedzialność.

%prep
%setup -q -n gala-%{gitref}
%patch0 -p1
%patch1 -p1

%build
# not autoconf configure
./configure \
	--prefix=%{_prefix}

%{__make}

%if %{with tests}
%{__make} check \
	CXX="%{__cxx}" \
	LOCAL_CXXFLAGS="%{rpmcxxflags} %{rpmcppflags} -std=gnu++11"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc README TODO
%{_includedir}/gala
%{_examplesdir}/%{name}-%{version}
