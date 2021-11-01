import os
import pwd
import re

import osgtest.library.core as core
import osgtest.library.osgunittest as osgunittest
import osgtest.library.voms as voms


class TestVOMS(osgunittest.OSGTestCase):

    def proxy_info(self, msg):
        voms.skip_ok_unless_installed()
        self.skip_bad_unless(core.state['voms.got-proxy'], 'no proxy')

        command = ('voms-proxy-info', '-all')
        stdout = core.check_system(command, 'Run voms-proxy-info', user=True)[0]
        self.assert_(('/%s/Role=NULL' % (core.config['voms.vo'])) in stdout, msg)

    def test_00_setup(self):
        core.state.setdefault('voms.got-proxy', False)
        core.state.setdefault('proxy.valid', False)

    def test_01_add_user(self):
        core.state['voms.added-user'] = False
        voms.skip_ok_unless_installed()

        pwd_entry = pwd.getpwnam(core.options.username)
        cert_path = os.path.join(pwd_entry.pw_dir, '.globus', 'usercert.pem')

        voms.add_user(core.config['voms.vo'], cert_path)

        core.state['voms.added-user'] = True

    def test_02_good_voms_proxy_init(self):
        voms.skip_ok_unless_installed()
        self.skip_bad_unless(core.state['voms.added-user'])

        command = ('voms-proxy-init', '-voms', core.config['voms.vo'])
        password = core.options.password + '\n'
        core.check_system(command, 'Run voms-proxy-init', user=True, stdin=password)
        core.state['voms.got-proxy'] = True

    def test_03_voms_proxy_info(self):
        self.proxy_info('voms-proxy-info output has sentinel')

    def test_04_bad_voms_proxy_init(self):
        voms.skip_ok_unless_installed()
        self.skip_bad_unless(core.state['voms.added-user'])

        command = ('voms-proxy-init', '-voms', core.config['voms.vo'] + ':/Bogus')
        password = core.options.password + '\n'
        status, stdout, _ = core.system(command, True, password)
        self.assertNotEqual(status, 0, 'voms-proxy-init fails on bad group')
        self.assert_('Unable to satisfy' in stdout, 'voms-proxy-init failure message')

    # Copy of 03 above, to make sure failure did not affect good proxy
    def test_05_voms_proxy_info(self):
        self.proxy_info('second voms-proxy-info output is ok')

    def test_06_rfc_voms_proxy_init(self):
        voms.skip_ok_unless_installed()
        self.skip_bad_unless(core.state['voms.added-user'])

        command = ('voms-proxy-init', '-voms', core.config['voms.vo'], '-rfc')
        password = core.options.password + '\n'
        core.check_system(command, 'Run voms-proxy-init', user=True, stdin=password)
        core.state['voms.got-proxy'] = True

    def test_07_rfc_voms_proxy_info(self):
        self.proxy_info('third voms-proxy-info output is ok')

    def test_08_voms_proxy_check(self):
        """
        Check generated proxies to make sure that they use the same signing
        algorithm as the certificate
        """
        voms.skip_ok_unless_installed()
        self.skip_bad_unless(core.state['voms.got-proxy'], 'no proxy')

        pwd_entry = pwd.getpwnam(core.options.username)
        cert_path = os.path.join(pwd_entry.pw_dir, '.globus', 'usercert.pem')
        # Note: We're only looking for the "Signature Algorithm" line which has the same output format
        # regardless of openssl version.
        command = ['openssl', 'x509', '-in', cert_path, '-text']
        signature_re = re.compile(r'Signature Algorithm:\s+(\w+)\s')
        stdout = core.check_system(command, 'Check X.509 certificate algorithm', user=True)[0]
        match = signature_re.search(stdout)
        if match is None:
            self.fail("Can't find user cert's signing algorithm")
        cert_algorithm = match.group(1)
        command[3] = os.path.join('/', 'tmp', "x509up_u%s" % pwd_entry[2])
        stdout = core.check_system(command, 'Check X.509 proxy algorithm', user=True)[0]
        match = signature_re.search(stdout)
        if match is None:
            self.fail("Can't find proxy's signing algorithm")
        proxy_algorithm = match.group(1)
        self.assertEqual(cert_algorithm, proxy_algorithm)

        core.state['proxy.valid'] = True

    def test_09_basic_grid_proxy(self):
        """
        Use voms-proxy-init to create a basic grid proxy (without VOMS attributes)
        if we don't already have one.  We may need this for tests in other modules.
        """
        core.skip_ok_unless_installed("voms-clients", by_dependency=True)
        self.skip_ok_if(core.state['proxy.valid'], "Already have a proxy")
        self.skip_bad_unless(core.state['voms.added-user'])

        password = core.options.password + '\n'
        core.check_system(['voms-proxy-init', '-rfc'], 'Run voms-proxy-init w/o VO', user=True, stdin=password)
        core.check_system(['voms-proxy-info'], "Check resulting proxy", user=True)
        core.state['proxy.valid'] = True
