from unittest import TestCase
from bin.jobs.libconso_py37 import parse_config

# @TODO: Test the rest of the function before splitting it. Just basic outputs are tested here

class TestParse_config(TestCase):

    def setUp(self):
        #self.path = '../tests/config_test.ini/'
        self.path = '/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/tests/config_test.ini'
    def test_parse_config(self):
        self.assertEqual(2, 2)

    def test_project_name(self):
        project_name, DIR, OUT = parse_config(self.path)
        self.assertEqual(project_name, 'gencmip6_conso')

    def test_project_directories(self):
        project_name, DIR, OUT = parse_config(self.path)
        self.assertEqual(DIR["ROOT_DIR"], '/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6')
        self.assertEqual(DIR["DATA"], '/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/output')
        self.assertEqual(DIR["PLOT"], '/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/plot')
        self.assertEqual(DIR["SAVE"], '/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/SORTIES/SAVE')
        self.assertEqual(DIR["SAVEDATA"], '/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/SORTIES/SAVE/data_conso')
        self.assertEqual(DIR["SAVEPLOT"], '/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/SORTIES/SAVE/plot')


    def test_project_files(self):
        project_name, DIR, OUT = parse_config(self.path)
        self.assertEqual(OUT["PARAM"], '/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/OUT_CONSO_PARAM')
        self.assertEqual(OUT["BILAN"], 'OUT_CONSO_BILAN')
        self.assertEqual(OUT["UTHEO"], '/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/OUT_CONSO_UTHEO')
        self.assertEqual(OUT["LOGIN"], 'OUT_CONSO_LOGIN')
        self.assertEqual(OUT["STORE"], 'OUT_CONSO_STORE')
        self.assertEqual(OUT["SINIT"], 'OUT_CONSO_STORE_INIT')
        self.assertEqual(OUT["CCCMP"], 'ccc_myproject.dat')
        self.assertEqual(OUT["JOBS"], 'OUT_JOBS_PENDING')
        self.assertEqual(OUT["JOBSF"], 'OUT_JOBS_PEN_FULL')





if __name__ == '__main__':
    unittest.main()