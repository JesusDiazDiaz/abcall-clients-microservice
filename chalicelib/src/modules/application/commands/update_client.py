import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import ClientRepository

LOGGER = logging.getLogger('abcall-clients-microservice')


@dataclass
class UpdateClientCommand(Command):
    client_id: str
    client_data: dict


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: UpdateClientCommand):
        LOGGER.info("Handle createClientCommand")

        repository = self.client_factory.create_object(ClientRepository.__class__)
        repository.update(command.client_id, command.client_data)


@execute_command.register(UpdateClientCommand)
def execute_update_information_command(command:  UpdateClientCommand):
    handler = UpdateInformationHandler()
    handler.handle(command)
