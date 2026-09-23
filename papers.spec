## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%bcond bundled_rust_deps %{defined rhel}

# djvulibre is not available in RHEL 10+
%bcond djvu %{undefined rhel}

# Filter out soname provides for plugins
%global __provides_exclude_from ^(%{_libdir}/papers/.*\\.so|%{_libdir}/nautilus/extensions-4/.*\\.so)$

Name:           papers
Version:        51~beta
Release:        %autorelease
Summary:        View multipage documents

# papers itself is:
SourceLicense:  GPL-2.0-or-later AND GPL-3.0-or-later AND LGPL-2.0-or-later AND LGPL-2.1-or-later AND MIT AND libtiff
# ... and its crate dependencies are:
# (MIT OR Apache-2.0) AND Unicode-3.0
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause
# BSD-2-Clause AND ISC
# BSD-2-Clause OR Apache-2.0 OR MIT
# BSD-3-Clause
# BSD-3-Clause OR Apache-2.0
# GPL-2.0-or-later
# MIT
# MIT AND BSD-2-Clause AND ISC AND LicenseRef-BSD-2-Clause-WITH-AdditionRef-AOMPL-1.0
# MIT OR Apache-2.0
# MIT OR Apache-2.0 OR Zlib
# MIT OR Zlib OR Apache-2.0
# Unlicense OR MIT
# Zlib
# Zlib OR Apache-2.0 OR MIT
License:        %{shrink:
    GPL-2.0-or-later
    AND GPL-3.0-or-later
    AND LGPL-2.0-or-later
    AND LGPL-2.1-or-later
    AND MIT
    AND libtiff
    AND Apache-2.0
    AND BSD-2-Clause
    AND BSD-3-Clause
    AND ISC
    AND LicenseRef-BSD-2-Clause-WITH-AdditionRef-AOMPL-1.0
    AND Unicode-3.0
    AND Unicode-DFS-2016
    AND Zlib
    AND (0BSD OR MIT OR Apache-2.0)
    AND (Apache-2.0 OR MIT)
    AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT)
    AND (BSD-2-Clause OR Apache-2.0 OR MIT)
    AND (BSD-2-Clause AND ISC)
    AND (BSD-3-Clause OR Apache-2.0)
    AND (MIT OR Apache-2.0 OR Zlib)
    AND (Unlicense OR MIT)
}
URL:            https://gitlab.gnome.org/GNOME/papers
Source:         https://download.gnome.org/sources/%{name}/%{gnome_major_version}/%{name}-%{gnome_tarball_version}.tar.xz
# To generate vendored cargo sources:
#   tar xf papers-%%{gnome_tarball_version}.tar.xz
#   pushd papers-%%{gnome_tarball_version}
#   patch -p1 < ../0001-bump-formatx-dependency-from-0.2-to-0.4.patch
#   cargo vendor --versioned-dirs
#   tar Jcvf ../papers-%%{gnome_tarball_version}-vendor.tar.xz vendor/
#   popd
Source1:        papers-%{gnome_tarball_version}-vendor.tar.xz

# bump formatx dependency to v0.4 to match other GNOME 51.beta releases
Patch:          0001-bump-formatx-dependency-from-0.2-to-0.4.patch

%gnome_check_version

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  appstream
BuildRequires:  blueprint-compiler
BuildRequires:  gcc
BuildRequires:  itstool
BuildRequires:  meson
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-pdf)
BuildRequires:  pkgconfig(cairo-ps)
BuildRequires:  pkgconfig(dbus-1)
%if %{with djvu}
BuildRequires:  pkgconfig(ddjvuapi)
%endif
BuildRequires:  pkgconfig(exempi-2.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-unix-print)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libgxps)
BuildRequires:  pkgconfig(libnautilus-extension-4)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(sysprof-capture-4)
BuildRequires:  pkgconfig(libspelling-1)
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/desktop-file-validate
BuildRequires:  /usr/bin/gi-docgen

%if 0%{?rhel}
BuildRequires:  rust-toolset
%else
BuildRequires:  cargo-rpm-macros
%endif

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-previewer%{?_isa} = %{version}-%{release}
Requires:       %{name}-thumbnailer%{?_isa} = %{version}-%{release}

# For hicolor icon theme directories
Requires:       hicolor-icon-theme

%description
Papers is a document viewer for multiple document formats for GNOME.


