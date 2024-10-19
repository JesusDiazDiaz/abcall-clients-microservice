from dataclasses import dataclass
from chalicelib.src.seedwork.domain.factory import Factory
from chalicelib.src.seedwork.domain.repository import Repository
from chalicelib.src.modules.domain.repository import ClientRepository
from .exceptions import ImplementationNotExistsForFactoryException
from .repository import ClientRepositoryPostgres


@dataclass
class ClientFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == ClientRepository.__class__:
            return ClientRepositoryPostgres()

        raise ImplementationNotExistsForFactoryException()