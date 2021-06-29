from __future__ import annotations
from abc import ABC, abstractmethod
from .musinsa import Musinsa


class StragyVendor(ABC):
    @abstractmethod
    def run():
        pass


class MusinsaStagy(StragyVendor):
    def run(self,
            id,
            password,
            address,
            address_detail,
            recipient,
            shipping_address,
            phone_number_head,
            phone_number_middle,
            phone_number_tail):
        obj = Musinsa(id,
                      password,
                      address,
                      address_detail,
                      recipient,
                      shipping_address,
                      phone_number_head,
                      phone_number_middle,
                      phone_number_tail)
        obj.run()


class Context():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy: StragyVendor) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> StragyVendor:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: StragyVendor) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy

    # def do_some_business_logic(self) -> None:
    def address_run(self,
                    id,
                    password,
                    address,
                    address_detail,
                    recipient,
                    shipping_address,
                    phone_number_head,
                    phone_number_middle,
                    phone_number_tail) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """

        # ...

        print("Context: Sorting data using the strategy (not sure how it'll do it)")
        self._strategy.run(id,
                           password,
                           address,
                           address_detail,
                           recipient,
                           shipping_address,
                           phone_number_head,
                           phone_number_middle,
                           phone_number_tail)
        # ...
