from dataclasses import dataclass
from .utils import VMRunBase


@dataclass
class HostNetworkInfo:
    index: int
    name: str
    type: str
    dhcp: bool
    subnet: str
    mask: str


@dataclass
class PortForwardingInfo:
    index: int
    protocol: str
    host_port: int
    guest_ip: str
    guest_port: int
    description: str | None


class HostNetworkControl(VMRunBase):
    """
    处理主机网络操作的类
    注意: 与虚拟网络编辑器相比，vmrun 对主机网络管理的支持有限。
    该类作为占位符或用于可用的 vmrun 主机命令 </br>
    Handles host network operations.
    Note: vmrun has limited support for host network management compared to Virtual Network Editor.
    This class serves as a placeholder or for available vmrun host commands.
    """
    
    def list_host_networks(self) -> list[HostNetworkInfo]:
        """
        列出主机上的所有网络适配器

        Returns:
            list[HostNetworkInfo]: 主机网络适配器的结构化列表
        """
        try:
            output = self._run_command("listHostNetworks", [])
        except RuntimeError as e:
            message = str(e)
            lowered = message.lower()
            if "listhostnetworks" in lowered and ("unknown command" in lowered or "not supported" in lowered):
                return []
            raise
        lines = output.splitlines()
        if len(lines) <= 1:
            return []
        result: list[HostNetworkInfo] = []
        for line in lines[1:]:
            parts = line.split()
            if len(parts) < 6:
                continue
            index_str, name, type_, dhcp_str, subnet, mask = parts[:6]
            try:
                index = int(index_str)
            except ValueError:
                continue
            dhcp = dhcp_str.lower() == "true"
            result.append(
                HostNetworkInfo(
                    index=index,
                    name=name,
                    type=type_,
                    dhcp=dhcp,
                    subnet=subnet,
                    mask=mask,
                )
            )
        return result

    def list_port_forwardings(self, host_network: str) -> list[PortForwardingInfo]:
        """
        列出指定主机网络适配器上的所有端口转发规则

        Args:
            host_network (str): 主机网络适配器的名称

        Returns:
            list[PortForwardingInfo]: 端口转发规则的结构化列表
        """
        output = self._run_command("listPortForwardings", [host_network])
        lines = output.splitlines()
        if len(lines) <= 1:
            return []
        result: list[PortForwardingInfo] = []
        for line in lines[1:]:
            parts = line.split()
            if len(parts) < 5:
                continue
            index_str, protocol, host_port_str, guest_ip, guest_port_str = parts[:5]
            description = " ".join(parts[5:]) if len(parts) > 5 else None
            try:
                index = int(index_str)
                host_port = int(host_port_str)
                guest_port = int(guest_port_str)
            except ValueError:
                continue
            result.append(
                PortForwardingInfo(
                    index=index,
                    protocol=protocol,
                    host_port=host_port,
                    guest_ip=guest_ip,
                    guest_port=guest_port,
                    description=description,
                )
            )
        return result

    def set_port_forwarding(
        self,
        host_network: str,
        protocol: str,
        host_port: int,
        guest_ip: str,
        guest_port: int,
        description: str | None = None,
    ):
        """
        设置端口转发规则

        Args:
            host_network (str): 主机网络适配器的名称
            protocol (str): 协议类型（"tcp" 或 "udp"）
            host_port (int): 主机端口号
            guest_ip (str): 虚拟机 IP 地址
            guest_port (int): 虚拟机端口号
            description (str | None, optional): 端口转发规则的描述. Defaults to None.

        Returns:
            str: 命令执行结果的字符串表示
        """
        args = [host_network, protocol, str(host_port), guest_ip, str(guest_port)]
        if description:
            args.append(description)
        return self._run_command("setPortForwarding", args)

    def delete_port_forwarding(self, host_network: str, protocol: str, host_port: int):
        """
        删除指定主机网络适配器上的端口转发规则

        Args:
            host_network (str): 主机网络适配器的名称
            protocol (str): 协议类型（"tcp" 或 "udp"）
            host_port (int): 主机端口号

        Returns:
            str: 命令执行结果的字符串表示
        """
        args = [host_network, protocol, str(host_port)]
        return self._run_command("deletePortForwarding", args)
