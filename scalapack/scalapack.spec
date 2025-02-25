%if 0%{?fedora} >= 40
%ifarch %{ix86}
%bcond_with openmpi
%else
%bcond_without openmpi
%endif
%else
%bcond_without openmpi
%endif

# openmpi3 only exists in RHEL7
# and not on ppc ppc64
%if 0%{?rhel} == 7
%ifarch ppc ppc64
  %bcond_with openmpi3
%else
  %bcond_without openmpi3
%endif
%else
  %bcond_with openmpi3
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
%ifarch ppc ppc64 s390 s390x
  # No mpich in RHEL < 7 for these arches
  %bcond_with mpich
%else
  %bcond_without mpich
%endif
%else
  # Enable mpich on RHEL >= 7 and on Fedora
  %bcond_without mpich
%endif

%bcond_without optimized_blas

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global blaslib flexiblas
%if %{with optimized_blas}
%global blasflags -DBLA_VENDOR=FlexiBLAS
%else
%global blasflags -DBLA_VENDOR=Generic
%endif
%else
%global blaslib openblas
%if %{with optimized_blas}
%global blasflags -DLAPACK_LIBRARIES=-l%{blaslib} -DBLAS_LIBRARIES=-l%{blaslib}
%else
%global blasflags -DLAPACK_LIBRARIES=-llapack -DBLAS_LIBRARIES=-lblas
%endif
%endif

Summary: A subset of LAPACK routines redesigned for heterogeneous computing
Name: scalapack
Version: 2.2.0
Release: 11%{?dist}
License: BSD-3-Clause-Open-MPI
URL: http://www.netlib.org/scalapack/
Source0: https://github.com/Reference-ScaLAPACK/scalapack/archive/v%{version}.tar.gz
BuildRequires: cmake
%if %{with optimized_blas}
BuildRequires: %{blaslib}-devel
%else
BuildRequires: lapack-devel
BuildRequires: blas-devel
%endif
BuildRequires: gcc-gfortran, glibc-devel
%if %{with mpich}
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires: mpich-devel
%else
BuildRequires: mpich-devel-static
%endif
%endif
%if %{with openmpi}
BuildRequires: openmpi-devel
%endif
%if %{with openmpi3}
BuildRequires: openmpi3-devel
%endif
Patch1: scalapack-2.2-fix-version.patch
Patch2: scalapack-2.2-set-CMAKE_POSITION_INDEPENDENT_CODE.patch
Patch3: scalapack-2.2.0-fix57.patch

%description
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for inter-processor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all inter-processor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

%package common
Summary: Common files for scalapack
# The blacs symbols live in libscalapack
Provides: blacs-common = %{version}-%{release}
Obsoletes: blacs-common <= 2.0.2

%description common
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for inter-processor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all inter-processor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains common files which are not specific
to any MPI implementation.

%if %{with mpich}

%package mpich
Summary: ScaLAPACK libraries compiled against mpich
Requires: %{name}-common = %{version}-%{release}
Requires: mpich
Provides: %{name}-mpich2 = %{version}-%{release}
Obsoletes: %{name}-mpich2 < 1.7.5-19
# This is a lie, but something needs to obsolete it.
Provides: %{name}-lam = %{version}-%{release}
Obsoletes: %{name}-lam <= 1.7.5-7
# The blacs symbols live in libscalapack
Provides: blacs-mpich = %{version}-%{release}
Obsoletes: blacs-mpich <= 2.0.2

%description mpich
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for inter-processor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all inter-processor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains ScaLAPACK libraries compiled with mpich.

%package mpich-devel
Summary: Development libraries for ScaLAPACK (mpich)
Requires: %{name}-mpich = %{version}-%{release}
Requires: mpich-devel
Provides: %{name}-lam-devel = %{version}-%{release}
Obsoletes: %{name}-lam-devel <= 1.7.5-7
Provides: %{name}-mpich2-devel = %{version}-%{release}
Obsoletes: %{name}-mpich2-devel < 1.7.5-19
# The blacs symbols live in libscalapack
Provides: blacs-mpich-devel = %{version}-%{release}
Obsoletes: blacs-mpich-devel <= 2.0.2

%description mpich-devel
This package contains development libraries for ScaLAPACK, compiled against mpich.

