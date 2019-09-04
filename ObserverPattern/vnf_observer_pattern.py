from abc import ABC, abstractmethod



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

class VnfObserver(ABC):
    @abstractmethod
    def updateIpSubject(self, subject: VnfIpSubject) -> None:
        pass
