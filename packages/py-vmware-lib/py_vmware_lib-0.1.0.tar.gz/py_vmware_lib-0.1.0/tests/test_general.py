import unittest
from unittest.mock import MagicMock
from py_vmware_lib.general import GeneralControl

class TestGeneralControl(unittest.TestCase):
    def setUp(self):
        self.general = GeneralControl()
        self.general._run_command = MagicMock(return_value="")
        self.vmx_path = "C:\\VMs\\test.vmx"

    def test_list_running_vms(self):
        self.general._run_command.return_value = "Total running VMs: 1\nC:\\VMs\\test.vmx"
        vms = self.general.list_running_vms()
        self.general._run_command.assert_called_with("list", [])
        self.assertEqual(vms, ["C:\\VMs\\test.vmx"])

    def test_upgrade_vm(self):
        self.general.upgrade_vm(self.vmx_path)
        self.general._run_command.assert_called_with("upgradevm", [self.vmx_path])

    def test_install_tools(self):
        self.general.install_tools(self.vmx_path)
        self.general._run_command.assert_called_with("installTools", [self.vmx_path])

    def test_check_tools_state(self):
        self.general.check_tools_state(self.vmx_path)
        self.general._run_command.assert_called_with("checkToolsState", [self.vmx_path])

    def test_delete_vm(self):
        self.general.delete_vm(self.vmx_path)
        self.general._run_command.assert_called_with("deleteVM", [self.vmx_path])

    def test_clone_basic(self):
        dest = "C:\\VMs\\clone.vmx"
        self.general.clone(self.vmx_path, dest, "full")
        self.general._run_command.assert_called_with("clone", [self.vmx_path, dest, "full"])

    def test_clone_linked_with_options(self):
        dest = "C:\\VMs\\clone.vmx"
        self.general.clone(
            self.vmx_path, 
            dest, 
            "linked", 
            snapshot_name="Snap1", 
            clone_name="MyClone"
        )
        # Verifying expectation based on user provided doc: [-snapshot=Snapshot Name] [-cloneName=Name]
        self.general._run_command.assert_called_with(
            "clone", 
            [self.vmx_path, dest, "linked", "-snapshot=Snap1", "-cloneName=MyClone"]
        )
