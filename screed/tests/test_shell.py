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

        cmd = ['python', '-m', 'screed.fadbm', self._testfa]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret
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

        cmd = ['python', '-m', 'screed.fqdbm', self._testfq]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret
        self.db = screed.ScreedDB(self._testfq)

    def teardown(self):
        os.unlink(self._testfq + fileExtension)


class Test_fa_shell_command(test_fasta.Test_fasta):

    """
    Tests the functionality of the script 'fadbm' in creating a
    screed database correctly from the shell
    """

    def setup(self):
        thisdir = os.path.dirname(__file__)

        self._testfa = utils.get_temp_filename('test.fa')
        shutil.copy(utils.get_test_data('test.fa'), self._testfa)

        cmd = ['screed', 'db', self._testfa]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret
        self.db = screed.ScreedDB(self._testfa)

    def teardown(self):
        os.unlink(self._testfa + fileExtension)


class Test_fq_shell_command(test_fastq.Test_fastq):

    """
    Tests the functionality of the script 'fqdbm' in creating a
    screed database correctly from the shell
    """

    def setup(self):
        thisdir = os.path.dirname(__file__)

        self._testfq = utils.get_temp_filename('test.fastq')
        shutil.copy(utils.get_test_data('test.fastq'), self._testfq)

        cmd = ['screed', 'db', self._testfq]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret
        self.db = screed.ScreedDB(self._testfq)

    def teardown(self):
        os.unlink(self._testfq + fileExtension)


class Test_fa_shell_module(test_fasta.Test_fasta):

    """
    Tests the functionality of the script 'fadbm' in creating a
    screed database correctly from the shell
    """

    def setup(self):
        thisdir = os.path.dirname(__file__)

        self._testfa = utils.get_temp_filename('test.fa')
        shutil.copy(utils.get_test_data('test.fa'), self._testfa)

        cmd = ['python', '-m', 'screed', 'db', self._testfa]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret
        self.db = screed.ScreedDB(self._testfa)

    def teardown(self):
        os.unlink(self._testfa + fileExtension)


class Test_fq_shell_module(test_fastq.Test_fastq):

    """
    Tests the functionality of the script 'fqdbm' in creating a
    screed database correctly from the shell
    """

    def setup(self):
        thisdir = os.path.dirname(__file__)

        self._testfq = utils.get_temp_filename('test.fastq')
        shutil.copy(utils.get_test_data('test.fastq'), self._testfq)

        cmd = ['python', '-m', 'screed', 'db', self._testfq]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret
        self.db = screed.ScreedDB(self._testfq)

    def teardown(self):
        os.unlink(self._testfq + fileExtension)
