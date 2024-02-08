import atexit
import struct

import snap7

client = snap7.client.Client()
client.connect('192.168.0.1', rack=0, slot=1)


def cleanup():
    if client.get_connected():
        set_trolley_cmd_spd(0)
        client.disconnect()
        client.destroy()


atexit.register(cleanup)


def get_hoist_height():
    byte_arrays = client.db_read(21, 812, 4)
    if byte_arrays:
        # byte_arrays = self.client.read_area(snap7.types.S7AreaDB, 21, 812, 4)  # 读出变量的字节数组
        value = snap7.util.get_dint(byte_arrays, 0)  # 通过数据类型取值
        # self.client.disconnect()  # 断开连接
        # self.client.destroy()  # 销毁
        return value
    else:
        return 0


def get_trolley_position():
    byte_arrays = client.db_read(30, 994, 4)
    if byte_arrays:
        value = snap7.util.get_dint(byte_arrays, 0)
        return value
    else:
        return 0


def get_trolley_set_spd():
    byte_arrays = client.db_read(30, 222, 4)
    if byte_arrays:
        value = snap7.util.get_real(byte_arrays, 0)
        return value
    else:
        return 0


def get_trolley_act_spd():
    byte_arrays = client.db_read(30, 14, 4)
    if byte_arrays:
        value = snap7.util.get_real(byte_arrays, 0)
        return value
    else:
        return 0


def set_trolley_cmd_spd(cmd_spd):
    byte_arrays = bytearray(struct.pack('>f', cmd_spd))
    return client.db_write(30, 154, byte_arrays)


