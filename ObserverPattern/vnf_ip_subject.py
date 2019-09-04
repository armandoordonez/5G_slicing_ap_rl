from abc import ABC, abstractmethod
from ObserverPattern.vnf_obs import VnfObserver as Observer

class VnfIpSubject(ABC):

    @abstractmethod
    def attach (self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass
    
    @abstractmethod
    def notify(self, observer: Observer) -> None: 
        pass