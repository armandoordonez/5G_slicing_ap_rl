from abc import ABC, abstractmethod



class VnfCpuSubject(ABC):

    @abstractmethod
    def attach (self, observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer) -> None:
        pass
    
    @abstractmethod
    def notify(self, observer) -> None: 
        pass

"""
class VnfIpSubject(ABC):
    @abstractmethod
    def attach (self, observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer) -> None:
        pass
    
    @abstractmethod
    def notify(self, observer) -> None: 
        pass

"""
class VnfObserver(ABC):
    @abstractmethod
    def updateCpuUsageSubject(self, subject: VnfCpuSubject) -> None:
        pass
    """
    @abstractmethod
    def updateNsIps(self, subject: VnfIpSubject) -> None:
        pass
    """
