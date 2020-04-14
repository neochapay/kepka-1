Name: kepka
Version: 2.0.0
Release: 1%{?dist}

License: GPLv3+
Summary: Unofficial Telegram desktop messaging app
URL: https://github.com/procxx/%{name}
Source0: %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Additional runtime requirements...
#?Requires: qt5-qtimageformats%{?_isa}
#?Requires: hicolor-icon-theme

# Compilers and tools...
BuildRequires: desktop-file-utils
#BuildRequires: libappstream-glib
BuildRequires: ninja
BuildRequires: cmake >= 3.10
BuildRequires: gcc-c++
BuildRequires: gcc

# Development packages for main application...
#Disabled. GSL already bundled #BuildRequires: guidelines-support-library-devel
#?BuildRequires: libappindicator-devel
#?BuildRequires: mapbox-variant-devel
BuildRequires: ffmpeg-devel >= 3.1
#Disabled System openal used #BuildRequires: openal-soft-devel
BuildRequires: OpenAL-devel
#BuildRequires: qt5-qtbase-devel
BuildRequires: libstdc++-devel
#?BuildRequires: range-v3-devel | https://github.com/ericniebler/range-v3
BuildRequires: openssl-devel
BuildRequires: minizip-devel
BuildRequires: opus-devel
BuildRequires: zlib-devel
BuildRequires: xz-devel
BuildRequires: python3-devel
BuildRequires: python3-base
BuildRequires: qt5-qtgui-devel
BuildRequires: qt5-qtcore-devel

BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Network)

# Development packages for libtgvoip...
BuildRequires: pulseaudio-devel
BuildRequires: alsa-lib-devel

%description
Kepka is a messaging app with a focus on speed and security, it’s super
fast, simple and free. You can use Kepka on all your devices at the same
time — your messages sync seamlessly across any of your phones, tablets or
computers.

With Kepka you can send messages, photos, videos and files of any type
(doc, zip, mp3, etc), as well as create groups for up to 200 people. You can
write to your phone contacts and find people by their usernames. As a result,
Kepka is like SMS and email combined — and can take care of all your
personal or business messaging needs.

%global debug_package %{nil}
%global __provides_exclude_from ^%{_prefix}/local/%{name}/lib/.*$
%global __requires_exclude ^lib(stdc|sw|av|gcc).*so.*$

%prep
# Unpacking main source archive...
%autosetup -p1
mkdir -p %{_target_platform}

%build
# Configuring application...
pushd %{_target_platform}
	%cmake -G Ninja \
	 	-DSAILFISH_OS_BUILD=ON \
	 	-DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3 \
		-DPACKAGED_BUILD=1 \
	 	-DCMAKE_BUILD_TYPE=Release \
	 	..
popd

# Building application...
%ninja_build -C %{_target_platform}

%install
# Installing application...
%ninja_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%check
# Checking AppStream manifest and desktop file...
#? appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/kservices5/tg.protocol
%{_datadir}/metainfo/%{name}.appdata.xml
