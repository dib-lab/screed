# Copyright (c) 2016, The Regents of the University of California.

import gc
import os
import sys
import tarfile
import urllib

thisdir = os.path.dirname(__file__)
libdir = os.path.abspath(os.path.join(thisdir, '..', 'screed'))
sys.path.insert(0, libdir)

from screed import read_fastq_sequences  # nopep8
from screed import read_fasta_sequences  # nopep8
from screed import ScreedDB  # nopep8

tests22 = os.path.join(thisdir,  's_2_2_sequence.fastq')
tests31 = os.path.join(thisdir, 's_3_1_sequence.fastq')
tests42 = os.path.join(thisdir, 's_4_2_sequence.fastq')
pongo = os.path.join(thisdir, 'Pongo_pygmaeus.PPYG2.50.cdna.abinitio.fa')
tri = os.path.join(thisdir, 'triCas2.fa')
mus = os.path.join(thisdir, 'Mus_musculus.NCBIM37.50.dna_rm.chromosome.9.fa')
xeno = os.path.join(thisdir, 'Xenopus_tropicalis.JGI4.1.50.dna.toplevel.fa')
sorex = os.path.join(thisdir, 'Sorex_araneus.COMMON_SHREW1.53.dna.toplevel.fa')


def getfile(f):
    """
    Downloads and extracts the given file
    """
    filetype = f[1]
    filename = "%s.tar.gz" % f[0]
    urlname = os.path.split(filename)[1]
    base_url = 'http://lyorn.idyll.org/~nolleyal/genomes/%s/%s' % \
        (filetype, urlname)

    fp = open(filename, 'wb')
    try:
        up = urllib.urlopen(base_url)
    except IOError:
        raise IOError("Error downloading testfiles, are you connected to "
                      "the internet?")
    fp.write(up.read())
    fp.close()

    tar = tarfile.open(filename)
    tar.extractall(path=thisdir)
    tar.close()
    os.unlink(filename)
    return


def setup():
    # Create databases
    endings = ['_screed']
    filenames = [
        (tests22, 'fastq'), (tests31, 'fastq'), (tests42, 'fastq'),
        (pongo, 'fasta'), (tri, 'fasta'), (mus, 'fasta'), (xeno, 'fasta'),
        (sorex, 'fasta')
    ]
    for f in filenames:
        fname = f[0]
        if not os.path.isfile(fname):  # Download files if necessary
            getfile(f)
        parser = None
        if f[1] == 'fasta':
            parser = read_fasta_sequences
        elif f[1] == 'fastq':
            parser = read_fastq_sequences
        created = True
        for end in endings:
            if not os.path.isfile(fname + end):
                created = False
        if not created:
            parser(fname)


