from abc import ABC, abstractmethod
from typing_extensions import TypedDict

"""
A simple object/dict to represent `IValidator` responses
"""


class ValidationResponse(TypedDict):
    valid: bool
    errors: list



"""
An interface for string validators
"""


class IValidator(ABC):

    @abstractmethod
    def validate(self, data: str) -> ValidationResponse:
        """
        Implementation required
        :param data: string to be validated
        :return: object of type Validation response
        :raise: NotImplementedError is not implemented in concrete class
        """
        raise NotImplementedError



