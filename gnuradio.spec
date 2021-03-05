# TODO:
# - fix uhd build (create uhd.spec first)
# - GUIs split/subpackages?
%bcond_with	uhd

Summary:	Software defined radio framework
Name:		gnuradio
Version:	3.8.0.0
Release:	5
License:	GPL v3
Group:		Applications/Engineering
Source0:	http://gnuradio.org/releases/gnuradio/%{name}-%{version}.tar.gz
# Source0-md5:	85e1ed4b18c46227731d83f8c3fbe45a
Patch0:		link.patch
Patch1:		python-libdir.patch
Patch2:		%{name}-boost.patch
URL:		http://www.gnuradio.org/
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5DBus-devel >= 5
BuildRequires:	Qt5Declarative-devel >= 5
BuildRequires:	Qt5Designer-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Help-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	Qt5OpenGL-devel >= 5
BuildRequires:	Qt5Script-devel >= 5
BuildRequires:	Qt5ScriptTools-devel >= 5
BuildRequires:	Qt5Sql-devel >= 5
BuildRequires:	Qt5Svg-devel >= 5
BuildRequires:	Qt5Test-devel >= 5
BuildRequires:	Qt5UiTools-devel >= 5
BuildRequires:	Qt5WebKit-devel >= 5
BuildRequires:	Qt5Xml-devel >= 5
BuildRequires:	Qt5XmlPatterns-devel >= 5
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	boost-devel >= 1.53
# GI
BuildRequires:	cairo-gobject >= 1.0
BuildRequires:	cmake >= 3.5.1
BuildRequires:	cppunit-devel >= 1.9.14
BuildRequires:	cppzmq-devel
BuildRequires:	doxygen >= 1.5
BuildRequires:	fftw3-devel >= 3.0
BuildRequires:	fftw3-single-devel >= 3.0
BuildRequires:	gsl-devel >= 1.10
BuildRequires:	gmp-c++-devel
# GI
BuildRequires:	gtk+3 >= 3.10.8
BuildRequires:	ice-devel
BuildRequires:	jack-audio-connection-kit-devel >= 0.8
BuildRequires:	libstdc++-devel >= 6:4.8.4
BuildRequires:	libusb-devel
BuildRequires:	log4cpp-devel
BuildRequires:	orc-devel >= 0.4.11
# PangoCairo GI
BuildRequires:	pango >= 1:1.26.0
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel >= 19
BuildRequires:	python3 >= 1:3.6.5
BuildRequires:	python3-Mako >= 0.9.1
# R/S instead?
BuildRequires:	python3-PyOpenGL
# R/S instead?
BuildRequires:	python3-PyYAML >= 3.10
BuildRequires:	python3-click
BuildRequires:	python3-devel >= 2.5
BuildRequires:	python3-devel-tools
BuildRequires:	python3-lxml >= 1.3.6
BuildRequires:	python3-numpy >= 1.1.0
BuildRequires:	python3-pygobject3 >= 2.28.6
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
BuildRequires:	qwt5-devel
BuildRequires:	sip-PyQt5
BuildRequires:	sphinx-pdg
BuildRequires:	swig-python >= 3.0.8
BuildRequires:	texlive-latex
%{?with_uhd:BuildRequires:	uhd-devel >= 3.0.0}
BuildRequires:	xdg-utils
BuildRequires:	xmlto
BuildConflicts:	python-thrift
Requires:	portaudio
Requires:	python3-PyQt5
Requires:	python3-PyYAML >= 3.10
Requires:	python3-click
Requires:	python3-lxml
Requires:	python3-numpy
Requires:	python3-scipy
Obsoletes:	grc < 0.80-1
Obsoletes:	usrp < 3.3.0-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_cpp	-pipe

%description
GNU Radio is a collection of software that when combined with minimal
hardware, allows the construction of radios where the actual waveforms
transmitted and received are defined by software. What this means is
that it turns the digital modulation schemes used in today's high
performance wireless devices into software problems.

%package devel
Summary:	GNU Radio development files
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel
Obsoletes:	usrp-devel < 3.3.0-1

%description devel
GNU Radio Headers.

