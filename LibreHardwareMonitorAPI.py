import clr
import os


def init_librehardwaremonitor():
    cwd = os.getcwd()
    clr.AddReference(cwd + '\\LibreHardwareMonitorLib.dll')
    clr.AddReference(cwd + '\\HidSharp.dll')
    from LibreHardwareMonitor import Hardware
    handle = Hardware.Computer()
    handle.IsCpuEnabled = True
    handle.IsGpuEnabled = True
    # handle.IsMemoryEnabled = True
    # handle.IsMotherboardEnabled = True
    # handle.IsControllerEnabled = True
    # handle.IsNetworkEnabled = True
    # handle.IsStorageEnabled = True

    handle.Open()

    return handle


class HWMonitor:
    def __init__(self, handle):
        self.handle = handle

    def get_hardware_brief_information(self):
        """
        :return:
        {'CPU_Temperature', 'CPU_Power', 'CPU_Load',
        'GPU_Temperature', 'GPU_Power', 'GPU_Core_Frequency', 'GPU_Core_Load', 'GPU_Memory_Load'}
        """
        sensortype_to_load = ['Load', 'Power', 'Clock', 'Temperature']

        dict_to_return = dict()
        for i in self.handle.Hardware:
            i.Update()
            for sensor in i.Sensors:
                if str(sensor.SensorType) in sensortype_to_load:
                    identifier = str(sensor.Identifier)
                    sensor_name = str(sensor.Name)
                    sensor_type = str(sensor.SensorType)
                    value = sensor.Value
                    if sensor_type == 'Temperature':
                        if 'Core' in sensor_name and 'cpu' in identifier:
                            dict_to_return['CPU_Temperature'] = value
                        if 'Core' in sensor_name and 'gpu' in identifier:
                            dict_to_return['GPU_Temperature'] = value
                    elif sensor_type == 'Power':
                        if 'Package' in sensor_name and 'cpu' in identifier:
                            dict_to_return['CPU_Power'] = value
                        if 'Package' in sensor_name and 'gpu' in identifier:
                            dict_to_return['GPU_Power'] = value
                    elif sensor_type == 'Load':
                        if 'CPU Total' == sensor_name:
                            dict_to_return['CPU_Load'] = value
                        if 'GPU Core' == sensor_name:
                            dict_to_return['GPU_Core_Load'] = value
                        if 'GPU Memory' == sensor_name:
                            dict_to_return['GPU_Memory_Load'] = value
                    elif sensor_type == 'Clock':
                        if 'GPU Core' == sensor_name:
                            dict_to_return['GPU_Core_Frequency'] = value
        return dict_to_return


if __name__ == "__main__":
    monitor = HWMonitor(init_librehardwaremonitor())
    print(monitor.get_hardware_brief_information())
