"""Pydantic models for ledger operations."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field


class SWAP(BaseModel):
    """Swap operation."""

    type: Literal["SWAP"] = "SWAP"
    from_token_id: str
    to_token_id: str
    from_amount: str
    to_amount: str
    from_amount_usd: float
    to_amount_usd: float
    transaction_hash: str | None = None
    transaction_status: str | None = None
    transaction_receipt: dict[str, Any] | None = None


class LEND(BaseModel):
    type: Literal["LEND"] = "LEND"
    contract: str
    amount: int


class UNLEND(BaseModel):
    type: Literal["UNLEND"] = "UNLEND"
    contract: str
    amount: int


# Type alias for operation types (currently only SWAP is used)
# Add more operation types here as needed
Operation = SWAP | LEND | UNLEND


class STRAT_OP(BaseModel):
    op_data: Annotated[Operation, Field(discriminator="type")]
