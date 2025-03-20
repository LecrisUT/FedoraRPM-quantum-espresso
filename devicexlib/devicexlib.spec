%global         forgeurl https://gitlab.com/max-centre/components/devicexlib

Name:           devicexlib
Version:        0.8.5
Release:        %autorelease
Summary:        Library wrapping device-oriented routines and utilities
URL:      	    https://gitlab.com/max-centre/components/devicexlib
ExcludeArch:    %{ix86}

%global         tag %{version}
%forgemeta -a

Source:         %{forgesource}

# Fix Fortran module build path and allow to install fortran modules
Patch:          https://gitlab.com/max-centre/components/devicexlib/-/merge_requests/15.patch

# TODO: Do a proper license review
License:      %{shrink:
    MIT
}

# Build system
BuildRequires:      cmake
BuildRequires:      ninja-build
BuildRequires:      gcc-gfortran
# Project dependencies
BuildRequires:      flexiblas-devel
BuildRequires:      cmake(rocblas)

%description
deviceXlib, fortran library wrapping device-oriented routines and utilities


%prep
%autosetup -p1 -n devicexlib-%{version}


%conf
%cmake \
    -G Ninja \
    -DDEVXLIB_ENABLE_ACC=OPENACC \
    -DDEVXLIB_ENABLE_GPU_BLAS=ROCBLAS \
    -DCMAKE_INSTALL_MODULEDIR:PATH=%{_fmoddir}


%build
%cmake_build


%install
%cmake_install


%files
%license LICENSE.txt


%changelog
%autochangelog
