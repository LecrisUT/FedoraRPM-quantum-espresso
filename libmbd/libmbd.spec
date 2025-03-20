# Python bindings needs more work
%bcond python 0
%global         forgeurl https://github.com/libmbd/libmbd

Name:           libmbd
Version:        0.13.0
Release:        %autorelease
Summary:        Many-body dispersion library
URL:      	    https://github.com/libmbd/libmbd
ExcludeArch:    %{ix86}

%global         tag %{version}
%forgemeta -a

Source:         %{forgesource0}

# Expose Fotran install module dir
Patch:          https://github.com/libmbd/libmbd/pull/73.patch

# TODO: Do a proper license review
License:      %{shrink:
    MPL-2.0
}

# Build system
BuildRequires:      cmake
BuildRequires:      ninja-build
BuildRequires:      gcc-gfortran
# Project dependencies
BuildRequires:      flexiblas-devel
# MPI variants
BuildRequires:      openmpi-devel
BuildRequires:      scalapack-openmpi-devel
BuildRequires:      mpich-devel
BuildRequires:      scalapack-mpich-devel

%global _description %{expand:
libMBD implements the many-body dispersion (MBD) method in several programming
languages and frameworks}

%description
%{_description}

Serial version.

%package openmpi
Summary:        %{name} - openmpi version

%description openmpi
%{_description}

This package contains the openmpi version.

%package mpich
Summary:        %{name} - mpich version

%description mpich
%{_description}

This package contains the mpich version.

%if %{with python}
%package -n python3-pymbd
Summary:        %{name} - python version

%description -n python3-pymbd
%{_description}

This package contains the python package.c
%endif


%prep
%autosetup -p1 -n libmbd-%{version}

# See https://github.com/libmbd/libmbd/blob/89a3cc199c0a200c9f0f688c3229ef6b9a8d63bd/devtools/source-dist.sh#L7
echo "set(VERSION_TAG \"%{version}\")" > cmake/libMBDVersionTag.cmake

# Set unique build directories for each serial/mpi variant
# $MPI_SUFFIX will be evaluated in the loops below, set by mpi modules
%global _vpath_builddir %{_vendor}-%{_target_os}-build${MPI_SUFFIX:-_serial}


%if %{with python}
%generate_buildrequires
export POETRY_DYNAMIC_VERSIONING_BYPASS=%{version}
%pyproject_buildrequires -x mpi,test
%endif


%conf
cmake_common_args=(
  "-G Ninja"
)
for mpi in '' mpich openmpi; do
  if [ -n "$mpi" ]; then
    module load mpi/${mpi}-%{_arch}
    cmake_mpi_args=(
      "-DENABLE_SCALAPACK_MPI:BOOL=ON"
      "-DCMAKE_INSTALL_PREFIX:PATH=${MPI_HOME}"
      "-DCMAKE_INSTALL_MODULEDIR:PATH=${MPI_FORTRAN_MOD_DIR}"
      "-DCMAKE_INSTALL_LIBDIR:PATH=lib"
      # TODO: Scalapack's CMake files are broken, need to use pkg-config instead
      # https://bugzilla.redhat.com/show_bug.cgi?id=2243083
      "-DCMAKE_DISABLE_FIND_PACKAGE_scalapack=ON"
    )
  else
    cmake_mpi_args=(
      "-DCMAKE_INSTALL_MODULEDIR:PATH=%{_fmoddir}"
      "-DENABLE_SCALAPACK_MPI:BOOL=OFF"
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
%if %{with python}
export POETRY_DYNAMIC_VERSIONING_BYPASS=%{version}
%pyproject_wheel
%endif


%install
for mpi in '' mpich openmpi; do
  [ -n "$mpi" ] && module load mpi/${mpi}-%{_arch}
  %cmake_install
  [ -n "$mpi" ] && module unload mpi/${mpi}-%{_arch}
done
%if %{with python}
%pyproject_install
%pyproject_save_files -l pymbd
%endif


%check
for mpi in '' mpich openmpi; do
  [ -n "$mpi" ] && module load mpi/${mpi}-%{_arch}
  %ctest
  [ -n "$mpi" ] && module unload mpi/${mpi}-%{_arch}
done
%if %{with python}
%pytest
%endif


%files
%license LICENSE

%files openmpi
%license LICENSE

%files mpich
%license LICENSE

%if %{with python}
%files -n python3-pymbd -f %{pyproject_files}
%endif


%changelog
%autochangelog
