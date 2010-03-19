import test_fastq
import os
import screed
from dbConstants import fileExtension

class test_fq_recover(test_fastq.Test_fastq):
    def setup(self):
        thisdir = os.path.dirname(__file__)
        self._fileName = os.path.join(thisdir, 'fastqRecovery')
        self._testfq = os.path.join(thisdir, 'test.fastq')
        screed.read_fastq_sequences(self._testfq)
        screed.toFastq(self._testfq, self._fileName)
        screed.read_fastq_sequences(self._fileName)
        self.db = screed.screedDB(self._fileName)

    def teardown(self):
        os.unlink(self._fileName)
        os.unlink(self._fileName + fileExtension)
        os.unlink(self._testfq + fileExtension)