%package mpich-static
Summary: Static libraries for ScaLAPACK (mpich)
Provides: %{name}-lam-static = %{version}-%{release}
Obsoletes: %{name}-lam-static <= 1.7.5-7
Requires: %{name}-mpich-devel = %{version}-%{release}
Provides: %{name}-mpich2-static = %{version}-%{release}
Obsoletes: %{name}-mpich2-static < 1.7.5-19
# The blacs symbols live in libscalapack
Provides: blacs-mpich-static = %{version}-%{release}
Obsoletes: blacs-mpich-static <= 2.0.2

%description mpich-static
This package contains static libraries for ScaLAPACK, compiled against mpich.

%endif

%if %{with openmpi}
%package openmpi
Summary: ScaLAPACK libraries compiled against openmpi
Requires: %{name}-common = %{version}-%{release}
Requires: openmpi
# The blacs symbols live in libscalapack
Provides: blacs-openmpi = %{version}-%{release}
Obsoletes: blacs-openmpi <= 2.0.2

%description openmpi
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for inter-processor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all inter-processor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains ScaLAPACK libraries compiled with openmpi.

%package openmpi-devel
Summary: Development libraries for ScaLAPACK (openmpi)
Requires: %{name}-openmpi = %{version}-%{release}
Requires: openmpi-devel
# The blacs symbols live in libscalapack
Provides: blacs-openmpi-devel = %{version}-%{release}
Obsoletes: blacs-openmpi-devel <= 2.0.2

%description openmpi-devel
This package contains development libraries for ScaLAPACK, compiled against openmpi.

%package openmpi-static
Summary: Static libraries for ScaLAPACK (openmpi)
Requires: %{name}-openmpi-devel = %{version}-%{release}
# The blacs symbols live in libscalapack
Provides: blacs-openmpi-static = %{version}-%{release}
Obsoletes: blacs-openmpi-static <= 2.0.2

%description openmpi-static
This package contains static libraries for ScaLAPACK, compiled against openmpi.
%endif

%if %{with openmpi3}
%package openmpi3
Summary: ScaLAPACK libraries compiled against openmpi3
Requires: %{name}-common = %{version}-%{release}
Requires: openmpi3
# The blacs symbols live in libscalapack
Provides: blacs-openmpi3 = %{version}-%{release}
Obsoletes: blacs-openmpi3 <= 2.0.2

%description openmpi3
The ScaLAPACK (or Scalable LAPACK) library includes a subset
of LAPACK routines redesigned for distributed memory MIMD
parallel computers. It is currently written in a
Single-Program-Multiple-Data style using explicit message
passing for inter-processor communication. It assumes
matrices are laid out in a two-dimensional block cyclic
decomposition.

ScaLAPACK is designed for heterogeneous computing and is
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on
block-partitioned algorithms in order to minimize the frequency
of data movement between different levels of the memory hierarchy.
(For such machines, the memory hierarchy includes the off-processor
memory of other processors, in addition to the hierarchy of registers,
cache, and local memory on each processor.) The fundamental building
blocks of the ScaLAPACK library are distributed memory versions (PBLAS)
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra
Communication Subprograms (BLACS) for communication tasks that arise
frequently in parallel linear algebra computations. In the ScaLAPACK
routines, all inter-processor communication occurs within the PBLAS and the
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK
routines resemble their LAPACK equivalents as much as possible.

This package contains ScaLAPACK libraries compiled with openmpi3.

%package openmpi3-devel
Summary: Development libraries for ScaLAPACK (openmpi3)
Requires: %{name}-openmpi3 = %{version}-%{release}
Requires: openmpi3-devel
# The blacs symbols live in libscalapack
Provides: blacs-openmpi3-devel = %{version}-%{release}
Obsoletes: blacs-openmpi3-devel <= 2.0.2

%description openmpi3-devel
This package contains development libraries for ScaLAPACK, compiled against openmpi3.

%package openmpi3-static
Summary: Static libraries for ScaLAPACK (openmpi3)
Requires: %{name}-openmpi3-devel = %{version}-%{release}
# The blacs symbols live in libscalapack
Provides: blacs-openmpi3-static = %{version}-%{release}
Obsoletes: blacs-openmpi3-static <= 2.0.2

%description openmpi3-static
This package contains static libraries for ScaLAPACK, compiled against openmpi3.
%endif

