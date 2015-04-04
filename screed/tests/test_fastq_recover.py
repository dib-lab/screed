import test_fastq
import os
import screed
from screed.DBConstants import fileExtension
import screed_tst_utils as utils
import shutil


class test_fq_recover(test_fastq.Test_fastq):

    def setup(self):
        thisdir = os.path.dirname(__file__)
        self._fileName = utils.get_temp_filename('fastqRecovery')

        tempfile = utils.get_temp_filename('test.fastq')
        shutil.copy(utils.get_test_data('test.fastq'), tempfile)
        self._testfq = tempfile

        screed.read_fastq_sequences(self._testfq)
        screed.ToFastq(self._testfq, self._fileName)
        screed.read_fastq_sequences(self._fileName)
        self.db = screed.ScreedDB(self._fileName)

    def teardown(self):
        os.unlink(self._fileName)
        os.unlink(self._fileName + fileExtension)
        os.unlink(self._testfq + fileExtension)
