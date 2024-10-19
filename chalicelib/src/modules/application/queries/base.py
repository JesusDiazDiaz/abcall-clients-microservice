from chalicelib.src.modules.infrastructure.factory import ClientFactory
from chalicelib.src.seedwork.application.commands import CommandHandler
from chalicelib.src.seedwork.application.queries import QueryHandler


class QueryBaseHandler(QueryHandler):
    def __init__(self):
        self._client_factory: ClientFactory = ClientFactory()

    @property
    def client_factory(self):
        return self._client_factory