Name:           xml2dir
Version:        1.0.0
Release:        1
Summary:        XML file routing service
License:        MIT
Group:          System/Daemons
URL:            https://github.com/alfred-1999/xml2dir
Source0:        %{name}-%{version}.tar

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  pugixml-devel
BuildRequires:  pkgconfig(systemd)

%{?systemd_requires}

Requires(pre):  shadow

%description
xml2dir is a system service that monitors a queue directory for XML files.
It reads the route information from each XML file and routes the file to
the appropriate destination directory.

The xml2dir service runs as root. Members of the xml2dir group can place
XML files into the queue directory.

%prep
%setup -q

%build
%cmake
%cmake_build

%install
%cmake_install

# Configuration

install -Dm0644 
%{_builddir}/%{name}-%{version}/config/xml2dir.conf 
%{buildroot}%{_sysconfdir}/xml2dir/xml2dir.conf

# systemd service

install -Dm0644 
%{_builddir}/%{name}-%{version}/systemd/xml2dir.service 
%{buildroot}%{_unitdir}/xml2dir.service

# SUSE service compatibility link

mkdir -p %{buildroot}%{_sbindir}
ln -sf %{_sbindir}/service 
%{buildroot}%{_sbindir}/rcxml2dir

# Runtime directories

install -d %{buildroot}%{_localstatedir}/lib/xml2dir
install -d %{buildroot}%{_localstatedir}/lib/xml2dir/queue
install -d %{buildroot}%{_localstatedir}/lib/xml2dir/output
install -d %{buildroot}%{_localstatedir}/log/xml2dir

%pre

# Create group used by normal users submitting XML files.

getent group xml2dir >/dev/null 2>&1 || 
groupadd --system xml2dir

%service_add_pre xml2dir.service

%post
%service_add_post xml2dir.service

# Queue and output are accessible to members of xml2dir group.

chown root:xml2dir %{_localstatedir}/lib/xml2dir
chown root:xml2dir %{_localstatedir}/lib/xml2dir/queue
chown root:xml2dir %{_localstatedir}/lib/xml2dir/output

chmod 2775 %{_localstatedir}/lib/xml2dir
chmod 2775 %{_localstatedir}/lib/xml2dir/queue
chmod 2775 %{_localstatedir}/lib/xml2dir/output

# Logs remain controlled by root.

chown root:root %{_localstatedir}/log/xml2dir
chmod 0755 %{_localstatedir}/log/xml2dir

%preun
%service_del_preun xml2dir.service

%postun
%service_del_postun xml2dir.service

%files
%license LICENSE
%doc README.md

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

* Thu Sep 17 2026 alfred [alfred@example.com](mailto:alfred@example.com) - 1.0.0-1

- Run xml2dir service as root.
- Add xml2dir group for queue access.
- Add queue, output and log directories.
- Add systemd service integration.
- Add SUSE rcxml2dir compatibility link.

* Thu Sep 10 2026 alfred [alfred@example.com](mailto:alfred@example.com) - 1.0.0-0

- Initial package.
