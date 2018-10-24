# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library heat-translator
%global module translator
%global executable heat-translator

%global common_desc \
OpenStack Heat Translator \
Heat-Translator is an Openstack command line tool which takes non-Heat \
templates as an input and produces a Heat Orchestration Template (HOT) which \
can be deployed by Heat.

%global common_desc_tests OpenStack Heat Translator


Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Heat Translator
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n python%{pyver}-%{library}
Summary:    OpenStack Heat Translator
%{?python_provide:%python_provide python%{pyver}-%{library}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git

# Test Requirements
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-requests
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-tosca-parser
BuildRequires:  python%{pyver}-cliff

Requires:   python%{pyver}-pbr
Requires:   python%{pyver}-babel
Requires:   python%{pyver}-cliff
Requires:   python%{pyver}-dateutil
Requires:   python%{pyver}-six
Requires:   python%{pyver}-tosca-parser
Requires:   python%{pyver}-keystoneauth1 >= 3.4.0
Requires:   python%{pyver}-novaclient >= 1:9.1.0
Requires:   python%{pyver}-heatclient >= 1.10.0
Requires:   python%{pyver}-glanceclient >= 1:2.8.0
Requires:   python%{pyver}-requests

# Handle python2 exception
%if %{pyver} == 2
Requires:   PyYAML
%else
Requires:   python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{library}
%{common_desc}

%package -n python%{pyver}-%{library}-tests
Summary:    OpenStack heat-translator library tests
%{?python_provide:%python_provide python%{pyver}-%{library}-tests}

Requires:   python%{pyver}-%{library} = %{version}-%{release}
Requires:   python%{pyver}-hacking
Requires:   python%{pyver}-fixtures
Requires:   python%{pyver}-oslotest
Requires:   python%{pyver}-subunit
Requires:   python%{pyver}-testrepository
Requires:   python%{pyver}-testscenarios
Requires:   python%{pyver}-testtools
Requires:   python%{pyver}-tosca-parser

%description -n python%{pyver}-%{library}-tests
%{common_desc_tests}

This package contains the Heat Translator test files.

%package -n python-%{library}-doc
Summary:    OpenStack heat-translator library documentation

BuildRequires: python%{pyver}-sphinx
# FIXME(jpena): remove once a version including https://review.openstack.org/570889 is tagged
BuildRequires: python%{pyver}-oslo-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python-%{library}-doc
%{common_desc_tests}

This package contains the documentation.

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{pyver_build}

# generate html docs
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s ./%{executable} %{buildroot}%{_bindir}/%{executable}-%{pyver}

# Looks like Unit tests depend on sockets
# need to mock out sockets upstream
# running %check non-fatally for now
%check
export PYTHON=%{pyver_bin}
%{pyver_bin} setup.py test ||:

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/heat_%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests
%{_bindir}/%{executable}
%{_bindir}/%{executable}-%{pyver}

%files -n python%{pyver}-%{library}-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst

%changelog
