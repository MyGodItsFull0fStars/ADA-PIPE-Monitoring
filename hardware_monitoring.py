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

    @staticmethod
    def get_virtual_memory(as_dict: bool = False):
        vm = psutil.virtual_memory()
        return vm._asdict() if as_dict else vm



if __name__ == '__main__':
    pass
    # before = HardwareMonitoring.get_virtual_memory(True)
    # test_list = []
    # for idx in range(1000000):
    #     test_list.append(idx)
    # after = HardwareMonitoring.get_virtual_memory(True)
