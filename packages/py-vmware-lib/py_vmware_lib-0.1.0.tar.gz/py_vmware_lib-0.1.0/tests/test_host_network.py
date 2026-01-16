import unittest
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from py_vmware_lib.host_network import HostNetworkControl, HostNetworkInfo, PortForwardingInfo


class TestHostNetworkControl(unittest.TestCase):
    def setUp(self):
        self.host_network = "vmnet8"

        with patch('py_vmware_lib.utils.VMRunBase.__init__', return_value=None):
            self.host = HostNetworkControl()
            self.host.vmrun_path = r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"

    def test_list_host_networks(self):
        output = "INDEX  NAME         TYPE         DHCP         SUBNET           MASK\n1      vmnet1       hostOnly     true         192.168.88.0     255.255.255.0   \n8      vmnet8       nat          false        192.168.200.0    255.255.255.0"
        self.host._run_command = MagicMock(return_value=output)

        result = self.host.list_host_networks()
        self.host._run_command.assert_called_with("listHostNetworks", [])
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], HostNetworkInfo)
        self.assertEqual(result[0].index, 1)
        self.assertEqual(result[0].name, "vmnet1")
        self.assertEqual(result[0].type, "hostOnly")
        self.assertEqual(result[0].dhcp, True)
        self.assertEqual(result[0].subnet, "192.168.88.0")
        self.assertEqual(result[0].mask, "255.255.255.0")

    def test_list_host_networks_unsupported_command(self):
        def raise_error(*args, **kwargs):
            raise RuntimeError("VMRun command failed: Unknown command: listHostNetworks")

        self.host._run_command = MagicMock(side_effect=raise_error)

        result = self.host.list_host_networks()
        self.host._run_command.assert_called_with("listHostNetworks", [])
        self.assertEqual(result, [])

    def test_list_port_forwardings(self):
        output = (
            "INDEX  PROTOCOL     HOST PORT    GUEST IP         GUEST PORT       DESCRIPTION\n"
            "0      tcp          8080         192.168.200.128  80               Test Port Forwarding"
        )
        self.host._run_command = MagicMock(return_value=output)

        result = self.host.list_port_forwardings(self.host_network)
        self.host._run_command.assert_called_with("listPortForwardings", [self.host_network])
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], PortForwardingInfo)
        self.assertEqual(result[0].index, 0)
        self.assertEqual(result[0].protocol, "tcp")
        self.assertEqual(result[0].host_port, 8080)
        self.assertEqual(result[0].guest_ip, "192.168.200.128")
        self.assertEqual(result[0].guest_port, 80)
        self.assertEqual(result[0].description, "Test Port Forwarding")

    def test_set_port_forwarding_without_description(self):
        self.host._run_command = MagicMock(return_value="OK")

        self.host.set_port_forwarding(self.host_network, "tcp", 8080, "192.168.56.101", 80)
        self.host._run_command.assert_called_with(
            "setPortForwarding",
            [self.host_network, "tcp", "8080", "192.168.56.101", "80"],
        )

    def test_set_port_forwarding_with_description(self):
        self.host._run_command = MagicMock(return_value="OK")

        self.host.set_port_forwarding(self.host_network, "tcp", 8080, "192.168.56.101", 80, "web")
        self.host._run_command.assert_called_with(
            "setPortForwarding",
            [self.host_network, "tcp", "8080", "192.168.56.101", "80", "web"],
        )

    def test_delete_port_forwarding(self):
        self.host._run_command = MagicMock(return_value="OK")

        self.host.delete_port_forwarding(self.host_network, "tcp", 8080)
        self.host._run_command.assert_called_with(
            "deletePortForwarding",
            [self.host_network, "tcp", "8080"],
        )


if __name__ == "__main__":
    unittest.main()
