%global sonum 1
# run variances can make the tests fail
# upstream is investigating better test regime
# disable for now
%bcond_with tests

Name:		cminpack
Version:	1.3.11
Release:	1
Summary:	Solver for nonlinear equations and nonlinear least squares problems
License:	Minpack
Group:		System/Libraries
URL:		https://devernay.free.fr/hacks/cminpack
Source0:	https://github.com/devernay/cminpack/archive/v%{version}/%{name}-%{version}.tar.gz

BuildSystem:	cmake
BuildRequires:	cmake
BuildRequires:	flexiblas
BuildRequires:	flexiblas-devel
BuildRequires:	gcc
BuildRequires:	gcc-gfortran

%description
A C/C++ rewrite of the MINPACK software (originally in FORTRAN) for solving
nonlinear equations and nonlinear least squares problems.

cminpack is an has standard (ISO C99) parameters passing, is fully
reentrant, multithread-safe and has a full set of examples and tests.

%package 	devel
Summary:	Header files and libraries for cminpack
Requires:	%{name} = %{version}-%{release}
Requires:	flexiblas-devel

%description	devel
Development headers and libraries required to build a program with cminpack

%prep
%autosetup -p1

%build
#######################################
# Shared Regular Libaries
# Double, Single s, Long-Double ld precision
export CFLAGS="%{optflags}"
%cmake \
	-DSHARED_LIBS=ON \
	-DCMINPACK_PRECISION="all" \
	-DUSE-FPIC=ON \
	-DUSE_BLAS=OFF \
	-DBUILD_EXAMPLES=ON \
	-DBUILD_EXAMPLES_FORTRAN=ON \
	-DCMINPACK_LIB_INSTALL_DIR=%{_lib} \
	-DCMAKE_BUILD_TYPE=none \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

%if %{with tests}
%check
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
%ninja_test -C build
%endif

%files
%{_libdir}/lib%{name}.so.%{version}
%{_libdir}/lib%{name}.so.%{sonum}
%{_libdir}/lib%{name}ld.so.%{version}
%{_libdir}/lib%{name}ld.so.%{sonum}
%{_libdir}/lib%{name}s.so.%{version}
%{_libdir}/lib%{name}s.so.%{sonum}
%doc README.md
%license CopyrightMINPACK.txt

%files	devel
%{_datarootdir}/%{name}
%{_includedir}/%{name}-%{sonum}
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}ld.pc
%{_libdir}/pkgconfig/%{name}s.pc
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}ld.so
%{_libdir}/lib%{name}s.so
%doc docs/*.html
%doc docs/*.txt
