from unittest import TestCase, TestLoader
import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().index('Merger')]+'Merger')
sys.path.append(os.getcwd()[:os.getcwd().index('Merger')]+'Merger/MergeTypes')
from AlphaSimMerge import AlphaSimMerge


class TestAlphaSimMerge(TestCase):

    def test_read_generator(self):
        asm = AlphaSimMerge('test', 'test', 'test', 'test', 'test', 'test', 9)
        with self.assertRaises(NotImplementedError) as context:
            asm.read_generator()
        self.assertTrue('AlphaSimMerge uses a different read methodology' in context.exception)

    def test_map_generator(self):
        asm = AlphaSimMerge('test', 'Tests/TestFiles/SnpInformation.txt', 'test', 'test', 'test', 'test', 9)
        map_gen = asm.map_generator()
        expected_line = '1	1	0.0000049361	1\n'
        self.assertEquals(map_gen.next(), expected_line)

    def test_ped_generator(self):
        asm = AlphaSimMerge('test', 'test', 'Tests/TestFiles/Pedigree.txt', 'Tests/TestFiles/Gender.txt',
                            'Tests/TestFiles/Genotype.txt', 'Tests/TestFiles/SnpSolutions.txt', 9)
        ped_line = asm.ped_generator().next()
        self.assertTrue(ped_line.startswith('1\t1\t0\t0\t2\t0.0000017752\t0 B 0 0 A A'))

    def test_pedigree_generator(self):
        asm = AlphaSimMerge('test', 'test', 'Tests/TestFiles/Pedigree.txt', 'test', 'test', 'test', 9)
        ped_tuple = asm.pedigree_generator().next()
        self.assertEquals(ped_tuple, ('1', '0', '0', '1.0544434262'))

    def test_snp_solution_generator(self):
        asm = AlphaSimMerge('test', 'test', 'Tests/TestFiles/Pedigree.txt', 'Tests/TestFiles/Gender.txt',
                            'Tests/TestFiles/Genotype.txt', 'Tests/TestFiles/SnpSolutions.txt', 9)
        ped_tuple = asm.snp_solution_generator().next()
        self.assertEquals(ped_tuple, ('1', '0', '0', '0.0000017752'))

    def test_gender_generator(self):
        asm = AlphaSimMerge('test', 'test', 'test', 'Tests/TestFiles/Gender.txt',
                            'test', 'test', 9)
        gender_tuple = asm.gender_generator().next()
        self.assertEquals(gender_tuple, ('1', '2'))

    def test_genotype_generator(self):
        asm = AlphaSimMerge('test', 'test', 'test', 'test',
                            'Tests/TestFiles/Genotype.txt', 'test', 9)
        geno_tuple = asm.genotype_generator().next()
        self.assertEquals(geno_tuple[0], '1')
        self.assertTrue(geno_tuple[1].startswith('0 B 0 0 A A B'))


def get_test_suite():
    return TestLoader().loadTestsFromTestCase(TestAlphaSimMerge)
