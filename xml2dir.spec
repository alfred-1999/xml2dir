Name:           xml2dir
Version:        1.0.0
Release:        0
Summary:        XML file routing service
License:        MIT
Group:          System/Daemons
URL:            https://example.com/xml2dir
Source0:        %{name}-%{version}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  pugixml-devel
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(systemd)
%{?systemd_requires}

# Runtime service account
Requires(pre):  shadow

%description
A daemon that watches a queue directory for XML files and routes them into
subdirectories based on the <route> tag in each file. Logs all activity.

%prep
%setup -q

%build
%cmake
%cmake_build

%install
%cmake_install

install -Dm0644 %{_builddir}/%{name}-%{version}/config/xml2dir.conf \
    %{buildroot}%{_sysconfdir}/xml2dir/xml2dir.conf
install -Dm0644 %{_builddir}/%{name}-%{version}/systemd/xml2dir.service \
    %{buildroot}%{_unitdir}/xml2dir.service

# SUSE rc symlink
mkdir -p %{buildroot}%{_sbindir}
ln -sf %{_sbindir}/service %{buildroot}%{_sbindir}/rcxml2dir

# Runtime directories (root-owned)
install -d %{buildroot}%{_localstatedir}/lib/xml2dir/queue
install -d %{buildroot}%{_localstatedir}/lib/xml2dir/output
install -d %{buildroot}%{_localstatedir}/log/xml2dir

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
%doc README.md doc/test_protocol.md
%{_bindir}/xml2dir
%{_sbindir}/rcxml2dir
%dir %{_sysconfdir}/xml2dir
%config(noreplace) %{_sysconfdir}/xml2dir/xml2dir.conf
%{_unitdir}/xml2dir.service
%dir %{_localstatedir}/lib/xml2dir
%dir %{_localstatedir}/lib/xml2dir/queue
%dir %{_localstatedir}/lib/xml2dir/output
%dir %{_localstatedir}/log/xml2dir


%changelog
* Thu Sep 17 2026 alfred <alfred@example.com> - 1.0.0-0
- Create xml2dir system user and runtime directories.
- Add SUSE rc symlink; own /etc/xml2dir and /var/lib/xml2dir.
- Switch to Boost.Filesystem for GCC 7 compatibility.
* Thu Sep 10 2026 alfred <alfred@example.com> - 1.0.0
- Initial package.