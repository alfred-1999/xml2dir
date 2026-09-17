Name:           xml2dir
Version:        1.0.0
Release:        0
Summary:        XML file routing service
License:        MIT
Group:          System/Daemons
URL:            https://example.com/xml2dir
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  pugixml-devel
BuildRequires:  libboost_filesystem-devel
BuildRequires:  libboost_system-devel
BuildRequires:  pkgconfig(systemd)
%{?systemd_requires}

%description
A daemon that watches a queue directory for XML files and routes them into
subdirectories based on the <route> tag in each file. Logs all activity.

%prep
%setup -q

%build
%cmake -DCMAKE_C_COMPILER=gcc-12 -DCMAKE_CXX_COMPILER=g++-12
%cmake_build

%install
%cmake_install

# Install config and systemd unit
install -Dm0644 %{_builddir}/%{name}-%{version}/config/xml2dir.conf \
    %{buildroot}%{_sysconfdir}/xml2dir/xml2dir.conf
install -Dm0644 %{_builddir}/%{name}-%{version}/systemd/xml2dir.service \
    %{buildroot}%{_unitdir}/xml2dir.service

%pre
%service_add_pre xml2dir.service

%post
%service_add_post xml2dir.service

%preun
%service_del_preun xml2dir.service

%postun
%service_del_postun xml2dir.service

%files
%license LICENSE
%doc README.md
%{_bindir}/xml2dir
%config(noreplace) %{_sysconfdir}/xml2dir/xml2dir.conf
%{_unitdir}/xml2dir.service

%changelog
* Thu Sep 10 2026 alfred - 1.0.0
- Initial package.