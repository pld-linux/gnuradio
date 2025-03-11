# TODO:
# - fix uhd build (create uhd.spec first)
# - GUIs split/subpackages?
#
# Conditional build:
%bcond_without	uhd	# UHD driver support

Summary:	Software defined radio framework
Summary(pl.UTF-8):	Szkielet radia programowego
Name:		gnuradio
Version:	3.10.11.0
Release:	4
License:	GPL v3
Group:		Applications/Engineering
#Source0:	https://www.gnuradio.org/releases/gnuradio/%{name}-%{version}.tar.gz
Source0:	https://github.com/gnuradio/gnuradio/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f31c96146a3cec787a59cf70144c846e
URL:		https://www.gnuradio.org/
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
BuildRequires:	cmake >= 3.16
BuildRequires:	cppunit-devel >= 1.9.14
BuildRequires:	cppzmq-devel
BuildRequires:	doxygen >= 1.5
BuildRequires:	fftw3-devel >= 3.0
BuildRequires:	fftw3-single-devel >= 3.0
BuildRequires:	gmp-c++-devel
BuildRequires:	gsl-devel >= 1.10
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
BuildRequires:	python3-PyQt5-devel
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
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	sphinx-pdg
BuildRequires:	swig-python >= 3.0.8
BuildRequires:	texlive-latex
%{?with_uhd:BuildRequires:	uhd-devel >= 3.0.0}
BuildRequires:	volk-devel
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

%description -l pl.UTF-8
GNU Radio to zbiór oprogramowania, który, w połączeniu z minimum
sprzętu, pozwala na tworzenie odbiorników/nadajników radiowych, w
których przesyłane fale są definiowane programowo. Oznacza to, że
schematy modulacji cyfrowej, używane w obecnych wydajnych urządzeniach
bezprzewodowych, stają się problemami programowymi.

%package devel
Summary:	GNU Radio development files
Summary(pl.UTF-8):	Pliki programistyczne GNU Radio
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel
Obsoletes:	usrp-devel < 3.3.0-1

%description devel
GNU Radio header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe GNU Radio.

%package doc
Summary:	GNU Radio documentation
Summary(pl.UTF-8):	Dokumentacja do GNU Radio
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
GNU Radio documentation.

%description doc -l pl.UTF-8
Dokumentacja do GNU Radio.

%package examples
Summary:	GNU Radio examples
Summary(pl.UTF-8):	Przykłady do GNU Radio
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description examples
GNU Radio examples.

%description examples -l pl.UTF-8
Przykłady do GNU Radio.

%prep
%setup -q

%build
%{__mkdir_p} build
cd build
export CFLAGS="%{rpmcflags} %{rpmcppflags}"
export CXXFLAGS="%{rpmcxxflags} %{rpmcppflags}"
export LDFLAGS="%{rpmldflags}"
%cmake -Wno-dev \
	-DCMAKE_BUILD_TYPE=None \
	-DENABLE_DOXYGEN=ON \
	-DENABLE_COMMON_PCH=ON \
	-DENABLE_GNURADIO_RUNTIME=ON \
	-DENABLE_GR_ANALOG=ON \
	-DENABLE_GR_ATSC=ON \
	-DENABLE_GR_AUDIO=ON \
	-DENABLE_GR_BLOCKS=ON \
	-DENABLE_GR_BLOCKTOOL=ON \
	-DENABLE_GR_CHANNELS=ON \
	-DENABLE-GR_COMEDI=ON \
	-DENABLE_GR_CORE=ON \
	-DENABLE_GR_CTRLPORT=ON \
	-DENABLE_GR_DIGITAL=ON \
	-DENABLE_GR_DTV=ON \
	-DENABLE_GR_FCD=ON \
	-DENABLE_GR_FEC=ON \
	-DENABLE_GR_FFT=ON \
	-DENABLE_GR_FILTER=ON \
	-DENABLE_GR_MODTOOL=ON \
	-DENABLE_GR_NETWORK=ON \
	-DENABLE_GR_NOAA=ON \
	-DENABLE_GR_PAGER=ON \
	-DENABLE_GR_PDU=ON \
	-DENABLE_GR_QTGUI=ON \
	-DENABLE_GR_TRELLIS=ON \
	%{cmake_on_off uhd ENABLE_GR_UHD} \
	%{cmake_on_off uhd DENABLE_UHD_RFNOC} \
	-DENABLE_GR_UTILS=ON \
	-DENABLE_GR_VIDEO_SDL=ON \
	-DENABLE_GR_VOCODER=ON \
	-DENABLE_GR_WAVELET=ON \
	-DENABLE_GR_WXGUI=ON \
	-DENABLE_GR_ZEROMQ=ON \
	-DENABLE_GRC=ON \
	-DENABLE_GRUEL=ON \
	-DENABLE_PYTHON=ON \
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

