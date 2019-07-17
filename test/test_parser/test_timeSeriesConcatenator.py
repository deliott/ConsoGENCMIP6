from unittest import TestCase
from bin.parser.concatenate_into_time_serie import TimeSeriesConcatenator
import json


class TestTimeSeriesConcatenator(TestCase):

    maxDiff = None

    def setUp(self) -> None:
        self.mock_concat = TimeSeriesConcatenator('/home/edupont/ccc_myproject_data/mocks/mock_time_series')
        self.file_13 = 'Irene_gen0826_20190513.json'
        self.file_14 = 'Irene_gen0826_20190514.json'
        self.file_15 = 'Irene_gen0826_20190515.json'
        self.mock_concat.load_daily_data(self.file_13)

    def test_load_daily_data(self):
        self.mock_concat.load_daily_data(self.file_13)
        mock_dict_20190513 = {"date": "2019-05-13",
                              "project": "gen0826", "project_deadline": "2019-11-04", "machine": "Irene",
                              "processor_type": {
                                  "KNL": {
                                      "sous_projet": {
                                          "gen0826": {"subtotal": 59460.32,
                                                      "login_conso": {"desroche": 59460.32, "derickin": 0.0,
                                                                      "pierre": 0.0,
                                                                      "p24demus": 0.0, "p86fisa": 0.0, "p86mno": 0.0,
                                                                      "p86mnop": 0.0,
                                                                      "p86fann": 0.0, "francesc": 0.0}}},
                                      "total": 59460.32,
                                      "allocated": 200000.0},
                                  "Skylake": {
                                      "sous_projet": {
                                          "gen0826": {"subtotal": 6935.07,
                                                      "login_conso": {"desroche": 6295.58, "derickin": 3.13,
                                                                      "pierre": 0.0,
                                                                      "p24demus": 4.0, "p86fisa": 4.12,
                                                                      "p86mno": 622.33,
                                                                      "p86mnop": 1.04, "p86fann": 4.85,
                                                                      "francesc": 0.02}}},
                                      "total": 6935.07,
                                      "allocated": 40000.0}}}
        self.assertDictEqual(mock_dict_20190513, self.mock_concat.daily_dict)

    def test_set_daily_time(self):
        self.mock_concat.set_daily_time()
        self.assertEqual(self.mock_concat.daily_time, '2019-05-13')

        self.mock_concat.load_daily_data(self.file_14)
        self.mock_concat.set_daily_time()
        self.assertEqual(self.mock_concat.daily_time, '2019-05-14')

        self.mock_concat.load_daily_data(self.file_15)
        self.mock_concat.set_daily_time()
        self.assertEqual(self.mock_concat.daily_time, '2019-05-15')

    def test_remove_date_from_dailydict(self):
        self.mock_concat.remove_date_from_dailydict()
        mock_dict_20190513 = {
            "project": "gen0826", "project_deadline": "2019-11-04", "machine": "Irene", "processor_type": {
                "KNL": {
                     "sous_projet": {
                         "gen0826": {"subtotal": 59460.32, "login_conso": {"desroche": 59460.32, "derickin": 0.0, "pierre": 0.0, "p24demus": 0.0, "p86fisa": 0.0, "p86mno": 0.0, "p86mnop": 0.0, "p86fann": 0.0, "francesc": 0.0}}},
                     "total": 59460.32,
                     "allocated": 200000.0},
                "Skylake": {
                     "sous_projet": {
                         "gen0826": {"subtotal": 6935.07, "login_conso": {"desroche": 6295.58, "derickin": 3.13, "pierre": 0.0, "p24demus": 4.0, "p86fisa": 4.12, "p86mno": 622.33, "p86mnop": 1.04, "p86fann": 4.85, "francesc": 0.02}}},
                     "total": 6935.07,
                     "allocated": 40000.0}}
        }
        self.assertDictEqual(mock_dict_20190513, self.mock_concat.daily_dict)

    def test_add_dailydict_to_timeseries(self):
        self.mock_concat.set_daily_time()
        self.mock_concat.add_dailydict_to_timeseries()
        mock_timeseries_20190513 = {
            "2019-05-13": {
                "project": "gen0826", "project_deadline": "2019-11-04", "machine": "Irene", "processor_type": {
                    "KNL": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 59460.32,
                                        "login_conso": {"desroche": 59460.32, "derickin": 0.0, "pierre": 0.0,
                                                        "p24demus": 0.0, "p86fisa": 0.0, "p86mno": 0.0, "p86mnop": 0.0,
                                                        "p86fann": 0.0, "francesc": 0.0}}},
                        "total": 59460.32,
                        "allocated": 200000.0},
                    "Skylake": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 6935.07,
                                        "login_conso": {"desroche": 6295.58, "derickin": 3.13, "pierre": 0.0,
                                                        "p24demus": 4.0, "p86fisa": 4.12, "p86mno": 622.33,
                                                        "p86mnop": 1.04, "p86fann": 4.85, "francesc": 0.02}}},
                        "total": 6935.07,
                        "allocated": 40000.0}}
            }
        }
        self.assertDictEqual(self.mock_concat.time_series_dict, mock_timeseries_20190513)

        self.mock_concat.time_series_dict.clear()
        self.mock_concat.load_daily_data(self.file_14)
        self.mock_concat.set_daily_time()
        self.mock_concat.add_dailydict_to_timeseries()
        mock_timeseries_20190514 = {
            "2019-05-14": {
                "project": "gen0826", "project_deadline": "2019-11-04", "machine": "Irene", "processor_type": {
                    "KNL": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 59460.32,
                                        "login_conso": {"desroche": 59460.32, "derickin": 0.0, "pierre": 0.0,
                                                        "p24demus": 0.0, "p86fisa": 0.0, "p86mno": 0.0, "p86mnop": 0.0,
                                                        "p86fann": 0.0, "francesc": 0.0}}},
                        "total": 59460.32,
                        "allocated": 200000.0},
                    "Skylake": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 6935.07,
                                        "login_conso": {"desroche": 6295.58, "derickin": 3.13, "pierre": 0.0,
                                                        "p24demus": 4.0, "p86fisa": 4.12, "p86mno": 622.33,
                                                        "p86mnop": 1.04, "p86fann": 4.85, "francesc": 0.02}}},
                        "total": 6935.07,
                        "allocated": 40000.0}}
            }
        }
        self.assertDictEqual(self.mock_concat.time_series_dict, mock_timeseries_20190514)

        self.mock_concat.load_daily_data(self.file_15)
        self.mock_concat.set_daily_time()
        self.mock_concat.add_dailydict_to_timeseries()
        mock_timeseries_20190514_20190515 = {
            "2019-05-14": {
                "project": "gen0826", "project_deadline": "2019-11-04", "machine": "Irene", "processor_type": {
                    "KNL": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 59460.32,
                                        "login_conso": {"desroche": 59460.32, "derickin": 0.0, "pierre": 0.0,
                                                        "p24demus": 0.0, "p86fisa": 0.0, "p86mno": 0.0, "p86mnop": 0.0,
                                                        "p86fann": 0.0, "francesc": 0.0}}},
                        "total": 59460.32,
                        "allocated": 200000.0},
                    "Skylake": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 6935.07,
                                        "login_conso": {"desroche": 6295.58, "derickin": 3.13, "pierre": 0.0,
                                                        "p24demus": 4.0, "p86fisa": 4.12, "p86mno": 622.33,
                                                        "p86mnop": 1.04, "p86fann": 4.85, "francesc": 0.02}}},
                        "total": 6935.07,
                        "allocated": 40000.0}}
            },
            "2019-05-15": {
                "project": "gen0826", "project_deadline": "2019-11-04", "machine": "Irene", "processor_type": {
                    "KNL": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 59460.32,
                                        "login_conso": {"desroche": 59460.32, "derickin": 0.0, "pierre": 0.0,
                                                        "p24demus": 0.0, "p86fisa": 0.0, "p86mno": 0.0, "p86mnop": 0.0,
                                                        "p86fann": 0.0, "francesc": 0.0}}},
                        "total": 59460.32,
                        "allocated": 200000.0},
                    "Skylake": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 6935.07,
                                        "login_conso": {"desroche": 6295.58, "derickin": 3.13, "pierre": 0.0,
                                                        "p24demus": 4.0, "p86fisa": 4.12, "p86mno": 622.33,
                                                        "p86mnop": 1.04, "p86fann": 4.85, "francesc": 0.02}}},
                        "total": 6935.07,
                        "allocated": 40000.0}}
            }
        }
        self.assertDictEqual(self.mock_concat.time_series_dict, mock_timeseries_20190514_20190515)

    def test_set_file_list(self):
        self.mock_concat.set_file_list()
        self.assertEqual(len(self.mock_concat.file_list), 3)

    def test_create_timeseries(self):
        self.mock_concat.create_timeseries()
        mock_timeseries_20190513_20190514_20190515 = {
            "2019-05-13": {
                "project": "gen0826", "project_deadline": "2019-11-04", "machine": "Irene", "processor_type": {
                    "KNL": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 59460.32,
                                        "login_conso": {"desroche": 59460.32, "derickin": 0.0, "pierre": 0.0,
                                                        "p24demus": 0.0, "p86fisa": 0.0, "p86mno": 0.0, "p86mnop": 0.0,
                                                        "p86fann": 0.0, "francesc": 0.0}}},
                        "total": 59460.32,
                        "allocated": 200000.0},
                    "Skylake": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 6935.07,
                                        "login_conso": {"desroche": 6295.58, "derickin": 3.13, "pierre": 0.0,
                                                        "p24demus": 4.0, "p86fisa": 4.12, "p86mno": 622.33,
                                                        "p86mnop": 1.04, "p86fann": 4.85, "francesc": 0.02}}},
                        "total": 6935.07,
                        "allocated": 40000.0}}
            },
            "2019-05-14": {
                "project": "gen0826", "project_deadline": "2019-11-04", "machine": "Irene", "processor_type": {
                    "KNL": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 59460.32,
                                        "login_conso": {"desroche": 59460.32, "derickin": 0.0, "pierre": 0.0,
                                                        "p24demus": 0.0, "p86fisa": 0.0, "p86mno": 0.0, "p86mnop": 0.0,
                                                        "p86fann": 0.0, "francesc": 0.0}}},
                        "total": 59460.32,
                        "allocated": 200000.0},
                    "Skylake": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 6935.07,
                                        "login_conso": {"desroche": 6295.58, "derickin": 3.13, "pierre": 0.0,
                                                        "p24demus": 4.0, "p86fisa": 4.12, "p86mno": 622.33,
                                                        "p86mnop": 1.04, "p86fann": 4.85, "francesc": 0.02}}},
                        "total": 6935.07,
                        "allocated": 40000.0}}
            },
            "2019-05-15": {
                "project": "gen0826", "project_deadline": "2019-11-04", "machine": "Irene", "processor_type": {
                    "KNL": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 59460.32,
                                        "login_conso": {"desroche": 59460.32, "derickin": 0.0, "pierre": 0.0,
                                                        "p24demus": 0.0, "p86fisa": 0.0, "p86mno": 0.0, "p86mnop": 0.0,
                                                        "p86fann": 0.0, "francesc": 0.0}}},
                        "total": 59460.32,
                        "allocated": 200000.0},
                    "Skylake": {
                        "sous_projet": {
                            "gen0826": {"subtotal": 6935.07,
                                        "login_conso": {"desroche": 6295.58, "derickin": 3.13, "pierre": 0.0,
                                                        "p24demus": 4.0, "p86fisa": 4.12, "p86mno": 622.33,
                                                        "p86mnop": 1.04, "p86fann": 4.85, "francesc": 0.02}}},
                        "total": 6935.07,
                        "allocated": 40000.0}}
            }
        }
        self.assertDictEqual(self.mock_concat.time_series_dict, mock_timeseries_20190513_20190514_20190515)

    def test_suppress_zeroes_from_timeseries(self):
        self.mock_concat.create_timeseries()
        self.mock_concat.suppress_zeroes_from_timeseries()

        path_to_mock_timeseries_without_zeroes = "/home/edupont/ccc_myproject_data/mocks/mock_time_series/timeseries_gen0826_Irene_from_20190513_to_20190515_without_zeroes.json"
        with open(path_to_mock_timeseries_without_zeroes) as file_object:
            # store file data in object
            mock_clean_timeseries = json.load(file_object)


        self.assertDictEqual(mock_clean_timeseries, self.mock_concat.time_series_dict)



    def test_get_timeseries_name(self):
        name = self.mock_concat.get_timeseries_name()
        self.assertEqual(name, 'timeseries.json')

        self.mock_concat.create_timeseries()
        name = self.mock_concat.get_timeseries_name()
        self.assertEqual(name, 'timeseries_gen0826_Irene_from_20190513_to_20190515.json')

    # def test_dump_dict_to_json(self):
    #     self.mock_concat.create_timeseries()
    #
    #     self.mock_concat.dump_dict_to_json()
    #     self.fail()

if __name__ == '__main__':
    unittest.main()