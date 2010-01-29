import sys, os, gc

thisdir = os.path.dirname(__file__)
libdir = os.path.abspath(os.path.join(thisdir, '..', 'sqeaqr'))
sys.path.insert(0, libdir)
import sqeaqrDB
#import fqByIntDict
#import fqByNameDict
#import faByIntDict
#import faByNameDict
import sqeaqrExtension
from seqparse import read_fastq_sequences
from seqparse import read_fasta_sequences

testfa = os.path.join(thisdir, 'test.fa')
testfq = os.path.join(thisdir, 'test.fastq')
testha = os.path.join(thisdir, 'test.hava')

#def setup():
    # index databases
#    read_fasta_sequences(testfa)
#    read_hava_sequences(testha)
#    read_fastq_sequences(testfq)

#def teardown():
#    os.unlink(testfq + sqeaqrExtension.fileExtension)
#    os.unlink(testfa + sqeaqrExtension.fileExtension)

## class Test_hava_methods(object):
##     """
##     Make sure that screed can retrieve even retrieve data from imaginary filetypes, like HAVA
##     """
##     def setup(self):
##         self.db = dbr.dbread(testha)

##     def test_contains(self):
##         assert "test_006" in self.db

##     def test_beginning_key_retrieval(self):
##         result = self.db['test_000']
##         assert result.hava == 'test_000'
##         assert result.quarzk == 'ACGGTGACGGTCACCGTCGACGGCCCAAGCCCATCGAACGTACCACCCCCACCTATCGTCACGCTGGTGGAGAGCCAATG'
##         assert result.muchalo == 'AFPPCLHBCCILGMMOCHKNNDBKCCPNHAMKJOCCDJAOEPNMHFHCBAJOKEMMMBHCPHIOAEPFFCAOJPGIMKGK'
##         assert result.fakours == '21858316587186112771945148345529452186568176931571171542294878855181415261425688'
##         assert result.selimizicka == 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
##         assert result.marshoon == 'C7AF246AC7AAEABE5A557FCBC6FD5F5263BCDE4E745BEF1GG7DD1AB511GBC63A4GF1F4E1A154B35D'

##     def test_middle_key_retrieval(self):
##         result = self.db['test_0063']
##         assert result.hava == 'test_0063'
##         assert result.quarzk == 'CAACACGATCAAGTTTGGTAAGAATTCCGCCTTAAGCTTTCTAGAACGATAGTTGCCCCCAATCTGGTTCGAAATCTCTT'
##         assert result.muchalo == 'GMDAPLMOOFANDHHMLBPIKGHIAFFFOABFMNNJNIJILEEFEPOCAJLNDLIFBPMGKOFJIEFAHNJPIOFAJMLM'
##         assert result.fakours == '39236397139389852275613887648533427438439122136418369146118333919885587613673488'
##         assert result.selimizicka == 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
##         assert result.marshoon == 'FC25E2CFC2BAFA7A2AA4757F3GFFFEE37G7752FCDBAEADBA1AC7374FB5C15552E6E2GG6GFF62C6GE'

##     def test_end_key_retrieval(self):
##         result = self.db['test_00124']
##         assert result.hava == 'test_00124'
##         assert result.quarzk == 'ATCGCAACCGTTTCCCCTATCTGGCAATTGAATCCGCGTCCTAAAACGAAAGCTTATCCCTGGCGAGGCACGCTAGGCCT'
##         assert result.muchalo == 'CIHNCECANFNLKGCHNOEHJDHADHPAEMMNKGMMMPDOBMOCKNBCMCPHEBEOINHMBMMGCHEMOIOAPEFPDDJP'
##         assert result.fakours == '32736451148353713169532559587626971677814946924334424648676283848861393812686731'
##         assert result.selimizicka == 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
##         assert result.marshoon == '4FE5FDD76CC5DE4DC2F25AA2GFBD7BEG326C6D7AB5B71GA67BAFD63AE1A562CDC1C2D157G6EF17CD'

