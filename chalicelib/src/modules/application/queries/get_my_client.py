from dataclasses import dataclass

from chalicelib.src.modules.infrastructure.facades import MicroservicesFacade
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import ClientRepository


@dataclass
class GetMyClientQuery(Query):
    user_sub: str


class GetClientHandler(QueryBaseHandler):
    def handle(self, query: GetMyClientQuery):
        repository = self.client_factory.create_object(ClientRepository.__class__)
        facade = MicroservicesFacade()
        client_id = facade.get_user(query.user_sub)['client_id']
        result = repository.get(client_id)
        return QueryResult(result=result)


@execute_query.register(GetMyClientQuery)
def execute_get_client(query: GetMyClientQuery):
    handler = GetClientHandler()
    return handler.handle(query)
