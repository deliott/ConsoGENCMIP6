from unittest import TestCase
from bin.pandas_plot import get_project_name


class TestGet_project_name(TestCase):
    def test_get_project_name(self):
        self.assertEqual(get_project_name("/home/edupont/data_conso/conso_anacmip6.dat"), 'anacmip6')


    def test_path_too_small(self):
        self.assertRaises(IndexError, get_project_name, "0")
        self.assertRaises(IndexError, get_project_name, "01")
        self.assertRaises(IndexError, get_project_name, "012")
        self.assertRaises(IndexError, get_project_name, "0123")
        self.assertRaises(IndexError, get_project_name, "01234")
        self.assertRaises(IndexError, get_project_name, "012345")
        self.assertRaises(IndexError, get_project_name, "0123456")
        self.assertRaises(IndexError, get_project_name, "01234567")
        self.assertRaises(IndexError, get_project_name, "01234567.")
        self.assertRaises(IndexError, get_project_name, "01234567.d")
        self.assertRaises(IndexError, get_project_name, "01234567.da")
        self.assertEqual(get_project_name("01234567.dat"), '01234567')

    def test_portabilite(self):
        self.assertEqual(get_project_name("/home/edupont/data_conso/conso_anacmip6.dat"), 'anacmip6')
        self.assertEqual(get_project_name("/home/eldupont/data_conso/conso_geocmip6.dat"), 'geocmip6')
        self.assertEqual(get_project_name("/ccc/cont003/home/gencmip6/oboucher/CONSO/IRENE/conso_volcmip6.dat"),\
                         'volcmip6')


if __name__ == '__main__':
    unittest.main()
