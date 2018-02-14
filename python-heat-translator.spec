%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


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

%package -n python2-%{library}
Summary:    OpenStack Heat Translator
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  git

# Test Requirements
BuildRequires:  python2-hacking
BuildRequires:  python2-fixtures
BuildRequires:  python2-oslotest
BuildRequires:  python2-oslo-sphinx
BuildRequires:  python2-subunit
BuildRequires:  python2-sphinx
BuildRequires:  python2-requests
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
BuildRequires:  python2-testtools
BuildRequires:  python2-tosca-parser
BuildRequires:  python2-cliff

Requires:   python2-pbr
Requires:   python2-babel
Requires:   python2-cliff
Requires:   PyYAML
Requires:   python2-dateutil
Requires:   python2-six
Requires:   python2-tosca-parser
Requires:   python2-keystoneauth1 >= 3.3.0
Requires:   python2-novaclient >= 9.1.0
Requires:   python2-heatclient >= 1.10.0
Requires:   python2-glanceclient >= 2.8.0
Requires:   python2-requests

%description -n python2-%{library}
%{common_desc}

%package -n python2-%{library}-tests
Summary:    OpenStack example library tests
Requires:   python2-%{library} = %{version}-%{release}
Requires:   python2-hacking
Requires:   python2-fixtures
Requires:   python2-oslotest
Requires:   python2-oslo-sphinx
Requires:   python2-subunit
Requires:   python2-sphinx
Requires:   python2-testrepository
Requires:   python2-testscenarios
Requires:   python2-testtools
Requires:   python2-tosca-parser

%description -n python2-%{library}-tests
%{common_desc_tests}

This package contains the Heat Translator test files.

%package -n python-%{library}-doc
Summary:    OpenStack example library documentation

BuildRequires: python2-sphinx
BuildRequires: python2-oslo-sphinx

%description -n python-%{library}-doc
%{common_desc_tests}

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    OpenStack Heat Translator
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:   python3-pbr
Requires:   python3-babel
Requires:   python3-cliff
Requires:   python3-PyYAML
Requires:   python3-dateutil
Requires:   python3-six
Requires:   python3-tosca-parser
Requires:   python3-keystoneauth1 >= 3.3.0
Requires:   python3-novaclient >= 9.1.0
Requires:   python3-heatclient >= 1.10.0
Requires:   python3-glanceclient >= 2.8.0
Requires:   python3-requests

%description -n python3-%{library}
%{common_desc}

%package -n python3-%{library}-tests
Summary:    OpenStack Heat Translator tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-hacking
Requires:   python3-fixtures
Requires:   python3-oslotest
Requires:   python3-oslo-sphinx
Requires:   python3-subunit
Requires:   python3-sphinx
Requires:   python3-testrepository
Requires:   python3-testscenarios
Requires:   python3-testtools
Requires:   python3-tosca-parser

%description -n python3-%{library}-tests
%{common_desc_tests}

This package contains the Heat Translator test files.

%endif # with_python3


%description
%{common_desc}


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python3_version}
ln -s ./%{executable}-%{python3_version} %{buildroot}%{_bindir}/%{executable}-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python2_version}
ln -s ./%{executable}-%{python2_version} %{buildroot}%{_bindir}/%{executable}-2

ln -s ./%{executable}-2 %{buildroot}%{_bindir}/%{executable}

# Looks like Unit tests depend on sockets
# need to mock out sockets upstream
# running %check non-fatally for now
%check
%if 0%{?with_python3}
%{__python3} setup.py test ||:
rm -rf .testrepository
%endif
%{__python2} setup.py test ||:

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/heat_%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests
%{_bindir}/%{executable}
%{_bindir}/%{executable}-2
%{_bindir}/%{executable}-%{python2_version}

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/heat_%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests
%{_bindir}/%{executable}-3
%{_bindir}/%{executable}-%{python3_version}

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%changelog