%package doc
Summary:	GNU Radio
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
GNU Radio Documentation.

%package examples
Summary:	GNU Radio examples
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description examples
GNU Radio examples.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__mkdir_p} build
cd build
%cmake -Wno-dev \
	-DCMAKE_BUILD_TYPE=None \
	-DENABLE_DOXYGEN=FORCE \
	-DENABLE_GR_ATSC=FORCE \
	-DENABLE_GR_AUDIO=FORCE \
	-DENABLE_GRC=FORCE \
	-DENABLE-GR_COMEDI=FORCE \
	-DENABLE_GR_CORE=FORCE \
	-DENABLE_GR_FCD=FORCE \
	-DENABLE_GR_NOAA=FORCE \
	-DENABLE_GR_PAGER=FORCE \
	-DENABLE_GR_TRELLIS=FORCE \
	-DENABLE_GRUEL=FORCE \
	%{?with_uhd:-DENABLE_GR_UHD=FORCE} \
	-DENABLE_GR_UTILS=FORCE \
	-DENABLE_GR_VIDEO_SDL=FORCE \
	-DENABLE_GR_VOCODER=FORCE \
	-DENABLE_GR_WXGUI=FORCE \
	-DENABLE_PYTHON=FORCE \
	-DENABLE_VOLK=FORCE \
	-DSYSCONFDIR=%{_sysconfdir} \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf inst-doc
