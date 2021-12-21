%bcond_without pzstd

Name:            zstd
Version:         1.5.0
Release:	 1
Summary:         A fast lossless compression algorithm
License:         BSD and GPLv2
URL:             https://github.com/facebook/zstd
Source0:         https://github.com/facebook/zstd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:   gtest-devel gcc-c++ pkg-config

Provides:        libzstd
Obsoletes:       libzstd

%description
Zstd is a fast lossless compression algorithm. It's backed by a very fast entropy stage,
provided by Huff0 and FSE library. It's a real-time compression scenario for zlib levels
and has a better compression ratio.

%package         devel
Summary:         Header files for zstd library
Requires:        %{name} = %{version}-%{release}
Provides:        libzstd-devel
Obsoletes:       libzstd-devel

%description     devel
This package contains the header files for zstd library.

%package         help
Summary:         Help documentation related to zstd
BuildArch:       noarch

%description     help
This package includes help documentation and manuals related to zstd.

%prep
%autosetup -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"
for dir in lib programs; do
  %make_build -C "$dir"
done
%if %{with pzstd}
%make_build -C contrib/pzstd CXXFLAGS="$RPM_OPT_FLAGS -std=c++11"
%endif

%check
%ifarch %{arm}
make -C tests test-zstd
%endif
%if %{with pzstd}
make -C contrib/pzstd test CXXFLAGS="$RPM_OPT_FLAGS -std=c++11"
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
%if %{with pzstd}
install -D -m755 contrib/pzstd/pzstd %{buildroot}%{_bindir}/pzstd
install -D -m644 programs/zstd.1 %{buildroot}%{_mandir}/man1/pzstd.1
%endif

%files
%doc CHANGELOG README.md
%license LICENSE COPYING
%{_bindir}/*

%{_libdir}/libzstd.so.*

%exclude %{_bindir}/%{name}less
%exclude %{_bindir}/%{name}grep
%exclude %{_libdir}/libzstd.a

%files devel
%{_includedir}/*.h

%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so

%files help
%{_mandir}/man1/*.1*

%changelog
* Tue Dec 21 2021 shixuantong <shixuantong@huawei.com> - 1.5.0-1
- update version to 1.5.0

* Tue Mar 16 2021 shixuantong <shixuantong@huawei.com> - 1.4.8-2
- fix CVE-2021-24032

* Thu Jan 28 2021 liudabo <liudabo1@huawei.com> - 1.4.8-1
- upgrade version to 1.4.8 

* Sat Jun 20 2020 maqiang<maqiang42@huawei.com> -1.4.5
- Type:Update 
- ID:
- SUG:NA
- DESC:Update to version 1.4.5

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.3.6-3
- Delete useless files.

* Sun Sep 15 2019 dongjian <dongjian13@huawei.com> - 1.3.6-2
- Modification summary
