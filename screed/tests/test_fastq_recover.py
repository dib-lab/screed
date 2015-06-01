from __future__ import absolute_import
from . import test_fastq
import os
import screed
from screed.DBConstants import fileExtension
from . import screed_tst_utils as utils
import shutil


class test_fq_recover(test_fastq.Test_fastq):

    def setup(self):
        self._fileName = utils.get_temp_filename('fastqRecovery')

        self._testfq = utils.get_temp_filename('test.fastq')
        shutil.copy(utils.get_test_data('test.fastq'), self._testfq)

        screed.read_fastq_sequences(self._testfq)
        screed.ToFastq(self._testfq, self._fileName)
        screed.read_fastq_sequences(self._fileName)
        self.db = screed.ScreedDB(self._fileName)

    def teardown(self):
        os.unlink(self._fileName)
        os.unlink(self._fileName + fileExtension)
        os.unlink(self._testfq + fileExtension)
