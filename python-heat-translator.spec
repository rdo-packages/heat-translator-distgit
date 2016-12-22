%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library heat-translator
%global module translator
%global executable heat-translator

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Heat Translator
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-master.tar.gz

BuildArch:  noarch

%package -n python2-%{library}
Summary:    OpenStack Heat Translator
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git

# Test Requirements
BuildRequires:  python-hacking
BuildRequires:  python-coverage
BuildRequires:  python-fixtures
BuildRequires:  python-oslotest
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-subunit
BuildRequires:  python-sphinx
BuildRequires:  python-requests
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-tosca-parser
BuildRequires:  python-cliff

Requires:   python-pbr
Requires:   python-babel
Requires:   python-cliff
Requires:   PyYAML
Requires:   python-dateutil
Requires:   python-six
Requires:   python-tosca-parser
Requires:   python-keystoneauth1
Requires:   python-novaclient
Requires:   python-heatclient
Requires:   python-glanceclient
Requires:   python-requests

%description -n python2-%{library}
OpenStack Heat Translator
Heat-Translator is an Openstack command line tool which takes non-Heat
templates as an input and produces a Heat Orchestration Template (HOT) which
can be deployed by Heat.

%package -n python2-%{library}-tests
Summary:    OpenStack example library tests
Requires:   python2-%{library} = %{version}-%{release}
Requires:   python-hacking
Requires:   python-coverage
Requires:   python-fixtures
Requires:   python-oslotest
Requires:   python-oslo-sphinx
Requires:   python-subunit
Requires:   python-sphinx
Requires:   python-testrepository
Requires:   python-testscenarios
Requires:   python-testtools
Requires:   python-tosca-parser

%description -n python2-%{library}-tests
OpenStack Heat Translator

This package contains the Heat Translator test files.

%package -n python-%{library}-doc
Summary:    OpenStack example library documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{library}-doc
OpenStack Heat Translator

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
Requires:   python3-python-dateutil
Requires:   python3-six
Requires:   python3-tosca-parser
Requires:   python3-keystoneauth1
Requires:   python3-python-novaclient
Requires:   python3-python-heatclient
Requires:   python3-python-glanceclient
Requires:   python3-requests

%package -n python3-%{library}-tests
Summary:    OpenStack Heat Translator tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-hacking
Requires:   python3-coverage
Requires:   python3-fixtures
Requires:   python3-oslotest
Requires:   python3-oslosphinx
Requires:   python3-python-subunit
Requires:   python3-sphinx
Requires:   python3-testrepository
Requires:   python3-testscenarios
Requires:   python3-testtools
Requires:   python3-tosca-parser

%description -n python3-%{library}-tests
OpenStack Heat Translator

This package contains the Heat Translator test files.

%endif # with_python3


%description
OpenStack Heat Translator
Heat-Translator is an Openstack command line tool which takes non-Heat
templates as an input and produces a Heat Orchestration Template (HOT) which
can be deployed by Heat.


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
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}%{python3_version}
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
%files python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/heat_%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests
%{_bindir}/neutron-3
%{_bindir}/neutron-%{python3_version}

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%changelog
* Mon Dec 19 2016 Dan Radez <dradez@redhat.com> - 0.6.1.dev35-1
- Initial Packaging
