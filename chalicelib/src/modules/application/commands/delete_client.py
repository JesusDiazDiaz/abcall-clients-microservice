import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import ClientRepository

LOGGER = logging.getLogger('abcall-client-microservice')


@dataclass
class DeleteClientCommand(Command):
    client_id: str


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: DeleteClientCommand):
        LOGGER.info("Handle createClientCommand")

        repository = self.client_factory.create_object(ClientRepository.__class__)
        repository.remove(command.client_id)


@execute_command.register(DeleteClientCommand)
def execute_update_information_command(command: DeleteClientCommand):
    handler = UpdateInformationHandler()
    handler.handle(command)
