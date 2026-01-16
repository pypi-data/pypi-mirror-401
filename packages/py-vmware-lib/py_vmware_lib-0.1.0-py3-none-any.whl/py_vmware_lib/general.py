from .utils import VMRunBase

class GeneralControl(VMRunBase):
    """
    处理一般的虚拟机操作
    Handles general VM operations.
    """
    
    def list_running_vms(self) -> list[str]:
        """
        获取当前运行中的虚拟机列表
        Lists all running VMs.
        
        Returns:
            list[str]: 运行中的虚拟机路径列表
        """
        output = self._run_command("list", [])
        lines = output.splitlines()
        # Output: "Total running VMs: N\npath1\npath2..."
        if len(lines) > 1:
            return lines[1:]
        return []

    def upgrade_vm(self, vmx_path: str):
        """
        升级虚拟机
        Upgrades the VM to the latest version.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
        """
        return self._run_command("upgradevm", [vmx_path])

    def install_tools(self, vmx_path: str):
        """
        安装虚拟机工具
        Installs VMware Tools in the guest OS.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
        """
        return self._run_command("installTools", [vmx_path])

    def check_tools_state(self, vmx_path: str) -> str:
        """
        检查虚拟机工具状态
        Checks the state of VMware Tools in the guest.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
        
        Returns:
            str: 虚拟机工具状态，可能的状态包括：unknown, installed, running
        """
        return self._run_command("checkToolsState", [vmx_path])

    def clone(self, vmx_path: str, dest_path: str, clone_type: str = "full", snapshot_name: str = None, clone_name: str = None):
        """
        克隆虚拟机
        Clones a VM.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
            dest_path (str): 克隆后的虚拟机配置文件的路径
            clone_type (str, optional): 克隆类型，"full"或"linked". Defaults to "full".
            snapshot_name (str, optional): 快照名称，用于创建链接克隆. Defaults to None.
            clone_name (str, optional): 克隆后的虚拟机名称. Defaults to None.
        
        Returns:
            str: 克隆操作的结果，通常是成功或失败的消息
        """
        args = [vmx_path, dest_path, clone_type]
        if snapshot_name:
            args.append(f"-snapshot={snapshot_name}")
        if clone_name:
            args.append(f"-cloneName={clone_name}")
        return self._run_command("clone", args)

    def delete_vm(self, vmx_path: str):
        """
        删除虚拟机
        Deletes a VM.
        
        Args:
            vmx_path (str): 虚拟机配置文件的路径
        """
        return self._run_command("deleteVM", [vmx_path])