%prep
%setup -q -c -n %{name}-%{version}
%patch -P1 -p1 -b .version
%patch -P2 -p1 -b .picfix
%patch -P3 -p1 -b .fix57

for i in %{?with_mpich:mpich} %{?with_openmpi:openmpi} %{?with_openmpi3:openmpi3}; do
  cp -a %{name}-%{version} %{name}-%{version}-$i
done

%build
%global build_type_safety_c 0
CC="$CC -std=gnu89"
%global build_fflags %(echo %build_fflags -fallow-argument-mismatch| sed 's|-Werror=format-security||g')
%global dobuild() \
cd %{name}-%{version}-$MPI_COMPILER_NAME ; \
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF -DBUILD_STATIC_LIBS:BOOL=ON -DMPI_BASE_DIR=%{_libdir}/$MPI_COMPILER_NAME %{blasflags} ; \
%cmake_build ;\
%cmake -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=OFF -DMPI_BASE_DIR=%{_libdir}/$MPI_COMPILER_NAME %{blasflags} ; \
%cmake_build ;\
cd ..

%if %{with mpich}
# Build mpich version
export MPI_COMPILER_NAME=mpich
%{_mpich_load}
%dobuild
%{_mpich_unload}
%endif

%if %{with openmpi}
# Build OpenMPI version
export MPI_COMPILER_NAME=openmpi
%{_openmpi_load}
%dobuild
%{_openmpi_unload}
%endif

%if %{with openmpi3}
# Build OpenMPI3 version
export MPI_COMPILER_NAME=openmpi3
%{_openmpi3_load}
%dobuild
%{_openmpi3_unload}
%endif

%install
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/cmake
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}

for i in %{?with_mpich:mpich} %{?with_openmpi:openmpi} %{?with_openmpi3:openmpi3}; do
  mkdir -p %{buildroot}%{_libdir}/$i/lib/
  pushd %{name}-%{version}-$i
  %cmake_install
  cp -f %{_vpath_builddir}/lib/libscalapack.a %{buildroot}%{_libdir}/$i/lib/
  popd
  mkdir -p %{buildroot}%{_includedir}/$i-%{_arch}/
  # This file is independent of the MPI compiler used, but it is poorly named
  # So we'll put it in %{_includedir}/blacs/
  mkdir -p %{buildroot}%{_includedir}/blacs/
  install -p %{name}-%{version}-$i/BLACS/SRC/Bdef.h %{buildroot}%{_includedir}/blacs/

  for f in *.so*; do
    mv %{buildroot}%{_libdir}/$f %{buildroot}%{_libdir}/$i/lib/
  done
  mv %{buildroot}%{_libdir}/pkgconfig %{buildroot}%{_libdir}/$i/lib/
done

# Copy docs
cd %{name}-%{version}
cp -f README ../

# Fixup .pc files
%if %{with openmpi}
sed -i 's|mpi|ompi|g' %{buildroot}%{_libdir}/openmpi/lib/pkgconfig/scalapack.pc
%endif

%files common
%doc README
%{_includedir}/blacs/
%{_libdir}/cmake/%{name}-%{version}/

%if %{with mpich}
%files mpich
%{_libdir}/mpich/lib/libscalapack.so.*

%files mpich-devel
%{_includedir}/mpich-%{_arch}/
%{_libdir}/mpich/lib/libscalapack.so
%{_libdir}/mpich/lib/pkgconfig/scalapack.pc

%files mpich-static
%{_libdir}/mpich/lib/libscalapack.a
%endif

%if %{with openmpi}
%files openmpi
%{_libdir}/openmpi/lib/libscalapack.so.*

%files openmpi-devel
%{_includedir}/openmpi-%{_arch}/
%{_libdir}/openmpi/lib/libscalapack.so
%{_libdir}/openmpi/lib/pkgconfig/scalapack.pc

%files openmpi-static
%{_libdir}/openmpi/lib/libscalapack.a
%endif

%if %{with openmpi3}
%files openmpi3
%{_libdir}/openmpi3/lib/libscalapack.so.*

%files openmpi3-devel
%{_includedir}/openmpi3-%{_arch}/
%{_libdir}/openmpi3/lib/libscalapack.so
%{_libdir}/openmpi3/lib/pkgconfig/scalapack.pc

%files openmpi3-static
%{_libdir}/openmpi3/lib/libscalapack.a
%endif

%changelog
%autochangelog