%package        libs
Summary:        Libraries for the Papers document viewer

%description    libs
This package contains shared libraries needed for Papers.


%package        devel
Summary:        Support for developing backends for the Papers document viewer
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files needed for Papers
backend development.


%package doc
Summary: Documentation files for %{name}
BuildArch: noarch

%description doc
This package contains developer documentation for %{name}.


%package        nautilus
Summary:        Papers extension for nautilus
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       nautilus%{?_isa}
Supplements:    (nautilus and %{name})

%description    nautilus
This package contains the Papers extension for the Nautilus file manager.
It adds an additional tab called "Document" to the file properties dialog.


%package        previewer
Summary:        Papers previewer
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    previewer
This package brings the Papers previewer independently from Papers.
It provides the printing preview for the GTK printing dialog.


%package        thumbnailer
Summary:        Papers thumbnailer
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    thumbnailer
This package brings the Papers thumbnailer independently from Papers.


%prep
%if %{without bundled_rust_deps}
%autosetup -p1 -n %{name}-%{gnome_tarball_version}
%cargo_prep
%else
%autosetup -p1 -n %{name}-%{gnome_tarball_version} -a1
%cargo_prep -v vendor
%endif

%if %{without bundled_rust_deps}
%generate_buildrequires
%cargo_generate_buildrequires -a -t
%endif


%build
export GETTEXT_SYSTEM=1
%meson \
       -Ddjvu=%{?with_djvu:enabled}%{!?with_djvu:disabled} \
       -Dintrospection=enabled \
       -Dtests=false \
       %{nil}

%meson_build

%cargo_license_summary -a
%{cargo_license -a} > LICENSE.dependencies
%if %{with bundled_rust_deps}
%cargo_vendor_manifest
%endif


%install
%meson_install
%find_lang papers --with-gnome


%check
%meson_test

appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_metainfodir}/*.metainfo.xml
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop


%files -f papers.lang
%doc README.md
%license COPYING
%license LICENSE.dependencies
%if %{with bundled_rust_deps}
%license cargo-vendor.txt
%endif
%{_bindir}/papers
%{_datadir}/applications/org.gnome.Papers.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.Papers.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/org.gnome.Papers.svg
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.Papers-symbolic.svg
%{_mandir}/man1/papers.1*
%{_metainfodir}/org.gnome.Papers.metainfo.xml

%files libs
%license COPYING
%{_libdir}/girepository-1.0/PapersDocument-4.0.typelib
%{_libdir}/girepository-1.0/PapersView-4.0.typelib
%{_libdir}/libppsdocument-4.0.so.6{,.*}
%{_libdir}/libppsview-4.0.so.5{,.*}
%{_libdir}/papers/
%{_metainfodir}/org.gnome.Papers.ComicsDocument.metainfo.xml
%if %{with djvu}
%{_metainfodir}/org.gnome.Papers.DjvuDocument.metainfo.xml
%endif
%{_metainfodir}/org.gnome.Papers.PdfDocument.metainfo.xml
%{_metainfodir}/org.gnome.Papers.TiffDocument.metainfo.xml

%files devel
%{_includedir}/papers/
%{_libdir}/libppsdocument-4.0.so
%{_libdir}/libppsview-4.0.so
%{_libdir}/pkgconfig/papers-document-4.0.pc
%{_libdir}/pkgconfig/papers-view-4.0.pc
%{_datadir}/gir-1.0/PapersDocument-4.0.gir
%{_datadir}/gir-1.0/PapersView-4.0.gir

%files doc
%{_datadir}/doc/libppsdocument/*
%{_datadir}/doc/libppsview/*

%files nautilus
%{_libdir}/nautilus/extensions-4/libpapers-document-properties.so

%files previewer
%{_bindir}/papers-previewer
%{_datadir}/applications/org.gnome.Papers-previewer.desktop
%{_mandir}/man1/papers-previewer.1*

%files thumbnailer
%{_bindir}/papers-thumbnailer
%{_datadir}/thumbnailers/
%{_mandir}/man1/papers-thumbnailer.1*


%changelog
## START: Generated by rpmautospec
* Tue Aug 11 2026 Fabio Valentini <decathorpe@gmail.com> - 51~beta-1
- Update to version 51.beta; Fixes RHBZ#2426985

* Thu Jul 30 2026 Jan Grulich <jgrulich@redhat.com> - 49.7-5
- Add BR:appstream for appstream-cli

* Thu Jul 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 49.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Thu Jul 02 2026 Milan Crha <mcrha@redhat.com> - 49.7-2
- Build with introspection (required by sushi 51.alpha)

* Tue Jun 30 2026 Milan Crha <mcrha@redhat.com> - 49.7-1
- Update to 49.7

* Wed Mar 25 2026 Jan Grulich <jgrulich@redhat.com> - 49.6-2
- Add configuration for release-monitoring

* Wed Mar 25 2026 Milan Crha <mcrha@redhat.com> - 49.6-1
- Update to 49.6

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 49.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jan 07 2026 Fabio Valentini <decathorpe@gmail.com> - 49.3-1
- Update to version 49.3

* Thu Dec 11 2025 Adrian Vovk <adrianvovk@gmail.com> - 49.2-1
- Update to 49.2

* Mon Oct 13 2025 Petr Schindler <pschindl@redhat.com> - 49.1-2
- Update license tag

* Mon Oct 13 2025 Petr Schindler <pschindl@redhat.com> - 49.1-1
- Update to 49.1

* Sun Sep 14 2025 Fabio Valentini <decathorpe@gmail.com> - 49.0-1
- Update to version 49.0; Fixes RHBZ#2395023

* Tue Sep 02 2025 Fabio Valentini <decathorpe@gmail.com> - 49~rc-1
- Update to version 49.rc

* Mon Aug 18 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 49~beta-2
- Restore conditional on DjvuDocument metainfo

* Thu Aug 14 2025 nmontero <nmontero@redhat.com> - 49~beta-1
- Update to 49~beta

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 49~alpha-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Fabio Valentini <decathorpe@gmail.com> - 49~alpha-2
- Add missing dependencies and update library versions in files list

* Fri Jul 04 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-1
- Update to 49.alpha

* Wed May 21 2025 nmontero <nmontero@redhat.com> - 48.3-1
- Update to 48.3

* Thu Apr 24 2025 nmontero <nmontero@redhat.com> - 48.2-1
- Update to 48.2

* Mon Apr 21 2025 nmontero <nmontero@redhat.com> - 48.1-1
- Update to 48.1

* Fri Mar 14 2025 Fabio Valentini <decathorpe@gmail.com> - 48.0-2
- Fix ELN build (third time's the charm)

* Fri Mar 14 2025 nmontero <nmontero@redhat.com> - 48.0-1
- Update to 48.0

* Tue Mar 11 2025 Fabio Valentini <decathorpe@gmail.com> - 48~rc-2
- Fix ELN build (again)

* Mon Mar 10 2025 Steve Cossette <farchord@gmail.com> - 48~rc-1
- v48 RC release

* Tue Feb 25 2025 Fabio Valentini <decathorpe@gmail.com> - 48~beta-2
- Simplify cargo macro usage and fix ELN build

* Tue Feb 25 2025 Steve Cossette <farchord@gmail.com> - 48~beta-1
- Update to 48 beta

* Sun Feb 09 2025 Fabio Valentini <decathorpe@gmail.com> - 47.3-1
- Update to 47.3

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 47.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 27 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 47.0-8
- Remove unused libspectre dependency

* Mon Nov 11 2024 Kalev Lember <klember@redhat.com> - 47.0-7
- Add RHEL conditionals

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47.0-6
- Co-own /usr/share/thumbnailers directory

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47.0-5
- Add a spec file comment explaining why libppsshell is in the main package

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47.0-4
- Filter out soname provides for the nautilus extension
- Move provides filtering to the top of the spec file

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47.0-3
- Simplify license tag

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47.0-2
- Remove the %%check bcond and use %%cargo_generate_buildrequires -t
  explicitly

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47.0-1
- Update to 47.0
- Fix the build with glib-macros 0.20.3

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47~beta-5
- Use globs to ensure all desktop and metainfo files get validated

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47~beta-4
- Tighten soname globs

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47~beta-3
- Remove duplicate '(MIT OR Apache-2.0)' from license tag

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47~beta-2
- Package review fixes (rhbz#2305882)
- Explicitly BR gcc
- Filter out soname provides for plugins
- Drop all references to gi-docgen as we don't currently install
  documentation

* Wed Nov 06 2024 Kalev Lember <klember@redhat.com> - 47~beta-1
- Initial Fedora packaging (rhbz#2305882)
## END: Generated by rpmautospec
