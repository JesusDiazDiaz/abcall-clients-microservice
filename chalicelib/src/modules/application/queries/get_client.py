from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import ClientRepository


@dataclass
class GetClientQuery(Query):
    client_id:str

class GetClientHandler(QueryBaseHandler):
    def handle(self, query: GetClientQuery):
        repository = self.client_factory.create_object(ClientRepository.__class__)
        result = repository.get(query.client_id)
        return QueryResult(result=result)

@execute_query.register(GetClientQuery)
def execute_get_client(query: GetClientQuery):
    handler = GetClientHandler()
    return handler.handle(query)