class Test_fastq_int(object):
    def setup(self):
        read_fastq_sequences(testfq)
        self.db = sqeaqrDB.sqeaqrDB(testfq)

    def teardown(self):
        os.unlink(testfq + sqeaqrExtension.fileExtension)

    def test_length(self):
        assert len(self.db) == 125

    def test_keys(self):
        for key in self.db:
            assert key == self.db[key].id

    def test_contains_front(self):
        first = self.db[1]
        assert first.id == 1
        assert first.name == 'HWI-EAS_4_PE-FC20GCB:2:1:492:573/2'
        assert first.sequence == 'ACAGCAAAATTGTGATTGAGGATGAAGAACTGCTGT'
        assert first.accuracy == 'AA7AAA3+AAAAAA.AAA.;7;AA;;;;*;<1;<<<'

    def test_contains_middle(self):
        middle = self.db[63]
        assert middle.id == 63
        assert middle.name == 'HWI-EAS_4_PE-FC20GCB:2:1:245:483/2'
        assert middle.sequence == 'TGTCGAGCAAAGCAAAACAGGCGTAAAAATTGCCAT'
        assert middle.accuracy == 'AAAAAAAAAAAAAAAAAAAAA>AAAAAAAA?9>6><'

    def test_contains_end(self):
        end = self.db[125]
        assert end.id == 125
        assert end.name == 'HWI-EAS_4_PE-FC20GCB:2:1:350:588/2'
        assert end.sequence == 'GGTACAAAATAGATGCTGGACTCTCCGAATCCTATA'
        assert end.accuracy == ';?5AAAAAAAAAA?A??;?AA;AAA>AAAA?4?844'

    def test_contains(self):
        for k in self.db:
            assert self.db.has_key(k)

        assert not 0 in self.db

    def test_iterv(self):
        entries = []
        for entry in self.db:
            entries.append(self.db[entry])

        ivalues = list(self.db.itervalues())
        assert sorted(entries) == sorted(ivalues)

    def test_iteri(self):
        for id, entry in self.db.iteritems():
            assert id == self.db[entry.id].id
            assert entry == self.db[entry.id]

class Test_fastq_name(object):
    def setup(self):
        read_fastq_sequences(testfq)
        self.db = sqeaqrDB.sqeaqrDB(testfq, 'name')

    def teardown(self):
        os.unlink(testfq + sqeaqrExtension.fileExtension)

    def test_length(self):
        assert len(self.db) == 125

    def test_keys(self):
        for key in self.db:
            assert key == self.db[key].name

    def test_contains_front(self):
        first = self.db[self.db.keys()[0]]
        assert first.id == 1
        assert first.name == 'HWI-EAS_4_PE-FC20GCB:2:1:492:573/2'
        assert first.sequence == 'ACAGCAAAATTGTGATTGAGGATGAAGAACTGCTGT'
        assert first.accuracy == 'AA7AAA3+AAAAAA.AAA.;7;AA;;;;*;<1;<<<'

    def test_contains_middle(self):
        middle = self.db[self.db.keys()[62]]
        assert middle.id == 63
        assert middle.name == 'HWI-EAS_4_PE-FC20GCB:2:1:245:483/2'
        assert middle.sequence == 'TGTCGAGCAAAGCAAAACAGGCGTAAAAATTGCCAT'
        assert middle.accuracy == 'AAAAAAAAAAAAAAAAAAAAA>AAAAAAAA?9>6><'

    def test_contains_end(self):
        end = self.db[self.db.keys()[124]]
        assert end.id == 125
        assert end.name == 'HWI-EAS_4_PE-FC20GCB:2:1:350:588/2'
        assert end.sequence == 'GGTACAAAATAGATGCTGGACTCTCCGAATCCTATA'
        assert end.accuracy == ';?5AAAAAAAAAA?A??;?AA;AAA>AAAA?4?844'

    def test_contains(self):
        for k in self.db:
            assert self.db.has_key(k)

        assert not 'FOO' in self.db

    def test_iterv(self):
        entries = []
        for entry in self.db:
            entries.append(self.db[entry])

        ivalues = list(self.db.itervalues())
        assert sorted(entries) == sorted(ivalues)

    def test_iteri(self):
        for id, entry in self.db.iteritems():
            assert id == self.db[entry.name].id
            assert entry == self.db[entry.name]

