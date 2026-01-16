from .utils import VMRunBase
from typing import Literal

class PowerControl(VMRunBase):
    """
    虚拟机电源操作类
    Handles power operations for a VM.
    """
    
    def start(self, vmx_path: str, mode: Literal["gui", "nogui"] = "gui"):
        """
        启动虚拟机。

        参数:
            vmx_path (str): .vmx 文件的路径。
            mode (str): 启动模式，可选值为 "gui" 或 "nogui"。默认为 "gui"。
        
        说明:
            - gui: 以交互方式启动虚拟机，这是显示 Workstation Pro 界面所必需的。（默认）
            - nogui: 禁止显示 Workstation Pro 界面（包括启动对话框）以允许使用非交互脚本。
            
        注意:
            要启动加密的虚拟机，请使用 nogui 标志。vmrun 实用工具在加密的虚拟机中不支持 GUI 模式。
        """
        if mode not in ["gui", "nogui"]:
            raise ValueError("mode must be 'gui' or 'nogui'")
        return self._run_command("start", [vmx_path, mode])

    def stop(self, vmx_path: str, mode: Literal["hard", "soft"] = "soft"):
        """
        停止虚拟机。

        参数:
            vmx_path (str): .vmx 文件的路径。
            mode (str): 停止模式，可选值为 "soft" 或 "hard"。默认为 "soft"。

        说明:
            - soft: 在运行关机脚本后关闭客户机电源。（默认）
            - hard: 关闭客户机电源而不运行脚本，就像按电源按钮一样。
        """
        if mode not in ["hard", "soft"]:
            raise ValueError("mode must be 'hard' or 'soft'")
        return self._run_command("stop", [vmx_path, mode])

    def reset(self, vmx_path: str, mode: Literal["hard", "soft"] = "soft"):
        """
        重置虚拟机。

        参数:
            vmx_path (str): .vmx 文件的路径。
            mode (str): 重置模式，可选值为 "soft" 或 "hard"。默认为 "soft"。

        说明:
            - soft: 在重新引导客户机之前运行关机脚本。（默认）
            - hard: 重新引导客户机而不运行脚本，就像按电源按钮一样。
        """
        if mode not in ["hard", "soft"]:
            raise ValueError("mode must be 'hard' or 'soft'")
        return self._run_command("reset", [vmx_path, mode])

    def suspend(self, vmx_path: str, mode: Literal["hard", "soft"] = "soft"):
        """
        挂起虚拟机。
        挂起而不关闭虚拟机，因此，以后可以恢复本地工作。

        参数:
            vmx_path (str): .vmx 文件的路径。
            mode (str): 挂起模式，可选值为 "soft" 或 "hard"。默认为 "soft"。

        说明:
            - soft: 在运行系统脚本后挂起客户机。（默认）
                - 在 Windows 客户机上，这些脚本释放 IP 地址。
                - 在 Linux 客户机上，这些脚本挂起网络连接。
            - hard: 挂起客户机而不运行脚本。

        注意:
            要在 suspend 命令完成后恢复运行虚拟机，请使用 start 命令。
            - 在 Windows 上，将检索 IP 地址。
            - 在 Linux 上，将重新启动网络连接。
        """
        if mode not in ["hard", "soft"]:
            raise ValueError("mode must be 'hard' or 'soft'")
        return self._run_command("suspend", [vmx_path, mode])

    def pause(self, vmx_path: str):
        """
        暂停虚拟机。

        参数:
            vmx_path (str): .vmx 文件的路径。
        """
        return self._run_command("pause", [vmx_path])

    def unpause(self, vmx_path: str):
        """
        恢复运行暂时停止正常运行的虚拟机。

        参数:
            vmx_path (str): .vmx 文件的路径。
        """
        return self._run_command("unpause", [vmx_path])
