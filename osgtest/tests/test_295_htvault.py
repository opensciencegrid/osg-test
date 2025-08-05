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


        # TODO are there existing libraries within the test framework to support this? Cagen doesn't seem
        # to support exactly this

        # Create a cert/key pair for vault
        core.config['vault.hostkey'] = '/etc/htvault-config/hostkey.pem'
        core.config['vault.hostcert'] = '/etc/htvault-config/hostcert.pem'
        core.system((
            'openssl', 
            'req', 
            '-x509', 
            '-newkey', 'rsa:4096', 
            '-keyout', core.config['vault.hostkey'], 
            '-out', core.config['vault.hostcert'],
            '-sha256',
            '-days', '365',
            '-nodes',
            '-subj', '/C=US/ST=WI/L=Madison/O=UW/OU=CHTC/CN=TestVault'))

        # Need to set ownership of certs
        core.system((
            'chown', 'vault', core.config['vault.hostkey'], core.config['vault.hostcert'] 
        ))

        service.check_start('vault')
        # htvault-config depends on vault and should be started automatically
        service.check_start('htvault-config')

        core.state['vault.started-service'] = True
        core.state['vault.running-service'] = True


    def test_02_stop_htvault(self):
        """ Shut down the vault instance set up in the previous step and
        clean up config files 
        """

        # Check that the vault (and htvault) services were started successfully
        if not (service.is_running('vault') and service.is_running('htvault-config')):
            core.state['vault.running-service'] = False
            return

        # Attempt to stop the vault and htvault-config services
        service.check_stop('htvault-config')
        service.check_stop('vault')

        core.state['vault.running-service'] = False


        # Clean up the files created for the htvault-config test
        files.remove(core.config['vault.issuer-config'])
        files.remove(core.config['vault.secrets-config'])
        files.remove(core.config['vault.hostcert'])
        files.remove(core.config['vault.hostkey'])
        

