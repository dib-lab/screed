from __future__ import absolute_import
from . import test_fasta
from . import test_fastq
import os
import subprocess
import screed
from screed.DBConstants import fileExtension
from . import screed_tst_utils as utils
import shutil


class Test_fa_shell_command(test_fasta.Test_fasta):
    """
    Tests the functionality of the 'db' command in creating a
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
    Tests the functionality of the 'db' command in creating a
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
    Tests the functionality of the 'db' command in creating a
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
    Tests the functionality of the 'db' command in creating a
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


class Test_convert_shell(test_fasta.Test_fasta):

    """
    Tests the ability to convert a fasta db to a fastq file, parse it into
    a fastq db, save to a fasta file, parse the fasta file into a fasta
    db and then run the fasta suite, all from the command line.
    """

    def setup(self):

        self._fqName = utils.get_temp_filename('fa_to_fq')
        self._faName = utils.get_temp_filename('fq_to_fa')
        self._testfa = utils.get_temp_filename('test.fa')
        shutil.copy(utils.get_test_data('test.fa'), self._testfa)

        cmd = ['screed', 'db', self._testfa]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret

        cmd = ['screed', 'dump_fastq', self._testfa, self._fqName]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret

        cmd = ['screed', 'db', self._fqName]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret

        cmd = ['screed', 'dump_fasta', self._fqName, self._faName]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret

        cmd = ['screed', 'db', self._faName]
        ret = subprocess.check_call(cmd, stdout=subprocess.PIPE)
        assert ret == 0, ret

        self.db = screed.ScreedDB(self._faName)

    def teardown(self):
        os.unlink(self._fqName)
        os.unlink(self._fqName + fileExtension)
        os.unlink(self._faName)
        os.unlink(self._faName + fileExtension)
        os.unlink(self._testfa + fileExtension)
