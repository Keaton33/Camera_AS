import snap7

client = snap7.client.Client()
client.connect('192.168.0.1', rack=0, slot=1)


def get_hoist_height():
    byte_arrays = client.db_read(21, 812, 4)
    # byte_arrays = self.client.read_area(snap7.types.S7AreaDB, 21, 812, 4)  # 读出变量的字节数组
    value = snap7.util.get_dint(byte_arrays, 0)  # 通过数据类型取值
    # self.client.disconnect()  # 断开连接
    # self.client.destroy()  # 销毁
    # print(value)
    return value
