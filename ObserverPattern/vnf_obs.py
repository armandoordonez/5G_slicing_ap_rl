from abc import ABC, abstractmethod
from ObserverPattern.vnf_ip_subject import VnfIpSubject as IpSubject

class VnfObserver(ABC):
    @abstractmethod
    def updateIpSubject(self, subject: IpSubject) -> None:
        pass