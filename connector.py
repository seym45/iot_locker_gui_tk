import serial
import serial.tools.list_ports


def get_value(var):
    ret_val = ''
    try:
        ser = serial.Serial('COM8', 9600, timeout=1)
        var = 'deligram' + var + '\n'
        ser.write(var.encode())
        ret_val = ser.readline()
    except:
        ret_val = 'COM_PORT_ERROR'
    return ret_val


if __name__ == "__main__":
    ret = get_value("?")
    ret = ret.decode()
    ret = ret.strip()
    print(ret)

    ret = get_value("A")
    ret = ret.decode()
    ret = ret.strip()
    print(ret)
