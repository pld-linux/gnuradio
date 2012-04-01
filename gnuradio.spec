# TODO:
# - fix volk, drop bcond and enable by default
# - fix uhd build
%bcond_with	uhd
%bcond_with	volk
#
%define	snap	2012-03-26
%define	snaps	%(echo %{snap} | tr -d "-")
Summary:	Software defined radio framework
Name:		gnuradio
Version:	3.5.3
Release:	0.%{snaps}.0.1
License:	GPL v3
Group:		Applications/Engineering
URL:		http://www.gnuradio.org
Source0:	http://gnuradio.org/files/builds/%{name}-%{version}-%{snap}.tar.gz
# Source0-md5:	597245618a773bad2ff6b973e83d5bcb
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
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
Requires:	PyQt4
Requires:	portaudio
Requires:	python-cheetah
Requires:	python-lxml
Requires:	python-numpy
Requires:	python-pygtk-gtk
Requires:	python-wxPython
Requires:	scipy
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

%package doc
Summary:	GNU Radio
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description doc
GNU Radio Documentation

%package examples
Summary:	GNU Radio
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description examples
GNU Radio examples

%prep
%setup -q -n %{name}

#force regeneration of cached moc output files
find . -name "*_moc.cc" -exec rm {} \;

%build
./bootstrap
#enabling deps tracking is workaround to build
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

sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} clean
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -n gnuradio -p /sbin/ldconfig
%postun -n gnuradio -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{py_sitedir}/*
%attr(755,root,root) %{_bindir}/*
%{_libdir}/lib*.so.*
%{_libexecdir}/*
%{_datadir}/gnuradio
%config(noreplace) %{_sysconfdir}/gnuradio/conf.d/*.conf
%exclude %{_datadir}/gnuradio/examples
%exclude %{py_sitedir}/gnuradio/*.la
%exclude %{_docdir}/%{name}-%{version}/html
%exclude %{_docdir}/%{name}-%{version}/xml
%doc ChangeLog NEWS INSTALL COPYING AUTHORS

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/lib*.so
%{_pkgconfigdir}/*.pc
%exclude %{_libdir}/*.la

%files doc
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}/html
%doc %{_docdir}/%{name}-%{version}/xml

%files examples
%defattr(644,root,root,755)
%{_datadir}/gnuradio/examples
