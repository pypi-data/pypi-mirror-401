from ab_core.database.mixins.created_at import CreatedAtMixin
from ab_core.database.mixins.created_by import CreatedByMixin
from ab_core.database.mixins.id import IDMixin
from ab_core.database.mixins.updated_at import UpdatedAtMixin
from ab_core.token_issuer.token_issuers import TokenIssuer
from pydantic import TypeAdapter, computed_field
from sqlalchemy import JSON, Column, Index, String, UniqueConstraint
from sqlmodel import Field, SQLModel


class ManagedTokenIssuer(IDMixin, CreatedAtMixin, CreatedByMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__ = "token_issuer"
    __table_args__ = (
        UniqueConstraint("created_by", "name", name="uq_token_issuer_creator_name"),
        # Optional helper index if you often look up by (created_by, name)
        Index("ix_token_issuer_created_by_name", "created_by", "name"),
    )

    name: str = Field(sa_column=Column(String, nullable=False, index=True))
    token_issuer_json: dict = Field(
        sa_column=Column(JSON, nullable=False),
        exclude=True,
    )

    # expose the typed union as a computed field (read-only, included in responses)
    @computed_field(return_type=TokenIssuer)
    @property
    def token_issuer(self) -> TokenIssuer:
        return TypeAdapter(TokenIssuer).validate_python(self.token_issuer_json)
