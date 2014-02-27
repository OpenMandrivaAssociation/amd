%define NAME 	AMD
%define major 	2
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Name:		amd
Version:	2.3.1
Release:	3
Epoch:		1
Summary:	Routines for permuting sparse matricies prior to factorization
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.cise.ufl.edu/research/sparse/amd/
Source0:	http://www.cise.ufl.edu/research/sparse/amd/%{NAME}-%{version}.tar.gz
BuildRequires:	suitesparse-common-devel >= 4.0.0

%description
AMD provides a set of routines for permuting sparse matricies prior to
Cholesky factorization (or LU factorization with diagonal pivoting).

%package -n %{libname}
Summary:	Library of routines for permuting sparse matricies prior to factorization
Group:		System/Libraries
%define	oldname	%{mklibname %{name} 2.3.1}
%rename		%{oldname}

%description -n %{libname}
AMD provides a set of routines for permuting sparse matricies prior to
Cholesky factorization (or LU factorization with diagonal pivoting).

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{devname}
Summary:	C routines for permuting sparse matricies prior to factorization
Group:		Development/C
Requires:	suitesparse-common-devel >= 3.0.0
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}amd2-devel < 1:2.3.0

%description -n %{devname}
AMD provides a set of routines for permuting sparse matricies prior to
Cholesky factorization (or LU factorization with diagonal pivoting).

This package contains the files needed to develop applications that 
use %{NAME}.

%prep
%setup -q -c -n %{name}-%{version}
cd %{NAME}
find . -perm 640 | xargs chmod 644
mkdir ../SuiteSparse_config
ln -sf %{_includedir}/suitesparse/SuiteSparse_config.* ../SuiteSparse_config

%build
cd %{NAME}
pushd Lib
    %global optflags %{optflags} -fforce-addr -frename-registers -funroll-loops -Ofast
    %make -f GNUmakefile CC=gcc CFLAGS="%{optflags} -fPIC -I%{_includedir}/suitesparse" INC=
    gcc %{ldflags} -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lm *.o
popd

%install
cd %{NAME}
install -d -m 755 %{buildroot}%{_libdir}
install -d -m 755 %{buildroot}%{_includedir}/suitesparse

for f in Lib/*.so*; do
    install -m 755 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    install -m 644 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    install -m 644 $f %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README.txt Doc/*.txt Doc/*.pdf Doc/ChangeLog Doc/License %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%attr(755,root,root) %{_libdir}/lib%{name}.so.%{major}

%files -n %{devname}
%{_docdir}/%{name}
%{_includedir}/suitesparse/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a
