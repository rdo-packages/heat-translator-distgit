%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library heat-translator
%global module translator
%global executable heat_translator

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

Requires:   python-oslo-config >= 2:3.4.0

%description -n python2-%{library}
OpenStack Heat Translator
Heat-Translator is an Openstack command line tool which takes non-Heat
templates as an input and produces a Heat Orchestration Template (HOT) which
can be deployed by Heat.

%package -n python2-%{library}-tests
Summary:    OpenStack example library tests
Requires:   python2-%{library} = %{version}-%{release}

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
BuildRequires:  git

Requires:   python3-oslo-config >= 2:3.4.0

%package -n python3-%{library}-tests
Summary:    OpenStack Heat Translator tests
Requires:   python3-%{library} = %{version}-%{release}

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
%py2_install
%if 0%{?with_python3}
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/python2-%{executable}
%py3_install
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/python3-%{executable}
%if 0%{?default_python} >= 3
ln -s %{_bindir}/python3-%{executable} %{buildroot}%{_bindir}/%{executable}
%else
ln -s %{_bindir}/python2-%{executable} %{buildroot}%{_bindir}/%{executable}
%endif
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/heat_%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests
%{_bindir}/python2-%{executable}
%if 0%{?default_python} <= 2
%{_bindir}/%{executable}
%endif

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
%{_bindir}/python3-%{executable}
%if 0%{?default_python} >= 3
%{_bindir}/%{executable}
%endif

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%changelog
* Mon Dec 19 2016 Dan Radez <dradez@redhat.com> - 0.6.1.dev35-1
- Initial Packaging
