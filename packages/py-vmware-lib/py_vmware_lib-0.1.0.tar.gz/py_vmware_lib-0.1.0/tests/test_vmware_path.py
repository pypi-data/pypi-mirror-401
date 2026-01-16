import unittest
import os
import sys
import warnings

# Add project root to path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from py_vmware_lib import get_vmware_install_path, check_vmrun_exists

class TestVMwarePath(unittest.TestCase):
    def test_get_vmware_install_path(self):
        print("\nTesting VMware Install Path Detection...")
        path = get_vmware_install_path()
        print(f"Detected VMware Path: {path}")
        
        if path is not None:
            self.assertIsInstance(path, str)
            print(f"Verified path type is string.")
            
            # Test checking for vmrun.exe
            print("\nTesting vmrun.exe existence...")
            has_vmrun = check_vmrun_exists(path)
            if has_vmrun:
                print("vmrun.exe found.")
            else:
                print("vmrun.exe NOT found.")
        else:
            print("VMware Workstation not found in registry.")
            # We don't fail the test if not found, as the environment might not have it.
            # But the function executed successfully.
            
    def test_check_vmrun_exists_negative(self):
        print("\nTesting vmrun.exe existence with invalid path...")
        # Suppress warnings for this test to keep output clean, or capture them
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = check_vmrun_exists("C:\\NonExistentPath\\")
            self.assertFalse(result)
            self.assertTrue(len(w) > 0)
            self.assertTrue("not found" in str(w[-1].message))
            print("Verified warning and False return for invalid path.")

if __name__ == '__main__':
    unittest.main()
