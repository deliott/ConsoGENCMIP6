from unittest import TestCase
from bin.ccc_myproject_parser import Project


class TestProject(TestCase):

    def test_parser_init_(self):
            project = Project("gencmip6")
            self.assertEqual(project.name, "gencmip6")

        # def test_parse_config(self):
        #     self.assertEqual(True, True)
