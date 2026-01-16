from multiprocessing import Queue
from typing import Literal
from loguru import logger
from qlsdk.persist import ARSKindlingEDFHandler
from qlsdk.rsc.interface import IDevice
from qlsdk.rsc.command import *
from qlsdk.rsc.device.base import QLBaseDevice

    
def intersection_positions(A, B):
    setB = set(B)
    seen = set()
    return [idx for idx, elem in enumerate(A) 
            if elem in setB and elem not in seen and not seen.add(elem)]
 
def get_sorted_indices_basic(A, B):
    """
    找出数组A中存在于数组B的元素，并返回这些元素在A中的位置，且顺序与它们在B中的顺序一致。

    参数:
        A (list): 待查找的数组。
        B (list): 作为参考的数组。

    返回:
        list: 一个列表，包含符合条件的元素在A中的索引，顺序与这些元素在B中的出现顺序一致。
    """
    # 1. 创建B中元素到其索引的映射
    b_index_map = {value: idx for idx, value in enumerate(B)}
    
    # 2. 筛选A中存在于B的元素，并记录其在A中的索引及在B中的位置
    # 使用列表推导式，同时避免重复元素干扰（如果B有重复，以第一次出现为准）
    found_elements = []
    for idx_a, value in enumerate(A):
        if value in b_index_map:
            # 记录: (该元素在A中的索引, 该元素在B中的索引)
            found_elements.append((idx_a, b_index_map[value]))
    
    # 3. 根据元素在B中的位置进行排序
    # 排序的依据是元组的第二个元素，即 b_index_map[value]
    found_elements_sorted = sorted(found_elements, key=lambda x: x[1])
    
    # 4. 提取排序后在A中的索引，形成结果数组C
    array_C = [item[0] for item in found_elements_sorted]
    
    return array_C
   
