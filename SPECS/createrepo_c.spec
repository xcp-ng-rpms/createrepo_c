%global package_speccommit 8502528ecf00b68bb415fe98fdbef6cebdc2ae60
%global usver 0.21.1
%global xsver 3
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global libmodulemd_version 2.3.0

%define __cmake_in_source_build 1

%global bash_completion %{_datadir}/bash-completion/completions/*

%bcond_with drpm
%if 0%{?xenserver} < 9
%bcond_with zchunk
%bcond_with libmodulemd
%else
%bcond_without zchunk
%bcond_without libmodulemd
%endif
%bcond_with legacy_hashes

Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        0.21.1
Release:        %{?xsrel}~XCPNG2710.3%{?dist}
License:        GPL-2.0-or-later
URL:            https://github.com/rpm-software-management/createrepo_c
Source0: createrepo_c-0.21.1.tar.gz
Patch0: 0001-src-cmd_parser.c-add-a-missing-parameter-name.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  bzip2-devel
BuildRequires:  file-devel
BuildRequires:  glib2-devel >= 2.22.0
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  rpm-devel >= 4.8.0-28
BuildRequires:  sqlite-devel
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
%if %{with zchunk}
BuildRequires:  pkgconfig(zck) >= 0.9.11
BuildRequires:  zchunk
%endif
%if %{with libmodulemd}
BuildRequires:  pkgconfig(modulemd-2.0) >= %{libmodulemd_version}
BuildRequires:  libmodulemd
Requires:       libmodulemd >= %{libmodulemd_version}
%endif
Requires:       %{name}-libs =  %{version}-%{release}
BuildRequires:  bash-completion
Requires: rpm >= 4.9.0
%if %{with drpm}
BuildRequires:  drpm-devel >= 0.4.0
%endif

Obsoletes:      createrepo < 0.11.0
Provides:       createrepo = %{version}-%{release}

%description
C implementation of Createrepo.
A set of utilities (createrepo_c, mergerepo_c, modifyrepo_c)
for generating a common metadata repository from a directory of
rpm packages and maintaining it.

%package libs
Summary:    Library for repodata manipulation

%description libs
Libraries for applications using the createrepo_c library
for easy manipulation with a repodata.

%package devel
Summary:    Library for repodata manipulation
Requires:   %{name}-libs = %{version}-%{release}

%description devel
This package contains the createrepo_c C library and header files.
These development files are for easy manipulation with a repodata.

%package -n python3-%{name}
Summary:        Python 3 bindings for the createrepo_c library
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       %{name}-libs = %{version}-%{release}

%description -n python3-%{name}
Python 3 bindings for the createrepo_c library.

%prep
%autosetup -p1

mkdir build-py3

%build
# Build createrepo_c with Pyhon 3
pushd build-py3
  %cmake .. \
      -DWITH_ZCHUNK=%{?with_zchunk:ON}%{!?with_zchunk:OFF} \
      -DWITH_LIBMODULEMD=%{?with_libmodulemd:ON}%{!?with_libmodulemd:OFF} \
      -DWITH_LEGACY_HASHES=%{?with_legacy_hashes:ON}%{!?with_legacy_hashes:OFF} \
      -DENABLE_DRPM=%{?with_drpm:ON}%{!?with_drpm:OFF}
  make %{?_smp_mflags} RPM_OPT_FLAGS="%{optflags}"
popd

%check
# Run Python 3 tests
pushd build-py3
  # Compile C tests
  make tests

  # Run Python 3 tests
  make ARGS="-V" test
popd

%install
pushd build-py3
  # Install createrepo_c with Python 3
  make install DESTDIR=%{buildroot}
popd

ln -sr %{buildroot}%{_bindir}/createrepo_c %{buildroot}%{_bindir}/createrepo
ln -sr %{buildroot}%{_bindir}/mergerepo_c %{buildroot}%{_bindir}/mergerepo
ln -sr %{buildroot}%{_bindir}/modifyrepo_c %{buildroot}%{_bindir}/modifyrepo


%ldconfig_scriptlets libs

%files
%if 0%{?xenserver} < 9
%{bash_completion}
%endif
%{_bindir}/createrepo_c
%{_bindir}/mergerepo_c
%{_bindir}/modifyrepo_c
%{_bindir}/sqliterepo_c

%{_bindir}/createrepo
%{_bindir}/mergerepo
%{_bindir}/modifyrepo

%exclude %{_mandir}/man8/createrepo_c.8.gz
%exclude %{_mandir}/man8/mergerepo_c.8.gz
%exclude %{_mandir}/man8/modifyrepo_c.8.gz
%exclude %{_mandir}/man8/sqliterepo_c.8.gz


%files libs
%license COPYING
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Nov 13 2024 Deli Zhang <deli.zhang@cloud.com> - 0.21.1-3
- CP-52243: Restore packaging bash completion

* Fri Sep 27 2024 AshwinH <ashwin.h@cloud.com> - 0.21.1-2
- CP-51607: Removed legacy Buildrequires doxygen

* Wed Aug 09 2023 Lin Liu <lin.liu@citrix.com> - 0.21.1-1
- First imported release

