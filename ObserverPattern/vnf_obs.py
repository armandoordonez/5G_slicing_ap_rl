from abc import ABC, abstractmethod
from ObserverPattern.vnf_ip_subject import VnfCpuSubject as CpuSubject

class VnfObserver(ABC):
    @abstractmethod
    def updateCpuUsageSubject(self, subject: CpuSubject) -> None:
        pass