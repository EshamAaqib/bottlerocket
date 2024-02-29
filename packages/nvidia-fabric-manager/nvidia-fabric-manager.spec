# The MIT License (MIT)
# 
# Copyright (c) 2020 NVIDIA Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

License:        NVIDIA Proprietary
URL:            http://www.nvidia.com
Source0:        https://developer.download.nvidia.com/compute/nvidia-driver/redist/fabricmanager/linux-x86_64/fabricmanager-linux-x86_64-550.54.14-archive.tar.xz
Source1: nvidia-fabrics-manager.service

Provides:       nvidia-fabricmanager = %{version}
Provides:       nvidia-fabricmanager-%{branch} = %{version}

%description
Fabric Manager for NVIDIA NVSwitch based systems.

%package -n nvidia-fabric-manager-devel
Summary:        Fabric Manager API headers and associated library
# Normally we would have a dev package depend on its runtime package. However
# FM isn't a normal package. All the libs are in the dev package, and the
# runtime package is actually a service package.
Provides:       nvidia-fabricmanager-devel-%{branch} = %{version}

%description -n nvidia-fabric-manager-devel
Fabric Manager API headers and associated library

%package -n cuda-drivers-fabricmanager-%{branch}
Summary:        Meta-package for FM and Driver
Requires:       nvidia-fabric-manager = %{version}
Requires:       cuda-drivers-%{branch} = %{version}

Conflicts:      cuda-drivers-fabricmanager-%{branch} < %{version}
Conflicts:      cuda-drivers-fabricmanager-branch

%description -n cuda-drivers-fabricmanager-%{branch}
Convience meta-package for installing fabricmanager and the cuda-drivers
meta-package simultaneously while keeping version equivalence. This meta-
package is branch-specific.

%package -n cuda-drivers-fabricmanager
Summary:        Meta-package for FM and Driver
Requires:       cuda-drivers-fabricmanager-%{branch} = %{version}

%description -n cuda-drivers-fabricmanager
Convience meta-package for installing fabricmanager and the cuda-drivers
meta-package simultaneously while keeping version equivalence. This meta-
package is across all driver branches.

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

%post -n nvidia-fabric-manager-devel -p /sbin/ldconfig

%postun -n nvidia-fabric-manager-devel -p /sbin/ldconfig

%files
%{_cross_bindir}/*
/usr/lib/systemd/system/*
/usr/share/nvidia/nvswitch/*
/x86_64-bottlerocket-linux-gnu/sys-root/usr/share/licenses/nvidia-fabric-manager/attribution.txt

%files -n nvidia-fabric-manager-devel
%{_cross_libdir}/*
%{_cross_includedir}/*

%files -n cuda-drivers-fabricmanager-%{branch}

%files -n cuda-drivers-fabricmanager

%changelog
* Fri Jun 18 2021 Kevin Mittman <kmittman@nvidia.com>
- Rename packages

* Fri Jun 29 2018 Shibu Baby <sbaby@nvidia.com>
- Initial Fabric Manager RPM packaging