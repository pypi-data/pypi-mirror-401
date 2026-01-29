from loguru import logger
from qlsdk.persist import RscEDFHandler
from qlsdk.rsc.interface import IDevice
from qlsdk.rsc.command import *
from qlsdk.rsc.device.base import QLBaseDevice

class C64S1(QLBaseDevice):
    
    device_type = 0x40  # C64RS-S1设备类型标识符
    
    def __init__(self, socket):
        super().__init__(socket)
    
    @classmethod
    def from_parent(cls, parent:IDevice) -> IDevice:
        rlt = cls(parent.socket)
        rlt.device_id = parent.device_id
        rlt._device_no = parent.device_no
        return rlt
        
        
    def init_edf_handler(self):
        self._edf_handler = RscEDFHandler(self.sample_rate,  self.sample_range * 1000 , - self.sample_range * 1000, self.resolution)  
        self._edf_handler.set_device_type(self.device_type)
        self._edf_handler.set_device_no(self.device_no)
        self._edf_handler.set_storage_path(self._storage_path)
        self._edf_handler.set_file_prefix(self._file_prefix if self._file_prefix else 'C64S1')
        logger.debug(f"EDF Handler initialized")
        