install -d inst-doc
%{__mv} $RPM_BUILD_ROOT%{_docdir}/gnuradio-*/* inst-doc

# filter bundled cmake files for other libraries
cd $RPM_BUILD_ROOT%{_libdir}/cmake/gnuradio
for f in *.cmake; do
	case $f in
		FindUHD.cmake|Gr*.cmake|Gnu*.cmake)
			;;
		*)
			rm "$f"
			;;
	esac
done

# obsolete theme
%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/gnome

# remove binary from noarch examples
%{__rm} $RPM_BUILD_ROOT%{_datadir}/gnuradio/examples/{audio/dial_tone,qt-gui/display_qt}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.hacking
%attr(755,root,root) %{_bindir}/gnuradio-*
%attr(755,root,root) %{_bindir}/gr-*
%attr(755,root,root) %{_bindir}/gr_*
%attr(755,root,root) %{_bindir}/grcc
%attr(755,root,root) %{_bindir}/polar_channel_construction
%attr(755,root,root) %{_bindir}/volk-config-info
%attr(755,root,root) %{_bindir}/volk_modtool
%attr(755,root,root) %{_bindir}/volk_profile
%attr(755,root,root) %{_libdir}/libgnuradio-*.so.*.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnuradio-*.so.3.8.0
%attr(755,root,root) %{_libdir}/libvolk.so.*.*
%dir %{_sysconfdir}/gnuradio
%dir %{_sysconfdir}/gnuradio/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gnuradio/conf.d/*.conf

%dir %{py3_sitedir}/gnuradio
%{py3_sitedir}/gnuradio/*.py*
%dir %{py3_sitedir}/gnuradio/analog
%attr(755,root,root) %{py3_sitedir}/gnuradio/analog/*.so
%{py3_sitedir}/gnuradio/analog/*.py*

%dir %{py3_sitedir}/gnuradio/audio
%attr(755,root,root) %{py3_sitedir}/gnuradio/audio/*.so
%{py3_sitedir}/gnuradio/audio/*.py*

%dir %{py3_sitedir}/gnuradio/blocks
%attr(755,root,root) %{py3_sitedir}/gnuradio/blocks/*.so
%{py3_sitedir}/gnuradio/blocks/*.py*

%dir %{py3_sitedir}/gnuradio/channels
%attr(755,root,root) %{py3_sitedir}/gnuradio/channels/*.so
%{py3_sitedir}/gnuradio/channels/*.py*

%{py3_sitedir}/gnuradio/ctrlport

%dir %{py3_sitedir}/gnuradio/digital
%attr(755,root,root) %{py3_sitedir}/gnuradio/digital/*.so
%{py3_sitedir}/gnuradio/digital/*.py*
%{py3_sitedir}/gnuradio/digital/utils

%dir %{py3_sitedir}/gnuradio/dtv
%{py3_sitedir}/gnuradio/dtv/*.py*
%attr(755,root,root) %{py3_sitedir}/gnuradio/dtv/_dtv_swig.so

%dir %{py3_sitedir}/gnuradio/fec
%attr(755,root,root) %{py3_sitedir}/gnuradio/fec/*.so
%{py3_sitedir}/gnuradio/fec/*.py*
%dir %{py3_sitedir}/gnuradio/fec/LDPC
%{py3_sitedir}/gnuradio/fec/LDPC/*.py*
%dir %{py3_sitedir}/gnuradio/fec/polar
%{py3_sitedir}/gnuradio/fec/polar/*.py*

%dir %{py3_sitedir}/gnuradio/fft
%attr(755,root,root) %{py3_sitedir}/gnuradio/fft/*.so
%{py3_sitedir}/gnuradio/fft/*.py*

%dir %{py3_sitedir}/gnuradio/filter
%attr(755,root,root) %{py3_sitedir}/gnuradio/filter/*.so
%{py3_sitedir}/gnuradio/filter/*.py*

%dir %{py3_sitedir}/gnuradio/gr
%attr(755,root,root) %{py3_sitedir}/gnuradio/gr/*.so
%{py3_sitedir}/gnuradio/gr/*.py*

%{py3_sitedir}/gnuradio/grc
%{py3_sitedir}/gnuradio/gru

%dir %{py3_sitedir}/gnuradio/qtgui
%attr(755,root,root) %{py3_sitedir}/gnuradio/qtgui/*.so
%{py3_sitedir}/gnuradio/qtgui/*.py*

%dir %{py3_sitedir}/gnuradio/trellis
%attr(755,root,root) %{py3_sitedir}/gnuradio/trellis/*.so
%{py3_sitedir}/gnuradio/trellis/*.py*

%dir %{py3_sitedir}/gnuradio/video_sdl
%attr(755,root,root) %{py3_sitedir}/gnuradio/video_sdl/*.so
%{py3_sitedir}/gnuradio/video_sdl/*.py*

%dir %{py3_sitedir}/gnuradio/vocoder
%attr(755,root,root) %{py3_sitedir}/gnuradio/vocoder/*.so
%{py3_sitedir}/gnuradio/vocoder/*.py*

%dir %{py3_sitedir}/gnuradio/wavelet
%attr(755,root,root) %{py3_sitedir}/gnuradio/wavelet/*.so
%{py3_sitedir}/gnuradio/wavelet/*.py*

%dir %{py3_sitedir}/gnuradio/zeromq
%attr(755,root,root) %{py3_sitedir}/gnuradio/zeromq/*.so
%{py3_sitedir}/gnuradio/zeromq/*.py*

%dir %{py3_sitedir}/pmt
%attr(755,root,root) %{py3_sitedir}/pmt/_pmt_swig.so
%{py3_sitedir}/pmt/*.py*
%{py3_sitedir}/volk_modtool

%{_datadir}/gnuradio
%exclude %{_datadir}/gnuradio/examples

%dir %{_libexecdir}/gnuradio
%attr(755,root,root) %{_libexecdir}/gnuradio/grc_setup_freedesktop

%{_desktopdir}/gnuradio-grc.desktop
%{_iconsdir}/hicolor/*x*/apps/gnuradio-grc.png
%{_datadir}/mime/packages/gnuradio-grc.xml

%files devel
%defattr(644,root,root,755)
%{_includedir}/gnuradio
%{_includedir}/pmt
%{_includedir}/volk
%attr(755,root,root) %{_libdir}/libgnuradio-*.so
%attr(755,root,root) %{_libdir}/libvolk.so
%{_pkgconfigdir}/gnuradio-*.pc
%{_pkgconfigdir}/volk.pc
%{_libdir}/cmake/gnuradio
%{_libdir}/cmake/volk

%files doc
%defattr(644,root,root,755)
%doc inst-doc/*

%files examples
%defattr(644,root,root,755)
%{_datadir}/gnuradio/examples
