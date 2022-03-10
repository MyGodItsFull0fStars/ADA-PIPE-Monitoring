from os import stat
from typing import Any, List
from pandas import value_counts
import psutil
from psutil import cpu_times
from psutil import cpu_percent

from flask_restful import Resource


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
    def get_cpu_percent(per_cpu: bool = False, interval: float = None):
        """Get the CPU Usage of the device

        Args:
            `per_cpu` (bool, optional): If set to `True`, get the usage per cpu core, otherwise get an average cpu usage. Defaults to `False`.
            `interval` (float, optional): Tracks the cpu usage in a given interval. ATTENTION: If a value is provided, this method is blocking other calls. Defaults to None.

        Returns:
            `float` | `List[float]`: Returns a float if the value `per_cpu` is `False` otherwise will return a list of `float` values.
        """
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
    def get_cpu_load_average(as_dict: bool = False) -> Any:
        """Get the system load average in percent.

        Returns:
            List[float] | Dict[str, float]: Returns a list of floats representing the load average over the last 1, 5 and 15 minutes of the system running.
        """
        load_average = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
        if as_dict is True:
            temp_dict = {}
            for key, value in zip(['cpu_load_avg_1_min', 'cpu_load_avg_5_min', 'cpu_load_avg_15_min'], load_average):
                temp_dict[key] = value

            load_average = temp_dict

        return load_average

    @staticmethod
    def get_sensors_temperatures():
        """Get the sensor temperatures of the device.
        ATTENTION: For now only works on Linux systems.

        Returns:
            dict: dictionary containing the temperature information of the device.
        """
        if not psutil.LINUX:
            return f'Function only implemented for Linux distributions'
        # Return sensor temperature for Linux System
        return psutil.sensors_temperatures()



    @staticmethod
    def get_system_status() -> dict:
        system_status: dict = {

            'cpu_load_average': HardwareMonitoring.get_cpu_load_average(as_dict=True),
            'virtual_memory': HardwareMonitoring.get_virtual_memory(True),
            # 'disk_partitions': HardwareMonitoring.get_disk_partitions() # Not sure if needed
        }

        return system_status


if __name__ == '__main__':

    # print(HardwareMonitoring.get_cpu_percent(per_cpu=True))
    # print(HardwareMonitoring.get_disk_partitions())
    # print(HardwareMonitoring.get_system_info())
    print(HardwareMonitoring.get_system_status())
    # print(HardwareMonitoring.get_cpu_load_average())
    # print(HardwareMonitoring.get_cpu_load_average(True))
    print(HardwareMonitoring.get_sensors_temperatures())
    

    