class Test_fasta_int(object):
    def setup(self):
        read_fasta_sequences(testfa)
        self.db = sqeaqrDB.sqeaqrDB(testfa)

    def teardown(self):
        os.unlink(testfa + sqeaqrExtension.fileExtension)

    def test_length(self):
        assert len(self.db) == 22

    def test_keys(self):
        for key in self.db:
            assert key == self.db[key].id

    def test_contains_front(self):
        first = self.db[1]
        assert first.id == 1
        assert first.name == 'ENSMICT00000012722'
        assert first.description == 'cdna:pseudogene scaffold:micMur1:scaffold_185008:9:424:1 gene:ENSMICG00000012730'
        assert first.sequence.startswith('TGCAGAAAATATCAAGAGTCAGCAGAAAAACTATACAAGGGCTGGTATTTTGATTATTCT')

    def test_contains_middle(self):
        middle = self.db[11]
        assert middle.id == 11
        assert middle.name == 'ENSMICT00000012078'
        assert middle.description == 'cdna:pseudogene scaffold:micMur1:scaffold_180699:3:774:-1 gene:ENSMICG00000012085'
        assert middle.sequence.startswith('GCGCACTCCCAGTGGCTACCCACGGCAGGAGGCGGCGGCAGTGACTGGGCCGGCGGCCCG')

    def test_contains_end(self):
        end = self.db[22]
        assert end.id == 22
        assert end.name == 'ENSMICT00000003880'
        assert end.description == 'cdna:novel scaffold:micMur1:scaffold_175819:130:631:1 gene:ENSMICG00000003884'
        assert end.sequence.startswith('ATGCTGCCTAAGTTTGACCCCAACGCGATCAAAGTCATGTACCTGAGGTGCACGGGTGGC')

    def test_contains(self):
        for k in self.db:
            assert self.db.has_key(k)

        assert not 'FOO' in self.db

    def test_iterv(self):
        entries = []
        for entry in self.db:
            entries.append(self.db[entry])

        ivalues = list(self.db.itervalues())
        assert sorted(entries) == sorted(ivalues)

    def test_iteri(self):
        for id, entry in self.db.iteritems():
            assert id == self.db[entry.id].id
            assert entry == self.db[entry.id]

class Test_fasta_name(object):
    def setup(self):
        read_fasta_sequences(testfa)
        self.db = sqeaqrDB.sqeaqrDB(testfa, 'name')

    def teardown(self):
        os.unlink(testfa + sqeaqrExtension.fileExtension)

    def test_length(self):
        assert len(self.db) == 22

    def test_keys(self):
        for key in self.db:
            assert key == self.db[key].name

    def test_contains_front(self):
        first = self.db[self.db.keys()[0]]
        assert first.id == 1
        assert first.name == 'ENSMICT00000012722'
        assert first.description == 'cdna:pseudogene scaffold:micMur1:scaffold_185008:9:424:1 gene:ENSMICG00000012730'
        assert first.sequence.startswith('TGCAGAAAATATCAAGAGTCAGCAGAAAAACTATACAAGGGCTGGTATTTTGATTATTCT')

    def test_contains_middle(self):
        middle = self.db[self.db.keys()[10]]
        assert middle.id == 11
        assert middle.name == 'ENSMICT00000012078'
        assert middle.description == 'cdna:pseudogene scaffold:micMur1:scaffold_180699:3:774:-1 gene:ENSMICG00000012085'
        assert middle.sequence.startswith('GCGCACTCCCAGTGGCTACCCACGGCAGGAGGCGGCGGCAGTGACTGGGCCGGCGGCCCG')

    def test_contains_end(self):
        end = self.db[self.db.keys()[21]]
        assert end.id == 22
        assert end.name == 'ENSMICT00000003880'
        assert end.description == 'cdna:novel scaffold:micMur1:scaffold_175819:130:631:1 gene:ENSMICG00000003884'
        assert end.sequence.startswith('ATGCTGCCTAAGTTTGACCCCAACGCGATCAAAGTCATGTACCTGAGGTGCACGGGTGGC')

    def test_contains(self):
        for k in self.db:
            assert self.db.has_key(k)

        assert not 'FOO' in self.db

    def test_iterv(self):
        entries = []
        for entry in self.db:
            entries.append(self.db[entry])

        ivalues = list(self.db.itervalues())
        assert sorted(entries) == sorted(ivalues)

    def test_iteri(self):
        for id, entry in self.db.iteritems():
            assert id == self.db[entry.name].id
            assert entry == self.db[entry.name]

## class Test_dict_methods(object):
##     """
##     Make sure that screed returns sensible results for standard dictionary
##     queries.
##     """
##     def setup(self):
##         self.db = dbr.dbread(testfa)

##     def test_iter_stuff(self):
##         db = self.db
##         keys = db.keys()
##         ikeys = list(db.iterkeys())
##         assert sorted(keys) == sorted(ikeys)

##         values = db.values()
##         ivalues = list(db.itervalues())
##         assert sorted(values) == sorted(ivalues)

##         items = db.items()
##         iitems = list(db.iteritems())
##         assert sorted(items) == sorted(iitems)

##     def test_contains(self):
##         for k in self.db:
##             assert self.db.has_key(k)

##         assert not self.db.has_key('FOO')
            
##     def test_contains(self):
##         for k in self.db:
##             assert k in self.db

##         assert not 'FOO' in self.db

##     def test_get(self):
##         for k in self.db:
##             record = self.db.get(k)
##             assert record.name == k

##             record = self.db[k]
##             assert record.name == k

##         assert self.db.get('FOO') == None
##         try:
##             self.db['FOO']
##             assert False, "the previous line should raise a KeyError"
##         except KeyError:
##             pass

##     def test_missing(self):
##         """
##         Make sure that unsupported dict attributes are actually missing.
##         """
##         db = self.db

