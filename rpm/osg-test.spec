Summary:   Tests an OSG Software installation
Name:      osg-test
Version:   3.2.1
Release:   1%{?dist}
License:   Apache License, 2.0
Group:     Applications/Grid
Packager:  OSG Software <osg-software@opensciencegrid.org>
Source0:   %{name}-%{version}.tar.gz
AutoReq:   yes
AutoProv:  yes
BuildArch: noarch

Requires: python3-rpm

# 1.1.0 introduced CILogon-like CA/cert generation
Requires: osg-ca-generator >= 1.1.0

%description
The OSG Test system runs functional integration tests against an OSG Software
installation.

%package log-viewer
Summary:   Views the output of %{name}
Group:     Applications/Grid
Requires: python3-tkinter

%description log-viewer
A GUI for viewing the output of %{name} in a structured manner.

%global __python /usr/bin/python3

%prep
%setup -q

%install
find . -type f -exec sed -ri '1s,^#!/usr/bin/env python.*,#!%{__python},' '{}' +
make install DESTDIR=$RPM_BUILD_ROOT PYTHON=%{__python}

%files
%{_datadir}/osg-test
%{_sbindir}/%{name}
%{python_sitelib}/osgtest

%files log-viewer
%{_sbindir}/%{name}-log-viewer

%changelog
* Thu Apr 14 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.2.1-1
- Allow condor-blahp rpm to be used in place of blahp (SOFTWARE-4964)

* Mon Aug 23 2021 Matyas Selmeci <matyas@cs.wisc.edu> - 3.2.0-1
- Use Python 3 on EL7 too

* Fri Jul 24 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.1.0-1
- Python 3/EL8 support for osg-test (SOFTWARE-4073)

* Tue May 07 2019 Brian Lin <blin@cs.wisc.edu> - 3.0.0-1
- Remove tests for OSG 3.3-only components
- Update StashCache and XRootD tests for XCache 1.0+
- Add XRootD third-party copy tests (SOFTWARE-3362, SOFTWARE-3670)
- Install x509-scitokens-issuer-client for scitokens tests (SOFTWARE-3649)

