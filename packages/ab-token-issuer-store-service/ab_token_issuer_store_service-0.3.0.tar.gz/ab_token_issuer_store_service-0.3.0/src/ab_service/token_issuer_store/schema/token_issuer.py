from uuid import UUID

from ab_core.token_issuer.token_issuers import TokenIssuer
from pydantic import BaseModel


class CreateTokenIssuerRequest(BaseModel):
    created_by: UUID
    name: str
    token_issuer: TokenIssuer


class UpdateTokenIssuerRequest(BaseModel):
    id: UUID
    created_by: UUID
    name: str
    token_issuer: TokenIssuer
