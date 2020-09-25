%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library heat-translator
%global module translator
%global executable heat-translator
%global with_doc 1

%global common_desc \
OpenStack Heat Translator \
Heat-Translator is an Openstack command line tool which takes non-Heat \
templates as an input and produces a Heat Orchestration Template (HOT) which \
can be deployed by Heat.

%global common_desc_tests OpenStack Heat Translator


Name:       python-%{library}
Version:    2.1.0
Release:    1%{?dist}
Summary:    OpenStack Heat Translator
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n python3-%{library}
Summary:    OpenStack Heat Translator
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git

# Test Requirements
BuildRequires:  python3-hacking
BuildRequires:  python3-fixtures
BuildRequires:  python3-oslotest
BuildRequires:  python3-subunit
BuildRequires:  python3-requests
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-tosca-parser
BuildRequires:  python3-cliff

BuildRequires:  /usr/bin/pathfix.py

Requires:   python3-pbr
Requires:   python3-babel
Requires:   python3-cliff
Requires:   python3-dateutil
Requires:   python3-six
Requires:   python3-tosca-parser
Requires:   python3-keystoneauth1 >= 3.4.0
Requires:   python3-novaclient >= 1:9.1.0
Requires:   python3-heatclient >= 1.10.0
Requires:   python3-glanceclient >= 1:2.8.0
Requires:   python3-requests
Requires:   python3-oslo-log >= 3.36.0

Requires:   python3-PyYAML

%description -n python3-%{library}
%{common_desc}

%package -n python3-%{library}-tests
Summary:    OpenStack heat-translator library tests
%{?python_provide:%python_provide python3-%{library}-tests}

Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-hacking
Requires:   python3-fixtures
Requires:   python3-oslotest
Requires:   python3-subunit
Requires:   python3-testrepository
Requires:   python3-testscenarios
Requires:   python3-testtools
Requires:   python3-tosca-parser

%description -n python3-%{library}-tests
%{common_desc_tests}

This package contains the Heat Translator test files.

%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    OpenStack heat-translator library documentation

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme

%description -n python-%{library}-doc
%{common_desc_tests}

This package contains the documentation.
%endif

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s ./%{executable} %{buildroot}%{_bindir}/%{executable}-3

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{python3_sitelib}/%{module}/tests/data/artifacts/

# Looks like Unit tests depend on sockets
# need to mock out sockets upstream
# running %check non-fatally for now
%check
export PYTHON=%{__python3}
%{__python3} setup.py test ||:

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/heat_%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests
%{_bindir}/%{executable}
%{_bindir}/%{executable}-3

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
* Fri Sep 25 2020 RDO <dev@lists.rdoproject.org> 2.1.0-1
- Update to 2.1.0

