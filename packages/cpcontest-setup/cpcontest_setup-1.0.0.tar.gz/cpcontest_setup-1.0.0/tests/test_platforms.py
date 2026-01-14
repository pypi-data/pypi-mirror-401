import unittest
import os
import tempfile
import shutil
from cpcontest.platforms import CodeforcesContest, RPCContest, GenericContest


class TestPlataformas(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_codeforces_contest_creation(self):
        """Test creación de concurso Codeforces"""
        contest = CodeforcesContest(self.temp_dir, "cpp", "Linux")
        self.assertIsNotNone(contest)
    
    def test_rpc_contest_creation(self):
        """Test creación de ronda RPC"""
        contest = RPCContest(self.temp_dir, "cpp", "Linux")
        self.assertIsNotNone(contest)
    
    def test_generic_contest_creation(self):
        """Test creación de concurso genérico"""
        contest = GenericContest(self.temp_dir, "cpp", "Linux")
        self.assertIsNotNone(contest)


if __name__ == "__main__":
    unittest.main()