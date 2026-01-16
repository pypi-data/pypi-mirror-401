"""
XAI Blockchain Python SDK

A lightweight SDK for interacting with the XAI blockchain platform.
Supports wallet operations, transactions, governance, AI compute, and more.

Quick Start:
    >>> from xai_blockchain_sdk import XAIClient
    >>>
    >>> # Connect to testnet
    >>> client = XAIClient(base_url="https://testnet-rpc.xaiblockchain.com")
    >>>
    >>> # Get blockchain stats
    >>> stats = client.blockchain.get_stats()
    >>> print(f"Chain height: {stats.chain_height}")
    >>>
    >>> # Check wallet balance
    >>> balance = client.wallet.get_balance("xai1abc...")
    >>> print(f"Balance: {balance.balance_xai} XAI")
    >>>
    >>> # List governance proposals
    >>> proposals = client.governance.list_proposals()
    >>>
    >>> # Get AI compute stats
    >>> ai_stats = client.ai.get_stats()

For full documentation, visit: https://docs.xaiblockchain.com/sdk/python
"""

from .client import XAIClient
from .exceptions import (
    AuthenticationError,
    NetworkError,
    RateLimitError,
    ValidationError,
    XAIError,
)
from .models import (
    Balance,
    Block,
    BlockchainStats,
    MiningStatus,
    Proposal,
    ProposalStatus,
    TradeOrder,
    Transaction,
    TransactionStatus,
    Wallet,
    WalletType,
)

__version__ = "1.0.0"
__author__ = "XAI Blockchain"
__email__ = "info@xaiblockchain.com"

__all__ = [
    # Main client
    "XAIClient",
    # Models
    "Wallet",
    "WalletType",
    "Balance",
    "Transaction",
    "TransactionStatus",
    "Block",
    "BlockchainStats",
    "Proposal",
    "ProposalStatus",
    "MiningStatus",
    "TradeOrder",
    # Exceptions
    "XAIError",
    "AuthenticationError",
    "RateLimitError",
    "NetworkError",
    "ValidationError",
]
