import datetime
import json
import unittest
from unittest.mock import patch, MagicMock
import boto3
from chalice.test import Client
from moto import mock_aws
import app
import jwt


class TestClientService(unittest.TestCase):

    def create_test_jwt(self):
        secret = 'your_secret'
        payload = {
            'sub': 'testuser',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, secret, algorithm='HS256')
        return token

    @mock_aws
    def setUp(self):
        self.cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
        self.user_pool_id = self.cognito_client.create_user_pool(PoolName='TestPool')['UserPool']['Id']

        self.username = 'testuser'
        self.password = 'TestPassword123!'
        self.cognito_client.admin_create_user(
            UserPoolId=self.user_pool_id,
            Username=self.username,
            UserAttributes=[
                {'Name': 'email', 'Value': 'testuser@example.com'},
                {'Name': 'custom:user_role', 'Value': 'superadmin'}
            ]
        )

        self.access_token = self.create_test_jwt()
        self.test_client = Client(app.app)
        self.client_data = {
            "perfil": "Empresa",
            "id_type": "NIT",
            "legal_name": "Claro",
            "id_number": "123456789",
            "address": "calle falsa 123",
            "type_document_rep": "cedula",
            "id_rep_lega": "45678913",
            "name_rep": "Test",
            "last_name_rep": "Tester",
            "email_rep": "testTester@gmail.com",
            "plan_type": "empresario_plus",
            "cellphone": ""
        }

    def tearDown(self):
        self.cognito_client = None
        self.test_client = None

    @patch("app.CognitoUserPoolAuthorizer")
    def test_get_clients(self, mock_authorizer):
        mock_authorizer.return_value.get_claims.return_value = {
            'sub': {
                'Username': self.username,
                'UserAttributes': [
                    {'Name': 'email', 'Value': 'testuser@example.com'},
                    {'Name': 'custom:user_role', 'Value': 'superadmin'}
                ]
            }
        }

        mock_authorizer.authorizer = {
            'context': {
                'authorizer': {
                    'claims': {
                        'sub': '1234567890',
                        'name': 'John Doe',
                        'email': 'john.doe@example.com'
                    }
                }
            }
        }

        headers = {'Authorization': self.access_token, 'Content-Type': 'application/json'}
        response = self.test_client.http.get('/clients', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json_body), 0)

    @patch('app.cognito_client', autospec=True)
    def test_create_client(self, mock_cognito):
        client_data = {
            "perfil": "Test Perfil",
            "id_type": "cedula",
            "legal_name": "Test Legal Name",
            "id_number": "1234567890",
            "address": "123 Test Street",
            "type_document_rep": "cedula",
            "id_rep_lega": "987654321",
            "name_rep": "John",
            "last_name_rep": "Doe",
            "email_rep": "john.doe@example.com",
            "plan_type": "emprendedor"
        }

        headers = {'Authorization': self.access_token, 'Content-Type': 'application/json'}
        response = self.test_client.http.post('/client', body=json.dumps(client_data), headers=headers)

        self.assertEqual(response.status_code, 200)
        response_body = response.json_body[0]
        self.assertEqual(response_body['message'], "Client created successfully")
        self.client_data = response_body['data']

        headers = {'Authorization': self.access_token}
        response = self.test_client.http.get('/client/' + str(self.client_data['id']), headers=headers)
        response_body = response.json_body[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client_data, response_body['data'])

        headers = {'Authorization': self.access_token}
        response = self.test_client.http.delete('/client/' + str(self.client_data['id']), headers=headers)

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
