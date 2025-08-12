from os.path import join, exists
import shutil

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
        """ Basic test that confirms the vault and htvault-config systemd services
        can be configured and started
        """
        core.state['vault.started-service'] = False
        core.state['vault.running-service'] = False

        core.skip_ok_unless_installed('htvault-config', 'htgettoken')

        core.config['vault.config-dir'] = '/etc/htvault-config/config.d/'

        # Check that the vault (and htvault) services aren't already running
        if service.is_running('vault'):
            core.state['vault.running-service'] = True
            return

        # Pre-configure HTVault: Create Yaml config files for vault's (dummy) identity provider
        core.config['vault.issuer-config'] = join(core.config['vault.config-dir'], '20-cilogon.yaml')
        files.write(core.config['vault.issuer-config'], HTVAULT_ISSUER_CONFIG, owner='vault', chmod=0o644, backup=False)

        core.config['vault.secrets-config'] = join(core.config['vault.config-dir'], '80-secrets.yaml')
        files.write(core.config['vault.secrets-config'], HTVAULT_SECRET_CONFIG, owner='vault', chmod=0o644, backup=False)



        # HTVault requires a dedicated cert/key pair in its own config directory.  
        # The default test certs live in /etc/grid-security, so copy them and
        # change their permissions

        core.config['vault.hostkey'] = '/etc/htvault-config/hostkey.pem'
        core.config['vault.hostcert'] = '/etc/htvault-config/hostcert.pem'

        # Confirm that the cert/key were created in a previous test (test_080_certs)
        self.assertTrue(exists(core.config['certs.hostcert']), 'HTVault Test requires hostcert/key')

        # Copy the cert/key pair to vault's config
        shutil.copy(core.config['certs.hostcert'], core.config['vault.hostcert'])
        shutil.copy(core.config['certs.hostkey'], core.config['vault.hostkey'])

        # Set ownership of certs
        shutil.chown(core.config['vault.hostcert'], 'vault')
        shutil.chown(core.config['vault.hostkey'], 'vault')

        service.check_start('vault')
        # htvault-config depends on vault and should be started automatically
        service.check_start('htvault-config')

        core.state['vault.started-service'] = True
        core.state['vault.running-service'] = True
