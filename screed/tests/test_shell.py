from __future__ import absolute_import
from . import test_fasta
from . import test_fastq
import os
import subprocess
import screed
from screed.DBConstants import fileExtension
from . import screed_tst_utils as utils
import shutil


class Test_fa_shell(test_fasta.Test_fasta):

    """
    Tests the functionality of the script 'fadbm' in creating a
    screed database correctly from the shell
    """

    def setup(self):
        thisdir = os.path.dirname(__file__)

        self._testfa = utils.get_temp_filename('test.fa')
        shutil.copy(utils.get_test_data('test.fa'), self._testfa)

        fadbm = os.path.join(thisdir, '..', 'fadbm.py')
        subprocess.check_call(['python', fadbm, self._testfa],
                              stdout=subprocess.PIPE)
        self.db = screed.ScreedDB(self._testfa)

    def teardown(self):
        os.unlink(self._testfa + fileExtension)


class Test_fq_shell(test_fastq.Test_fastq):

    """
    Tests the functionality of the script 'fqdbm' in creating a
    screed database correctly from the shell
    """

    def setup(self):
        thisdir = os.path.dirname(__file__)

        self._testfq = utils.get_temp_filename('test.fastq')
        shutil.copy(utils.get_test_data('test.fastq'), self._testfq)

        fqdbm = os.path.join(thisdir, '..', 'fqdbm.py')
        subprocess.check_call(['python', fqdbm, self._testfq],
                              stdout=subprocess.PIPE)
        self.db = screed.ScreedDB(self._testfq)

    def teardown(self):
        os.unlink(self._testfq + fileExtension)
