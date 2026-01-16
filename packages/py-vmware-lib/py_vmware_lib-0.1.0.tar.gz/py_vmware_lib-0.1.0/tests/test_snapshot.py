import unittest
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from py_vmware_lib.snapshot import SnapshotControl


class TestSnapshotControl(unittest.TestCase):
    def setUp(self):
        self.vmx_path = r"E:\win764\Windows 7 x64.vmx"

        with patch('py_vmware_lib.utils.VMRunBase.__init__', return_value=None):
            self.snapshot = SnapshotControl()
            self.snapshot.vmrun_path = r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"

    def test_list_snapshots_default(self):
        output = "Total snapshots: 2\nsnap1\nsnap2"
        self.snapshot._run_command = MagicMock(return_value=output)

        result = self.snapshot.list_snapshots(self.vmx_path)
        self.snapshot._run_command.assert_called_with("listSnapshots", [self.vmx_path])
        self.assertEqual(result, ["snap1", "snap2"])

    def test_list_snapshots_showtree(self):
        output = "Total snapshots: 2\nroot\n\tchild"
        self.snapshot._run_command = MagicMock(return_value=output)

        result = self.snapshot.list_snapshots(self.vmx_path, show_tree=True)
        self.snapshot._run_command.assert_called_with("listSnapshots", [self.vmx_path, "showtree"])
        self.assertEqual(result, ["root", "\tchild"])

    def test_create_snapshot(self):
        self.snapshot._run_command = MagicMock(return_value="OK")
        name = "snap1"
        self.snapshot.create_snapshot(self.vmx_path, name)
        self.snapshot._run_command.assert_called_with("snapshot", [self.vmx_path, name])

    def test_delete_snapshot_default(self):
        self.snapshot._run_command = MagicMock(return_value="OK")
        name = "snap1"
        self.snapshot.delete_snapshot(self.vmx_path, name)
        self.snapshot._run_command.assert_called_with("deleteSnapshot", [self.vmx_path, name])

    def test_delete_snapshot_and_children(self):
        self.snapshot._run_command = MagicMock(return_value="OK")
        name = "snap1"
        self.snapshot.delete_snapshot(self.vmx_path, name, and_delete_children=True)
        self.snapshot._run_command.assert_called_with("deleteSnapshot", [self.vmx_path, name, "andDeleteChildren"])

    def test_revert_to_snapshot_name(self):
        self.snapshot._run_command = MagicMock(return_value="OK")
        name = "snap1"
        self.snapshot.revert_to_snapshot(self.vmx_path, name)
        self.snapshot._run_command.assert_called_with("revertToSnapshot", [self.vmx_path, name])

    def test_revert_to_snapshot_path(self):
        self.snapshot._run_command = MagicMock(return_value="OK")
        path = 'Snap1/Snap2'
        self.snapshot.revert_to_snapshot(self.vmx_path, path)
        self.snapshot._run_command.assert_called_with("revertToSnapshot", [self.vmx_path, path])


if __name__ == '__main__':
    unittest.main()