class Test_s22_fastq:
    """
    Test screed methods on the s22 fastq file
    """
    def setup(self):
        self.db = ScreedDB(tests22 + '_screed')

    def tearDown(self):
        del self.db
        gc.collect()

    def test_iteration(self):
        """
        Runs through the database, accessing each element by index and then by
        name
        """
        for idx in xrange(0, len(self.db)):
            rcrd = self.db.loadRecordByIndex(idx)
            nameRcrd = self.db[rcrd.name]
            assert rcrd == nameRcrd

    def test_dict_stuff(self):
        """
        Tests some dictionary methods on the database
        """
        keys = self.db.keys()
        ikeys = list(self.db.iterkeys())
        assert sorted(keys) == sorted(ikeys)
        del keys
        del ikeys
        gc.collect()

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert 'FOO' not in self.db

    def test_get(self):
        for k in self.db:
            record = self.db.get(k)
            assert record.name == k

            record = self.db[k]
            assert record.name == k

        assert self.db.get('FOO') is None
        try:
            self.db['FOO']
            assert False, "the previous line should raise a KeyError"
        except KeyError:
            pass

    def test_missing(self):
        """
        Make sure that unsupported dict attributes are actually missing.
        """
        db = self.db

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.update({})
            assert 0
        except AttributeError:
            pass

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.setdefault(None)
            assert 0
        except AttributeError:
            pass

        try:
            db.pop()
            assert 0
        except AttributeError:
            pass

        try:
            db.popitem()
            assert 0
        except AttributeError:
            pass

    def test_certain_records(self):
        """
        Pulls first, last, middle and few other records out of database and
        compares them to known quantities
        """
        testcases = {}
        testcases['HWI-EAS_4_PE-FC20GCB:2:1:492:573/2'] = {
            'id': 0,
            'annotations': '',
            'quality': 'AA7AAA3+AAAAAA.AAA.;7;AA;;;;*;<1;<<<',
            'name': 'HWI-EAS_4_PE-FC20GCB:2:1:492:573/2',
            'sequence': 'ACAGCAAAATTGTGATTGAGGATGAAGAACTGCTGT'}

        testcases['HWI-EAS_4_PE-FC20GCB:2:162:131:826/2'] = {
            'id': 1895228,
            'annotations': '',
            'quality': 'AAAAAAAAAAAAAAAAAAAAAA+@6=7A<05<*15:',
            'name': 'HWI-EAS_4_PE-FC20GCB:2:162:131:826/2',
            'sequence': 'ATGAATACAAACAATGCGGCAGTCATAATGCCCCTC'}

        testcases['HWI-EAS_4_PE-FC20GCB:2:330:88:628/2'] = {
            'id': 3790455,
            'annotations': '',
            'quality': 'AA;AA??A5A;;+AA?AAAA;AA;9AA.AA?????9',
            'name': 'HWI-EAS_4_PE-FC20GCB:2:330:88:628/2',
            'sequence': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAA'}

        testcases['HWI-EAS_4_PE-FC20GCB:2:4:707:391/2'] = {
            'id': 29999,
            'annotations': '',
            'quality': 'AAAAAAAAAA@<)A*AAA6A::<@AA<>A>-8?>4<',
            'name': 'HWI-EAS_4_PE-FC20GCB:2:4:707:391/2',
            'sequence': 'ATTAATCTCCAGTTTCTGGCAAACATTCAGGCCATT'}

        testcases['HWI-EAS_4_PE-FC20GCB:2:36:158:208/2'] = {
            'id': 342842,
            'annotations': '',
            'quality': 'AA5?AAAAA?AAAA5?AAA5A???5A>AAA4?;.;;',
            'name': 'HWI-EAS_4_PE-FC20GCB:2:36:158:208/2',
            'sequence': 'TTTCCCTACAGAAGTGTCTGTACCGGTAATAAAGAA'}

        for case in testcases:
            assert testcases[case] == self.db[case]


class Test_s31_fastq:
    """
    Test screed methods on the s31 fastq file
    """
    def setup(self):
        self.db = ScreedDB(tests31 + '_screed')

    def tearDown(self):
        del self.db
        gc.collect()

    def test_iteration(self):
        """
        Runs through the database, accessing each element by index and then by
        name
        """
        for idx in xrange(0, len(self.db)):
            rcrd = self.db.loadRecordByIndex(idx)
            nameRcrd = self.db[rcrd.name]
            assert rcrd == nameRcrd

    def test_dict_stuff(self):
        """
        Tests some dictionary methods on the database
        """
        keys = self.db.keys()
        ikeys = list(self.db.iterkeys())
        assert sorted(keys) == sorted(ikeys)
        del keys
        del ikeys
        gc.collect()

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert 'FOO' not in self.db

    def test_get(self):
        for k in self.db:
            record = self.db.get(k)
            assert record.name == k

            record = self.db[k]
            assert record.name == k

        assert self.db.get('FOO') is None
        try:
            self.db['FOO']
            assert False, "the previous line should raise a KeyError"
        except KeyError:
            pass

    def test_missing(self):
        """
        Make sure that unsupported dict attributes are actually missing.
        """
        db = self.db

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.update({})
            assert 0
        except AttributeError:
            pass

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.setdefault(None)
            assert 0
        except AttributeError:
            pass

        try:
            db.pop()
            assert 0
        except AttributeError:
            pass

        try:
            db.popitem()
            assert 0
        except AttributeError:
            pass

    def test_certain_records(self):
        """
        Pulls first, last, middle and few other records out of database and
        compares them to known quantities
        """
        testcases = {}
        testcases['HWI-EAS_4_PE-FC20GCB:3:1:71:840/1'] = {
            'id': 0,
            'annotations': '',
            'quality': 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
            'name': 'HWI-EAS_4_PE-FC20GCB:3:1:71:840/1',
            'sequence': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'}

        testcases['HWI-EAS_4_PE-FC20GCB:3:330:957:433/1'] = {
            'id': 4439695,
            'annotations': '',
            'quality': 'AAAAAAAAAAA<A?<AA<AAAAA?AAA?<:*??&::',
            'name': 'HWI-EAS_4_PE-FC20GCB:3:330:957:433/1',
            'sequence': 'CTTTGTGGAGAAGAGGGCGTGGGCAAGGCACTGATA'}

        testcases['HWI-EAS_4_PE-FC20GCB:3:166:443:410/1'] = {
            'id': 2219847,
            'annotations': '',
            'quality': 'AAAAAAAAAAAAAAAAAAAAAAAA6<@AA959???%',
            'name': 'HWI-EAS_4_PE-FC20GCB:3:166:443:410/1',
            'sequence': 'TGGCATTCGCACACATCATGATGGTGCTGACCGTAA'}

        testcases['HWI-EAS_4_PE-FC20GCB:3:1:803:878/1'] = {
            'id': 2999,
            'annotations': '',
            'quality': '?6AAA6A<A6AA<<AA?A&A066/6:/&?&1191+0',
            'name': 'HWI-EAS_4_PE-FC20GCB:3:1:803:878/1',
            'sequence': 'AAGATGCTGTAGTGGCCGCATGTGTAATAGGCTTTA'}

        testcases['HWI-EAS_4_PE-FC20GCB:3:245:54:506/1'] = {
            'id': 3329772,
            'annotations': '',
            'quality': "AAAAAAAAAAAAAAAA>A+AAA+@AA+A>A%8*?'%",
            'name': 'HWI-EAS_4_PE-FC20GCB:3:245:54:506/1',
            'sequence': 'CTTCGTTGCTGTTTATCAGTAACTTTTTCTGGCTAG'}

        for case in testcases:
            assert testcases[case] == self.db[case]


class Test_s42_fastq:
    """
    Test screed methods on the s42 fastq file
    """
    def setup(self):
        self.db = ScreedDB(tests42 + '_screed')

    def tearDown(self):
        del self.db
        gc.collect()

    def test_iteration(self):
        """
        Runs through the database, accessing each element by index and then by
        name
        """
        for idx in xrange(0, len(self.db)):
            rcrd = self.db.loadRecordByIndex(idx)
            nameRcrd = self.db[rcrd.name]
            assert rcrd == nameRcrd

    def test_dict_stuff(self):
        """
        Tests some dictionary methods on the database
        """
        keys = self.db.keys()
        ikeys = list(self.db.iterkeys())
        assert sorted(keys) == sorted(ikeys)
        del keys
        del ikeys
        gc.collect()

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert 'FOO' not in self.db

    def test_get(self):
        for k in self.db:
            record = self.db.get(k)
            assert record.name == k

            record = self.db[k]
            assert record.name == k

        assert self.db.get('FOO') is None
        try:
            self.db['FOO']
            assert False, "the previous line should raise a KeyError"
        except KeyError:
            pass

    def test_missing(self):
        """
        Make sure that unsupported dict attributes are actually missing.
        """
        db = self.db

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.update({})
            assert 0
        except AttributeError:
            pass

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.setdefault(None)
            assert 0
        except AttributeError:
            pass

        try:
            db.pop()
            assert 0
        except AttributeError:
            pass

        try:
            db.popitem()
            assert 0
        except AttributeError:
            pass

    def test_certain_records(self):
        """
        Pulls first, last, middle and few other records out of database and
        compares them to known quantities
        """
        testcases = {}
        testcases['HWI-EAS_4_PE-FC20GCB:4:1:257:604/2'] = {
            'id': 0,
            'annotations': '',
            'quality': 'AAAAAAAA:4>>AAA:44>>->-&4;8+8826;66.',
            'name': 'HWI-EAS_4_PE-FC20GCB:4:1:257:604/2',
            'sequence': 'TGTGGATAGTCGCCCGTGATGGCGTCGAAGTTCCGG'}

        testcases['HWI-EAS_4_PE-FC20GCB:4:330:96:902/2'] = {
            'id': 4148632,
            'annotations': '',
            'quality': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA??????',
            'name': 'HWI-EAS_4_PE-FC20GCB:4:330:96:902/2',
            'sequence': 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC'}

        testcases['HWI-EAS_4_PE-FC20GCB:4:166:158:532/2'] = {
            'id': 2074316,
            'annotations': '',
            'quality': 'AAAAAAA?A?AAAAAAA?A>A?A?AAAAAA?.<?-?',
            'name': 'HWI-EAS_4_PE-FC20GCB:4:166:158:532/2',
            'sequence': 'ATCGCCAATGCCCAGGCCTGGTTCTCTTTAACCTAT'}

        testcases['HWI-EAS_4_PE-FC20GCB:4:1:332:634/2'] = {
            'id': 3000,
            'annotations': '',
            'quality': '?A?AAAAAAAAA8>AAAAAA*AA?A?AA.?)<9)9?',
            'name': 'HWI-EAS_4_PE-FC20GCB:4:1:332:634/2',
            'sequence': 'ACCGTGCCAGATCAGAACCTAGTGGCGATTCCAATT'}

        testcases['HWI-EAS_4_PE-FC20GCB:4:242:843:13/2'] = {
            'id': 3111474,
            'annotations': '',
            'quality': "ABAAACA?CAAA??%A;2A;/5/&:?-*1-'11%71",
            'name': 'HWI-EAS_4_PE-FC20GCB:4:242:843:13/2',
            'sequence': 'GTTTCTATATTCTGGCGTTAGTCGTCGCCGATAATT'}

        for case in testcases:
            assert testcases[case] == self.db[case]


class Test_po_fasta:
    """
    Test screed methods on the pongo fasta file
    """
    def setup(self):
        self.db = ScreedDB(pongo + '_screed')

    def tearDown(self):
        del self.db
        gc.collect()

    def test_iteration(self):
        """
        Runs through the database, accessing each element by index and then by
        name
        """
        for idx in xrange(0, len(self.db)):
            rcrd = self.db.loadRecordByIndex(idx)
            nameRcrd = self.db[rcrd.name]
            assert rcrd == nameRcrd

    def test_dict_stuff(self):
        """
        Tests some dictionary methods on the database
        """
        keys = self.db.keys()
        ikeys = list(self.db.iterkeys())
        assert sorted(keys) == sorted(ikeys)
        del keys
        del ikeys
        gc.collect()

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert 'FOO' not in self.db

    def test_get(self):
        for k in self.db:
            record = self.db.get(k)
            assert record.name == k

            record = self.db[k]
            assert record.name == k

        assert self.db.get('FOO') is None
        try:
            self.db['FOO']
            assert False, "the previous line should raise a KeyError"
        except KeyError:
            pass

    def test_missing(self):
        """
        Make sure that unsupported dict attributes are actually missing.
        """
        db = self.db

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.update({})
            assert 0
        except AttributeError:
            pass

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.setdefault(None)
            assert 0
        except AttributeError:
            pass

        try:
            db.pop()
            assert 0
        except AttributeError:
            pass

        try:
            db.popitem()
            assert 0
        except AttributeError:
            pass

    def test_certain_records(self):
        """
        Pulls first, last, middle and few other records out of database and
        compares them to known quantities
        """
        testcases = {}
        testcases['GENSCAN00000032971'] = {
            'id': 0,
            'description': 'cdna:Genscan chromosome:PPYG2:6_qbl_hap2_random'
            ':95622:98297:1',
            'name': 'GENSCAN00000032971',
            'sequence': 'ATGGCGCCCCGAACCCTCCTCCTGCTGCTCTCGGCGGCCCTGGCCCCGAC'
            'CGAGACCTGG'}
        testcases['GENSCAN00000042282'] = {
            'id': 53997,
            'description': 'cdna:Genscan chromosome:PPYG2:1:229892060:22989'
            '2800:1',
            'name': 'GENSCAN00000042282',
            'sequence': 'ATGATGCCATTGCAAGGACCCTCTGCAGGGCCTCAGTCCCGAGGATGGCA'
            'CACAGCCTTC'}
        testcases['GENSCAN00000051311'] = {
            'id': 30780,
            'description': 'cdna:Genscan chromosome:PPYG2:10:132962172:132'
            '962871:1',
            'name': 'GENSCAN00000051311',
            'sequence': 'ATGACCCAGCCACCTACCAGGCCGCTCTGCAGACCCCCCACGGGAGCAGC'
            'CTCTGCCCCC'}
        testcases['GENSCAN00000006030'] = {
            'id': 1469,
            'description': 'cdna:Genscan chromosome:PPYG2:14_random:1765749'
            ':1766075:-1',
            'name': 'GENSCAN00000006030',
            'sequence': 'ATGTGTGGCAACAAGGGCATTTCTGCCTTCCCTGAATCAGACCACCTTTT'
            'CACATGGGTA'}
        testcases['GENSCAN00000048263'] = {
            'id': 43029,
            'description': 'cdna:Genscan chromosome:PPYG2:6:100388173:10048'
            '5454:-1',
            'name': 'GENSCAN00000048263',
            'sequence': 'ATGTGTCCCTTTGAATATGCCGGAGAACAACAGTTGCCATGGATGTGTTC'
            'TGGGGAGCCC'}

        for case in testcases:
            assert testcases[case]['name'] == self.db[case]['name']
            assert testcases[case]['description'] == \
                self.db[case]['description']
            assert str(self.db[case]['sequence']).startswith(
                testcases[case]['sequence']
            )


class Test_mus_fasta:
    """
    Test screed methods on the mus_musculus fasta file
    """
    def setup(self):
        self.db = ScreedDB(mus + '_screed')

    def tearDown(self):
        del self.db
        gc.collect()

    def test_iteration(self):
        """
        Runs through the database, accessing each element by index and then by
        name
        """
        for idx in xrange(0, len(self.db)):
            rcrd = self.db.loadRecordByIndex(idx)
            nameRcrd = self.db[rcrd.name]
            assert rcrd == nameRcrd

    def test_dict_stuff(self):
        """
        Tests some dictionary methods on the database
        """
        keys = self.db.keys()
        ikeys = list(self.db.iterkeys())
        assert sorted(keys) == sorted(ikeys)
        del keys
        del ikeys
        gc.collect()

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert 'FOO' not in self.db

    def test_get(self):
        for k in self.db:
            record = self.db.get(k)
            assert record.name == k

            record = self.db[k]
            assert record.name == k

        assert self.db.get('FOO') is None
        try:
            self.db['FOO']
            assert False, "the previous line should raise a KeyError"
        except KeyError:
            pass

    def test_missing(self):
        """
        Make sure that unsupported dict attributes are actually missing.
        """
        db = self.db

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.update({})
            assert 0
        except AttributeError:
            pass

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.setdefault(None)
            assert 0
        except AttributeError:
            pass

        try:
            db.pop()
            assert 0
        except AttributeError:
            pass

        try:
            db.popitem()
            assert 0
        except AttributeError:
            pass

    def test_certain_records(self):
        """
        Pulls first, last, middle and few other records out of database and
        compares them to known quantities
        """
        testcases = {}
        testcases['9'] = {
            'id': 0,
            'description': 'dna_rm:chromosome chromosome:NCBIM37:9:1:124076'
                           '172:1',
            'name': '9',
            'sequence': 'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN'
                        'NNNNNNNNNN'
        }

        for case in testcases:
            assert testcases[case]['name'] == self.db[case]['name']
            assert testcases[case]['description'] == \
                self.db[case]['description']
            assert str(self.db[case]['sequence']).startswith(
                testcases[case]['sequence']
            )


class Test_tri_fasta:
    """
    Test screed methods on the tri fasta file
    """
    def setup(self):
        self.db = ScreedDB(tri + '_screed')

    def tearDown(self):
        del self.db
        gc.collect()

    def test_iteration(self):
        """
        Runs through the database, accessing each element by index and then by
        name
        """
        for idx in xrange(0, len(self.db)):
            rcrd = self.db.loadRecordByIndex(idx)
            nameRcrd = self.db[rcrd.name]
            assert rcrd == nameRcrd

    def test_dict_stuff(self):
        """
        Tests some dictionary methods on the database
        """
        keys = self.db.keys()
        ikeys = list(self.db.iterkeys())
        assert sorted(keys) == sorted(ikeys)
        del keys
        del ikeys
        gc.collect()

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert 'FOO' not in self.db

    def test_get(self):
        for k in self.db:
            record = self.db.get(k)
            assert record.name == k

            record = self.db[k]
            assert record.name == k

        assert self.db.get('FOO') is None
        try:
            self.db['FOO']
            assert False, "the previous line should raise a KeyError"
        except KeyError:
            pass

    def test_missing(self):
        """
        Make sure that unsupported dict attributes are actually missing.
        """
        db = self.db

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.update({})
            assert 0
        except AttributeError:
            pass

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.setdefault(None)
            assert 0
        except AttributeError:
            pass

        try:
            db.pop()
            assert 0
        except AttributeError:
            pass

        try:
            db.popitem()
            assert 0
        except AttributeError:
            pass

    def test_certain_records(self):
        """
        Pulls first, last, middle and few other records out of database and
        compares them to known quantities
        """
        testcases = {}
        testcases['singleUn_100'] = {
            'id': 0,
            'description': '',
            'name': 'singleUn_100',
            'sequence': 'TTTAAACACGTGTCCGCGCCATTTTTTTATTTATTTACCGATCAAGTGCA'}
        testcases['singleUn_9'] = {
            'id': 2210,
            'description': '',
            'name': 'singleUn_9',
            'sequence': 'TTTAATTTTTTTACAACTCAAAATTTTGAGTAGTGTTTTAAATAGTACAC'}
        testcases['ChLG6'] = {
            'id': 2016,
            'description': '',
            'name': 'ChLG6',
            'sequence': 'CAAAAAAATTCATAACTCAAAAACTAAAAGTCGTAGAGCAATGCGGTTTG'}
        testcases['singleUn_286'] = {
            'id': 186,
            'description': '',
            'name': 'singleUn_286',
            'sequence': 'AAACTAAAACATCCTTTTCAGCATATTATTTGTTATATTTAAAAAAAAAC'}
        testcases['ChLG9'] = {
            'id': 2019,
            'description': '',
            'name': 'ChLG9',
            'sequence': 'CTGCCGATAATATTTCCTACCAGAAATAACCAATTTATTTTACGTATTAC'}

        for case in testcases:
            assert testcases[case]['name'] == self.db[case]['name']
            assert testcases[case]['description'] == \
                self.db[case]['description']
            assert str(self.db[case]['sequence']).startswith(
                testcases[case]['sequence']
            )


class Test_xeno_fasta:
    """
    Test screed methods on the xeno fasta file
    """
    def setup(self):
        self.db = ScreedDB(xeno + '_screed')

    def tearDown(self):
        del self.db
        gc.collect()

    def test_iteration(self):
        """
        Runs through the database, accessing each element by index and then by
        name
        """
        for idx in xrange(0, len(self.db)):
            rcrd = self.db.loadRecordByIndex(idx)
            nameRcrd = self.db[rcrd.name]
            assert rcrd == nameRcrd

    def test_dict_stuff(self):
        """
        Tests some dictionary methods on the database
        """
        keys = self.db.keys()
        ikeys = list(self.db.iterkeys())
        assert sorted(keys) == sorted(ikeys)
        del keys
        del ikeys
        gc.collect()

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert 'FOO' not in self.db

    def test_get(self):
        for k in self.db:
            record = self.db.get(k)
            assert record.name == k

            record = self.db[k]
            assert record.name == k

        assert self.db.get('FOO') is None
        try:
            self.db['FOO']
            assert False, "the previous line should raise a KeyError"
        except KeyError:
            pass

    def test_missing(self):
        """
        Make sure that unsupported dict attributes are actually missing.
        """
        db = self.db

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.update({})
            assert 0
        except AttributeError:
            pass

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.setdefault(None)
            assert 0
        except AttributeError:
            pass

        try:
            db.pop()
            assert 0
        except AttributeError:
            pass

        try:
            db.popitem()
            assert 0
        except AttributeError:
            pass

    def test_certain_records(self):
        """
        Pulls first, last, middle and few other records out of database and
        compares them to known quantities
        """
        testcases = {}
        testcases['scaffold_20095'] = {
            'id': 0,
            'description': 'dna:scaffold scaffold:JGI4.1:scaffold_20095:1:2'
                           '001:1',
            'name': 'scaffold_20095',
            'sequence': 'GATGAGATCACCTTTCATGCTTTTTGTATCCCTATTATCTAGAGACAACAA'
                        'ATCAGTTGC'}
        testcases['scaffold_1'] = {
            'id': 19500,
            'description': 'dna:scaffold scaffold:JGI4.1:scaffold_1:1:781781'
                           '4:1',
            'name': 'scaffold_1',
            'sequence': 'CCTCCCTTTTTGGCTGTCTTTTCACTGTATCATAGCCTGGCGTGAACCAAG'
                        'CCTCAAAAA'}
        testcases['scaffold_271'] = {
            'id': 19230,
            'description': 'dna:scaffold scaffold:JGI4.1:scaffold_271:1:156'
                           '7461:1',
            'name': 'scaffold_271',
            'sequence': 'CGATTTTTGCGGAAAAACGCGAGTTTTTGGTAGCCATTCCGAAAGTTGCGA'
                        'TTTTTTGTA'}
        testcases['scaffold_19901'] = {
            'id': 329,
            'description': 'dna:scaffold scaffold:JGI4.1:scaffold_19901:1:22'
                           '56:1',
            'name': 'scaffold_19901',
            'sequence': 'ATACCGCAAAGGTTTCTTTCTTCTCAGTGCTCCATGCTGCCTCTCTTGTTT'
                        'TGCCTCCCT'}
        testcases['scaffold_95'] = {
            'id': 19408,
            'description': 'dna:scaffold scaffold:JGI4.1:scaffold_95:1:28996'
                           '70:1',
            'name': 'scaffold_95',
            'sequence': 'CCCTCCTGGTGATCCCACTTCAATCTCCCCATAGGCACACATCACTTCTAG'
                        'CAGTTCACA'}

        for case in testcases:
            assert testcases[case]['name'] == self.db[case]['name']
            assert testcases[case]['description'] == \
                self.db[case]['description']
            assert str(self.db[case]['sequence']).startswith(
                testcases[case]['sequence']
            )


class Test_sorex_fasta:
    """
    Test screed methods on the sorex fasta file
    """
    def setup(self):
        self.db = ScreedDB(sorex + '_screed')

    def tearDown(self):
        del self.db
        gc.collect()

    def test_iteration(self):
        """
        Runs through the database, accessing each element by index and then by
        name
        """
        for idx in xrange(0, len(self.db)):
            rcrd = self.db.loadRecordByIndex(idx)
            nameRcrd = self.db[rcrd.name]
            assert rcrd == nameRcrd

    def test_dict_stuff(self):
        """
        Tests some dictionary methods on the database
        """
        keys = self.db.keys()
        ikeys = list(self.db.iterkeys())
        assert sorted(keys) == sorted(ikeys)
        del keys
        del ikeys
        gc.collect()

    def test_contains(self):
        for k in self.db:
            assert k in self.db

        assert 'FOO' not in self.db

    def test_get(self):
        for k in self.db:
            record = self.db.get(k)
            assert record.name == k

            record = self.db[k]
            assert record.name == k

        assert self.db.get('FOO') is None
        try:
            self.db['FOO']
            assert False, "the previous line should raise a KeyError"
        except KeyError:
            pass

    def test_missing(self):
        """
        Make sure that unsupported dict attributes are actually missing.
        """
        db = self.db

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.update({})
            assert 0
        except AttributeError:
            pass

        try:
            db.clear()
            assert 0
        except AttributeError:
            pass

        try:
            db.setdefault(None)
            assert 0
        except AttributeError:
            pass

        try:
            db.pop()
            assert 0
        except AttributeError:
            pass

        try:
            db.popitem()
            assert 0
        except AttributeError:
            pass

    def test_certain_records(self):
        """
        Pulls first, last, middle and few other records out of database and
        compares them to known quantities
        """
        testcases = {}
        testcases['scaffold_93039'] = {
            'id': 0,
            'description': 'dna:scaffold scaffold:COMMON_SHREW1:scaffold_93'
                           '039:1:203:1',
            'name': 'scaffold_93039',
            'sequence': 'GCTGAGCCTTGTAGTTCTGCTCCCTTTGACTGACGGCCCACTATGGACCG'
                        'GAAAAACTAC'}

        testcases['scaffold_107701'] = {
            'id': 1,
            'description': 'dna:scaffold scaffold:COMMON_SHREW1:scaffold_10'
                           '7701:1:203:1',
            'name': 'scaffold_107701',
            'sequence': 'TAAACCCAAAATAAACATTCCCCAAATTATATTTCTTCCTTTCCTTCTGA'
                        'ATAAAAGAAA'}

        testcases['GeneScaffold_6994'] = {
            'id': 243135,
            'description': 'dna:genescaffold genescaffold:COMMON_SHREW1:Gen'
                           'eScaffold_6994:1:2349312:1',
            'name': 'GeneScaffold_6994',
            'sequence': 'TATTGAGAGAAGTGGGAACTTCTCTAGTGGTGGGGTATGGTGATGGAATG'
                        'ATGTATGAAT'}

        testcases['scaffold_118324'] = {
            'id': 13823,
            'description': 'dna:scaffold scaffold:COMMON_SHREW1:scaffold_11'
                           '8324:1:884:1',
            'name': 'scaffold_118324',
            'sequence': 'CAGCCCCCTGCAACAAATTTTATACTCTAGAAACAGTTTAATGGCTGTTG'
                        'GAATATTTCC'}

        testcases['scaffold_92895'] = {
            'id': 14573,
            'description': 'dna:scaffold scaffold:COMMON_SHREW1:scaffold_92'
                           '895:1:890:1',
            'name': 'scaffold_92895',
            'sequence': 'GGGAAGCTTGCAAGGCTGTCCCATGTGGGCAGGAAGCTCTCAGTAGCTTG'
                        'CCAGTTTCTC'}

        testcases['scaffold_62271'] = {
            'id': 37101,
            'description': 'dna:scaffold scaffold:COMMON_SHREW1:scaffold_62'
                           '271:1:1064:1',
            'name': 'scaffold_62271',
            'sequence': 'AGAGTATCTCCCCCACATGGCAGAGCCTGGCAAGCTACCCATGGCGTATT'
                        'CAATATGCCA'}

        for case in testcases:
            assert testcases[case]['name'] == self.db[case]['name']
            assert testcases[case]['description'] == \
                self.db[case]['description']
            assert str(self.db[case]['sequence']).startswith(
                testcases[case]['sequence']
            )