##         try:
##             db.clear()
##             assert 0
##         except AttributeError:
##             pass

##         try:
##             db.update({})
##             assert 0
##         except AttributeError:
##             pass

##         try:
##             db.clear()
##             assert 0
##         except AttributeError:
##             pass

##         try:
##             db.setdefault(None)
##             assert 0
##         except AttributeError:
##             pass

##         try:
##             db.pop()
##             assert 0
##         except AttributeError:
##             pass

##         try:
##             db.popitem()
##             assert 0
##         except AttributeError:
##             pass

## class Test_pyx_err:
##     def setup(self):
##         self.db = dbr.dbread(testfa)

##     def teardown(self):
##         self.db.clearErrorFlag()

##     def test_open(self):
##         try:
##             foo = dbr.dbread('foobar')
##         except dbr.DbException, e:
##             assert e.value == 'Invalid database filename'

##     def test_loadrecord(self): 
##         try:
##             self.db.loadRecordByIndex(-1)
##         except dbr.DbException, e:
##             assert e.value == 'Index query out of range'

##     def test_clear(self):
##         try:
##             self.db.loadRecordByIndex(-1) # makes sure the error is raised
##             assert 1 == 0, "Not raising an exception with loading bad record"
##         except dbr.DbException:
##             pass

## #        try: # doesn't clear the last error so should raise another exception
## #            self.db.getFieldValue('name')
## #        except dbr.DbException, e:
## #            assert e.value == 'Invalid query'
## # @CTB

##     def test_typename(self):
##         if 0:                           # @@CTB
##             try:
##                 print self.db.getFieldValue('FOOBAR')
##             except dbr.DbException, e:
##                 assert e.value == 'Invalid typename query'

##     def test_typekey(self):
##         if 0:                           # @@CTB
##             try:
##                 self.db.getFieldName(10)
##             except dbr.DbException, e:
##                 assert e.value == 'Bad typekey request'

## class Test_pyx_Fasta:
##     def setup(self):
##         self.db = dbr.dbread(testfa)

##     def test_delete(self):
##         gc.collect()
        
##         db = dbr.dbread(testfa)
##         del db

##         gc.collect()
        

##     def test_simple(self):
##         db = self.db
##         assert len(db.fields) == 3

##         fields = list(db.fields)
##         fields.sort()
##         assert fields == ['description', 'name', 'sequence']
        
##         assert len(db) == 22

##         record = db.loadRecordByIndex(0)
        
##         assert record['description'].startswith('cdna:pseudogene ')
##         assert record['name'] == 'ENSMICT00000012722'
##         assert record['sequence'].startswith('TGCAGAAAATATCAAGAGTC')

##     def test_bag_attr(self):
##         db = self.db
##         assert len(db.fields) == 3

##         record = db.loadRecordByIndex(0)

##         assert record['description'] == record.description
##         assert record['name'] == record.name
##         assert record['sequence'] == record.sequence
        
##     def test_iter(self):
##         for i, k in enumerate(self.db):
##             record = self.db[k]
##             record2 = self.db.loadRecordByIndex(i)
##             assert record.name == record2.name

##     def test_name_hashing(self):
##         db = self.db
##         for k in db:
##             record = db[k]
##             record2 = db.loadRecordByName(record['name'])
##             assert record == record2

## class Test_pyx_FastQ:
##     def setup(self):
##         self.db = dbr.dbread(testfq)

##     def test_simple(self):
##         db = self.db
##         assert len(db.fields) == 3
##         assert len(db) == 125

##         fields = list(db.fields)
##         fields.sort()
##         assert fields == ['accuracy', 'name', 'sequence']

##         record = db.loadRecordByIndex(0)

##         assert record['accuracy'] == 'AA7AAA3+AAAAAA.AAA.;7;AA;;;;*;<1;<<<', record['accuracy']
##         assert record['name'] == 'HWI-EAS_4_PE-FC20GCB:2:1:492:573/2'
##         assert record['sequence'] == 'ACAGCAAAATTGTGATTGAGGATGAAGAACTGCTGT'

##     def test_bag(self):
##         db = self.db

##         record = db.loadRecordByIndex(0)
##         assert record['accuracy'] == record.accuracy
##         assert record['name'] == record.name
##         assert record['sequence'] == record.sequence

##     def test_iter(self):
##         for i, k in enumerate(self.db):
##             record = self.db[k]
##             record2 = self.db.loadRecordByIndex(i)
##             assert record.name == record2.name
            
##     def test_name_hashing(self):
##         db = self.db
##         for k in db:
##             record = db[k]
##             record2 = db.loadRecordByName(record['name'])
##             assert record == record2
            
