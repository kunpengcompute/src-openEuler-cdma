Summary: Implementation of CDMA
Name: libcdma
Version: 1.0.4
Release: 3
License: MIT
%global major_version 1

Source0: %{name}-%{version}.tar.gz

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
Requires: %{name}%{?_isa} = %{version}-%{release}

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
%setup -q -n %{name}-%{version}

%build
rm -rf build
cmake -S . -B build \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_INSTALL_LIBDIR=lib64 \
      -DCMAKE_C_FLAGS="%{optflags}" \
      -DCMAKE_CXX_FLAGS="%{optflags}" \
      -DPROJECT_VERSION=%{version} \
      -DLIB_SOVERSION=%{major_version}

cmake --build build

%install
mkdir -p %{buildroot}%{_docdir}/ub/%{name}/
cp -a doc/* %{buildroot}%{_docdir}/ub/%{name}/
install -m 644 README.md %{buildroot}%{_docdir}/ub/%{name}/

cmake --install build --prefix=%{buildroot}/usr

%files
%{_libdir}/libcdma.so.*

%files devel
%{_includedir}/cdma_u_lib.h
%{_includedir}/cdma_abi.h
%{_libdir}/libcdma.so
%doc %{_docdir}/ub/%{name}/*

%changelog
* Wed May 20 2026 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0.4-3
- change source package name

* Mon Apr 27 2026 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0.4-2
- fix cdma code format issue

* Wed Jan 14 2026 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0.1-2
- merge master to Next

* Tue Jan 13 2026 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0.1-1
- cdma debug ability enhance and add some log print
- jfs 64K page table memory adaptation

* Tue Dec 9 2025 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0.1-0
- add version and fix some format and add doc to devel package
- change the compile command and the usage of so

* Fri Nov 21 2025 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0-3
- add cdma_abi.h to devel package

* Mon Nov 17 2025 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0-2
- fix wait cqe and unregister ras

* Thu Nov 6 2025 Zhipeng Lu <luzhipeng8@h-partners.com> - 1.0-1
- Support resource creation and destruction in CDMA
  user mode, enabling read and write semantic functions
  for CDMA user mode.
