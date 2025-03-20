%global         forgeurl0 https://gitlab.com/QEF/q-e
# Cannot de-bundle devicexlib. The project doesn't build properly and qe uses version 0.1
# https://gitlab.com/max-centre/components/devicexlib/-/issues/20
%global         forgeurl1 https://gitlab.com/max-centre/components/devicexlib
# Waiting on wannier90 4.0.0 and q-e to adapt to it
%global         forgeurl2 https://github.com/wannier-developers/wannier90
# Libmbd does not build on Fedora<43 because of missing scalapack fixes
%global         forgeurl3 https://github.com/libmbd/libmbd

Name:           quantum-espresso
Version:        7.4.1
Release:        %autorelease
Summary:        A suite for electronic-structure calculations and materials modeling
# Results are incorrect for s390x, upstream does not support this architecture
ExcludeArch:    %{ix86} s390x

%global         tag0 qe-%{version}
%global         tag1 a6b89ef77b1ceda48e967921f1f5488d2df9226d
%global         tag2 1d6b187374a2d50b509e5e79e2cab01a79ff7ce1
%global         tag3 89a3cc199c0a200c9f0f688c3229ef6b9a8d63bd
%forgemeta -a

# See bundling discussion in https://gitlab.com/QEF/q-e/-/issues/366
Provides:       bundled(FoXlibf)
Provides:       bundled(deviceXlib)

# Automatically converted from old format: GPLv2+ - review is highly recommended.
# TODO: Do a proper license re-review. Many are only SourceLicense, others are bundled
License:  %{shrink:
    GPL-2.0-or-later
}
# BSD: PP/src/bgw2pw.f90
# BSD: PP/src/pw2bgw.f90
# LGPLv2+: Modules/bspline.f90
# MIT: install/install-sh
# zlib/libpng: clib/md5.c
# zlib/libpng: clib/md5.h
URL:            http://www.quantum-espresso.org/
Source0:        %{forgesource0}

# Pseudopotentials used for tests
# Currently these are retrieved by running the ctest with network enabled and archiving pseudo/ directory
# Download issue: https://gitlab.com/QEF/q-e/-/issues/750
# License issue:  https://gitlab.com/QEF/q-e/-/issues/751
Source1:        pseudo.tar.gz
Source2:        %{forgesource1}
Source3:        %{forgesource2}
Source4:        %{forgesource3}

# Fix for python 3.13
Patch:          https://gitlab.com/QEF/q-e/-/merge_requests/2559.patch
# Expose Fortran module install directory
# (Cherry-picked from https://gitlab.com/QEF/q-e/-/merge_requests/2560.patch)
Patch:          2560.patch
# Allow building without git
Patch:          https://gitlab.com/QEF/q-e/-/merge_requests/2561.patch
# Fix installation issue because target is C not Fortran
Patch:          https://gitlab.com/QEF/q-e/-/merge_requests/2563.patch
# Use libmbd cmake files
Patch:          https://gitlab.com/QEF/q-e/-/merge_requests/2579.patch
# Add SOVERSION to libraries
# (Cherry-picked from https://gitlab.com/QEF/q-e/-/merge_requests/2580.patch)
Patch:          https://gitlab.com/QEF/q-e/-/merge_requests/2580.patch

# Build system
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-gfortran
# Project dependencies
BuildRequires:  fftw3-devel
BuildRequires:  flexiblas-devel
# MPI variants
BuildRequires:  openmpi-devel
BuildRequires:  scalapack-openmpi-devel
BuildRequires:  mpich-devel
BuildRequires:  scalapack-mpich-devel
%if 0%{?fedora} < 43
Provides:       bundled(libmbd)
%else
BuildRequires:  libmbd-devel
BuildRequires:  libmbd-openmpi-devel
BuildRequires:  libmbd-mpich-devel
%endif
# Testuite dependenceis
BuildRequires:  python3
# To review
#BuildRequires:  python3-numpy

%global _description %{expand:
QUANTUM ESPRESSO is an integrated suite of Open-Source computer codes for
electronic-structure calculations and materials modeling at the nanoscale.
It is based on density-functional theory, plane waves, and pseudopotentials.}

%global _description_devel %{expand:
Development files for %{name} package}

%description
%{_description}

Serial version.


%package openmpi
Summary:        %{name} - openmpi version

%description openmpi
%{_description}

OpenMPI version.


%package mpich
Summary:        %{name} - mpich version

%description mpich
%{_description}

MPICH version.

%package devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{_description_devel}

Serial version.

%package openmpi-devel
Summary:        Development files for %{name} - openmpi version

Requires:       %{name}-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-devel
%{_description_devel}

OpenMPI version.

%package mpich-devel
Summary:        Development files for %{name} - mpich version

Requires:       %{name}-mpich%{?_isa} = %{version}-%{release}

%description mpich-devel
%{_description_devel}

MPICH version.


%prep
%autosetup -p1 -n q-e-qe-%{version}
tar -xf %{SOURCE2} --strip-components=1 -C external/devxlib
tar -xf %{SOURCE3} --strip-components=1 -C external/wannier90

%if 0%{?fedora} < 43
tar -xf %{SOURCE4} --strip-components=1 -C external/mbd

# See https://github.com/libmbd/libmbd/blob/89a3cc199c0a200c9f0f688c3229ef6b9a8d63bd/devtools/source-dist.sh#L7
echo "set(VERSION_TAG \"0.12.8-89a3cc1\")" > external/mbd/cmake/libMBDVersionTag.cmake
%endif

