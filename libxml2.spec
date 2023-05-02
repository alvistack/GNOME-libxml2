# Copyright 2023 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: libxml2
Epoch: 100
Version: 2.11.1
Release: 1%{?dist}
Summary: Library providing XML and HTML support
License: MIT
URL: https://github.com/GNOME/libxml2/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?centos_version} == 700
BuildRequires: python-devel
%else
BuildRequires: python3-devel
%endif
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: fdupes
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: python-rpm-macros
BuildRequires: xz-devel
BuildRequires: zlib-devel

%description
This library allows to manipulate XML files. It includes support to
read, modify and write XML and HTML files. There is DTDs support this
includes parsing and validation even with complex DtDs, either at parse
time or later once the document has been modified. The output can be a
simple SAX stream or and in-memory DOM like representations. In this
case one can use the built-in XPath and XPointer implementation to
select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an URI
library.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%configure \
%if 0%{?centos_version} == 700
    PYTHON=%{__python2} \
%else
    PYTHON=%{__python3} \
%endif
    --bindir=%{_bindir} \
    --datadir=%{_datadir} \
    --enable-static \
    --with-legacy \
    --with-python
%{__make}

%install
%{__make} clean
%if 0%{?centos_version} == 700
sed -i 's?pyexecdir = .*?pyexecdir = %{python2_sitearch}?g' Makefile
sed -i 's?pythondir = .*?pythondir = %{python2_sitearch}?g' Makefile
%{__make} install \
    DESTDIR=%{buildroot} \
    PYTHON=%{__python2} \
    pyexecdir=%{python2_sitearch} \
    pythondir=%{python2_sitearch}
rm -rf %{buildroot}%{python2_sitearch}/*.a
rm -rf %{buildroot}%{python2_sitearch}/*.la
fdupes -qnrps %{buildroot}%{python2_sitearch}
%else
sed -i 's?pyexecdir = .*?pyexecdir = %{python3_sitearch}?g' Makefile
sed -i 's?pythondir = .*?pythondir = %{python3_sitearch}?g' Makefile
%{__make} install \
    DESTDIR=%{buildroot} \
    PYTHON=%{__python3} \
    pyexecdir=%{python3_sitearch} \
    pythondir=%{python3_sitearch}
rm -rf %{buildroot}%{python3_sitearch}/*.a
rm -rf %{buildroot}%{python3_sitearch}/*.la
fdupes -qnrps %{buildroot}%{python3_sitearch}
%endif
rm -rf %{buildroot}{_libdir}/*.la
rm -rf %{buildroot}{_datadir}/doc/libxml2-%{version}/*
rm -rf %{buildroot}{_datadir}/doc/libxml2-python-%{version}/*
fdupes -qnrps %{buildroot}%{_datadir}/doc
fdupes -qnrps %{buildroot}%{_datadir}/gtk-doc

%check

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n libxml2-2
Summary: Library providing XML and HTML support

%description -n libxml2-2
This library allows to manipulate XML files. It includes support to
read, modify and write XML and HTML files. There is DTDs support this
includes parsing and validation even with complex DtDs, either at parse
time or later once the document has been modified. The output can be a
simple SAX stream or and in-memory DOM like representations. In this
case one can use the built-in XPath and XPointer implementation to
select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an URI
library.

%package -n libxml2-tools
Summary: Tools using libxml
Provides: libxml2 = %{epoch}:%{version}-%{release}
Obsoletes: libxml2 < %{epoch}:%{version}-%{release}

%description -n libxml2-tools
This package contains xmllint, a very useful tool proving libxml's power.

%package -n libxml2-devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/Libraries
Requires: libxml2-2 = %{epoch}:%{version}-%{release}
Requires: pkgconfig
Requires: xz-devel
Requires: zlib-devel

%description -n libxml2-devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support to
read, modify and write XML and HTML files. There is DTDs support this
includes parsing and validation even with complex DtDs, either at parse
time or later once the document has been modified. The output can be a
simple SAX stream or and in-memory DOM like representations. In this
case one can use the built-in XPath and XPointer implementation to
select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an URI
library.

%package -n python%{python3_version_nodots}-libxml2
Summary: Python 3 bindings for the libxml2 library
Group: Development/Libraries
Obsoletes: libxml2-python3 < %{epoch}:%{version}-%{release}
Provides: libxml2-python3 = %{epoch}:%{version}-%{release}
Provides: python3-libxml2 = %{epoch}:%{version}-%{release}
Provides: python3dist(libxml2) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-libxml2 = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(libxml2) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-libxml2 = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(libxml2) = %{epoch}:%{version}-%{release}
Requires: libxml2-2 = %{epoch}:%{version}-%{release}

%description -n python%{python3_version_nodots}-libxml2
The libxml2-python3 package contains a Python 3 module that permits
applications written in the Python programming language, version 3, to
use the interface supplied by the libxml2 library to manipulate XML
files.

%post -n libxml2-2 -p /sbin/ldconfig
%postun -n libxml2-2 -p /sbin/ldconfig

%files -n libxml2-2
%license Copyright
%{_libdir}/lib*.so.*

%files -n libxml2-tools
%doc %{_mandir}/man*/*
%{_bindir}/xmlcatalog
%{_bindir}/xmllint