class ARSKindling(QLBaseDevice):
    
    device_type = 0x60 # C64RS设备类型标识符
    
    def __init__(self, socket):
        super().__init__(socket)
        
        self.channel_mapping = {
            "A1": 55, "A2": 56, "A3": 53, "A4": 54, "A5": 51, "A6": 52, "A7": 49, "A8": 50,
            "A9": 57, "A10": 58, "A11": 59, "A12": 60, "A13": 61, "A14": 62, 
            
            "B1": 39, "B2": 40,  "B3": 37, "B4": 38, "B5": 35, "B6": 36, "B7": 33, "B8": 34,
            "B9": 41, "B10": 42, "B11": 43, "B12": 44, "B13": 45, "B14": 46, 
            
            "C1": 23, "C2": 24, "C3": 21, "C4": 22, "C5": 19, "C6": 20, "C7": 17, "C8": 18,
            "C9": 25, "C10": 26, "C11": 27, "C12": 28, "C13": 29, "C14": 30, 
            
            "D1": 7, "D2": 8, "D3": 5, "D4": 6, "D5": 3, "D6": 4, "D7": 1, "D8": 2,
            "D9": 9, "D10": 10, "D11": 11, "D12": 12, "D13": 13, "D14": 14, 
        }
        
        self._channel_spilt = {
            "A" : [55, 56, 53, 54, 51, 52, 49, 50, 57, 58, 59, 60, 61, 62],
            "B" : [39, 40, 37, 38, 35, 36, 33, 34, 41, 42, 43, 44, 45, 46],
            "C" : [23, 24, 21, 22, 19, 20, 17, 18, 25, 26, 27, 28, 29, 30],
            "D" : [7, 8, 5, 6, 3, 4, 1, 2, 9, 10, 11, 12, 13, 14],
        }
        
        self._channel_mapping = {
            1: "7", 
            2: "8",
            3: "5", 
            4: "6",
            5: "3", 
            6: "4",
            7: "1", 
            8: "2",
            9: "9", 
            10: "10",
            11: "11", 
            12: "12",
            13: "13", 
            14: "14",
            
            17: "7", 
            18: "8",
            19: "5", 
            20: "6",
            21: "3", 
            22: "4",
            23: "1", 
            24: "2",
            25: "9", 
            26: "10",
            27: "11", 
            28: "12",
            29: "13", 
            30: "14",
            
            33: "7", 
            34: "8",
            35: "5", 
            36: "6",
            37: "3", 
            38: "4",
            39: "1", 
            40: "2",
            41: "9", 
            42: "10",
            43: "11", 
            44: "12",
            45: "13", 
            46: "14",
            
            49: "7", 
            50: "8",
            51: "5", 
            52: "6",
            53: "3", 
            54: "4",
            55: "1", 
            56: "2",
            57: "9", 
            58: "10",
            59: "11", 
            60: "12",
            61: "13", 
            62: "14"
        }
                
    @classmethod
    def from_parent(cls, parent:IDevice) -> IDevice:
        rlt = cls(parent.socket)
        rlt.device_id = parent.device_id
        rlt._device_no = parent.device_no
        return rlt
        
    def init_edf_handler(self):
        self._edf_handler = ARSKindlingEDFHandler(self.sample_rate,  self.sample_range * 1000 , - self.sample_range * 1000, self.resolution)  
        self._edf_handler.set_device_type(self.device_type)
        self._edf_handler.set_device_no(self.device_no)
        self._edf_handler.set_storage_path(self._storage_path)
        self._edf_handler.set_file_prefix(self._file_prefix if self._file_prefix else 'ARS')
        logger.debug(f"EDF Handler initialized")
        
    # 设置采集参数
    def set_acq_param(self, channels, sample_rate = 500, sample_range = 188):
        self._acq_param["original_channels"] = channels
        
        # 根据映射关系做通道转换
        for k in channels.keys():
            if isinstance(channels[k], list):
                temp = [k + str(i) for i in channels[k]]
                channels[k] = [self.channel_mapping.get(c, 1) for c in temp]
            else:
                channels[k] = [k + str(channels[k])]
                
                
        # 更新采集参数        
        self._acq_param["channels"] = channels 
        self._acq_param["sample_rate"] = sample_rate
        self._acq_param["sample_range"] = sample_range
        self._acq_channels = channels
        self._sample_rate = sample_rate
        self._sample_range = sample_range     
    
    @property
    def acq_channels(self):
        if self._acq_channels is None:
            self._acq_channels = [i for i in range(1, 63)]
            
        arr = []
        for k in self._acq_channels.keys():
            arr = list(arr + self._acq_channels[k])
            
        return list(set(arr))    
    
    def _produce_impedance(self, body: bytes):
        # 分发阻抗数据包给订阅者
        if len(self._impedance_consumer) > 0:
            packet = ImpedancePacket.transfer(body)
            real_data = self.__impedance_transfer(packet)
            for topic, q in self._impedance_consumer.items():
                try:
                    # 队列满了就丢弃最早的数据
                    if q.full(): 
                        q.get()
                    q.put(real_data, timeout=1)
                except Exception as e:
                    logger.error(f"impedance data put to queue exception: {str(e)}")
                    
    def _produce_signal(self, body: bytes):        
        
        # 处理信号数据
        data = self._signal_wrapper(body)  
        # logger.debug("pkg_id: {}, eeg len: {}".format(data.pkg_id, len(data.eeg)))
        
        trigger_positions = [index for index, value in enumerate(data.trigger) if value != 0]
        if len(trigger_positions) > 0:
            # logger.debug(f"Trigger触发点位置: {trigger_positions}, 触发点时间戳: {[data.time_stamp + int(pos * 1000 / data.sample_rate) for pos in trigger_positions]}")
            for pos in trigger_positions:
                self.trigger(self.trigger_info(data.trigger[pos]))
        
        if len(self.signal_consumers) > 0 :
            # 信号数字值转物理值
            data.eeg_p = self.eeg2phy(np.array(data.eeg))        
        
        real_data = self.__signal_transfer(data)   
               
        # 存储
        if self.storage_enable:            
            # 确保记录线程启动
            if self._recording is False:
                self._start_recording() 
                
            # 写入文件的缓存队列
            if self._signal_cache is None:
                self._signal_cache = Queue(1000000)  # 缓冲队列
            self._signal_cache.put(real_data)
                                    
        if len(self.signal_consumers) > 0 :
            # 订阅只返回物理值
            real_data.eeg = real_data.eeg_p
            # 发送数据包到订阅者
            for q in list(self.signal_consumers.values()):
                # 队列满了就丢弃最早的数据
                if q.full(): 
                    q.get()
                    
                q.put(real_data)      
     
    # 信号数据转换
    def __impedance_transfer(self, packet: ImpedancePacket):
        channels = {}
        impedance = {}
        #按分区拆分数据格式
        for k in self._channel_spilt.keys():      
            logger.trace(f'分区{k}的阻抗数据')   
            c, d, p = self.__packet_filter(packet, self._channel_spilt[k], type='impedance')
            if c is not None:
                channels[k] = c
                impedance[k] = d
        packet.channels = channels
        packet.impedance = impedance
            
        return packet
      
    # 信号数据转换
    def __signal_transfer(self, packet: RscPacket):
        channels = {}
        eeg = {}
        eeg_p = {}
        #按分区拆分数据格式
        for k in self._channel_spilt.keys():      
            logger.trace(f'分区{k}, {self._channel_spilt[k]}')   
            c, d, p = self.__packet_filter(packet, self._channel_spilt[k])
            if c is not None:
                channels[k] = c
                eeg[k] = d
            if p is not None:
                eeg_p[k] = p
        packet.channels = channels
        packet.eeg = eeg
        #物理值
        if packet.eeg_p is not None:
            packet.eeg_p = eeg_p
            
        return packet
    
    def __packet_filter(self, packet, channel_filter=None, type:Literal['signal','impedance']='signal'):
        # 参数检查
        if packet is None or channel_filter is None:
            logger.warning("空数据，忽略")
            return None, None, None
        
        channel_pos = get_sorted_indices_basic(packet.channels, channel_filter)
        
        if channel_pos is None or len(channel_pos) == 0 :
            logger.trace(f"没有指定分区的通道，跳过")
            return None, None, None
        
        # 分区数据包写入
        
        # 保留本分区的通道和数据
        channels = [packet.channels[p] for p in channel_pos]
        
        #阻抗数据
        if type == 'impedance':
            impedance = [packet.impedance[p] for p in channel_pos]
            return [self._channel_mapping.get(channel_id, []) for channel_id in channels], impedance, None
        
        # 信号数据
        eeg = [packet.eeg[p] for p in channel_pos]
        eeg_p = None
        if packet.eeg_p is not None:
            eeg_p = [packet.eeg_p[p] for p in channel_pos]
        
        return [self._channel_mapping.get(channel_id, []) for channel_id in channels], eeg, eeg_p
        
    
    