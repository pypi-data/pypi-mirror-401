import unittest
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from py_vmware_lib.guest_os import GuestOSControl, GuestProcessInfo


class TestGuestOSControl(unittest.TestCase):
    def setUp(self):
        self.vmx_path = r"E:\win764\Windows 7 x64.vmx"

        with patch('py_vmware_lib.utils.VMRunBase.__init__', return_value=None):
            self.guest = GuestOSControl()
            self.guest.vmrun_path = r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"

    def test_run_program_in_guest_flags(self):
        self.guest._run_command = MagicMock(return_value="OK")
        self.guest.run_program_in_guest(self.vmx_path, r"C:\prog.exe", "arg1", no_wait=True, active_window=True, interactive=True)
        self.guest._run_command.assert_called_with(
            "runProgramInGuest",
            [self.vmx_path, "-noWait", "-activeWindow", "-interactive", r"C:\prog.exe", "arg1"],
        )

    def test_file_exists_in_guest_true(self):
        self.guest._run_command = MagicMock(return_value="The file exists")
        result = self.guest.file_exists_in_guest(self.vmx_path, r"C:\file.txt")
        self.guest._run_command.assert_called_with("fileExistsInGuest", [self.vmx_path, r"C:\file.txt"])
        self.assertTrue(result)

    def test_file_exists_in_guest_false_on_error(self):
        def raise_error(*args, **kwargs):
            raise RuntimeError("error")

        self.guest._run_command = MagicMock(side_effect=raise_error)
        result = self.guest.file_exists_in_guest(self.vmx_path, r"C:\file.txt")
        self.assertFalse(result)

    def test_directory_exists_in_guest(self):
        self.guest._run_command = MagicMock(return_value="The directory exists")
        result = self.guest.directory_exists_in_guest(self.vmx_path, r"C:\dir")
        self.guest._run_command.assert_called_with("directoryExistsInGuest", [self.vmx_path, r"C:\dir"])
        self.assertTrue(result)

    def test_set_shared_folder_state(self):
        self.guest._run_command = MagicMock(return_value="OK")
        self.guest.set_shared_folder_state(self.vmx_path, "share", r"C:\host", True)
        self.guest._run_command.assert_called_with(
            "setSharedFolderState",
            [self.vmx_path, "share", r"C:\host", "writable"],
        )

    def test_add_and_remove_shared_folder(self):
        self.guest._run_command = MagicMock(return_value="OK")
        self.guest.add_shared_folder(self.vmx_path, "share", r"C:\host")
        self.guest._run_command.assert_called_with(
            "addSharedFolder",
            [self.vmx_path, "share", r"C:\host"],
        )
        self.guest.remove_shared_folder(self.vmx_path, "share")
        self.guest._run_command.assert_called_with(
            "removeSharedFolder",
            [self.vmx_path, "share"],
        )

    def test_enable_disable_shared_folders_runtime(self):
        self.guest._run_command = MagicMock(return_value="OK")
        self.guest.enable_shared_folders(self.vmx_path, runtime=True)
        self.guest._run_command.assert_called_with("enableSharedFolders", [self.vmx_path, "runtime"])
        self.guest.disable_shared_folders(self.vmx_path, runtime=True)
        self.guest._run_command.assert_called_with("disableSharedFolders", [self.vmx_path, "runtime"])

    def test_list_processes_in_guest(self):
        output = (
            "Processes: 2\n"
            "pid=1, owner=root, cmd=[init]\n"
            "pid=2, owner=SYSTEM, cmd=[systemd]"
        )
        self.guest._run_command = MagicMock(return_value=output)
        result = self.guest.list_processes_in_guest(self.vmx_path)
        self.guest._run_command.assert_called_with("listProcessesInGuest", [self.vmx_path])
        self.assertEqual(
            result,
            [
                GuestProcessInfo(pid=1, owner="root", cmd="init"),
                GuestProcessInfo(pid=2, owner="SYSTEM", cmd="systemd"),
            ],
        )

    def test_kill_process_in_guest(self):
        self.guest._run_command = MagicMock(return_value="OK")
        self.guest.kill_process_in_guest(self.vmx_path, 123)
        self.guest._run_command.assert_called_with("killProcessInGuest", [self.vmx_path, "123"])

    def test_run_script_in_guest(self):
        self.guest._run_command = MagicMock(return_value="OK")
        self.guest.run_script_in_guest(self.vmx_path, r"C:\Python\python.exe", "print('hi')", no_wait=True)
        self.guest._run_command.assert_called_with(
            "runScriptInGuest",
            [self.vmx_path, "-noWait", r"C:\Python\python.exe", "print('hi')"],
        )

    def test_file_and_directory_ops(self):
        self.guest._run_command = MagicMock(return_value="OK")
        self.guest.delete_file_in_guest(self.vmx_path, r"C:\file.txt")
        self.guest._run_command.assert_called_with("deleteFileInGuest", [self.vmx_path, r"C:\file.txt"])
        self.guest.create_directory_in_guest(self.vmx_path, r"C:\dir")
        self.guest._run_command.assert_called_with("createDirectoryInGuest", [self.vmx_path, r"C:\dir"])
        self.guest.delete_directory_in_guest(self.vmx_path, r"C:\dir")
        self.guest._run_command.assert_called_with("deleteDirectoryInGuest", [self.vmx_path, r"C:\dir"])

    def test_create_tempfile_in_guest(self):
        self.guest._run_command = MagicMock(return_value=r"C:\temp\vmware.tmp")
        result = self.guest.create_tempfile_in_guest(self.vmx_path)
        self.guest._run_command.assert_called_with("createTempfileInGuest", [self.vmx_path])
        self.assertEqual(result, r"C:\temp\vmware.tmp")

    def test_list_directory_in_guest(self):
        output = "Total files: 2\nfile1.txt\nfile2.txt"
        self.guest._run_command = MagicMock(return_value=output)
        result = self.guest.list_directory_in_guest(self.vmx_path, r"C:\dir")
        self.guest._run_command.assert_called_with("listDirectoryInGuest", [self.vmx_path, r"C:\dir"])
        self.assertEqual(result, ["file1.txt", "file2.txt"])

    def test_copy_files_host_guest(self):
        self.guest._run_command = MagicMock(return_value="OK")
        self.guest.copy_file_from_host_to_guest(self.vmx_path, r"C:\host.txt", r"C:\guest.txt")
        self.guest._run_command.assert_called_with(
            "CopyFileFromHostToGuest",
            [self.vmx_path, r"C:\host.txt", r"C:\guest.txt"],
        )
        self.guest.copy_file_from_guest_to_host(self.vmx_path, r"C:\guest.txt", r"C:\host.txt")
        self.guest._run_command.assert_called_with(
            "CopyFileFromGuestToHost",
            [self.vmx_path, r"C:\guest.txt", r"C:\host.txt"],
        )

    def test_rename_and_devices_and_capture(self):
        self.guest._run_command = MagicMock(return_value="OK")
        self.guest.rename_file_in_guest(self.vmx_path, r"C:\old.txt", r"C:\new.txt")
        self.guest._run_command.assert_called_with(
            "renameFileInGuest",
            [self.vmx_path, r"C:\old.txt", r"C:\new.txt"],
        )
        self.guest.connect_named_device(self.vmx_path, "sound")
        self.guest._run_command.assert_called_with(
            "connectNamedDevice",
            [self.vmx_path, "sound"],
        )
        self.guest.disconnect_named_device(self.vmx_path, "sound")
        self.guest._run_command.assert_called_with(
            "disconnectNamedDevice",
            [self.vmx_path, "sound"],
        )
        self.guest.capture_screen(self.vmx_path, r"C:\screen.png")
        self.guest._run_command.assert_called_with(
            "captureScreen",
            [self.vmx_path, r"C:\screen.png"],
        )

    def test_variables_and_guest_ip(self):
        self.guest._run_command = MagicMock(return_value="OK")
        self.guest.write_variable(self.vmx_path, "guestVar", "k", "v")
        self.guest._run_command.assert_called_with(
            "writeVariable",
            [self.vmx_path, "guestVar", "k", "v"],
        )
        self.guest._run_command = MagicMock(return_value="192.168.1.10")
        ip = self.guest.get_guest_ip_address(self.vmx_path, wait=True)
        self.guest._run_command.assert_called_with(
            "getGuestIPAddress",
            [self.vmx_path, "-wait"],
        )
        self.assertEqual(ip, "192.168.1.10")


if __name__ == "__main__":
    unittest.main()
