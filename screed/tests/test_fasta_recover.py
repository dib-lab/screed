import test_fasta
import os
import screed
from dbConstants import fileExtension

class test_fa_recover(test_fasta.Test_fasta):
    def setup(self):
        self._fileName = os.path.join(os.path.dirname(__file__), 'fastaRecovery')
        self._testfa = os.path.join(os.path.dirname(__file__), 'test.fa')
        screed.read_fasta_sequences(self._testfa)
        screed.toFasta(self._testfa, self._fileName)
        screed.read_fasta_sequences(self._fileName)
        self.db = screed.screedDB(self._fileName)

    def teardown(self):
        os.unlink(self._fileName)
        os.unlink(self._fileName + fileExtension)
        os.unlink(self._testfa + fileExtension)
