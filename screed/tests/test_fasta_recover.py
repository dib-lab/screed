from __future__ import absolute_import
from . import test_fasta
import os
import screed
from screed.DBConstants import fileExtension
from . import screed_tst_utils as utils
import shutil


class test_fa_recover(test_fasta.Test_fasta):

    def setup(self):
        self._fileName = utils.get_temp_filename('fastaRecovery')

        self._testfa = utils.get_temp_filename('test.fa')
        shutil.copy(utils.get_test_data('test.fa'), self._testfa)

        screed.read_fasta_sequences(self._testfa)
        screed.ToFasta(self._testfa, self._fileName)
        screed.read_fasta_sequences(self._fileName)
        self.db = screed.ScreedDB(self._fileName)

    def teardown(self):
        os.unlink(self._fileName)
        os.unlink(self._fileName + fileExtension)
        os.unlink(self._testfa + fileExtension)