%files -n libxml2-devel
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%doc %{_datadir}/doc/*
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/xml2-config
%{_datadir}/aclocal/libxml.m4
%{_includedir}/*
%{_libdir}/*a
%{_libdir}/cmake
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libxml-2.0.pc

%files -n python%{python3_version_nodots}-libxml2
%{python3_sitearch}/*
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n libxml2-devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/Libraries
Requires: libxml2 = %{epoch}:%{version}-%{release}
Requires: pkgconfig
Requires: xz-devel
Requires: zlib-devel

%description -n libxml2-devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support to
read, modify and write XML and HTML files. There is DTDs support this
includes parsing and validation even with complex DtDs, either at parse
time or later once the document has been modified. The output can be a
simple SAX stream or and in-memory DOM like representations. In this
case one can use the built-in XPath and XPointer implementation to
select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an URI
library.

%package -n libxml2-static
Summary: Static library for libxml2
Group: Development/Libraries
Requires: libxml2 = %{epoch}:%{version}-%{release}

%description -n libxml2-static
Static library for libxml2 provided for specific uses or shaving a few
microseconds when parsing, do not link to them for generic purpose
packages.

%if 0%{?centos_version} == 700
%package -n python-libxml2
Summary: Python 2 bindings for the libxml2 library
Group: Development/Libraries
Obsoletes: libxml2-python < %{epoch}:%{version}-%{release}
Provides: libxml2-python = %{epoch}:%{version}-%{release}
Provides: python-libxml2 = %{epoch}:%{version}-%{release}
Provides: pythondist(libxml2) = %{epoch}:%{version}-%{release}
Provides: python%{python2_version}-libxml2 = %{epoch}:%{version}-%{release}
Provides: python%{python2_version}dist(libxml2) = %{epoch}:%{version}-%{release}
Provides: python%{python2_version_nodots}-libxml2 = %{epoch}:%{version}-%{release}
Provides: python%{python2_version_nodots}dist(libxml2) = %{epoch}:%{version}-%{release}
Requires: libxml2 = %{epoch}:%{version}-%{release}

%description -n python-libxml2
The libxml2-python package contains a Python 2 module that permits
applications written in the Python programming language, version 2, to
use the interface supplied by the libxml2 library to manipulate XML
files.
%else
%package -n python3-libxml2
Summary: Python 3 bindings for the libxml2 library
Group: Development/Libraries
Obsoletes: libxml2-python3 < %{epoch}:%{version}-%{release}
Provides: libxml2-python3 = %{epoch}:%{version}-%{release}
Provides: python3-libxml2 = %{epoch}:%{version}-%{release}
Provides: python3dist(libxml2) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-libxml2 = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(libxml2) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-libxml2 = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(libxml2) = %{epoch}:%{version}-%{release}
Requires: libxml2 = %{epoch}:%{version}-%{release}

%description -n python3-libxml2
The libxml2-python3 package contains a Python 3 module that permits
applications written in the Python programming language, version 3, to
use the interface supplied by the libxml2 library to manipulate XML
files.
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license Copyright
%doc %{_mandir}/man*/*
%{_bindir}/xmlcatalog
%{_bindir}/xmllint
%{_libdir}/lib*.so.*

%files -n libxml2-devel
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%doc %{_datadir}/doc/*
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/xml2-config
%{_datadir}/aclocal/libxml.m4
%{_includedir}/*
%{_libdir}/cmake
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libxml-2.0.pc

%files -n libxml2-static
%{_libdir}/*a

%if 0%{?centos_version} == 700
%files -n python-libxml2
%{python2_sitearch}/*
%else
%files -n python3-libxml2
%{python3_sitearch}/*
%endif
%endif

%changelog
