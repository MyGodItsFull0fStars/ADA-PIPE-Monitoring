from utils import StrEnum

class RegisterEnum(StrEnum):
    DEVICE_NAME: str = 'device_name'
    IP_ADDRESS: str = 'ip_address'
    PORT_NUMBER: str = 'port_number'
    PROMETHEUS: str = 'prometheus'
    HARDWARE_DESCRIPTION: str = 'hardware_description'
