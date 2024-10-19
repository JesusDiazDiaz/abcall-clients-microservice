import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import ClientRepository

LOGGER = logging.getLogger('abcall-clients-microservice')


@dataclass
class CreateClientCommand(Command):
    perfil: str
    id_type: str
    legal_name: str
    id_number: str
    address: str
    type_document_rep: str
    id_rep_lega: str
    name_rep: str
    last_name_rep: str
    email_rep: str
    plan_type: str
    cellphone: str = ""


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: CreateClientCommand):
        LOGGER.info("Handle createClientCommand")

        repository = self.client_factory.create_object(ClientRepository.__class__)
        return repository.add(command)


@execute_command.register(CreateClientCommand)
def execute_update_information_command(command:  CreateClientCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
