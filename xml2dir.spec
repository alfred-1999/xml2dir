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

# Required for groupadd/usermod

Requires(pre):  shadow

%description
xml2dir is a system service that monitors a queue directory for XML files.
It reads the route information from each XML file and moves or copies the
file to the appropriate destination directory.

The xml2dir service runs as root. Normal users such as amf can place XML
files into the queue directory without having permission to start, stop,
or otherwise control the service.

%prep
%setup -q

%build
%cmake
%cmake_build

%install
%cmake_install

# Install configuration file

install -Dm0644 
%{_builddir}/%{name}-%{version}/config/xml2dir.conf 
%{buildroot}%{_sysconfdir}/xml2dir/xml2dir.conf

# Install systemd service

install -Dm0644 
%{_builddir}/%{name}-%{version}/systemd/xml2dir.service 
%{buildroot}%{_unitdir}/xml2dir.service

# SUSE systemd compatibility symlink

mkdir -p %{buildroot}%{_sbindir}
ln -sf %{_sbindir}/service 
%{buildroot}%{_sbindir}/rcxml2dir

# Runtime directories

install -d %{buildroot}%{_localstatedir}/lib/xml2dir
install -d %{buildroot}%{_localstatedir}/lib/xml2dir/queue
install -d %{buildroot}%{_localstatedir}/lib/xml2dir/output

# Log directory

install -d %{buildroot}%{_localstatedir}/log/xml2dir

%pre

# Create the xml2dir group if it does not already exist.

# This group is used to allow the normal AMF user to place

# XML files into the queue.

getent group xml2dir >/dev/null 2>&1 || 
groupadd --system xml2dir

%service_add_pre xml2dir.service

%post
%service_add_post xml2dir.service

# Make the queue and output directories writable by members

# of the xml2dir group.

chown root:xml2dir %{_localstatedir}/lib/xml2dir
chown root:xml2dir %{_localstatedir}/lib/xml2dir/queue
chown root:xml2dir %{_localstatedir}/lib/xml2dir/output

chmod 2775 %{_localstatedir}/lib/xml2dir
chmod 2775 %{_localstatedir}/lib/xml2dir/queue
chmod 2775 %{_localstatedir}/lib/xml2dir/output

# Log directory is controlled by root because the service runs as root.

chown root:root %{_localstatedir}/log/xml2dir
chmod 0755 %{_localstatedir}/log/xml2dir

%preun
%service_del_preun xml2dir.service

%postun
%service_del_postun xml2dir.service

%files
%license LICENSE

%doc README.md
%doc doc/test_protocol.md

# Executable

%{_bindir}/xml2dir

# SUSE service compatibility link

%{_sbindir}/rcxml2dir

# Configuration

%dir %{_sysconfdir}/xml2dir
%config(noreplace) %{_sysconfdir}/xml2dir/xml2dir.conf

# systemd service

%{_unitdir}/xml2dir.service

# Runtime directories

%dir %{_localstatedir}/lib/xml2dir
%dir %{_localstatedir}/lib/xml2dir/queue
%dir %{_localstatedir}/lib/xml2dir/output

# Log directory

%dir %{_localstatedir}/log/xml2dir

%changelog

* Thu Sep 17 2026 alfred [alfred@example.com](mailto:alfred@example.com) - 1.0.0-0

- Run xml2dir systemd service as root.
- Add xml2dir group for queue access.
- Allow normal users such as amf to submit XML files.
- Add runtime queue, output and log directories.
- Add SUSE rcxml2dir compatibility symlink.

* Thu Sep 10 2026 alfred [alfred@example.com](mailto:alfred@example.com) - 1.0.0

- Initial package.
