# TODO:
# - fix uhd build
%bcond_with	uhd
#
Summary:	Software defined radio framework
Name:		gnuradio
Version:	3.7.2.1
Release:	0.1
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
sed '/Prevented in-tree build. This is bad practice./d' -i CMakeLists.txt

%build
%{__mkdir_p} build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd build
%{__make} install \
	pythondir=%{py_sitedir} \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf inst-doc
install -d inst-doc
mv $RPM_BUILD_ROOT%{_docdir}/gnuradio-*/* inst-doc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.hacking
%doc inst-doc/*
%attr(755,root,root) %{_bindir}/gnuradio-*
%attr(755,root,root) %{_bindir}/gr_*
%attr(755,root,root) %{_bindir}/grcc
%attr(755,root,root) %{_libdir}/libgnuradio-*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnuradio-*.so.0
%attr(755,root,root) %{_libdir}/libvolk-*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libvolk-*.so.0
%dir %{_sysconfdir}/gnuradio
%dir %{_sysconfdir}/gnuradio/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gnuradio/conf.d/*.conf

%dir %{py_sitedir}/*
#%dir %{py_sitedir}/gruel
#%{py_sitedir}/gruel/*.py*
#%dir %{py_sitedir}/gruel/pmt
#%{py_sitedir}/gruel/pmt/*.py*
#%attr(755,root,root) %{py_sitedir}/gruel/pmt/*.so
#%dir %{py_sitedir}/gnuradio
#%{py_sitedir}/gnuradio/*.py*
#%attr(755,root,root) %{py_sitedir}/gnuradio/*.so
#%dir %{py_sitedir}/gnuradio/gr
#%{py_sitedir}/gnuradio/gr/*.py*
#%attr(755,root,root) %{py_sitedir}/gnuradio/gr/*.so
#%dir %{py_sitedir}/gnuradio/digital
#%{py_sitedir}/gnuradio/digital/*.py*
#%attr(755,root,root) %{py_sitedir}/gnuradio/digital/*.so
#%dir %{py_sitedir}/gnuradio/digital/utils
#%{py_sitedir}/gnuradio/digital/utils/*.py*
#%dir %{py_sitedir}/gnuradio/audio
#%{py_sitedir}/gnuradio/audio/*.py*
#%attr(755,root,root) %{py_sitedir}/gnuradio/audio/*.so
#%dir %{py_sitedir}/gnuradio/vocoder
#%{py_sitedir}/gnuradio/vocoder/*.py*
#%attr(755,root,root) %{py_sitedir}/gnuradio/vocoder/*.so
#%dir %{py_sitedir}/gnuradio/noaa
#%{py_sitedir}/gnuradio/noaa/*.py*
#%attr(755,root,root) %{py_sitedir}/gnuradio/noaa/*.so
#%dir %{py_sitedir}/gnuradio/pager
#%{py_sitedir}/gnuradio/pager/*.py*
#%attr(755,root,root) %{py_sitedir}/gnuradio/pager/*.so
#%dir %{py_sitedir}/gnuradio/qtgui
#%{py_sitedir}/gnuradio/qtgui/*.py*
#%attr(755,root,root) %{py_sitedir}/gnuradio/qtgui/*.so

#%{py_sitedir}/gnuradio/blks2
#%{py_sitedir}/gnuradio/blks2impl
#%{py_sitedir}/gnuradio/grc
#%{py_sitedir}/gnuradio/gru
#%{py_sitedir}/gnuradio/gruimpl
#%{py_sitedir}/gnuradio/wxgui
#%{py_sitedir}/grc_gnuradio

%{_datadir}/gnuradio
%exclude %{_datadir}/gnuradio/gr-newmod
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
%{_datadir}/gnuradio/gr-newmod

%files examples
%defattr(644,root,root,755)
%{_datadir}/gnuradio/examples
