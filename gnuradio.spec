# TODO:
# - fix volk, drop bcond and enable by default
# - fix uhd build
%bcond_with	uhd
%bcond_with	volk
#
%define	snap	2012-04-02
%define	snaps	%(echo %{snap} | tr -d "-")
%define		rel	4
Summary:	Software defined radio framework
Name:		gnuradio
Version:	3.5.3
Release:	0.%{snaps}.%{rel}
License:	GPL v3
Group:		Applications/Engineering
URL:		http://www.gnuradio.org/
Source0:	http://gnuradio.org/files/builds/%{name}-%{version}-%{snap}.tar.gz
# Source0-md5:	9d839403ef713a07e07131e4fc19a543
Patch0:		%{name}-build.patch
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.11.3-2
BuildRequires:	boost-devel >= 1.35
BuildRequires:	cppunit-devel
BuildRequires:	doxygen
BuildRequires:	fftw3-devel
BuildRequires:	graphviz
BuildRequires:	gsl-devel
BuildRequires:	guile-devel
BuildRequires:	libtool
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	orc-devel
BuildRequires:	portaudio-devel
BuildRequires:	python-PyQt4-devel
BuildRequires:	python-PyQwt-devel
BuildRequires:	python-cheetah
BuildRequires:	python-devel
BuildRequires:	python-lxml
BuildRequires:	python-numpy
BuildRequires:	python-pygtk-devel
BuildRequires:	python-wxPython-devel
BuildRequires:	qwt-devel
BuildRequires:	sdcc
BuildRequires:	swig
BuildRequires:	texlive-latex
%{?with_uhd:BuildRequires:	uhd-devel}
BuildRequires:	xdg-utils
BuildRequires:	xmlto
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

%description
GNU Radio is a collection of software that when combined with minimal
hardware, allows the construction of radios where the actual waveforms
transmitted and received are defined by software. What this means is
that it turns the digital modulation schemes used in today's high
performance wireless devices into software problems.

%package devel
Summary:	GNU Radio
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
Obsoletes:	usrp-devel < 3.3.0-1

%description devel
GNU Radio Headers

%package examples
Summary:	GNU Radio
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description examples
GNU Radio examples

%prep
%setup -q -n %{name}
%patch0 -p1

