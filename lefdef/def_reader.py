__all__ = ["C_DefReader"]

import ctypes
import os
from .def import C_Def

class C_DefReaderInstance(ctypes.Structure):
        pass

class C_DefReader():
    def __init__(self) -> None:
        # Store all open pointers of lef files
        self.sessions = []

        # Open library
        self.lefdef = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "lib/liblefdef.so"))

        # Add create reader function
        self.lefdef.createDefReader.restype = ctypes.POINTER(C_DefReaderInstance)
        self.lefdef.createDefReader.argtypes = []

        # Add delete reader function
        self.lefdef.deleteDefReader.restype = None
        self.lefdef.deleteDefReader.argtypes = [ctypes.POINTER(C_DefReaderInstance)]

        # Add delete lef function
        self.lefdef.deleteDef.restype = None
        self.lefdef.deleteDef.argtypes = [ctypes.POINTER(C_Def)]

        # Add read reader function
        self.lefdef.read.restype = ctypes.POINTER(C_Def)
        self.lefdef.read.argtypes = [ctypes.POINTER(C_DefReaderInstance), ctypes.c_char_p]

        # Create reader instance as pointer
        self.reader = self.lefdef.createDefReader()
    
    def read(self, file_name : str) -> C_Def:
        result = self.lefdef.read(self.reader, file_name.encode("utf-8"))

        self.sessions.append(result)

        return result.contents
         
    def __del__(self):
         for lef in self.sessions:
              self.lefdef.deleteDef(lef)
         
         self.lefdef.deleteDefReader(self.reader)