# remove binary from noarch examples
%{__rm} $RPM_BUILD_ROOT%{_datadir}/gnuradio/examples/{audio/dial_tone,qt-gui/display_qt%{?with_uhd:,uhd/tags_demo}}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/gnuradio-*
%attr(755,root,root) %{_bindir}/gr-*
%attr(755,root,root) %{_bindir}/gr_*
%attr(755,root,root) %{_bindir}/grcc
%attr(755,root,root) %{_bindir}/polar_channel_construction
%{?with_uhd:%{_bindir}/uhd_*}
%attr(755,root,root) %{_libdir}/libgnuradio-*.so.*.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnuradio-*.so.3.10.11
%dir %{_sysconfdir}/gnuradio
%dir %{_sysconfdir}/gnuradio/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gnuradio/conf.d/*.conf

%{_mandir}/man1/gnuradio-*.1*
%{_mandir}/man1/gr-*.1*
%{_mandir}/man1/gr_*.1*
%{_mandir}/man1/grcc.1*
%{_mandir}/man1/polar_channel_construction.1*
%{_mandir}/man1/tags_demo.1*
%{?with_uhd:%{_mandir}/man1/uhd_*.1*}

%dir %{py3_sitedir}/gnuradio
%{py3_sitedir}/gnuradio/*.py*
%dir %{py3_sitedir}/gnuradio/analog
%attr(755,root,root) %{py3_sitedir}/gnuradio/analog/*.so
%{py3_sitedir}/gnuradio/analog/*.py*

%dir %{py3_sitedir}/gnuradio/audio
%attr(755,root,root) %{py3_sitedir}/gnuradio/audio/*.so
%{py3_sitedir}/gnuradio/audio/*.py*

%{py3_sitedir}/gnuradio/bindtool

%dir %{py3_sitedir}/gnuradio/blocks
%attr(755,root,root) %{py3_sitedir}/gnuradio/blocks/*.so
%{py3_sitedir}/gnuradio/blocks/*.py*

%{py3_sitedir}/gnuradio/blocktool

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
%attr(755,root,root) %{py3_sitedir}/gnuradio/dtv/dtv_python.*.so

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
%{py3_sitedir}/gnuradio/modtool

%dir %{py3_sitedir}/gnuradio/network
%{py3_sitedir}/gnuradio/network/*.py
%attr(755,root,root) %{py3_sitedir}/gnuradio/network/network_python.*.so

%dir %{py3_sitedir}/gnuradio/pdu
%{py3_sitedir}/gnuradio/pdu/*.py
%attr(755,root,root) %{py3_sitedir}/gnuradio/pdu/pdu_python.*.so

%dir %{py3_sitedir}/pmt
%{py3_sitedir}/pmt/*.py
%attr(755,root,root) %{py3_sitedir}/pmt/pmt_python.*.so

%dir %{py3_sitedir}/gnuradio/qtgui
%attr(755,root,root) %{py3_sitedir}/gnuradio/qtgui/*.so
%{py3_sitedir}/gnuradio/qtgui/*.py*

%dir %{py3_sitedir}/gnuradio/trellis
%attr(755,root,root) %{py3_sitedir}/gnuradio/trellis/*.so
%{py3_sitedir}/gnuradio/trellis/*.py*

%if %{with uhd}
%dir %{py3_sitedir}/gnuradio/uhd
%{py3_sitedir}/gnuradio/uhd/*.py
%attr(755,root,root) %{py3_sitedir}/gnuradio/uhd/uhd_python.*.so
%endif

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

%{_datadir}/gnuradio
%exclude %{_datadir}/gnuradio/examples

#%{_desktopdir}/gnuradio-grc.desktop
#%{_iconsdir}/hicolor/*x*/apps/gnuradio-grc.png
#%{_datadir}/mime/packages/gnuradio-grc.xml

%files devel
%defattr(644,root,root,755)
%{_includedir}/gnuradio
%{_includedir}/pmt
%attr(755,root,root) %{_libdir}/libgnuradio-*.so
%{_pkgconfigdir}/gnuradio-*.pc
%{_libdir}/cmake/gnuradio

%files doc
%defattr(644,root,root,755)
%doc inst-doc/*

%files examples
%defattr(644,root,root,755)
%{_datadir}/gnuradio/examples
