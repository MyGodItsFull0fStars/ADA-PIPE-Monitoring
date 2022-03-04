from os import stat
import psutil

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



if __name__ == '__main__':
    print(HardwareMonitoring.get_cpu_frequency())
    print(HardwareMonitoring.get_num_physical_cpu_cores())
    print(HardwareMonitoring.get_num_total_cpu_cores())