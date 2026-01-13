"""User-related API routes."""

from typing import Annotated
from uuid import UUID

from ab_core.database.session_context import db_session_async
from ab_core.token_issuer.token_issuers import TokenIssuer
from fastapi import APIRouter, HTTPException
from fastapi import Depends as FDepends
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from ab_service.token_issuer_store.models.token_issuer import ManagedTokenIssuer
from ab_service.token_issuer_store.schema.token_issuer import CreateTokenIssuerRequest, UpdateTokenIssuerRequest

router = APIRouter(prefix="/token-issuer", tags=["Token Issuer"])


@router.get("/schema")
async def get_schema():
    """Return the discriminated-union schema (useful for dynamic forms)."""
    return TypeAdapter(TokenIssuer).json_schema()


@router.get("/{id}", response_model=ManagedTokenIssuer)
async def get(
    id: UUID,
    db_session: Annotated[AsyncSession, FDepends(db_session_async)],
):
    """Fetch a token issuer by id."""
    row = await db_session.get(ManagedTokenIssuer, id)
    if not row:
        raise HTTPException(status_code=404, detail="Token issuer not found.")
    return row


@router.post("", response_model=ManagedTokenIssuer)
async def create(
    request: CreateTokenIssuerRequest,
    db_session: Annotated[AsyncSession, FDepends(db_session_async)],
):
    """Create a token issuer."""
    row = ManagedTokenIssuer(
        name=request.name,
        token_issuer_json=request.token_issuer.model_dump(mode="json"),
        created_by=request.created_by,
    )
    db_session.add(row)
    await db_session.flush()
    return row


@router.patch("/{id}", response_model=ManagedTokenIssuer)
async def update(
    id: UUID,
    request: UpdateTokenIssuerRequest,
    db_session: Annotated[AsyncSession, FDepends(db_session_async)],
):
    """Update a token issuer."""
    row = await db_session.get(ManagedTokenIssuer, id)
    if not row:
        raise HTTPException(status_code=404, detail="Token issuer not found.")

    # Optional: name update (only if your model includes `name`)
    if request.name is not None:
        row.name = request.name
    if request.token_issuer is not None:
        row.token_issuer_json = request.token_issuer.model_dump(mode="json")

    await db_session.flush()
    return row


@router.delete("/{id}", status_code=204)
async def delete_one(
    id: UUID,
    db_session: Annotated[AsyncSession, FDepends(db_session_async)],
):
    row = await db_session.get(ManagedTokenIssuer, id)
    if not row:
        raise HTTPException(status_code=404, detail="Token issuer not found.")
    await db_session.delete(row)
    await db_session.flush()
    return None