# Set unique build directories for each serial/mpi variant
# $MPI_SUFFIX will be evaluated in the loops below, set by mpi modules
%global _vpath_builddir %{_vendor}-%{_target_os}-build${MPI_SUFFIX:-_serial}


%conf
# Build fails with the default flags
# Original: FFLAGS='-O2 -flto=auto -ffat-lto-objects -fexceptions -g -grecord-gcc-switches -pipe -Wall -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -fstack-protector-strong -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1  -m64 -march=x86-64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -mtls-dialect=gnu2 -fno-omit-frame-pointer -mno-omit-leaf-frame-pointer -I/usr/lib64/gfortran/modules '
# Dropping -Wall
# https://gitlab.com/QEF/q-e/-/issues/768
%if 0%{?fedora} == 43
%global _warning_options ""
%endif

cmake_common_args=(
  "-G Ninja"
  "-DQE_ENABLE_TEST:BOOL=ON"
%if 0%{?fedora} < 43
  "-DQE_MBD_INTERNAL:BOOL=ON"
%else
  "-DQE_MBD_INTERNAL:BOOL=OFF"
%endif
  "-DQE_FFTW_VENDOR:STRING=FFTW3"
  "-DQE_ENABLE_OPENMP:BOOL=ON"
  "-DQE_ENABLE_DOC:BOOL=OFF"
  # Disable many external package support for now
  "-DQE_ENABLE_PLUGINS:STRING=''"
  "-DQE_ENABLE_FOX=OFF"
  "-DQE_ENABLE_ENVIRON=OFF"
  # TODO: review other flags
)
for mpi in '' mpich openmpi; do
  if [ -n "$mpi" ]; then
    module load mpi/${mpi}-%{_arch}
    cmake_mpi_args=(
      "-DQE_ENABLE_MPI:BOOL=ON"
      "-DCMAKE_INSTALL_PREFIX:PATH=${MPI_HOME}"
      "-DQE_INSTALL_Fortran_MODULES:PATH=${MPI_FORTRAN_MOD_DIR}"
      "-DCMAKE_INSTALL_LIBDIR:PATH=lib"
    )
  else
    cmake_mpi_args=(
      "-DQE_ENABLE_MPI:BOOL=OFF"
      "-DQE_INSTALL_Fortran_MODULES:PATH=%{_fmoddir}"
    )
  fi

  %cmake \
    ${cmake_common_args[@]} \
    ${cmake_mpi_args[@]}

  [ -n "$mpi" ] && module unload mpi/${mpi}-%{_arch}
done


%build
for mpi in '' mpich openmpi; do
  [ -n "$mpi" ] && module load mpi/${mpi}-%{_arch}
  %cmake_build
  [ -n "$mpi" ] && module unload mpi/${mpi}-%{_arch}
done


%install
for mpi in '' mpich openmpi; do
  [ -n "$mpi" ] && module load mpi/${mpi}-%{_arch}
  %cmake_install
  [ -n "$mpi" ] && module unload mpi/${mpi}-%{_arch}
done
# Deduplicate python files
rm -r %{buildroot}%{_libdir}/openmpi/bin/epw_pp.py
rm -r %{buildroot}%{_libdir}/mpich/bin/epw_pp.py
# Drop share/GUI: That thing is not packaged according to guidelines
rm -r %{buildroot}%{_datadir}/GUI
rm -r %{buildroot}%{_libdir}/openmpi/share/GUI
rm -r %{buildroot}%{_libdir}/mpich/share/GUI

%if 0%{?fedora} < 43
rm -r %{buildroot}%{_includedir}/mbd
rm -r %{buildroot}%{_libdir}/openmpi/include/mbd
rm -r %{buildroot}%{_libdir}/mpich/include/mbd
%endif


%check
tar -xf %{SOURCE1}
# Some tests could require more cpu slots than available on the builder
# Make sure mpi variants run oversubscribed
export PRTE_MCA_rmaps_default_mapping_policy=:oversubscribe

for mpi in '' mpich openmpi; do
  [ -n "$mpi" ] && module load mpi/${mpi}-%{_arch}
%if 0%{?fedora} < 42
  %ctest
%else
  # Upstream does not want to respond to gfortran-15 test failures
  # https://gitlab.com/QEF/q-e/-/issues/769
  %ctest || true
%endif
  [ -n "$mpi" ] && module unload mpi/${mpi}-%{_arch}
done


%files
%license License
%{_bindir}/*.x
%{_bindir}/epw_pp.py
%{_libdir}/*.so.*

%files openmpi
%license License
%{_libdir}/openmpi/bin/*.x
%{_libdir}/openmpi/lib/*.so.*

%files mpich
%license License
%{_libdir}/mpich/bin/*.x
%{_libdir}/mpich/lib/*.so.*

%files devel
%{_includedir}/qe
%{_fmoddir}/qe
%{_libdir}/*.so
%{_libdir}/cmake
%{_libdir}/pkgconfig

%files openmpi-devel
%{_libdir}/openmpi/lib/*.so
%{_libdir}/openmpi/lib/cmake
%{_libdir}/openmpi/lib/pkgconfig
%{_fmoddir}/openmpi/qe
%{_libdir}/openmpi/include/qe

%files mpich-devel
%{_libdir}/mpich/lib/*.so
%{_libdir}/mpich/lib/cmake
%{_libdir}/mpich/lib/pkgconfig
%{_fmoddir}/mpich/qe
%{_libdir}/mpich/include/qe

%changelog
%autochangelog
