from loguru import logger
from qlsdk.core.entity import C256RSPacket
from qlsdk.persist import RscEDFHandler
from qlsdk.rsc.device.device_factory import DeviceFactory
from qlsdk.rsc.command import *
from qlsdk.rsc.device.base import QLBaseDevice

class C256RS(QLBaseDevice):
    # C256RS设备类型标识符
    device_type_001 = 0x51  
    device_type = 0x45  
    
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
        self._edf_handler.set_file_prefix(self._file_prefix if self._file_prefix else 'C256RS')
        logger.debug(f"EDF Handler initialized")
      
    @property
    def acq_channels(self):
        if self._acq_channels is None:
            self._acq_channels = [i for i in range(1, 256)]
        return self._acq_channels  
    
    def _signal_wrapper(self, body: bytes):
        return C256RSPacket().transfer(body)
        
    def get_stim_param(self) -> bytes:
        return self.stim_paradigm.to_bytes_c256()    
    
DeviceFactory.register(C256RS.device_type, C256RS) 
DeviceFactory.register(C256RS.device_type_001, C256RS) 