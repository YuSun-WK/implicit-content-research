import unittest
from unittest.mock import patch
from scripts.gpu_monitor import process_gpu_mib
class MemoryTests(unittest.TestCase):
 @patch('scripts.gpu_monitor.query_processes',return_value={999999:100})
 @patch('scripts.gpu_monitor.namespace_pids',return_value={123})
 def test_missing_mapping_is_null_not_zero(self,*_):self.assertIsNone(process_gpu_mib('0'))
 @patch('scripts.gpu_monitor.query_processes',return_value={999999:100,888888:30000})
 def test_bound_host_pid_only(self,*_):self.assertEqual(process_gpu_mib('0',999999),100)
