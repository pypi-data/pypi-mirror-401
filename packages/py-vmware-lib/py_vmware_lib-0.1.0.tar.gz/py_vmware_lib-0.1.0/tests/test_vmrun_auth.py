import unittest
from unittest.mock import patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from py_vmware_lib.utils import VMRunBase


class DummyControl(VMRunBase):
    def __init__(self):
        self.vmrun_path = "vmrun"


class TestVMRunAuthFlags(unittest.TestCase):
    @patch("py_vmware_lib.utils.subprocess.run")
    def test_no_auth_flags(self, mock_run):
        mock_run.return_value.stdout = ""
        mock_run.return_value.returncode = 0
        ctrl = DummyControl()
        ctrl._run_command("list", [])
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args, ["vmrun", "list"])

    @patch("py_vmware_lib.utils.subprocess.run")
    def test_all_auth_flags(self, mock_run):
        mock_run.return_value.stdout = ""
        mock_run.return_value.returncode = 0
        ctrl = DummyControl()
        ctrl.set_host_type("ws").set_vm_password("vmpass").set_guest_credentials("user", "pass")
        ctrl._run_command("list", ["arg1"])
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(
            args,
            ["vmrun", "-T", "ws", "-vp", "vmpass", "-gu", "user", "-gp", "pass", "list", "arg1"],
        )


if __name__ == "__main__":
    unittest.main()
