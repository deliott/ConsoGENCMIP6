import unittest
from unittest import TestCase
import datetime
from bin.jobs.libconso_py37 import Project

class TestProject(TestCase):
    def test_load_data_utheo(self):
        project = Project('gencmip6')
        path1 = u'/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/OUT_CONSO_UTHEO_20190604'
        result1_dates = (datetime.datetime(2019, 5, 13, 0, 0), datetime.datetime(2019, 5, 14, 0, 0), datetime.datetime(2019, 5, 15, 0, 0), datetime.datetime(2019, 5, 16, 0, 0))
        result1_utheos = (0.0329, 0.0356, 0.0384, 0.0411)

        dates1, utheos1 = project.load_data_utheo(path1)

        self.assertTupleEqual(result1_dates, dates1)
        self.assertTupleEqual(result1_utheos, utheos1)


        path2 = u'/home/edupont/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/OUT_CONSO_UTHEO_20181204'
        result2_dates = (datetime.datetime(2018, 12, 3, 0, 0), datetime.datetime(2018, 12, 4, 0, 0),
                         datetime.datetime(2018, 12, 5, 0, 0))
        # result2_utheos = (0.2612, 0.3033, 0.3128)
        #
        dates2, utheos2 = project.load_data_utheo(path2)
        #
        # self.assertTupleEqual(result2_dates, dates2)
        # self.assertTupleEqual(result2_utheos, utheos2)





if __name__ == '__main__':
    unittest.main()