* Wed Jan 23 2019 Carl Edquist <edquist@cs.wisc.edu> - 2.3.1-1
- Require globus-proxy-utils for xrootd-multiuser tests (SOFTWARE-3359, #154)
- Update test requirements for singularity-3.0.2 (SOFTWARE-3532, #157)
- Add comparison class for package version tests (#153)
- Update tests to support XCache 1.0.0 (SOFTWARE-3569)

* Wed Dec 19 2018 Brian Lin <blin@cs.wisc.edu> - 2.3.0-1
- Add extra digits to the test numbering scheme
- Fix bootstrap-osg-test (SOFTWARE-2232)
- Add tests for xrootd-multiuser, StashCache (SOFTWARE-3369, SOFTWARE-3360)
- Update tests for HTCondor 8.8.0 (SOFTWARE-3473)
- Re-enable xrootd-fuse tests

* Tue Oct 02 2018 Carl Edquist <edquist@cs.wisc.edu> - 2.2.2-1
- Update bootstrap-osg-test to fetch from source control (SOFTWARE-2232)
- Allow installing slurm without all of osg-tested-internal (SOFTWARE-3347)
- Conditionalize xrootd policy based on lcmaps version (SOFTWARE-3396)

* Tue Aug 7 2018 Suchandra Thapa <ssthapa@uchicago.edu> - 2.2.1-1
- Add crl and ca expiration tests for RSV
- Update to use Slurm 17.11.7

* Fri Apr 27 2018 Brian Lin <blin@cs.wisc.edu> - 2.2.0-1
- Move proxy generation to the beginning of the tests
- Add xrootd-lcmaps tests
- Fix BeStMan and gfal test GUMS dependencies
- Disable Gratia tests on EL7
- Drop osg-configure unit tests

* Tue Jan 30 2018 Brian Lin <blin@cs.wisc.edu> - 2.1.0-1
- Add test decorator to limit tests/modules to specific OSG or EL releases (SOFTWARE-2759)
- Fix gfal2 tests to not depend on bestman (SOFTWARE-2911)

* Fri Dec 08 2017 Brian Lin <blin@cs.wisc.edu> - 2.0.1-1
- Grab slurm from development repos instead of contrib (SOFTWARE-2994)
- Fix cagen.py calls for osg-ca-generator-1.3.0

* Wed Nov 01 2017 Brian Lin <blin@cs.wisc.edu> - 2.0.0-1
- Drop GRAM, RHEL5, OSG < 3.3, and dCache storage probe tests
  (SOFTWARE-2592, SOFTWARE-2913, SOFTWARE-2955)
- Add GridFTP-HDFS, XRootD-HDFS, and singularity tests (SOFTWARE-2639,
  SOFTWARE-2884)
- Fix tomcat startup issues in tests d.t. lack of entropy
  (SOFTWARE-2880)
- Fix GSISSH 3.3 EL7 test failures (SOFTWARE-2837)

* Thu Sep 07 2017 Brian Lin <blin@cs.wisc.edu> - 1.11.2-1
- Limit status checks before starting services (SOFTWARE-2846)
- Drop 'VO-supported' RSV probe (SOFTWARE-2882)

* Wed Aug 02 2017 Brian Lin <blin@cs.wisc.edu> - 1.11.1-1
- Added SELinux policy for GSI OpenSSH
- Added gfal2 tests against GridFTP
- Run Travis-CI tests out of OSG 3.4 

* Wed Jun 30 2017 Brian Lin <blin@cs.wisc.edu> - 1.11.0-1
- Use the LCMAPS VOMS plugin as the default authentication method
- Drop BDII, osg-info-services, lcg-utils, and lfc_multilib tests

* Mon Jan 30 2017 Brian Lin <blin@cs.wisc.edu> - 1.10.1-1
- Maintain order of package list specified by param files
- Limit condor_{ce_,}run tests to 10 minutes
- Use the default CVMFS cache location to avoid SELinux failures

* Wed Dec 21 2016 Brian Lin <blin@cs.wisc.edu> - 1.10.0-1
- Add HTCondor-CE + Slurm tests (SOFTWARE-2541)
- Configure Tomcat to log to catalina.log (SOFTWARE-2547)
- Add core.get_stat() function for use with core.monitor_file()
- Fix GridFTP server startup
- Package osg-test-log-viewer

* Tue Nov 01 2016 Brian Lin <blin@cs.wisc.edu> - 1.9.1-1
- Add check_start and check_stop functions to verify that services have started
  and stopped, respectively.
- Add convenience functions for retrieving condor configuration values
- Add HTCondor-CE View tests (SOFTWARE-2479)
- Increase service timeout checks to 10s from 5s

* Fri Sep 30 2016 Brian Lin <blin@cs.wisc.edu> - 1.9.0-1
- Add systemd support to services library and move all setup/teardown tests to
  use them GridFTP
- Ensure that PBS jobs cannot match to the Condor backend when simultaneously
  running
- Verify that the PBS blahp cache is populated
- Restart the CE if it's already running to acccommodate bad packaging in
  htcondor-ce-2.0.8-2


* Tue Sep 06 2016 Brian Lin <blin@cs.wisc.edu> - 1.8.4-1
- Improve tomcat7 startup time in VMU tests (SOFTWARE-2383)
- Simplify Gratia GridFTP probe/remove gums-host-cron (SOFTWARE-2398)
- Use hostname for MyProxy tests
- Add nightly option
- Add functions to wait for file generation and condor daemon readiness

* Tue Aug 02 2016 Brian Lin <blin@cs.wisc.edu> - 1.8.3-1
- Add VOMS library to set up test VOMS server without voms-admin
- Add tests for GSI-OpenSSH
- Update edg-mkgridmap tests to only require voms-admin
- Speed up Tomcat startup

* Tue Jul 05 2016 Brian Lin <blin@cs.wisc.edu> - 1.8.2-1
- Add MySQL functions (execute, check_execute, db_dump)
- Add function to compare RPM versions
- Add DummyClass that allows using osg-test modules in the Python interpreter
- Allow comments and blank lines in test_sequence
- get_package_envra: translate missing epochs to '0' 
- Set tomcat startup timeout to 20 minutes

* Thu Jun 09 2016 Brian Lin <blin@cs.wisc.edu> - 1.8.1-1
- Fix Gratia server.xml.template on EL7 that caused GUMS failures

* Fri Jun 03 2016 Brian Lin <blin@cs.wisc.edu> - 1.8.0-1
- Add option to run with CILogon-like CAs and certs (SOFTWARE-1863)
- Add ability to set timeouts for individual tests (SOFTWARE-646)
- Limit the number of yum cleans (SOFTWARE-2335)
- Fix detection of Tomcat startup (SOFTWARE-2344)
- RSV tests now run with HTCondor-CE (SOFTWARE-2337)

* Mon May 02 2016 Brian Lin <blin@cs.wisc.edu> - 1.7.0-1
- osg-test should exit non-zero if tests fail (SOFTWARE-2306)
- Fix Gratia automated test to run regardless of CE type (SOFTWARE-2293)
- Add option to osg-test that turns on SELinux (SOFTWARE-2270)
- Run gfal2 tests before GUMS/HTCondor-CE tests to accommodate inclusion of BeStMan in osg-tested-internal
- Allow regex in fetch-crl whitelists

* Tue Mar 29 2016 Brian Lin <blin@cs.wisc.edu> - 1.6.0-1
- Add option that exits osg-test on first failure (SOFTWARE-2229)
- Create an input file that determines test sequence (SOFTWARE-2228)
- java.verify_ver does not verify java-1.8.0 (SOFTWARE-2212)

* Fri Feb 26 2016 Brian Lin <blin@cs.wisc.edu> - 1.5.3-1
- Drop tarball tests (SOFTWARE-2214)
- Fix PBS test failures due to EPEL update

* Wed Feb 24 2016 Brian Lin <blin@cs.wisc.edu> - 1.5.2-1
- Drop automated tests of Gratia psacct probe (SOFTWARE-2209)
- Drop extra Gratia logging for failed tests
- use '-long' instead of deprecated '-verbose' for condor_status (SOFTWARE-2210)
- Ignore fetch-crl error when it can't get the lastUpdate time
- Remove htcondor-ce-condor requirement for HTCondor-CE setup tests

* Tue Feb 2 2016 Brian Lin <blin@cs.wisc.edu> - 1.5.1-1
- Fix error due to missing gratia outbox dir

* Tue Feb 2 2016 Brian Lin <blin@cs.wisc.edu> - 1.5.0-1
- Use the new osg-ca-generator library
- Add CVMFS and gratia psacct tests back to the nightlies
- Fix 3.1 -> 3.2 cvmfs cleanup failures (SOFTWARE-2131)

* Thu Dec 17 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.4.33-1
- Only remove OSG-Test CA certs if osg-test created them (SOFTWARE-2129)
- Fixes for pbs tests in EL7 (SOFTWARE-2130, SOFTWARE-1996)
- Handle gratia db schema update in 1.16.3+ (SOFTWARE-1932, SOFTWARE-2075)

* Mon Nov 30 2015 Brian Lin <blin@cs.wisc.edu> 1.4.32-1
- Include the failing command in test output (SOFTWARE-1819)
- Fail test if gatekeeper service succeeds but the gatekeeper is not running
- Ignore CRL signature verification failures

* Tue Oct 27 2015 Brian Lin <blin@cs.wisc.edu> 1.4.31-1
- Fix voms and gfal tests to deal with missing "voms-clients" (SOFTWARE-2085)
- Add osg-test-log-viewer
- Fixes for EL7 tests (SOFTWARE-1996)

* Mon Sep 16 2015 Brian Lin <blin@cs.wisc.edu> 1.4.30-1
- Disable SEG on EL5 (SOFTWARE-1929)
- Generalize retriable yum install error for EL7
- Fix osg-configure skips

* Mon Aug 31 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.29-1
- Skip myproxy tests if server fails to start
- Add skip for supported vo RSV probe in case gums-client is not installed
- Fix xrootd service start/stop under EL7 (SOFTWARE-2005)

* Wed Aug 19 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.28-1
- Fix OSG 3.3 release install bug
- Handle mariadb on EL7

* Tue Aug 13 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.27-1
- Skip lfc-multilib test in 3.3 for compatability
- Improvements to bootstrap-osg-test
- Increase debugging level of HTCondor CE

* Tue Jun 30 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.26-1
- Fix RSV version probe assertion
- Add GPG checks back to the OSG 3.3 tests

* Wed May 20 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.25-1
- Add support for OSG 3.3
- Fix torque configuration (SOFTWARE-1899)
- BadSkip HTCondor CE tests if the service failed to start (SOFTWARE-1898)
- Remove osg-configure unit test output that confused our test reporting (SOFTWARE-1818)

* Thu Mar 05 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.24-1
- Fix install/update failures involving 3.1 due to new xrootd-compat packages in EPEL
- Fix cleanup bug for tests with extra repos
- Add gfal2-plugin-file requirement to gfal2 tests (SOFTWARE-1799)
- Fix fetch-crl whitelist bug (SOFTWARE-1780)

* Wed Feb 04 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.23-1 
- Whitelist gratia-dCache and fetch-crl network failures (SOFTWARE-1748, SOFTWARE-1613)
- Fix skip mechanic of job tests (SOFTWARE-1730)
- Add support for secure passwords with -s/--securepass (SOFTWARE-644)
- Install Java according to the TWiki documentation (SOFTWARE-1720)

* Tue Jan 06 2015 Tim Cartwright <cat@cs.wisc.edu> - 1.4.22-1
- Small tweaks to HTCondor CE tests based on automated test results

* Mon Dec 22 2014 Tim Cartwright <cat@cs.wisc.edu> - 1.4.21-1
- Improve timeout semantics for yum installs & updates (per command)
- Add tests for job environment variables in routine job tests

* Wed Dec 10 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.20-1
- Fix for cleanup tests trying to remove pre-installed packages

* Wed Dec 03 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.19-1
- Improvements to update and cleanup tests for EL5
- Additional changes for EL7 support
- Fix for intermittent failure of condor_ce_ping tests

* Thu Oct 30 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.18-2
- Fix configuration bug that caused osg-test to error out

* Thu Oct 30 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.18-1
- Fix various tests to work with EL7
- Add gfal2 tests (SOFTWARE-1603)
- Add ability to specify multiple update repos

* Wed Sep 03 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.17-1
- Add oasis-config tests (SOFTWARE-901)
- Add condor_ce_trace tests against PBS (SOFTWARE-1459)
- Disable osg-release on EL7
- Fix xrootd4 cleanup errors

* Wed Aug 20 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.16-1
- Add osg-info-services tests
- Update xrootd tests to work with xrootd4 (SOFTWARE-1558)
- Prep work for EL7 (SOFTWARE-1579)

* Tue Jun 3 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.15-1
- Fix error with removing user (SW-1345)
- Add condor_ce_ping test (SW-1458)
- Restored files get restored with original owner/group
- Add more messages to retry list

* Tue May 6 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.14-1
- Add GUMS and HTCondor-CE tests (SOFTWARE-696, SOFTWARE-13338)
- Clean up osg-configure test (SOFTWARE-710)
- Split out lcg-utils tests
- Double gratia test timeouts 

* Mon Apr 7 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.13-1
- Add manual option and speed up fetch-crl tests
- Add lcg-utils tests
- Fixes to myproxy and cleanup tests

* Fri Mar 21 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.12-1
- Allow package cleanup to be retried
- Rebuild to fix dirty source from previous version

* Fri Mar 21 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.11-1
- Include the myproxy configuration file
- Add more retriable messages to yum commands

* Thu Mar 20 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1.4.10-1
- Added the myproxy tests (SOFTWARE-1414)
 
* Tue Mar 04 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.9-1
- Add password to usercert (SOFTWARE-1377)
- Fix condor_ce_trace test (SOFTWARE-1338)
- Update gratia probe dependencies (SOFTWARE-1375)
- Add more errors to yum retry

* Mon Feb 03 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.8-1
- Add retries to package updates
- Use SHA2 CAs/usercerts and test RFC proxies (SOFTWARE-1371)
- Add badskips to globus-job-run tests (SOFTWARE-1363)
- Add preliminary htcondor-ce tests (SOFTWARE-1338)
- Skip osg-configure-cemon tests in OSG 3.2

* Fri Jan 24 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.7-1
- Add retries to package installs
- Downgrade packages that were updated in installation
- Fix bug in osg-release upgrades

* Wed Jan 08 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.6-1
- Increase VOMS admin timeouts
- Clean yum cache after updating osg-release
- Better messages for failed installs

* Tue Dec 17 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.5-1
- Improve yum installation and cleanup

* Mon Nov 25 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.4-1
- All proxies created are now 1024 bits
- Add blahp test and updated PBS setup test accordingly
- Add support for testing updates between OSG versions

* Wed Oct 30 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.3-1
- Add gratia-probe-sge tests
- Add BeStMan debugging
- Additional MySQL backup fixes

* Wed Oct 16 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.2-1
- MySQL backup bug fixes

* Wed Oct 16 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.1-1
- Preserve old MySQL data and restore them on test completion

* Fri Oct 11 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.0-1
- Add creation of OSG CA/CRL and ability to sign host certs

* Wed Oct 9 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.3.7-1
- Reliability improvements to Gratia tests
- Fixed a file reading bug in monitor_file()
- Added a missing import in the timeout handler
- Removed --quiet option to rpm --verify
- Merge EL5 get_package_envra() fix from the ca-certs branch
- Made the global timeout value a config file option

* Thu Oct 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.6-2
- Bump release for 3.2 testing -- no functional change

* Fri Sep 27 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.3.6-1
- Fixed package requirements on two RSV tests

* Thu Sep 26 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.3.5-1
- Many small fixes, especially for VM universe tests

* Fri Sep 20 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.4-1
- Add Java7 specific installation logic

* Fri Sep 20 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.3-1
- New version: fix GUMS tests, add global timeout, add java-version RSV probe
- Fix for monitoring a file that has been log rotated

* Wed Sep 04 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.2-1
- Add GUMS and tarball tests

* Thu Aug 22 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.1-1
- Fix bug where certain config file options weren't being read

* Wed Aug 21 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.0-1
- Add support for a configuration file

* Mon Aug 12 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.11-1
- Added gratia probe tests
- Fixed bestman test bugs

* Mon Jul 22 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.10-1
- New version: Made improvements to core and files library

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9-3
- rebuilt

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9-2
- Bump to rebuild

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9-1
- Fix CVMFS test to work with new CVMFS 2.1

* Fri May 23 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.8-1
- Fix glexec create create user proxy test

* Thu May 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.7-1
- Fix lockfile name for HTCondor 7.8.8

* Wed Apr 10 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.6-1
- New version: Add tests for update installations

* Mon Jan 14 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.5-1
- New version: OkSkip/BadSkip test statuses; updated epel-release-6 rpm filename

* Fri Dec 21 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.4-2
- Remove python-nose dependency

* Wed Dec 19 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.4-1
- New version: some xrootd and fetch-crl test fixes 

* Tue Nov 13 2012 Doug Strain <dstrain@fnal.gov> - 1.2.3-1
- New Version to correct xrootd tests (SL6 GSI now working)

* Wed Oct 17 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.2-1
- New version of upstream software

* Tue Jul 31 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.1-1
- New version of upstream software: new RSV tests; cleanup fix

* Tue Jun 19 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.2.0-1
- New version of upstream software: better backups, more tests

* Wed May 09 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.1.1-1
- New version of upstream software: improve cleanup, fix RSV test

* Mon Apr 23 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.1.0-1
- New version of upstream software: LOTS of new tests, library code

* Wed Mar 14 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.0.1-1
- New version of upstream software: Bug fixes

* Thu Feb 23 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.0.0-1
- New version of upstream software: Fix cert hashes and bootstrap script

* Tue Feb 21 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.12-1
- New version of upstream software: Cleanup bug, new CA certificate hashes

* Mon Feb 20 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.11-1
- New version of upstream software: Fixed bug when tailing files

* Fri Feb 17 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.10-1
- New version of upstream software: Fixed install target

* Fri Feb 17 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.9-1
- New version of upstream software: New library, gLExec tests.
- First release to be built for EL 5 and 6.

* Thu Jan 19 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.8-1
- New version of upstream software: UberFTP tests, small bug fixes.

* Wed Dec 21 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.7-1
- New version of upstream software: VOMS tests; *many* other improvements.

* Tue Nov 16 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.6-1
- New version of upstream software: Better logging and first VOMS-related tests.

* Tue Nov 08 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.5-1
- New version of upstream software: Added GRAM tests.

* Mon Sep 26 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.4-1
- New version of upstream software.

* Thu Sep 15 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.3-1
- Skip the uninstall command when there are no RPMs to remove.

* Thu Sep 15 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.2-1
- Added a command-line option to add extra Yum repos when installing
- Removed the extraneous (and occasionally invalid) user password
- Tightened the verify options for epel- and osg-release

* Mon Sep 12 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.1-2
- Added the python-nose dependency

* Fri Sep 09 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.1-1
- Initial release
