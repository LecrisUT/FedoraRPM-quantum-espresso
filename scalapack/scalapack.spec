Summary: A subset of LAPACK routines redesigned for heterogeneous computing
Name: scalapack
Version: 2.2.0
Release: 11%{?dist}
License: BSD-3-Clause-Open-MPI
URL: http://www.netlib.org/scalapack/
Source0: https://github.com/Reference-ScaLAPACK/scalapack/archive/v%{version}.tar.gz
BuildRequires: cmake
BuildRequires: flexiblas-devel
BuildRequires: gcc-gfortran, glibc-devel
BuildRequires: mpich-devel
BuildRequires: openmpi-devel
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


%prep
%autosetup -p1

# Set unique build directories for each serial/mpi variant
# $MPI_SUFFIX will be evaluated in the loops below, set by mpi modules
%global _vpath_builddir %{_vendor}-%{_target_os}-build${MPI_SUFFIX:-_serial}


%conf
cmake_common_args=(
  "-G Ninja"
)
for mpi in mpich openmpi; do
  if [ -n "$mpi" ]; then
    module load mpi/${mpi}-%{_arch}
    cmake_mpi_args=(
      "-DCMAKE_INSTALL_PREFIX:PATH=${MPI_HOME}"
      "-DCMAKE_INSTALL_LIBDIR:PATH=lib"
    )
  fi

  %cmake \
    ${cmake_common_args[@]} \
    ${cmake_mpi_args[@]}

  [ -n "$mpi" ] && module unload mpi/${mpi}-%{_arch}
done


%build
for mpi in mpich openmpi; do
  [ -n "$mpi" ] && module load mpi/${mpi}-%{_arch}
  %cmake_build
  [ -n "$mpi" ] && module unload mpi/${mpi}-%{_arch}
done


%install
for mpi in mpich openmpi; do
  [ -n "$mpi" ] && module load mpi/${mpi}-%{_arch}
  %cmake_install
  [ -n "$mpi" ] && module unload mpi/${mpi}-%{_arch}
done


%check
for mpi in mpich openmpi; do
  [ -n "$mpi" ] && module load mpi/${mpi}-%{_arch}
  %ctest
  [ -n "$mpi" ] && module unload mpi/${mpi}-%{_arch}
done


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