# force regeneration of cached moc output files (for final tarballs)
find -name "*_moc.cc" | xargs -r rm

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoheader}
%{__automake} -Wno-portability -Wno-override -Wnone
%{__autoconf}
%configure \
	--enable-dependency-tracking \
	--enable-python \
	--enable-doxygen \
	--enable-dot \
	--%{?with_volk:en}%{!?with_volk:dis}able-volk \
	--enable-gruel \
	--enable-gnuradio-core \
	--enable-gr-msdd6000 \
	--enable-gr-audio \
	--enable-gr-atsc \
	--enable-gr-cvsd-vocoder \
	--enable-gr-gpio \
	%{?with_uhd:--enable-gr-uhd} \
	--enable-gr-gsm-fr-vocoder \
	--enable-gr-noaa \
	--enable-gr-pager \
	--enable-gr-radar-pager \
	--enable-gr-radar-mono \
	--enable-gr-radio-astronomy \
	--enable-gr-trellis \
	--enable-gr-video-sdl \
	--enable-gr-wxgui \
	--enable-gr-sounder \
	--enable-gr-utils \
	--enable-gnuradio-examples \
	--enable-grc \
	--enable-docs \
	--with-boost-libdir=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -j1 \
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
%doc ChangeLog NEWS INSTALL COPYING AUTHORS
%doc inst-doc/*
%attr(755,root,root) %{_bindir}/create-gnuradio-out-of-tree-project
%attr(755,root,root) %{_bindir}/file_rx_*.py
%attr(755,root,root) %{_bindir}/gnuradio-*
%attr(755,root,root) %{_bindir}/gr_*.py
%attr(755,root,root) %{_bindir}/hrpt_*.py
%attr(755,root,root) %{_bindir}/qt_digital_window.ui
%attr(755,root,root) %{_bindir}/usrp_display_qtgui.ui
%attr(755,root,root) %{_bindir}/usrp_*.py
%attr(755,root,root) %{_libdir}/libgnuradio-*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnuradio-*.so.0
%attr(755,root,root) %{_libdir}/libgruel-*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgruel-*.so.0
%dir %{_libdir}/gnuradio
%attr(755,root,root) %{_libdir}/gnuradio/grc_setup_freedesktop
%{_datadir}/gnuradio
%dir %{_sysconfdir}/gnuradio
%dir %{_sysconfdir}/gnuradio/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gnuradio/conf.d/*.conf
%dir %{py_sitedir}/gruel
%{py_sitedir}/gruel/*.py*
%dir %{py_sitedir}/gruel/pmt
%{py_sitedir}/gruel/pmt/*.py*
%attr(755,root,root) %{py_sitedir}/gruel/pmt/*.so
%dir %{py_sitedir}/gnuradio
%{py_sitedir}/gnuradio/*.py*
%attr(755,root,root) %{py_sitedir}/gnuradio/*.so
%dir %{py_sitedir}/gnuradio/gr
%{py_sitedir}/gnuradio/gr/*.py*
%attr(755,root,root) %{py_sitedir}/gnuradio/gr/*.so
%dir %{py_sitedir}/gnuradio/digital
%{py_sitedir}/gnuradio/digital/*.py*
%attr(755,root,root) %{py_sitedir}/gnuradio/digital/*.so
%dir %{py_sitedir}/gnuradio/digital/utils
%{py_sitedir}/gnuradio/digital/utils/*.py*
%dir %{py_sitedir}/gnuradio/audio
%{py_sitedir}/gnuradio/audio/*.py*
%attr(755,root,root) %{py_sitedir}/gnuradio/audio/*.so
%dir %{py_sitedir}/gnuradio/vocoder
%{py_sitedir}/gnuradio/vocoder/*.py*
%attr(755,root,root) %{py_sitedir}/gnuradio/vocoder/*.so
%dir %{py_sitedir}/gnuradio/noaa
%{py_sitedir}/gnuradio/noaa/*.py*
%attr(755,root,root) %{py_sitedir}/gnuradio/noaa/*.so
%dir %{py_sitedir}/gnuradio/pager
%{py_sitedir}/gnuradio/pager/*.py*
%attr(755,root,root) %{py_sitedir}/gnuradio/pager/*.so
%dir %{py_sitedir}/gnuradio/qtgui
%{py_sitedir}/gnuradio/qtgui/*.py*
%attr(755,root,root) %{py_sitedir}/gnuradio/qtgui/*.so
%{py_sitedir}/gnuradio/blks2
%{py_sitedir}/gnuradio/blks2impl
%{py_sitedir}/gnuradio/grc
%{py_sitedir}/gnuradio/gru
%{py_sitedir}/gnuradio/gruimpl
%{py_sitedir}/gnuradio/wxgui
%{py_sitedir}/grc_gnuradio
%exclude %{_datadir}/gnuradio/examples
%exclude %{py_sitedir}/gruel/*/*.la
%exclude %{py_sitedir}/gnuradio/*.la
%exclude %{py_sitedir}/gnuradio/*/*.la

%files devel
%defattr(644,root,root,755)
%{_includedir}/gnuradio
%{_includedir}/gruel
%attr(755,root,root) %{_libdir}/libgnuradio-*.so
%attr(755,root,root) %{_libdir}/libgruel.so
%{_pkgconfigdir}/gnuradio-*.pc
%{_pkgconfigdir}/gr-wxgui.pc
%{_pkgconfigdir}/gruel.pc
%exclude %{_libdir}/*.la

%files examples
%defattr(644,root,root,755)
%{_datadir}/gnuradio/examples
