%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

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
Version:    XXX
Release:    XXX
Summary:    OpenStack Heat Translator
License:    Apache-2.0
URL:        http://launchpad.net/%{library}/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{library}
Summary:    OpenStack Heat Translator

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core

BuildRequires:  /usr/bin/pathfix.py

%description -n python3-%{library}
%{common_desc}

%package -n python3-%{library}-tests
Summary:    OpenStack heat-translator library tests

Requires:   python3-%{library} = %{version}-%{release}
%description -n python3-%{library}-tests
%{common_desc_tests}

This package contains the Heat Translator test files.

%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    OpenStack heat-translator library documentation

%description -n python-%{library}-doc
%{common_desc_tests}

This package contains the documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{library}-%{upstream_version} -S git


sed -i /.*-c{env:TOX_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s ./%{executable} %{buildroot}%{_bindir}/%{executable}-3

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{python3_sitelib}/%{module}/tests/data/artifacts/

# Looks like Unit tests depend on sockets
# need to mock out sockets upstream
# running %check non-fatally for now
%check
export PYTHON=%{__python3}
%tox -e %{default_toxenv}

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/heat_%{module}-*.dist-info
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
