from os.path import join

import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.condor as condor
import osgtest.library.osgunittest as osgunittest
import osgtest.library.service as service

class TestStopHTVault(osgunittest.OSGTestCase):

    def test_01_stop_htvault(self):
        """ Shut down the vault instance set up in the startup test and
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
        


