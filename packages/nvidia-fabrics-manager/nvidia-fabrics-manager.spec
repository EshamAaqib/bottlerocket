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

%global debug_package %{nil}

%global version 470.57.02
%global branch 470
%global _missing_build_ids_terminate_build 0

Name:           nvidia-fabric-manager
Version:        %{?version}
Release:        1
Summary:        Fabric Manager for NVSwitch based systems

License:        NVIDIA Proprietary
URL:            http://www.nvidia.com
Source0:        fabricmanager-linux-%{_arch}-%{version}.tar.gz

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
%setup -q -n fabricmanager

%build

%install
export DONT_STRIP=1
%define _build_id_links none


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
/usr/share/doc/nvidia-fabricmanager/third-party-notices.txt
/usr/share/doc/nvidia-fabricmanager/LICENSE
/%{_includedir}/nv_fm_agent.h
/%{_includedir}/nv_fm_types.h
/%{_libdir}/libnvfm.so
/usr/share/nvidia/nvswitch/*
/usr/lib/systemd/system/nvidia-fabricmanager.service
/%{_bindir}/nv-fabricmanager
/%{_bindir}/nvswitch-audit


