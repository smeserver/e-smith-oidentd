# $Id: e-smith-oidentd.spec,v 1.2 2008/10/07 18:49:05 slords Exp $

Summary: e-smith server and gateway - ident daemon
%define name e-smith-oidentd
Name: %{name}
%define version 2.2.0
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
BuildArchitectures: noarch
Requires: e-smith-base >= 4.0.12-48
Requires: e-smith-lib >= 1.15.1-19
Requires: iptables
Requires: oidentd >= 2.0.6
BuildRequires: e-smith-devtools >= 1.13.1-03
AutoReqProv: no

%description
e-smith server and gateway software - ident daemon

%changelog
* Tue Oct 7 2008 Shad L. Lords <slords@mail.com> 2.2.0-1.sme
- Roll new stream to separate sme7/sme8 trees [SME: 4633]

* Sun Apr 29 2007 Shad L. Lords <slords@mail.com>
- Clean up spec so package can be built by koji/plague

* Thu Dec 07 2006 Shad L. Lords <slords@mail.com>
- Update to new release naming.  No functional changes.
- Make Packager generic

* Thu Apr 6 2006 Gavin Weight <gweight@gmail.com> 1.2.0-02
- Change default status from enabled to disabled. [SME: 85]

* Wed Mar 15 2006 Charlie Brady <charlie_brady@mitel.com> 1.2.0-01
- Roll stable stream version. [SME: 1016]

* Wed Nov 30 2005 Gordon Rowell <gordonr@gormand.com.au> 1.1.0-10
- Add COPYING file

* Tue Mar 29 2005 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-09]
- Use TCPPort fragment rather than explicit masq template fragment to
  create hole in firewall.

* Tue Jan 25 2005 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-08]
- Use generic_template_expand action, in place of conf-oidentd.
  Update e-smith-lib and e-smith-devtools dependencies. [MN00064130]

* Fri Sep  3 2004 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-07]
- Clean BuildRequires. [charlieb MN00043055]

* Thu Oct 30 2003 Tony Clayton <apc@e-smith.com>
- [1.1.0-06]
- Fix new_record() method call in migrate fragment [tonyc 9546]

* Wed Oct 29 2003 Tony Clayton <apc@e-smith.com>
- [1.1.0-05]
- Fix typo in migrate fragment [tonyc 9546]

* Mon Sep 22 2003 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-04]
- Add requires for later version of oidentd. Add -m option to enable
  masqueraded support (may be required, but needs custom template for
  full support). [charlieb 9546]

* Mon Sep 22 2003 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-03]
- Add missing /var/log/oidentd directory. [charlieb 9546]

* Mon Sep 22 2003 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-02]
- Run oidentd under supervise. Use default template fragments to init db
  entry. [charlieb 9546]

* Mon Jul 21 2003 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-01]
- Changing version to development stream number - 1.1.0

* Fri Oct 11 2002 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-01]
- Rolling stable version number to 1.0.0

* Thu Aug 29 2002 Charlie Brady <charlieb@e-smith.com>
- [0.0.2-01]
- Fix template issue - need "esmith::util", otherwise expand-template succeeds
  but action script fails. [charlieb 4435]

* Wed Aug 28 2002 Charlie Brady <charlieb@e-smith.com>
- Initial [charlieb 4435]

%prep
%setup

%build
perl createlinks
mkdir -p root/etc/rc.d/rc7.d
ln -s /etc/rc.d/init.d/e-smith-service root/etc/rc.d/rc7.d/S35oidentd
touch root/var/service/oidentd/down
mkdir -p root/service
ln -s /var/service/oidentd root/service/oidentd
mkdir -p root/var/log/oidentd

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
/sbin/e-smith/genfilelist \
 --dir '/var/log/oidentd' 'attr(0750,smelog,smelog)' \
 --file '/var/service/oidentd/run' 'attr(0755,root,root)' \
 --file '/var/service/oidentd/log/run' 'attr(0755,root,root)' \
 $RPM_BUILD_ROOT > e-smith-%{name}-%{version}-filelist
echo "%doc COPYING"          >> e-smith-%{name}-%{version}-filelist

%pre
/sbin/e-smith/create-system-user smelog 1002 \
    'sme log user' /var/log/smelog /bin/false

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f e-smith-%{name}-%{version}-filelist
%defattr(-,root,root)
