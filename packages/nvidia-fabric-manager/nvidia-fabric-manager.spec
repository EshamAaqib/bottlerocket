%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%global version 550.54.14
%global branch 550
%global _missing_build_ids_terminate_build 0

Name: %{_cross_os}nvidia-fabric-manager
Version:        %{?version}
Release:        1
Summary:        Fabric Manager for NVSwitch based systems

License: MIT
URL:            http://www.nvidia.com
Source0:        https://developer.download.nvidia.com/compute/nvidia-driver/redist/fabricmanager/linux-x86_64/fabricmanager-linux-x86_64-550.54.14-archive.tar.xz
Source1: nvidia-fabrics-manager.service

Provides:       nvidia-fabricmanager = %{version}
Provides:       nvidia-fabricmanager-%{branch} = %{version}

%description
Fabric Manager for NVIDIA NVSwitch based systems.

%prep
%setup -q -n fabricmanager-linux-x86_64-550.54.14-archive

%build

%install
export DONT_STRIP=1
%define _build_id_links none

rm -rf %{buildroot}

mkdir -p %{buildroot}%{_cross_bindir}/
cp -a bin/nv-fabricmanager %{buildroot}%{_cross_bindir}/
cp -a bin/nvswitch-audit %{buildroot}%{_cross_bindir}/

mkdir -p %{buildroot}/usr/lib/systemd/system
cp -a systemd/nvidia-fabricmanager.service  %{buildroot}/usr/lib/systemd/system

mkdir -p %{buildroot}/usr/share/nvidia/nvswitch
cp -a share/nvidia/nvswitch/*_topology %{buildroot}/usr/share/nvidia/nvswitch
cp -a etc/fabricmanager.cfg %{buildroot}/usr/share/nvidia/nvswitch

mkdir -p %{buildroot}%{_cross_libdir}/
cp lib/libnvfm.so.1 %{buildroot}%{_cross_libdir}/
ln -s lib/libnvfm.so.1 %{buildroot}%{_cross_libdir}/libnvfm.so

mkdir -p %{buildroot}%{_cross_includedir}/
cp include/nv_fm_agent.h %{buildroot}%{_cross_includedir}/
cp include/nv_fm_types.h %{buildroot}%{_cross_includedir}/

%files
%{_cross_bindir}/nv-fabricmanager
%{_cross_bindir}/nvswitch-audit
/usr/lib/systemd/system/nvidia-fabricmanager.service
/usr/share/nvidia/nvswitch/fabricmanager.cfg
/usr/share/nvidia/nvswitch/*_topology
%{_cross_attribution_file}
%{_cross_libdir}/libnvfm.so.1
%{_cross_libdir}/libnvfm.so
%{_cross_includedir}/nv_fm_agent.h
%{_cross_includedir}/nv_fm_types.h
