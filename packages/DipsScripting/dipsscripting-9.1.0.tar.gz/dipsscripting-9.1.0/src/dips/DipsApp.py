import grpc
from .DipsAPI_pb2_grpc import AppServiceStub
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from .ApplicationManager import ApplicationManager
from .ProjStubRef import ProjStubRef
from logging import Logger
import winreg

class DipsApp:
    @staticmethod
    def AttachToExisting(port):
        ret = DipsApp(port)
        return ret
    
    @staticmethod
    def LaunchApp(port, overridePathToExecutable : str = None, timeout : float = 120, headless : bool = False, fileToOpen : str = None):
        DipsApp.startApplication(port, overridePathToExecutable, timeout, headless, fileToOpen)
        ret = DipsApp(port)
        return ret

    def __init__(self, port):
        channel = grpc.insecure_channel('localhost:{port}'.format(port = port))
        self.__stub = AppServiceStub(channel)
        self.__channel = channel

    @staticmethod
    def startApplication(port : int, overridePathToExecutable : str = None, timeout : float = 120, headless : bool = False, fileToOpen : str = None) -> None:
        """Opens the most recently installed RS2 application. Starts the python server and binds it to the given port.

        Args:
            port (int): the port to bind the python server to. Use this same port when initializing RS2Modeler
            overridePathToExecutable (str, optional): full path to the desired executable to be opened. If not provided, the latest installation of rs2 is used
            timeout (float, optional): the maximum amount of time to wait for the application and server to start.
        
        Raises:
            ValueError: Port range must be between 49152 and 65535, otherwise ValueError is raised
            TimeoutError: if timeout is provided, raises TimeoutError if not able to connect to the server within that time.
        """
        appManager = ApplicationManager()
        if overridePathToExecutable is None:
            executablePath = DipsApp._getApplicationPath()
        else:
            executablePath = overridePathToExecutable
        

        appManager.startApplication(executablePath, port, DipsApp._isServerRunning, Logger("Test"), timeout, headless, fileToOpen)

    @staticmethod
    def _getApplicationPath() -> str:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(registry, r'SOFTWARE\Rocscience\Dips 9.0')
        installationLocation, type = winreg.QueryValueEx(key, "Install")
        dipsModelerInstallLocation = rf"{installationLocation}\Dips.exe"
        return dipsModelerInstallLocation
    
    @staticmethod
    def _isServerRunning(port) -> bool:
        channel = grpc.insecure_channel('localhost:{port}'.format(port = port))
        stub = AppServiceStub(channel)
        stub.Ping(google_dot_protobuf_dot_empty__pb2.Empty())
        channel.close()
        return True

    def GetModel(self) -> ProjStubRef:
        model = self.__stub.GetProjectReference(google_dot_protobuf_dot_empty__pb2.Empty())
        return ProjStubRef(self.__channel, model)
    
    def Show(self):
        self.__stub.Show(google_dot_protobuf_dot_empty__pb2.Empty())
    
    def Hide(self):
        self.__stub.Hide(google_dot_protobuf_dot_empty__pb2.Empty())

    def Ping(self):
        self.__stub.Ping(google_dot_protobuf_dot_empty__pb2.Empty())

    def Close(self):
        self.__stub.Close(google_dot_protobuf_dot_empty__pb2.Empty())



