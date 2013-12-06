%define NAME 		AMD
%define major 		%{version}
%define libname 	%mklibname %{name} %{major}
%define develname 	%mklibname %{name} -d

Name:		amd
Version:	2.3.1
Release:	2
Epoch:		1
Summary:	Routines for permuting sparse matricies prior to factorization
Group:		System/Libraries
License:	LGPL
URL:		http://www.cise.ufl.edu/research/sparse/amd/
Source0:	http://www.cise.ufl.edu/research/sparse/amd/%{NAME}-%{version}.tar.gz
BuildRequires:	suitesparse-common-devel >= 4.0.0

%description
AMD provides a set of routines for permuting sparse matricies prior to
Cholesky factorization (or LU factorization with diagonal pivoting).

%package -n %{libname}
Summary:	Library of routines for permuting sparse matricies prior to factorization
Group:		System/Libraries
Obsoletes:	%{_lib}amd2 < 1:2.3.0

%description -n %{libname}
AMD provides a set of routines for permuting sparse matricies prior to
Cholesky factorization (or LU factorization with diagonal pivoting).

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{develname}
Summary:	C routines for permuting sparse matricies prior to factorization
Group:		Development/C
Requires:	suitesparse-common-devel >= 3.0.0
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}amd2-devel < 1:2.3.0

%description -n %{develname}
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
    %make -f GNUmakefile CC=%__cc CFLAGS="%{optflags} -fPIC -I%{_includedir}/suitesparse" INC=
    %__cc -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lm *.o
popd

%install
cd %{NAME}
%__install -d -m 755 %{buildroot}%{_libdir}
%__install -d -m 755 %{buildroot}%{_includedir}/suitesparse

for f in Lib/*.so*; do
    %__install -m 755 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    %__install -m 644 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    %__install -m 644 $f %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

%__ln_s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

%__install -d -m 755 %{buildroot}%{_docdir}/%{name}
%__install -m 644 README.txt Doc/*.txt Doc/*.pdf Doc/ChangeLog Doc/License %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%attr(755,root,root) %{_libdir}/*.so.*

%files -n %{develname}
%{_docdir}/%{name}
%{_includedir}/suitesparse/*.h
%{_libdir}/*.so
%{_libdir}/*.a

