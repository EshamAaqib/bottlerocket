%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%global version 470.57.02
%global branch 470

# Define the compiler macros
%{!?compiler:%global compiler "gcc"}

# Use the defined compiler macro
%global _gcc_bin %{compiler}

# Set the compiler environment variable
%if "%{compiler}"
%global _cc %{compiler}
%endif

Name:           %{_cross_os}nvidia-fabric-manager
Version:        %{?version}
Release:        1
Summary:        Fabric Manager for NVSwitch based systems

License:        NVIDIA Proprietary
URL:            http://www.nvidia.com
Source0:        https://developer.download.nvidia.com/compute/cuda/redist/fabricmanager/linux-x86_64/fabricmanager-linux-x86_64-470.57.02.tar.gz

%description
Fabric Manager for NVIDIA NVSwitch based systems.

%package -n nvidia-fabric-manager-devel
Summary:        Fabric Manager API headers and associated library
# Normally we would have a dev package depend on its runtime package. However
# FM isn't a normal package. All the libs are in the dev package, and the
# runtime package is actually a service package.

%description -n nvidia-fabric-manager-devel
Fabric Manager API headers and associated library

%prep
%setup -q -n fabricmanager

%build

%install
export DONT_STRIP=1

rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}/
cp -a nv-fabricmanager %{buildroot}%{_bindir}/
cp -a nvswitch-audit %{buildroot}%{_bindir}/

mkdir -p %{buildroot}/usr/lib/systemd/system
cp -a nvidia-fabricmanager.service  %{buildroot}/usr/lib/systemd/system

mkdir -p %{buildroot}/usr/share/nvidia/nvswitch
cp -a *_topology %{buildroot}/usr/share/nvidia/nvswitch
cp -a fabricmanager.cfg %{buildroot}/usr/share/nvidia/nvswitch

mkdir -p %{buildroot}%{_libdir}/
cp libnvfm.so.1 %{buildroot}%{_libdir}/
ln -s libnvfm.so.1 %{buildroot}%{_libdir}/libnvfm.so

mkdir -p %{buildroot}%{_includedir}/
cp nv_fm_agent.h %{buildroot}%{_includedir}/
cp nv_fm_types.h %{buildroot}%{_includedir}/

mkdir -p %{buildroot}/usr/share/doc/nvidia-fabricmanager/
cp -a LICENSE %{buildroot}/usr/share/doc/nvidia-fabricmanager/
cp -a third-party-notices.txt %{buildroot}/usr/share/doc/nvidia-fabricmanager/

%post -n nvidia-fabric-manager-devel -p /sbin/ldconfig

%postun -n nvidia-fabric-manager-devel -p /sbin/ldconfig

%files
%{_bindir}/*
/usr/lib/systemd/system/*
/usr/share/nvidia/nvswitch/*
/usr/share/doc/nvidia-fabricmanager/*

%files -n nvidia-fabric-manager-devel
%{_libdir}/*
%{_includedir}/*
