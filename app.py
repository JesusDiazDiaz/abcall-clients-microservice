import logging
import re

import boto3
from chalice import Chalice, BadRequestError, CognitoUserPoolAuthorizer, UnauthorizedError, NotFoundError, \
    ChaliceViewError

from chalicelib.src.config.db import init_db
from chalicelib.src.modules.application.commands.create_client import CreateClientCommand
from chalicelib.src.modules.application.commands.delete_client import DeleteClientCommand
from chalicelib.src.modules.application.commands.update_client import UpdateClientCommand
from chalicelib.src.modules.application.queries.get_client import GetClientQuery
from chalicelib.src.modules.application.queries.get_clients import GetClientsQuery
from chalicelib.src.modules.application.queries.get_my_client import GetMyClientQuery
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.queries import execute_query

app = Chalice(app_name='abcall-clients-microservice')
app.debug = True

LOGGER = logging.getLogger('abcall-clients-microservice')

authorizer = CognitoUserPoolAuthorizer(
    'AbcPool',
    provider_arns=['arn:aws:cognito-idp:us-east-1:044162189377:userpool/us-east-1_YDIpg1HiU']
)

cognito_client = boto3.client('cognito-idp', region_name='us-east-1')

USER_POOL_ID = 'us-east-1_YDIpg1HiU'
CLIENT_ID = '65sbvtotc1hssqecgusj1p3f9g'


def check_superadmin_role(user_info):
    try:
        user_role = user_info['custom:custom:userRole']
        if str(user_role).lower() != 'superadmin':
            raise UnauthorizedError("Access denied, only 'superadmin' role is allowed")
    except Exception as e:
        raise UnauthorizedError(f"Error checking user role: {str(e)}")


@app.route('/clients', cors=True, methods=['GET'], authorizer=authorizer)
def index():
    auth_info = app.current_request.context['authorizer']['claims']
    check_superadmin_role(auth_info)

    try:
        query_result = execute_query(GetClientsQuery())
        return query_result.result
    except Exception as e:
        LOGGER.error(f"Error fetching clients: {str(e)}")
        raise ChaliceViewError('An error occurred while fetching the client')


@app.route('/client/{client_id}', cors=True, methods=['GET'], authorizer=authorizer)
def client_get(client_id):
    auth_info = app.current_request.context['authorizer']['claims']
    check_superadmin_role(auth_info)

    if not client_id:
        raise BadRequestError('Invalid client id')

    try:
        query_result = execute_query(GetClientQuery(client_id=client_id))
        if not query_result.result:
            raise NotFoundError('Client not found')

        return {'status': 'success', 'data': query_result.result}

    except Exception as e:
        LOGGER.error(f"Error fetching client: {str(e)}")
        raise ChaliceViewError('An error occurred while fetching the client')


@app.route('/client/{client_id}', cors=True, methods=['DELETE'], authorizer=authorizer)
def client_delete(client_id):
    auth_info = app.current_request.context['authorizer']['claims']
    check_superadmin_role(auth_info)

    if not client_id:
        raise BadRequestError('Invalid client id')

    command = DeleteClientCommand(client_id=client_id)

    try:
        execute_command(command)
        return {'status': 'success'}

    except Exception as e:
        LOGGER.error(f"Error fetching client: {str(e)}")
        raise ChaliceViewError('An error occurred while deleting the client')


@app.route('/client/{client_id}', cors=True, methods=['PUT'], authorizer=authorizer)
def client_update(client_id):
    auth_info = app.current_request.context['authorizer']['claims']
    check_superadmin_role(auth_info)

    if not client_id:
        return {'status': 'fail', 'message': 'Invalid client id'}, 400

    command = UpdateClientCommand(client_id=client_id, client_data=app.current_request.json_body)

    try:
        execute_command(command)
        return {'status': 'success'}

    except Exception as e:
        LOGGER.error(f"Error fetching client: {str(e)}")
        raise ChaliceViewError('An error occurred while fetching the client')


@app.route('/client', cors=True, methods=['POST'], authorizer=authorizer)
def client_post():
    auth_info = app.current_request.context['authorizer']['claims']
    check_superadmin_role(auth_info)

    client_as_json = app.current_request.json_body
    LOGGER.info("Receive create client request")
    required_fields = [
        "perfil", "id_type", "legal_name", "id_number", "address", "type_document_rep", "id_rep_lega", "name_rep",
        "last_name_rep", "email_rep", "plan_type"]
    for field in required_fields:
        if field not in client_as_json:
            raise BadRequestError(f"Missing required field: {field}")

    valid_types = ["cedula", "passport", "cedula_extranjeria", "NIT"]
    if client_as_json["id_type"] not in valid_types:
        raise BadRequestError(f"Invalid 'id type' value. Must be one of {valid_types}")

    valid_types = ["cedula", "passport", "cedula_extranjeria"]
    if client_as_json["type_document_rep"] not in valid_types:
        raise BadRequestError(f"Invalid 'document type for legal representative' value. Must be one of {valid_types}")

    valid_types = ['emprendedor', 'empresario', 'empresario_plus']
    if client_as_json["plan_type"] not in valid_types:
        raise BadRequestError(f"Invalid 'plan type' {client_as_json['id_rep_lega']}. Must be one of {valid_types}")

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, client_as_json["email_rep"]):
        raise BadRequestError("Invalid email format")

    command = CreateClientCommand(
        perfil=client_as_json["perfil"],
        id_type=client_as_json["id_type"],
        legal_name=client_as_json["legal_name"],
        id_number=client_as_json["id_number"],
        address=client_as_json["address"],
        type_document_rep=client_as_json["type_document_rep"],
        id_rep_lega=client_as_json["id_rep_lega"],
        name_rep=client_as_json["name_rep"],
        last_name_rep=client_as_json["last_name_rep"],
        email_rep=client_as_json["email_rep"],
        plan_type=client_as_json["plan_type"],
        cellphone=client_as_json.get("cellphone", "")
    )

    result = execute_command(command)

    return {'status': "ok", 'message': "Client created successfully", "data": result}


@app.route('/client/my', cors=True, methods=['GET'], authorizer=authorizer)
def my_client():
    auth_info = app.current_request.context['authorizer']['claims']

    try:
        query_result = execute_query(GetMyClientQuery(user_sub=auth_info['sub']))
        if not query_result.result:
            raise NotFoundError("Client not found")

        return {'status': 'success', 'data': query_result.result}

    except Exception as e:
        LOGGER.error(f"Error fetching client: {str(e)}")
        raise ChaliceViewError('An error occurred while fetching the client')


@app.route('/clients/short', cors=True, methods=['GET'])
def clients_short():
    try:
        query_result = execute_query(GetClientsQuery())
        return [{'id': cli['id'], 'legal_name': cli['legal_name']} for cli in query_result.result]
    except Exception as e:
        LOGGER.error(f"Error fetching clients: {str(e)}")
        raise ChaliceViewError('An error occurred while fetching the client')


@app.route('/migrate', methods=['POST'])
def migrate():
    try:
        init_db(migrate=True)
        return {"message": "Tablas creadas con éxito"}
    except Exception as e:
        return {"error": str(e)}
