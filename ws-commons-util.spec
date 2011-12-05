%global         with_maven 0

Name:           ws-commons-util
Version:        1.0.1
Release:        13%{?dist}
Summary:        Common utilities from the Apache Web Services Project 

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://apache.osuosl.org/ws/commons/util/
Source0:        http://apache.osuosl.org/ws/commons/util/sources/ws-commons-util-1.0.1-src.tar.gz
%if ! %{with_maven}
# Generated with mvn ant:ant and MANIFEST.MF added to jar task
Source1:        build.xml
Source2:        maven-build.xml
Source3:        MANIFEST.MF
%else
Patch0:         %{name}-addosgimanifest.patch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  jpackage-utils >= 1.5
%if %{with_maven}
BuildRequires:  maven2
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-source
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-surefire
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven2-plugin-eclipse
%else
BuildRequires:  ant
%endif
BuildRequires:  junit
BuildRequires:  java-javadoc

%description 
This is version 1.0.1 of the common utilities from the Apache Web
Services Project.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description    javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{version}
%if ! %{with_maven}
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .
cp -p %{SOURCE3} .
%else
%patch0
%endif

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
%if %{with_maven}
mvn-jpp \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  install javadoc:javadoc
%else
ant -Dmaven.mode.offline=true -Dmaven.repo.local=`pwd`/.m2 \
  -Djunit.skipped=true -Dmaven.test.skip=true javadoc package
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pR target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%changelog
* Tue Dec 08 2009 Andrew Overholt <overholt@redhat.com> 1.0.1-13
- Add missing maven-surefire-provider-junit BR.
- Remove gcj support
- Add ability to build with ant and not maven

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Andrew Overholt <overholt@redhat.com> 1.0.1-10
- Bump so I can chain-build with xmlrpc3.

* Fri Sep 12 2008 Andrew Overholt <overholt@redhat.com> 1.0.1-9
- Add ppc64.

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.1-8
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.1-7
- Autorebuild for GCC 4.3

* Thu Sep 13 2007 Andrew Overholt <overholt@redhat.com> 1.0.1-6
- Add BR on maven surefire resources, eclipse, and install plugins.

* Thu Sep 13 2007 Andrew Overholt <overholt@redhat.com> 1.0.1-5
- ExcludeArch ppc64 until maven is built on ppc64.

* Thu Sep 13 2007 Andrew Overholt <overholt@redhat.com> 1.0.1-4
- Bump again.

* Thu Sep 13 2007 Andrew Overholt <overholt@redhat.com> 1.0.1-3
- Bump release.

* Thu Sep 06 2007 Andrew Overholt <overholt@redhat.com> 1.0.1-2
- maven-ify.
- Add OSGi MANIFEST information.

* Fri Mar 16 2007 Anthony Green <green@redhat.com> - 1.0.1-1
- Created.
