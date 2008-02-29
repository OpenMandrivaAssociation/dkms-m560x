%define module m560x
%define name dkms-%{module}
%define version 0.4.0
%define svn 20080229
%define rel 1
%define release %mkrel 0.%{svn}.%{rel}
%define distname %{module}-driver-%{version}-%{svn}

# DATE=`date +%Y%m%d`
# svn export https://m560x-driver.svn.sourceforge.net/svnroot/m560x-driver/m560x/trunk/km_m560x m560x-driver-0.4.0-$DATE
# tar cjf SOURCES/m560x-driver-0.4.0-$DATE.tar.bz2 m560x-driver-0.4.0-$DATE

Summary: Driver for the Ali M5603C and M5602 webcam chipsets
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{distname}.tar.bz2
Patch0: m560x-driver-0.4.0-20080229-hardware.patch
License: GPL
Group: System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url: https://sourceforge.net/projects/m560x-driver/
BuildArch: noarch
Requires(post): dkms
Requires(preun): dkms

%description
m560x is a driver for the Ali M5603C and M5602 webcam chipsets.

%prep
%setup -q -n %{distname}
%patch0 -p1 -b .hardware
rm -rf fw/

cat > dkms.conf <<EOF
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}-%{release}
DEST_MODULE_LOCATION[0]="/kernel/drivers/media/video"
AUTOINSTALL=yes
EOF

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}-%{release}/
tar c . | tar x -C %{buildroot}/usr/src/%{module}-%{version}-%{release}/

%clean
rm -rf %{buildroot}

%post
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{module} -v %{version}-%{release}
:

%preun
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{module} -v %{version}-%{release} --all
:

%files
%defattr(-,root,root)
/usr/src/%{module}-%{version}-%{release}
