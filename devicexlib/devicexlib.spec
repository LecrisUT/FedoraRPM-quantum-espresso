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

%description
deviceXlib, fortran library wrapping device-oriented routines and utilities


%prep
%autosetup -p1 -n devicexlib-%{version}


%conf
%cmake \
    -G Ninja


%build
%cmake_build


%install
%cmake_install


%files
%license LICENSE.txt


%changelog
%autochangelog
