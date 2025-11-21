%define debug_package %{nil}
Summary: Implementation of CDMA
Name: libcdma
Version: 1.0
Release: 3
License: MIT
%global libcdma_version 1

Source0: libcdma.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  libummu-devel
Requires: libummu
ExclusiveArch: aarch64

%description
This implementation provides CDMA sending and reception.

%package devel
Summary:  Implementation of CDMA(UB) - Tools and header files for developers

%description devel
This package is required to develop alternate clients for cdma.

The libCDMA driver program is designed to implement the following two
functionalities:

1. Memory verbs, which are one-sided operations including read, write,
and atomic operations.

2. Event verbs, which involve
registering callback functions with the kernel-mode CDMA for post-processing
asynchronous events.

%prep
%setup -q -n cdma

%build
rm -rf build
cmake -S . -B build \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_BUILD_TYPE=Release

cmake --build build --config Release -- -j$(nproc)

%install
cmake --install build --prefix=%{buildroot}/usr

cd %{buildroot}%{_libdir}

cp -a libcdma.so libcdma.so.%{libcdma_version}

ln -sf libcdma.so.%{libcdma_version} libcdma.so

%files
%{_libdir}/libcdma.so.%{libcdma_version}

%files devel
%{_includedir}/cdma_u_lib.h
%{_includedir}/cdma_abi.h
%{_libdir}/libcdma.so*

%changelog
* Fri Nov 21 2025 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0-3
- add cdma_abi.h to devel package

* Mon Nov 17 2025 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0-2
- fix wait cqe and unregister ras

* Thu Nov 6 2025 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0-1
- Support resource creation and destruction in CDMA
  user mode, enabling read and write semantic functions
  for CDMA user mode.
