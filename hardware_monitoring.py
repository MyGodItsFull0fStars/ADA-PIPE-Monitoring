from os import stat
import psutil
from psutil import cpu_times
from psutil import cpu_percent


class HardwareMonitoring():

    @staticmethod
    def get_cpu_frequency():
        return psutil.cpu_freq()

    @staticmethod
    def get_num_physical_cpu_cores():
        return psutil.cpu_count(logical=False)

    @staticmethod
    def get_num_total_cpu_cores():
        return psutil.cpu_count(logical=True)

    @staticmethod
    def get_cpu_times(as_dict: bool = False):
        cpu_time = psutil.cpu_times()
        return cpu_time._asdict() if as_dict else cpu_time

    @staticmethod
    def get_cpu_percent(interval: float = 1, per_cpu: bool = False):
        return psutil.cpu_percent(interval=interval, percpu=per_cpu)

    @staticmethod
    def get_cpu_stats(as_dict: bool = False):
        return psutil.cpu_stats()._asdict() if as_dict else psutil.cpu_stats()

    @staticmethod
    def get_virtual_memory(as_dict: bool = False):
        vm = psutil.virtual_memory()
        return vm._asdict() if as_dict else vm

    @staticmethod
    def get_disk_partitions():
        return psutil.disk_partitions()

    @staticmethod
    def get_system_info() -> dict:
        """Retrieve the (static) system infos
        - `cpu_frequency`: CPU frequency (attention, static because Hypervisor hides the actual values)
        - `num_physical_cpu_cores`: Number of physical CPU cores
        - `num_total_cpu_cores`: Number of all CPU cores (physical and virtual)

        Returns:
            dict: Python Dictionary containing the system info
        """
        system_info: dict = {
            'cpu_frequency': int(HardwareMonitoring.get_cpu_frequency().current),
            'num_physical_cpu_cores': HardwareMonitoring.get_num_physical_cpu_cores(),
            'num_total_cpu_cores': HardwareMonitoring.get_num_total_cpu_cores()
        }

        return system_info

    @staticmethod
    def get_system_status() -> dict:
        system_status: dict = {
            
            'virtual_memory': HardwareMonitoring.get_virtual_memory(True),
            'disk_partitions': HardwareMonitoring.get_disk_partitions()
            }

        return system_status


if __name__ == '__main__':

    print(HardwareMonitoring.get_cpu_percent(True))
    print(HardwareMonitoring.get_disk_partitions())
    print(HardwareMonitoring.get_system_info())
