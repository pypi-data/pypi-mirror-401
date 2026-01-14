from nvidia_gpu_tools import find_gpus, Gpu, NvSwitch
from termcolor import cprint
from typing import List
import time





class ConfidentialComputeManager:
    """
    Manager for Confidential Compute (CC) mode on NVIDIA GPUs.
    """
    def __init__(self):
        self.gpus = self.get_gpus()
        self.devices = self.get_devices()

    def get_devices(self) -> List[Gpu | NvSwitch]:
        devices, _ = find_gpus()
        devices_list = []
        for device in devices:
            if device.is_ppcie_query_supported or device.is_cc_query_supported:
                devices_list.append(device)
        return devices_list


    def get_gpus(self) -> List[Gpu]:
        gpus, _ = find_gpus()
        return [gpu for gpu in gpus if gpu.is_cc_query_supported]



    def get_cc_mode(self, gpu: Gpu) -> str:
        try:
            mode = gpu.query_cc_mode()
            return mode
        except Exception as e:
            cprint(f"Error getting mode: {e}", "red")
            return None
  
    def execute_cc_mode(self, gpu: Gpu, mode: str):
        try:
            gpu.set_cc_mode(mode)
            gpu.reset_with_os()
            mode = gpu.query_cc_mode()
            cprint(f"CC mode is now: {mode}", "green")
            return mode
        except Exception as e:
            cprint(f"Error executing CC mode test for {gpu.name}: {e}", "red")
            return False
        return True

    def execute_set_ppcie_mode(self, device: NvSwitch, mode: str):
        try:
            device.set_ppcie_mode(mode)
            device.reset_with_os()
            mode = device.query_ppcie_mode()
            return mode
        except Exception as e:
            cprint(f"Error executing PPCIE mode test for {device.name}: {e}", "red")
            return False

    def run_all_gpus(self, mode: str):
        if len(self.gpus) == 0:
            cprint("No GPUs Supported for CC mode", "red")
            return False
        for gpu in self.gpus:
            cprint(f"Executing CC mode test for {gpu.name}", "green")
            self.execute_cc_mode_test(gpu, mode)
        return True

    def run_all_devices(self, mode: str):
        if len(self.devices) == 0:
            cprint("No Devices Supported for CC mode", "red")
            return False
        for device in self.devices:
            cprint(f"Executing PPCIE mode test for {device.name}", "green")
            self.execute_set_ppcie_mode(device, mode)
        return True


           



    






def toggle_cc_mode(mode: str):
    cc_manager = ConfidentialComputeManager()
    cc_manager.run_all_gpus(mode)
    time.sleep(10)
    cc_manager.run_all_devices(mode)
    return True


    
