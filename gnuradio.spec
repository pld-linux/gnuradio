# TODO:
# - fix uhd build (create uhd.spec first)
# - GUIs split/subpackages?
%bcond_with	uhd
#
Summary:	Software defined radio framework
Name:		gnuradio
Version:	3.7.2.1
Release:	5
License:	GPL v3
Group:		Applications/Engineering
Source0:	http://gnuradio.org/releases/gnuradio/%{name}-%{version}.tar.gz
# Source0-md5:	f2ea23a30cb02802870fe8cb9bf272c9
URL:		http://www.gnuradio.org/
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	Qt3Support >= 4.8
BuildRequires:	QtCLucene-devel >= 4.8
BuildRequires:	QtCore-devel >= 4.8
BuildRequires:	QtDBus-devel >= 4.8
BuildRequires:	QtDeclarative-devel >= 4.8
BuildRequires:	QtDesigner-devel >= 4.8
BuildRequires:	QtGui-devel >= 4.8
BuildRequires:	QtHelp-devel >= 4.8
BuildRequires:	QtNetwork-devel >= 4.8
BuildRequires:	QtOpenGL-devel >= 4.8
BuildRequires:	QtScript-devel >= 4.8
BuildRequires:	QtScriptTools-devel >= 4.8
BuildRequires:	QtSql-devel >= 4.8
BuildRequires:	QtSvg-devel >= 4.8
BuildRequires:	QtTest-devel >= 4.8
BuildRequires:	QtUiTools-devel >= 4.8
BuildRequires:	QtWebKit-devel >= 4.8
BuildRequires:	QtXml-devel >= 4.8
BuildRequires:	QtXmlPatterns-devel >= 4.8
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	boost-devel >= 1.35
BuildRequires:	cmake >= 2.6
BuildRequires:	cppunit-devel >= 1.9.14
BuildRequires:	doxygen >= 1.5
BuildRequires:	fftw3-devel >= 3.0
BuildRequires:	gsl-devel >= 1.10
BuildRequires:	ice-devel
BuildRequires:	jack-audio-connection-kit-devel >= 0.8
BuildRequires:	libusb-devel
BuildRequires:	log4cpp-devel
BuildRequires:	orc-devel >= 0.4.11
BuildRequires:	portaudio-devel >= 19
# R/S instead?
BuildRequires:	python-PyOpenGL
BuildRequires:	python-PyQt4-devel >= 4.4
# R/S instead?
BuildRequires:	python-PyQwt-devel >= 5.2
BuildRequires:	python-cheetah >= 2.0.0
BuildRequires:	python-devel >= 2.5
BuildRequires:	python-devel-tools
BuildRequires:	python-ice
BuildRequires:	python-lxml >= 1.3.6
BuildRequires:	python-numpy >= 1.1.0
BuildRequires:	python-pygtk-devel >= 2.10.0
# R/S instead?
BuildRequires:	python-wxPython-devel >= 2.8
BuildRequires:	qt4-qmake >= 4.2.0
BuildRequires:	qwt-devel >= 5.2
BuildRequires:	sphinx
BuildRequires:	swig-python >= 1.3.31
BuildRequires:	texlive-latex
%{?with_uhd:BuildRequires:	uhd-devel >= 3.0.0}
BuildRequires:	xdg-utils
BuildRequires:	xmlto
BuildConflicts:	boost-devel = 1.46.0
BuildConflicts:	boost-devel = 1.46.1
BuildConflicts:	boost-devel = 1.47.0
BuildConflicts:	boost-devel = 1.52.0
Requires:	portaudio
Requires:	python-PyQt4
Requires:	python-cheetah
Requires:	python-lxml
Requires:	python-numpy
Requires:	python-pygtk-gtk
Requires:	python-scipy
Requires:	python-wxPython
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

%package examples
Summary:	GNU Radio examples
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description examples
GNU Radio examples.

