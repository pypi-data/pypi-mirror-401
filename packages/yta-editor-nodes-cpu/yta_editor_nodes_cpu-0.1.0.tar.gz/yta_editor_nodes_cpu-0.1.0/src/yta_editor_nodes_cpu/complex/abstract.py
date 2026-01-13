from yta_programming.singleton import SingletonABCMeta
from abc import ABC, abstractmethod

import numpy as np



class _NodeComplexCPU(ABC):
    """
    *Abstract class*

    *For internal use only*

    A node that is made by applying different nodes. It
    is different than the other nodes because it needs
    to import different nodes to process the input(s),
    by using CPU.
    """

    def __init__(
        self,
        node_complex: 'NodeComplexCoreCPU'
    ):
        # TODO: Validate that is 'NodeComplexCoreCPU' or child
        self.node_complex: 'NodeComplexCoreCPU' = node_complex
        """
        The singleton instance of the complex node that
        will process the input and return the output.
        """

    def process(
        self,
        input: np.ndarray,
        **kwargs
    ) -> np.ndarray:
        """
        Process the provided 'input' and transform it by
        using the code that is defined here.
        """
        return self.node_complex.process(
            input = input,
            **kwargs
        )
    
class _NodeComplexCoreCPU(metaclass = SingletonABCMeta):
    """
    *Singleton class*

    *For internal use only*

    This class is to be able to use different nodes with
    the same input.

    This class will be called internally by the specific
    nodes to make the composition.
    """

    @abstractmethod
    def process(
        self,
        input: np.ndarray,
        **kwargs
    ) -> np.ndarray:
        """
        Process the provided 'input' and transform it by
        using the code that is defined here.
        """
        pass