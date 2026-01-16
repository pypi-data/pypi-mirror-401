import winreg
import os
import warnings
import subprocess

def get_vmware_install_path() -> str | None:
    r"""
    Reads the VMware Workstation installation path from the registry.
    Path: HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\VMware, Inc.\VMware Workstation
    Key: InstallPath
    """
    try:
        # The path provided by the user
        key_path = r"SOFTWARE\WOW6432Node\VMware, Inc.\VMware Workstation"
        
        # Connect to HKEY_LOCAL_MACHINE and Open Key
        # Using context managers for safe resource handling
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
            with winreg.OpenKey(hkey, key_path) as key:
                value, type_ = winreg.QueryValueEx(key, "InstallPath")
                return value
                
    except FileNotFoundError:
        # Key or value not found
        return None
    except OSError as e:
        # Permission error or other OS error
        print(f"Error reading registry: {e}")
        return None

def check_vmrun_exists(install_path: str) -> bool:
    """
    Checks if vmrun.exe exists in the installation directory.
    
    Args:
        install_path (str): The VMware installation path.
        
    Returns:
        bool: True if vmrun.exe exists, False otherwise.
    """
    if not install_path:
        warnings.warn("Installation path is empty or None.", UserWarning)
        return False
        
    vmrun_path = os.path.join(install_path, "vmrun.exe")
    if os.path.exists(vmrun_path):
        return True
    else:
        warnings.warn(f"vmrun.exe not found in {install_path}. VMware might not be installed or is a lite version.", UserWarning)
        return False

class VMRunBase:
    """Base class for VM operations using vmrun.exe"""
    def __init__(self, vmrun_path: str | None = None):
        self.host_type = None
        self.vm_password = None
        self.guest_user = None
        self.guest_password = None
        if vmrun_path:
            self.vmrun_path = vmrun_path
        else:
            install_path = get_vmware_install_path()
            if install_path and check_vmrun_exists(install_path):
                self.vmrun_path = os.path.join(install_path, "vmrun.exe")
            else:
                raise FileNotFoundError("vmrun.exe not found. Please specify path explicitly or ensure VMware is installed.")

    def set_host_type(self, host_type: str) -> "VMRunBase":
        self.host_type = host_type
        return self

    def set_vm_password(self, password: str) -> "VMRunBase":
        self.vm_password = password
        return self

    def set_guest_credentials(self, user: str, password: str) -> "VMRunBase":
        self.guest_user = user
        self.guest_password = password
        return self

    def _get_auth_flags(self) -> list[str]:
        flags: list[str] = []
        host_type = getattr(self, "host_type", None)
        vm_password = getattr(self, "vm_password", None)
        guest_user = getattr(self, "guest_user", None)
        guest_password = getattr(self, "guest_password", None)
        if host_type:
            flags.extend(["-T", host_type])
        if vm_password:
            flags.extend(["-vp", vm_password])
        if guest_user:
            flags.extend(["-gu", guest_user])
        if guest_password:
            flags.extend(["-gp", guest_password])
        return flags

    def _run_command(self, command: str, args: list[str]) -> str:
        """Executes a vmrun command."""
        full_cmd = [self.vmrun_path] + self._get_auth_flags() + [command] + args
        try:
            result = subprocess.run(
                full_cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                encoding='utf-8',
                errors='replace'  # 用占位符替换无法解码的字符
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"VMRun command failed: {e.stderr}") from e
