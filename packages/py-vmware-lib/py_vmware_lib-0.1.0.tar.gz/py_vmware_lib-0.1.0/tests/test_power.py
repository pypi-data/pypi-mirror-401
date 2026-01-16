import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from py_vmware_lib.power import PowerControl

class TestPowerControl(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        We mock VMRunBase.__init__ to avoid needing actual VMware installation/registry keys.
        """
        self.vmx_path = r"E:\win764\Windows 7 x64.vmx"
        
        # Patch the base class init to skip auto-detection of vmrun.exe
        # We need to patch where VMRunBase is defined or imported. 
        # Since PowerControl inherits from VMRunBase, we can just instantiate it 
        # if we patch the methods it calls in __init__, or patch __init__ itself.
        
        with patch('py_vmware_lib.utils.VMRunBase.__init__', return_value=None):
            self.power = PowerControl()
            # Manually set a dummy path for vmrun.exe
            self.power.vmrun_path = r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"
            
        # Mock the _run_command method to verify calls without executing them
        self.power._run_command = MagicMock(return_value="OK")

    def test_start_gui(self):
        """Test starting VM in GUI mode"""
        print(f"\nTesting start GUI for: {self.vmx_path}")
        self.power.start(self.vmx_path, mode="gui")
        self.power._run_command.assert_called_with("start", [self.vmx_path, "gui"])
        print("Command verified: start [vmx, 'gui']")

    def test_start_nogui(self):
        """Test starting VM in nogui mode"""
        print(f"\nTesting start nogui for: {self.vmx_path}")
        self.power.start(self.vmx_path, mode="nogui")
        self.power._run_command.assert_called_with("start", [self.vmx_path, "nogui"])
        print("Command verified: start [vmx, 'nogui']")

    def test_start_invalid(self):
        """Test start with invalid mode raises ValueError"""
        print("\nTesting start with invalid mode...")
        with self.assertRaises(ValueError):
            self.power.start(self.vmx_path, mode="invalid")
        print("ValueError caught as expected.")

    def test_stop_soft(self):
        """Test stopping VM with soft mode"""
        print(f"\nTesting stop soft for: {self.vmx_path}")
        self.power.stop(self.vmx_path, mode="soft")
        self.power._run_command.assert_called_with("stop", [self.vmx_path, "soft"])
        print("Command verified: stop [vmx, 'soft']")

    def test_stop_hard(self):
        """Test stopping VM with hard mode"""
        print(f"\nTesting stop hard for: {self.vmx_path}")
        self.power.stop(self.vmx_path, mode="hard")
        self.power._run_command.assert_called_with("stop", [self.vmx_path, "hard"])
        print("Command verified: stop [vmx, 'hard']")

    def test_reset(self):
        """Test reset VM"""
        print(f"\nTesting reset for: {self.vmx_path}")
        self.power.reset(self.vmx_path, mode="soft")
        self.power._run_command.assert_called_with("reset", [self.vmx_path, "soft"])
        print("Command verified: reset [vmx, 'soft']")

    def test_suspend(self):
        """Test suspend VM"""
        print(f"\nTesting suspend for: {self.vmx_path}")
        self.power.suspend(self.vmx_path, mode="soft")
        self.power._run_command.assert_called_with("suspend", [self.vmx_path, "soft"])
        print("Command verified: suspend [vmx, 'soft']")

    def test_pause(self):
        """Test pause VM"""
        print(f"\nTesting pause for: {self.vmx_path}")
        self.power.pause(self.vmx_path)
        self.power._run_command.assert_called_with("pause", [self.vmx_path])
        print("Command verified: pause [vmx]")

    def test_unpause(self):
        """Test unpause VM"""
        print(f"\nTesting unpause for: {self.vmx_path}")
        self.power.unpause(self.vmx_path)
        self.power._run_command.assert_called_with("unpause", [self.vmx_path])
        print("Command verified: unpause [vmx]")

if __name__ == '__main__':
    unittest.main()
