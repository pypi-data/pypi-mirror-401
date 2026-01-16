from .utils import VMRunBase

class SnapshotControl(VMRunBase):
    """
    虚拟机快照控制类
    Handles snapshot operations for a VM.
    """
    
    def list_snapshots(self, vmx_path: str, show_tree: bool = False) -> list[str]:
        """
        列出虚拟机的快照
        Lists snapshots for a VM.

        :param vmx_path: Path to the VMX file.
        :param show_tree: Whether to show the snapshot tree.
        :return: A list of snapshot names.
        """
        args = [vmx_path]
        if show_tree:
            args.append("showtree")
        output = self._run_command("listSnapshots", args)
        lines = output.splitlines()
        if len(lines) > 1:
            return lines[1:]
        return []

    def create_snapshot(self, vmx_path: str, snapshot_name: str) -> str:
        """
        创建虚拟机快照
        Creates a snapshot for a VM.

        :param vmx_path: Path to the VMX file.
        :param snapshot_name: Name of the snapshot.
        :return: The output of the command.
        """
        return self._run_command("snapshot", [vmx_path, snapshot_name])

    def delete_snapshot(self, vmx_path: str, snapshot_name: str, and_delete_children: bool = False) -> str:
        """
        删除虚拟机快照
        Deletes a snapshot for a VM.

        :param vmx_path: Path to the VMX file.
        :param snapshot_name: Name of the snapshot.
        :param and_delete_children: Whether to delete child snapshots.
        :return: The output of the command.
        """
        args = [vmx_path, snapshot_name]
        if and_delete_children:
            args.append("andDeleteChildren")
        return self._run_command("deleteSnapshot", args)

    def revert_to_snapshot(self, vmx_path: str, snapshot_name: str) -> str:
        """
        恢复虚拟机到指定快照
        Reverts a VM to a specified snapshot.

        :param vmx_path: Path to the VMX file.
        :param snapshot_name: Name of the snapshot.
        :return: The output of the command.
        """
        return self._run_command("revertToSnapshot", [vmx_path, snapshot_name])
