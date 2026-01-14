from abc import ABC, abstractmethod
from typing import List, Dict

class BaseDetector(ABC):

    @abstractmethod
    def detect(self, text: str) -> List[Dict]:
        """Return detected entities in standard format"""
        pass
