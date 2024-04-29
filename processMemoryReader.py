import ctypes
import win32api
import win32process
import win32con

class processMemoryReader:
    def __init__(self, process_name):
        self.process_name = process_name.lower()
        self.process_id = self._get_process_id()

    def _get_process_id(self):
        
        # Get list of running processes
        processes = win32process.EnumProcesses()
        for process_id in processes:
            if process_id == -1:
                continue
            try:
                
                # Load the processs
                p_handle = win32api.OpenProcess(
                    win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
                    True,
                    process_id
                )
                modules = win32process.EnumProcessModules(p_handle)
                for module_id in modules:
                    name = str(win32process.GetModuleFileNameEx(p_handle, module_id))
                    if name.lower().find(self.process_name) != -1:
                        return process_id
            finally:
                win32api.CloseHandle(p_handle)
        return None

    def read_memory(self, address, size_of_data=4):
        
        # Open the process handler
        p_handle = ctypes.windll.kernel32.OpenProcess(
            win32con.PROCESS_VM_READ, False, self.process_id
        )
        
        # Read memory at given address
        data = ctypes.c_uint(size_of_data)
        bytesRead = ctypes.c_uint(size_of_data)
        current_address = address

        ctypes.windll.kernel32.ReadProcessMemory(
                p_handle, current_address, ctypes.byref(data),
                ctypes.sizeof(data), ctypes.byref(bytesRead)
            )

        ctypes.windll.kernel32.CloseHandle(p_handle)
        return data.value

# Example usage
if __name__ == "__main__":
    process_name = "program.exe"
    reader = processMemoryReader(process_name)

    address = 0x2ADB1818
    value = reader.read_memory(address)
    print(f"Value at address {hex(address)}: {value}")

    offsets = [0xD84, 0x1B8, 0x38, 0x5C, 0x24, 0xF4, 0x1D08]
    value_with_offsets = reader.read_memory(address, offsets)
    print(f"Value with offsets: {value_with_offsets}")
