"""Natural Payments SDK - AI agent payment infrastructure.

https://natural.co
"""

from naturalpay.client import NaturalClient
from naturalpay._sync_client import NaturalClientSync
from naturalpay.exceptions import (
    AuthenticationError,
    InsufficientFundsError,
    InvalidRequestError,
    NaturalError,
    PaymentError,
    RateLimitError,
    RecipientNotFoundError,
    ServerError,
)
from naturalpay.models import (
    AccountBalance,
    Agent,
    AgentCreateResponse,
    AgentListResponse,
    AgentUpdateResponse,
    CancellationResult,
    Customer,
    CustomerPartyInfo,
    Delegation,
    DelegationListResponse,
    DepositResponse,
    Payment,
    Transaction,
    TransferDetail,
    TransferListResponse,
    TransferSummary,
    WithdrawResponse,
)

__version__ = "0.0.4"

__all__ = [
    # Clients
    "NaturalClient",
    "NaturalClientSync",
    # Models
    "Payment",
    "AccountBalance",
    "Transaction",
    "CancellationResult",
    "TransferSummary",
    "TransferDetail",
    "TransferListResponse",
    # Wallet models
    "DepositResponse",
    "WithdrawResponse",
    # Agent models
    "Agent",
    "AgentCreateResponse",
    "AgentUpdateResponse",
    "AgentListResponse",
    # Delegation models
    "Delegation",
    "DelegationListResponse",
    # Customer models
    "Customer",
    "CustomerPartyInfo",
    # Exceptions
    "NaturalError",
    "AuthenticationError",
    "InvalidRequestError",
    "PaymentError",
    "InsufficientFundsError",
    "RecipientNotFoundError",
    "RateLimitError",
    "ServerError",
]
