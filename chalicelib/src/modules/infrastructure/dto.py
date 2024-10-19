import enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Date, Text


Base = declarative_base()


class DocumentType(enum.Enum):
    cedula = "cedula"
    registro_civil = "registro_civil"
    passport = "passport"
    cedula_extranjeria = "cedula_extranjeria"
    NIT = "NIT"

class PlanType(enum.Enum):
    emprendedor = "emprendedor"
    empresario = "empresario"
    empresario_plus = "empresario_plus"

# Definición de la clase Client
class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    perfil = Column(String, nullable=False)
    id_type = Column(Enum(DocumentType), nullable=False)
    legal_name = Column(String, nullable=False)
    id_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    type_document_rep = Column(Enum(DocumentType), nullable=False)
    id_rep_lega = Column(String, nullable=False)
    name_rep = Column(String, nullable=False)
    last_name_rep = Column(String, nullable=False)
    email_rep = Column(String, nullable=False)
    plan_type = Column(Enum(PlanType), nullable=False)
    cellphone = Column(String, nullable=True, default="")

class ClientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True
