import torch.nn as nn
from .bridge.concepts import NeuralConcept
from .core.logic import Predicate


class NeuroSymbolicModel:
    """
    A container that holds the Neural Network and maps its outputs to Logic Predicates.
    """
    def __init__(self, network: nn.Module):
        self.network = network
        self.concept_map = {}

    def register(self, predicate: Predicate, output_index: int = None):
        """
        Easy registration:
        model.register(IsDigitZero, index=0)
        """
        concept = NeuralConcept(
            name=predicate.name, 
            module=self.network, 
            output_index=output_index
        )
        self.concept_map[predicate.name] = concept

    def get_concept_map(self):
        return self.concept_map