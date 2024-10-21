import json
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from chalice.test import Client

from app import app
from chalicelib.src.seedwork.application.queries import QueryResult


class TestClientService(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_clients(self):
        mock_context = {
            'authorizer': {
                'claims': {
                    'sub': 'user123',
                    'email': 'user@example.com',
                    'custom:custom:userRole': 'superadmin'
                }
            }
        }

        mock_clients = [
            {
                "id": 2,
                "perfil": "Empresa",
                "id_type": "NIT",
                "legal_name": "Abcall",
                "id_number": "345123213",
                "address": "Cra 1 #2-3",
                "type_document_rep": "cedula",
                "id_rep_lega": "234234234",
                "name_rep": "Roberto",
                "last_name_rep": "Colon",
                "email_rep": "roberto@mail.com",
                "plan_type": "empresario_plus",
                "cellphone": "3001234123"
            }
        ]

        mock_request = MagicMock()
        mock_request.context = mock_context
        mock_request.headers = {
            'Content-Type': 'application/json', 'Authorization': 'Bearer asdajdahsda'
        }

        with patch('chalice.app.Request', return_value=mock_request):
            with patch('chalicelib.src.modules.infrastructure.repository.ClientRepositoryPostgres.get_all',
                       return_value=mock_clients):
                with Client(app) as client:
                    response = client.http.get('/clients')
                    assert response.status_code == 200

                    response_data = json.loads(response.body)
                    assert response_data == mock_clients

    def test_create_client(self):
        mock_context = {
            'authorizer': {
                'claims': {
                    'sub': 'user123',
                    'email': 'user@example.com',
                    'custom:custom:userRole': 'superadmin'
                }
            }
        }

        mock_client_created = {
            "status": "ok",
            "message": "Client created successfully",
            "data": {
                "id": 3,
                "perfil": "Empresa",
                "id_type": "NIT",
                "legal_name": "Movistar",
                "id_number": "123456789",
                "address": "calle falsa 123",
                "type_document_rep": "cedula",
                "id_rep_lega": "45678913",
                "name_rep": "Pedro",
                "last_name_rep": "Perez",
                "email_rep": "pedroperez@gmail.com",
                "plan_type": "empresario_plus",
                "cellphone": ""
            }
        }

        mock_request = MagicMock()
        mock_request.context = mock_context
        mock_request.headers = {
            'Content-Type': 'application/json'
        }
        mock_request.json_body = {
            "perfil": "Empresa",
            "id_type": "NIT",
            "legal_name": "Movistar",
            "id_number": "123456789",
            "address": "calle falsa 123",
            "type_document_rep": "cedula",
            "id_rep_lega": "45678913",
            "name_rep": "Pedro",
            "last_name_rep": "Perez",
            "email_rep": "pedroperez@gmail.com",
            "plan_type": "empresario_plus"
        }

        with patch('chalice.app.Request', return_value=mock_request):
            with patch('chalicelib.src.modules.infrastructure.repository.ClientRepositoryPostgres.add',
                       return_value=mock_client_created['data']):
                with Client(app) as client:
                    response = client.http.post(
                        '/client',
                        headers={'Content-Type': 'application/json'},
                        body=json.dumps(mock_request.json_body)
                    )
                    assert response.status_code == 200

                    response_data = json.loads(response.body)
                    assert response_data == mock_client_created

    def test_get_client(self):
        mock_context = {
            'authorizer': {
                'claims': {
                    'sub': 'user123',
                    'email': 'user@example.com',
                    'custom:custom:userRole': 'superadmin'
                }
            }
        }

        mock_get_client = {
            "status": "success",
            "data": {
                "id": 2,
                "perfil": "Empresa",
                "id_type": "NIT",
                "legal_name": "Abcall",
                "id_number": "345123213",
                "address": "Cra 1 #2-3",
                "type_document_rep": "cedula",
                "id_rep_lega": "234234234",
                "name_rep": "Roberto",
                "last_name_rep": "Colon",
                "email_rep": "roberto@mail.com",
                "plan_type": "empresario_plus",
                "cellphone": "3001234123"
            }
        }

        mock_request = MagicMock()
        mock_request.context = mock_context
        mock_request.headers = {
            'Content-Type': 'application/json', 'Authorization': 'Bearer asdajdahsda'
        }

        with patch('chalice.app.Request', return_value=mock_request):
            with patch('chalicelib.src.modules.infrastructure.repository.ClientRepositoryPostgres.get',
                       return_value=mock_get_client['data']):
                with Client(app) as client:
                    response = client.http.get('/client/2')
                    assert response.status_code == 200

                    response_data = json.loads(response.body)
                    assert response_data == mock_get_client

    def test_update_client(self):
        mock_context = {
            'authorizer': {
                'claims': {
                    'sub': 'user123',
                    'email': 'user@example.com',
                    'custom:custom:userRole': 'superadmin'
                }
            }
        }

        mock_update_client = {
            "status": "success"
        }

        mock_request = MagicMock()
        mock_request.context = mock_context
        mock_request.headers = {
            'Content-Type': 'application/json', 'Authorization': 'Bearer asdajdahsda'
        }
        mock_request.json_body = {
            "perfil": "Empresa",
            "id_type": "NIT",
            "legal_name": "Movistar",
            "id_number": "123456789",
            "address": "calle falsa 123",
            "type_document_rep": "cedula",
            "id_rep_lega": "45678913",
            "name_rep": "Pedro",
            "last_name_rep": "Perez",
            "email_rep": "pedroperez@gmail.com",
            "plan_type": "empresario_plus"
        }

        with patch('chalice.app.Request', return_value=mock_request):
            with patch('chalicelib.src.modules.infrastructure.repository.ClientRepositoryPostgres.update',
                       return_value=mock_update_client):
                with Client(app) as client:
                    response = client.http.put(
                        '/client/2',
                        headers={'Content-Type': 'application/json'},
                        body=json.dumps(mock_request.json_body)
                    )
                    assert response.status_code == 200
                    response_data = json.loads(response.body)
                    assert response_data == mock_update_client

    def test_delete_client(self):
        mock_context = {
            'authorizer': {
                'claims': {
                    'sub': 'user123',
                    'email': 'user@example.com',
                    'custom:custom:userRole': 'superadmin'
                }
            }
        }

        mock_delete_client = {
            "status": "success"
        }

        mock_request = MagicMock()
        mock_request.context = mock_context
        mock_request.headers = {
            'Content-Type': 'application/json', 'Authorization': 'Bearer asdajdahsda'
        }

        with patch('chalice.app.Request', return_value=mock_request):
            with patch('chalicelib.src.modules.infrastructure.repository.ClientRepositoryPostgres.remove',
                       return_value=mock_delete_client):
                with Client(app) as client:
                    response = client.http.delete(
                        '/client/2',
                        headers={'Content-Type': 'application/json'}
                    )
                    assert response.status_code == 200
                    response_data = json.loads(response.body)
                    assert response_data == mock_delete_client

    def test_get_my_client(self):
        mock_context = {
            'authorizer': {
                'claims': {
                    'sub': 'user123',
                    'email': 'user@example.com',
                    'custom:custom:userRole': 'superadmin'
                }
            }
        }

        mock_my_client = {
            "status": "success",
            "data": {
                "id": 3,
                "perfil": "Empresa",
                "id_type": "NIT",
                "legal_name": "Movistar",
                "id_number": "123456789",
                "address": "calle falsa 123",
                "type_document_rep": "cedula",
                "id_rep_lega": "45678913",
                "name_rep": "Pedro",
                "last_name_rep": "Perez",
                "email_rep": "pedroperez@gmail.com",
                "plan_type": "empresario_plus",
                "cellphone": ""
            }
        }

        mock_request = MagicMock()
        mock_request.context = mock_context
        mock_request.headers = {
            'Content-Type': 'application/json', 'Authorization': 'Bearer asdajdahsda'
        }

        with Client(app) as client:
            with patch('chalice.app.Request', return_value=mock_request):
                with patch(
                        'chalicelib.src.modules.application.queries.get_my_client.GetClientHandler.handle',
                        return_value=QueryResult(result=mock_my_client['data'])):
                    response = client.http.get(
                        '/client/my',
                        headers={'Content-Type': 'application/json'}
                    )

                    assert response.status_code == 200
                    response_data = json.loads(response.body)
                    assert response_data == mock_my_client


if __name__ == '__main__':
    unittest.main()