%prep
%setup -q
sed -e '/Prevented in-tree build. This is bad practice./d' -i CMakeLists.txt
sed -e 's/list(APPEND gnuradio_runtime_libs rt)/list(APPEND gnuradio_runtime_libs rt pthread)/' -i gnuradio-runtime/lib/CMakeLists.txt
sed -e 's/list(APPEND gr_audio_libs ${JACK_LIBRARIES})/list(APPEND gr_audio_libs ${JACK_LIBRARIES} pthread)/' -i gr-audio/lib/CMakeLists.txt
sed -e 's/list(APPEND fcd_libs rt)/list(APPEND fcd_libs rt pthread)/' -i gr-fcd/lib/CMakeLists.txt
sed -e 's/target_link_libraries(volk ${volk_libraries})/target_link_libraries(volk ${volk_libraries} m)/' -i volk/lib/CMakeLists.txt

%build
%{__mkdir_p} build
cd build
%cmake \
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
mv $RPM_BUILD_ROOT%{_docdir}/gnuradio-*/* inst-doc

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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.hacking
%doc inst-doc/*
%attr(755,root,root) %{_bindir}/gnuradio-*
%attr(755,root,root) %{_bindir}/gr-ctrlport-*
%attr(755,root,root) %{_bindir}/gr-perf-*
%attr(755,root,root) %{_bindir}/gr_*
%attr(755,root,root) %{_bindir}/grcc
%attr(755,root,root) %{_bindir}/usrp_flex
%attr(755,root,root) %{_bindir}/usrp_flex_all
%attr(755,root,root) %{_bindir}/usrp_flex_band
%attr(755,root,root) %{_bindir}/volk_modtool
%attr(755,root,root) %{_bindir}/volk_profile
%attr(755,root,root) %{_libdir}/libgnuradio-*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnuradio-*.so.0
%attr(755,root,root) %{_libdir}/libvolk.so.*.*
#%attr(755,root,root) %ghost %{_libdir}/libvolk.so.0
%dir %{_sysconfdir}/gnuradio
%dir %{_sysconfdir}/gnuradio/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gnuradio/conf.d/*.conf

%{py_sitedir}/*.py*
%dir %{py_sitedir}/gnuradio
%{py_sitedir}/gnuradio/*.py*
%dir %{py_sitedir}/gnuradio/analog
%attr(755,root,root) %{py_sitedir}/gnuradio/analog/*.so
%{py_sitedir}/gnuradio/analog/*.py*

%dir %{py_sitedir}/gnuradio/atsc
%attr(755,root,root) %{py_sitedir}/gnuradio/atsc/*.so
%{py_sitedir}/gnuradio/atsc/*.py*

%dir %{py_sitedir}/gnuradio/audio
%attr(755,root,root) %{py_sitedir}/gnuradio/audio/*.so
%{py_sitedir}/gnuradio/audio/*.py*

%dir %{py_sitedir}/gnuradio/blocks
%attr(755,root,root) %{py_sitedir}/gnuradio/blocks/*.so
%{py_sitedir}/gnuradio/blocks/*.py*

%dir %{py_sitedir}/gnuradio/channels
%attr(755,root,root) %{py_sitedir}/gnuradio/channels/*.so
%{py_sitedir}/gnuradio/channels/*.py*

%{py_sitedir}/gnuradio/ctrlport

%dir %{py_sitedir}/gnuradio/digital
%attr(755,root,root) %{py_sitedir}/gnuradio/digital/*.so
%{py_sitedir}/gnuradio/digital/*.py*
%{py_sitedir}/gnuradio/digital/utils

%dir %{py_sitedir}/gnuradio/fcd
%attr(755,root,root) %{py_sitedir}/gnuradio/fcd/*.so
%{py_sitedir}/gnuradio/fcd/*.py*

%dir %{py_sitedir}/gnuradio/fec
%attr(755,root,root) %{py_sitedir}/gnuradio/fec/*.so
%{py_sitedir}/gnuradio/fec/*.py*

%dir %{py_sitedir}/gnuradio/fft
%attr(755,root,root) %{py_sitedir}/gnuradio/fft/*.so
%{py_sitedir}/gnuradio/fft/*.py*

%dir %{py_sitedir}/gnuradio/filter
%attr(755,root,root) %{py_sitedir}/gnuradio/filter/*.so
%{py_sitedir}/gnuradio/filter/*.py*

%dir %{py_sitedir}/gnuradio/gr
%attr(755,root,root) %{py_sitedir}/gnuradio/gr/*.so
%{py_sitedir}/gnuradio/gr/*.py*

%{py_sitedir}/gnuradio/grc
%{py_sitedir}/gnuradio/gru
%{py_sitedir}/gnuradio/modtool

%dir %{py_sitedir}/gnuradio/noaa
%attr(755,root,root) %{py_sitedir}/gnuradio/noaa/*.so
%{py_sitedir}/gnuradio/noaa/*.py*

%dir %{py_sitedir}/gnuradio/pager
%attr(755,root,root) %{py_sitedir}/gnuradio/pager/*.so
%{py_sitedir}/gnuradio/pager/*.py*

%dir %{py_sitedir}/gnuradio/qtgui
%attr(755,root,root) %{py_sitedir}/gnuradio/qtgui/*.so
%{py_sitedir}/gnuradio/qtgui/*.py*

%dir %{py_sitedir}/gnuradio/trellis
%attr(755,root,root) %{py_sitedir}/gnuradio/trellis/*.so
%{py_sitedir}/gnuradio/trellis/*.py*

%dir %{py_sitedir}/gnuradio/video_sdl
%attr(755,root,root) %{py_sitedir}/gnuradio/video_sdl/*.so
%{py_sitedir}/gnuradio/video_sdl/*.py*

%dir %{py_sitedir}/gnuradio/vocoder
%attr(755,root,root) %{py_sitedir}/gnuradio/vocoder/*.so
%{py_sitedir}/gnuradio/vocoder/*.py*

%dir %{py_sitedir}/gnuradio/wavelet
%attr(755,root,root) %{py_sitedir}/gnuradio/wavelet/*.so
%{py_sitedir}/gnuradio/wavelet/*.py*

%dir %{py_sitedir}/gnuradio/wxgui
%attr(755,root,root) %{py_sitedir}/gnuradio/wxgui/*.so
%{py_sitedir}/gnuradio/wxgui/*.py*
%{py_sitedir}/gnuradio/wxgui/forms
%{py_sitedir}/gnuradio/wxgui/plotter

%{py_sitedir}/grc_gnuradio
%dir %{py_sitedir}/pmt
%attr(755,root,root) %{py_sitedir}/pmt/_pmt_swig.so
%{py_sitedir}/pmt/*.py*
%{py_sitedir}/volk_modtool

%{_datadir}/gnuradio
%exclude %{_datadir}/gnuradio/examples

%files devel
%defattr(644,root,root,755)
%{_includedir}/gnuradio
%{_includedir}/pmt
%{_includedir}/volk
%attr(755,root,root) %{_libdir}/libgnuradio-*.so
%attr(755,root,root) %{_libdir}/libvolk.so
%{_pkgconfigdir}/gnuradio-*.pc
%{_pkgconfigdir}/gr-wxgui.pc
%{_pkgconfigdir}/volk.pc
%dir %{_libdir}/cmake/gnuradio
%{_libdir}/cmake/gnuradio/Gnu*.cmake
%{_libdir}/cmake/gnuradio/Gr*.cmake
%{?with_uhd:%{_libdir}/cmake/gnuradio/FindUHD.cmake}
%{_libdir}/cmake/volk

%files examples
%defattr(644,root,root,755)
%{_datadir}/gnuradio/examples
