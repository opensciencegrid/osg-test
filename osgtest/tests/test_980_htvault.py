import re
from os.path import join

import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.condor as condor
import osgtest.library.osgunittest as osgunittest
import osgtest.library.service as service

HTVAULT_ISSUER_CONFIG = '''
issuers:
  - name: cilogon
    clientid: xxx
    url: https://cilogon.org
    callbackmode: direct
    credclaim: wlcg.credkey
    roles:
      - name: default
        scopes: [profile,email,org.cilogon.userinfo,storage.read:,storage.create:]
      - name: readonly
        scopes: [profile,email,org.cilogon.userinfo,storage.read:]
'''

HTVAULT_SECRET_CONFIG = '''
issuers:
  - name: cilogon
    secret: xxx
'''

class TestStartHTVault(osgunittest.OSGTestCase):

    def test_01_start_htvault(self):
        core.state['vault.started-service'] = False
        core.state['vault.running-service'] = False

        core.skip_ok_unless_installed('htvault', 'htgettoken')

        core.config['vault.config-dir'] = '/etc/htvault-config/config.d/'

        # Check that the vault (and htvault) services aren't already running
        if service.is_running('vault'):
            core.state['vault.running-service'] = True
            return

        # Pre-configure HTVault: Create Yaml config files for vault's (dummy) identity provider
        core.config['vault.issuer-config'] = join(core.config['vault.config-dir'], '20-cilogon.yaml')
        files.write(core.config['vault.issuer-config'], HTVAULT_ISSUER_CONFIG, owner='vault', chmod=0o644)

        core.config['vault.secrets-config'] = join(core.config['vault.config-dir'], '80-secrets.yaml')
        files.write(core.config['vault.secrets-config'], HTVAULT_SECRET_CONFIG, owner='vault', chmod=0o644)


        # TODO are there existing libraries within the test framework to support this? Cagen doesn't seem
        # to support exactly this

        # Create a cert/key pair for vault
        core.system((
            'openssl', 
            'req', 
            '-x509', 
            '-newkey', 'rsa:4096', 
            '-keyout', '/etc/htvault-config/hostkey.pem', 
            '-out', '/etc/htvault-config/hostcert.pem',
            '-sha256',
            '-days', '365',
            '-nodes',
            '-subj', '/C=US/ST=WI/L=Madison/O=UW/OU=CHTC/CN=CommonNameOrHostname'))

        service.check_start('vault')
        # htvault-config depends on vault and should be started automatically
        service.check_start('htvault-config')

        core.state['vault.started-service'] = True
        core.state['vault.running-service'] = True

