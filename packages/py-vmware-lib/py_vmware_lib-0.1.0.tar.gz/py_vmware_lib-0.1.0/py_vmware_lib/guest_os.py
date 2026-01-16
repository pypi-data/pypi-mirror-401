from typing import Literal
from dataclasses import dataclass
from .utils import VMRunBase


@dataclass
class GuestProcessInfo:
    pid: int
    owner: str
    cmd: str

class GuestOSControl(VMRunBase):
    """
    处理虚拟机中操作系统操作的类
    Handles Guest OS operations.
    """
    
    def __init__(self, vmrun_path: str | None = None, user: str | None = None, password: str | None = None):
        super().__init__(vmrun_path)
        self.guest_user = user
        self.guest_password = password

    def run_program_in_guest(self, vmx_path: str, program_path: str, program_args: str = "", no_wait: bool = False, active_window: bool = False, interactive: bool = False):
        """
        在虚拟机中运行程序
        Runs a program in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            program_path (str): 要运行的程序路径
            program_args (str, optional): 程序的参数. Defaults to "".
            no_wait (bool, optional): 是否异步运行程序. Defaults to False.
            active_window (bool, optional): 是否激活窗口. Defaults to False.
            interactive (bool, optional): 是否交互模式. Defaults to False.
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path]
        if no_wait: args.append("-noWait")
        if active_window: args.append("-activeWindow")
        if interactive: args.append("-interactive")
        
        args.append(program_path)
        if program_args:
            args.append(program_args)
            
        return self._run_command("runProgramInGuest", args)

    def file_exists_in_guest(self, vmx_path: str, file_path: str) -> bool:
        """
        检查虚拟机中是否存在文件
        Checks if a file exists in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            file_path (str): 要检查的文件路径
        
        Returns:
            bool: 如果文件存在则返回True，否则返回False
        """
        args = [vmx_path, file_path]
        try:
            self._run_command("fileExistsInGuest", args)
            return True # Usually if it doesn't fail/output indicates existence? 
        except RuntimeError:
            return False

    def directory_exists_in_guest(self, vmx_path: str, directory_path: str) -> bool:
        """
        检查虚拟机中是否存在目录
        Checks if a directory exists in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            directory_path (str): 要检查的目录路径
        
        Returns:
            bool: 如果目录存在则返回True，否则返回False
        """
        args = [vmx_path, directory_path]
        try:
            self._run_command("directoryExistsInGuest", args)
            return True
        except RuntimeError:
            return False

    def set_shared_folder_state(self, vmx_path: str, share_name: str, host_path: str, writable: bool):
        """
        设置共享文件夹的状态
        Sets the state of a shared folder in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            share_name (str): 共享文件夹的名称
            host_path (str): 主机上的共享文件夹路径
            writable (bool): 是否可写
        
        Returns:
            str: 命令输出
        """
        state = "writable" if writable else "readonly"
        args = [vmx_path, share_name, host_path, state]
        return self._run_command("setSharedFolderState", args)

    def add_shared_folder(self, vmx_path: str, share_name: str, host_path: str):
        """
        添加共享文件夹
        Adds a shared folder in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            share_name (str): 共享文件夹的名称
            host_path (str): 主机上的共享文件夹路径
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, share_name, host_path]
        return self._run_command("addSharedFolder", args)

    def remove_shared_folder(self, vmx_path: str, share_name: str):
        """
        删除共享文件夹
        Removes a shared folder in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            share_name (str): 共享文件夹的名称
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, share_name]
        return self._run_command("removeSharedFolder", args)

    def enable_shared_folders(self, vmx_path: str, runtime: bool = False):
        """
        启用共享文件夹
        Enables shared folders in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            runtime (bool, optional): 是否在运行时启用. Defaults to False.
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path]
        if runtime:
            args.append("runtime")
        return self._run_command("enableSharedFolders", args)

    def disable_shared_folders(self, vmx_path: str, runtime: bool = False):
        """
        禁用共享文件夹
        Disables shared folders in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            runtime (bool, optional): 是否在运行时禁用. Defaults to False.
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path]
        if runtime:
            args.append("runtime")
        return self._run_command("disableSharedFolders", args)

    def list_processes_in_guest(self, vmx_path: str) -> list[GuestProcessInfo]:
        """
        列出虚拟机中的进程
        Lists processes running in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
        
        Returns:
            list[GuestProcessInfo]: 进程列表
        """
        args = [vmx_path]
        output = self._run_command("listProcessesInGuest", args)
        lines = output.splitlines()
        results: list[GuestProcessInfo] = []
        if len(lines) <= 1:
            return results
        for line in lines[1:]:
            parts = [p.strip() for p in line.split(",")]
            pid_str = ""
            owner = ""
            cmd = ""
            for part in parts:
                if part.startswith("pid="):
                    pid_str = part[len("pid="):]
                elif part.startswith("owner="):
                    owner = part[len("owner="):]
                elif part.startswith("cmd="):
                    value = part[len("cmd="):]
                    if value.startswith("[") and value.endswith("]"):
                        value = value[1:-1]
                    cmd = value
            try:
                pid = int(pid_str)
            except ValueError:
                continue
            results.append(GuestProcessInfo(pid=pid, owner=owner, cmd=cmd))
        return results

    def kill_process_in_guest(self, vmx_path: str, pid: int):
        """
        终止虚拟机中的进程
        Terminates a process running in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            pid (int): 进程ID
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, str(pid)]
        return self._run_command("killProcessInGuest", args)

    def run_script_in_guest(self, vmx_path: str, interpreter_path: str, script_text: str, no_wait: bool = False, active_window: bool = False, interactive: bool = False):
        """
        在虚拟机中运行脚本
        Runs a script in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            interpreter_path (str): 脚本解释器的路径
            script_text (str): 脚本内容
            no_wait (bool, optional): 是否异步运行. Defaults to False.
            active_window (bool, optional): 是否在活动窗口中运行. Defaults to False.
            interactive (bool, optional): 是否交互式运行. Defaults to False.
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path]
        if no_wait: args.append("-noWait")
        if active_window: args.append("-activeWindow")
        if interactive: args.append("-interactive")
        args.append(interpreter_path)
        args.append(script_text)
        return self._run_command("runScriptInGuest", args)

    def delete_file_in_guest(self, vmx_path: str, file_path: str):
        """
        删除虚拟机中的文件
        Deletes a file in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            file_path (str): 文件路径
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, file_path]
        return self._run_command("deleteFileInGuest", args)

    def create_directory_in_guest(self, vmx_path: str, directory_path: str):
        """
        创建虚拟机中的目录
        Creates a directory in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            directory_path (str): 目录路径
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, directory_path]
        return self._run_command("createDirectoryInGuest", args)

    def delete_directory_in_guest(self, vmx_path: str, directory_path: str):
        """
        删除虚拟机中的目录
        Deletes a directory in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            directory_path (str): 目录路径
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, directory_path]
        return self._run_command("deleteDirectoryInGuest", args)

    def create_tempfile_in_guest(self, vmx_path: str) -> str:
        """
        创建虚拟机中的临时文件
        Creates a temporary file in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
        
        Returns:
            str: 临时文件路径
        """
        args = [vmx_path]
        return self._run_command("createTempfileInGuest", args)

    def list_directory_in_guest(self, vmx_path: str, directory_path: str) -> list[str]:
        """
        列出虚拟机中的目录内容
        Lists the contents of a directory in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            directory_path (str): 目录路径
        
        Returns:
            list[str]: 目录内容列表
        """
        args = [vmx_path, directory_path]
        output = self._run_command("listDirectoryInGuest", args)
        lines = output.splitlines()
        if len(lines) > 1:
            return lines[1:]
        return []

    def copy_file_from_host_to_guest(self, vmx_path: str, host_path: str, guest_path: str):
        """
        从主机复制文件到虚拟机
        Copies a file from the host to the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            host_path (str): 主机文件路径
            guest_path (str): 虚拟机文件路径
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, host_path, guest_path]
        return self._run_command("CopyFileFromHostToGuest", args)

    def copy_file_from_guest_to_host(self, vmx_path: str, guest_path: str, host_path: str):
        """
        从虚拟机复制文件到主机
        Copies a file from the guest OS to the host.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            guest_path (str): 虚拟机文件路径
            host_path (str): 主机文件路径
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, guest_path, host_path]
        return self._run_command("CopyFileFromGuestToHost", args)

    def rename_file_in_guest(self, vmx_path: str, old_path: str, new_path: str):
        """
        重命名虚拟机中的文件
        Renames a file in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            old_path (str): 旧文件路径
            new_path (str): 新文件路径
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, old_path, new_path]
        return self._run_command("renameFileInGuest", args)

    def connect_named_device(self, vmx_path: str, device_name: str):
        """
        连接虚拟机中的命名设备
        Connects a named device in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            device_name (str): 设备名称
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, device_name]
        return self._run_command("connectNamedDevice", args)

    def disconnect_named_device(self, vmx_path: str, device_name: str):
        """
        断开虚拟机中的命名设备
        Disconnects a named device in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            device_name (str): 设备名称
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, device_name]
        return self._run_command("disconnectNamedDevice", args)

    def capture_screen(self, vmx_path: str, host_output_path: str):
        """
        捕获虚拟机屏幕
        Captures the screen of the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            host_output_path (str): 主机输出路径
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, host_output_path]
        return self._run_command("captureScreen", args)

    def write_variable(self, vmx_path: str, var_type: Literal["guestVar", "runtimeConfig", "guestEnv"], name: str, value: str):
        """
        写入虚拟机变量
        Writes a variable to the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            var_type (Literal["guestVar", "runtimeConfig", "guestEnv"]): 变量类型
            name (str): 变量名称
            value (str): 变量值
        
        Returns:
            str: 命令输出
        """
        args = [vmx_path, var_type, name, value]
        return self._run_command("writeVariable", args)

    def read_variable(self, vmx_path: str, var_type: Literal["guestVar", "runtimeConfig", "guestEnv"], name: str) -> str:
        """
        读取虚拟机变量
        Reads a variable from the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            var_type (Literal["guestVar", "runtimeConfig", "guestEnv"]): 变量类型
            name (str): 变量名称
        
        Returns:
            str: 变量值
        """
        args = [vmx_path, var_type, name]
        return self._run_command("readVariable", args)

    def get_guest_ip_address(self, vmx_path: str, wait: bool = False) -> str:
        """
        获取虚拟机的IP地址
        Gets the IP address of the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            wait (bool, optional): 是否等待IP地址分配完成. Defaults to False.
        
        Returns:
            str: 虚拟机的IP地址
        """
        args = [vmx_path]
        if wait:
            args.append("-wait")
        return self._run_command("getGuestIPAddress", args)
