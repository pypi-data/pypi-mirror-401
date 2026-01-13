from typing_extensions import Final, List
from string import Template
import subprocess

from libs.platforms import is_running_on_linux, is_running_on_windows


class Firewall:
    pass

    @classmethod
    def close_port(cls, port: int) -> None:
        raise NotImplementedError()

    @classmethod
    def open_port(cls, port: int) -> None:
        raise NotImplementedError()


class LinuxFirewall(Firewall):
    LINUX_FIREWALL_RULE_TEMPLATE: Final[Template] = Template(
        "sudo ufw$maybe_delete allow $port_number comment PORTify_automaticly_managed_rule:_allow_port_$port_number"
    )

    @classmethod
    def close_port(cls, port: int) -> None:
        command_to_run: List[str] = cls.LINUX_FIREWALL_RULE_TEMPLATE.substitute(
            maybe_delete=" delete", port_number=port
        ).split()
        print(f"Closing port: {port}")
        try:
            subprocess.run(command_to_run, check=False, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed closing port: {port} Crashing aggresively")
            raise e

    @classmethod
    def open_port(cls, port: int) -> None:
        command_to_run: List[str] = cls.LINUX_FIREWALL_RULE_TEMPLATE.substitute(
            maybe_delete="", port_number=port
        ).split()
        print(f"Opening port: {port}")
        try:
            subprocess.run(command_to_run, check=False, capture_output=True)
        except subprocess.CalledProcessError:
            print(f"Failed opening port: {port}")


class WindowsFirewall(Firewall):
    WINDOWS_GET_FIREWALL_RULE_TEMPLATE: Final[Template] = Template(
        "powershell -Command Get-NetFirewallRule -DisplayName 'PORTify_automaticly_managed_rule:_block_port_$port_number' -ErrorAction Stop"
    )
    WINDOWS_CREATE_FIREWALL_RULE_TEMPLATE: Final[Template] = Template(
        "powershell -Command New-NetFirewallRule -DisplayName 'PORTify_automaticly_managed_rule:_block_port_$port_number' -Protocol $protocol -LocalPort $port_number -Action block -Profile 'Public' -Direction Inbound"
    )
    WINDOWS_REMOVE_FIREWALL_RULE_TEMPLATE: Final[Template] = Template(
        "powershell -Command Remove-NetFirewallRule -DisplayName 'PORTify_automaticly_managed_rule:_block_port_$port_number'"
    )

    @classmethod
    def open_port(cls, port: int) -> None:
        if cls.check_rule_exists(port=port):
            print("Rule exists, openinig port")
            cls._open_port(port=port)

    @classmethod
    def _open_port(cls, port: int) -> None:
        command_to_run: List[str] = (
            cls.WINDOWS_REMOVE_FIREWALL_RULE_TEMPLATE.substitute(
                port_number=port
            ).split()
        )
        print(f"Opening port: {port}")
        try:
            subprocess.run(command_to_run, check=False, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed opening port: {port}")

    @classmethod
    def close_port(cls, port: int) -> None:
        if not cls.check_rule_exists(port=port):
            cls._close_port(port=port)

    @classmethod
    def _close_port(cls, port: int) -> None:
        command_to_run_tcp: List[str] = (
            cls.WINDOWS_CREATE_FIREWALL_RULE_TEMPLATE.substitute(
                port_number=port, protocol="TCP"
            ).split()
        )
        command_to_run_udp: List[str] = (
            cls.WINDOWS_CREATE_FIREWALL_RULE_TEMPLATE.substitute(
                port_number=port, protocol="UDP"
            ).split()
        )
        print(f"Closing port: {port}")
        try:
            subprocess.run(command_to_run_tcp, check=False, capture_output=True)
            subprocess.run(command_to_run_udp, check=False, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed closing port: {port} crashing aggresively")
            raise e

    @classmethod
    def check_rule_exists(cls, port: int) -> bool:
        command_to_run: List[str] = cls.WINDOWS_GET_FIREWALL_RULE_TEMPLATE.substitute(
            port_number=port
        ).split()
        try:
            subprocess.run(command_to_run, check=True, capture_output=True)
            # If we reached here the rule exists
            return True
        except subprocess.CalledProcessError:
            # If we reached here the rule doesn't exist
            return False


def determine_firewall() -> type[Firewall]:
    if is_running_on_windows():
        return WindowsFirewall
    elif is_running_on_linux():
        return LinuxFirewall
    else:
        raise NotImplementedError("Firewall support is not implemented on this OS")


def open_firewall_ports(firewall: type[Firewall], ports: frozenset[int]) -> None:
    for port in ports:
        firewall.open_port(port=port)


def close_firewall_ports(firewall: type[Firewall], ports: frozenset[int]) -> None:
    for port in ports:
        firewall.close_port(port=port)
