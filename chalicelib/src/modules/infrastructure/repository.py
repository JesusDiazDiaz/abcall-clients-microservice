from operator import and_
from uuid import UUID
import logging
from chalicelib.src.modules.domain.repository import ClientRepository
from chalicelib.src.modules.infrastructure.dto import Client, DocumentType, PlanType, ClientSchema
from chalicelib.src.config.db import db_session, init_db
from chalicelib.src.seedwork.infrastructure.utils import handle_db_session


LOGGER = logging.getLogger('abcall-client-microservice')


class ClientRepositoryPostgres(ClientRepository):
    def __init__(self):
        self.db_session = init_db()

    def add(self, client):
        LOGGER.info(f"Repository add client: {client}")
        client_schema = ClientSchema(many=False)
        new_client = Client(
            perfil=client.perfil,
            id_type=DocumentType[client.id_type],
            legal_name=client.legal_name,
            id_number=client.id_number,
            address=client.address,
            type_document_rep=DocumentType[client.type_document_rep],
            id_rep_lega=client.id_rep_lega,
            name_rep=client.name_rep,
            last_name_rep=client.last_name_rep,
            email_rep=client.email_rep,
            plan_type=PlanType[client.plan_type],
            cellphone=client.cellphone
        )
        self.db_session.add(new_client)
        self.db_session.commit()
        return client_schema.dump(new_client)

    def get(self, client_id):
        client_schema = ClientSchema()
        client = self.db_session.query(Client).filter_by(id=client_id).first()
        if not client:
            raise ValueError("Client not found")
        return client_schema.dump(client)

    def remove(self, client_id):
        LOGGER.info(f"Repository remove client: {client_id}")
        entity = self.db_session.query(Client).filter_by(id=client_id).first()
        if not entity:
            raise ValueError("Client not found")
        self.db_session.delete(entity)
        self.db_session.commit()
        LOGGER.info(f"Client {client_id} removed successfully")

    def get_all(self, query: dict[str, str]):
        client_schema = ClientSchema(many=True)
        if not query:
            result = self.db_session.query(Client).all()
            return client_schema.dump(result)

        filters = []
        if 'id_type' in query:
            filters.append(Client.id_type == DocumentType[query['id_type']])
        if 'legal_name' in query:
            filters.append(Client.legal_name.ilike(f"%{query['legal_name']}%"))
        if 'id_number' in query:
            filters.append(Client.id_number == query['id_number'])
        if 'address' in query:
            filters.append(Client.address.ilike(f"%{query['address']}%"))
        if 'name_rep' in query:
            filters.append(Client.name_rep.ilike(f"%{query['name_rep']}%"))
        if 'email_rep' in query:
            filters.append(Client.email_rep.ilike(f"%{query['email_rep']}%"))

        result = self.db_session.query(Client).filter(and_(*filters)).all()
        return client_schema.dump(result)

    def update(self, client_id, data) -> None:
        LOGGER.info(f"Repository update client ID: {client_id} with data: {data}")

        client = self.db_session.query(Client).filter_by(id=client_id).first()
        if not client:
            raise ValueError("Client not found")

        if 'perfil' in data:
            client.perfil = data['perfil']
        if 'id_type' in data:
            client.id_type = DocumentType[data['id_type']]
        if 'legal_name' in data:
            client.legal_name = data['legal_name']
        if 'id_number' in data:
            client.id_number = data['id_number']
        if 'address' in data:
            client.address = data['address']
        if 'type_document_rep' in data:
            client.type_document_rep = DocumentType[data['type_document_rep']]
        if 'id_rep_lega' in data:
            client.id_rep_lega = data['id_rep_lega']
        if 'name_rep' in data:
            client.name_rep = data['name_rep']
        if 'last_name_rep' in data:
            client.last_name_rep = data['last_name_rep']
        if 'email_rep' in data:
            client.email_rep = data['email_rep']
        if 'plan_type' in data:
            client.plan_type = PlanType[data['plan_type']]
        if 'cellphone' in data:
            client.cellphone = data['cellphone']

        self.db_session.commit()
        LOGGER.info(f"Client {client_id} updated successfully")
