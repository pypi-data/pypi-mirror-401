from __future__ import annotations

"""
Wallet Client for XAI SDK

Handles all wallet-related operations.

Note: The XAI testnet API provides limited wallet endpoints:
- GET /balance/{address} - Get wallet balance
- GET /history/{address} - Get transaction history

Wallet creation is done locally using xai.core.wallet, not via API.
"""

from typing import Any

from ..exceptions import ValidationError, WalletError
from ..http_client import HTTPClient
from ..models import Balance, Wallet, WalletType


class WalletClient:
    """Client for wallet operations."""

    def __init__(self, http_client: HTTPClient) -> None:
        """
        Initialize Wallet Client.

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    def create(
        self,
        wallet_type: WalletType = WalletType.STANDARD,
        name: str | None = None,
    ) -> Wallet:
        """
        Create a new wallet.

        Note: The XAI testnet does not have a wallet creation API endpoint.
        Wallets are created locally. Use `xai.core.wallet.Wallet.generate()`
        for local wallet creation.

        Args:
            wallet_type: Type of wallet to create
            name: Optional wallet name

        Raises:
            NotImplementedError: Wallet creation via API is not supported
        """
        raise NotImplementedError(
            "Wallet creation via API is not supported on XAI testnet. "
            "Use `from xai.core.wallet import Wallet; wallet = Wallet.generate()` "
            "for local wallet creation."
        )

    def get(self, address: str) -> Wallet:
        """
        Get wallet information.

        Note: The XAI testnet does not have a dedicated wallet info endpoint.
        Use `get_balance()` to check if an address exists and retrieve its balance.

        Args:
            address: Wallet address

        Raises:
            NotImplementedError: Wallet info endpoint is not available
        """
        if not address:
            raise ValidationError("Address is required")

        raise NotImplementedError(
            "Wallet info endpoint is not available on XAI testnet. "
            "Use `get_balance(address)` to check address balance, or "
            "`get_transactions(address)` to retrieve transaction history."
        )

    def get_balance(self, address: str) -> Balance:
        """
        Get wallet balance.

        Args:
            address: Wallet address

        Returns:
            Balance information

        Raises:
            WalletError: If balance retrieval fails
        """
        if not address:
            raise ValidationError("Address is required")

        try:
            response = self.http_client.get(f"/balance/{address}")
            # Map testnet API response fields to Balance model
            # API returns: {"address": "...", "balance": 0, "balance_base_units": "0", "balance_xai": "0.00..."}
            balance_value = response.get("balance_xai") or str(response.get("balance", "0"))
            return Balance(
                address=response["address"],
                balance=balance_value,
                locked_balance="0",
                available_balance=balance_value,
                nonce=response.get("nonce", 0),
            )
        except WalletError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise WalletError(f"Failed to get balance: {str(e)}") from e

    def get_transactions(
        self,
        address: str,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Get wallet transaction history.

        Args:
            address: Wallet address
            limit: Number of transactions to retrieve
            offset: Offset for pagination

        Returns:
            Transaction history with metadata

        Raises:
            WalletError: If transaction retrieval fails
        """
        if not address:
            raise ValidationError("Address is required")

        if limit > 100:
            limit = 100

        try:
            response = self.http_client.get(
                f"/history/{address}",
                params={"limit": limit, "offset": offset},
            )
            # Handle response - may be a list or a dict with transactions key
            if isinstance(response, list):
                transactions = response
                total = len(transactions)
            else:
                transactions = response.get("transactions", response.get("history", []))
                total = response.get("total", len(transactions))

            return {
                "transactions": transactions,
                "total": total,
                "limit": limit,
                "offset": offset,
            }
        except WalletError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise WalletError(f"Failed to get transactions: {str(e)}") from e

    def create_embedded(
        self,
        app_id: str,
        user_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create an embedded wallet.

        Note: Embedded wallets are not supported on XAI testnet.

        Args:
            app_id: Application ID
            user_id: User ID
            metadata: Optional metadata

        Raises:
            NotImplementedError: Embedded wallets are not supported
        """
        raise NotImplementedError(
            "Embedded wallets are not supported on XAI testnet."
        )

    def login_embedded(self, wallet_id: str, password: str) -> dict[str, Any]:
        """
        Login to an embedded wallet.

        Note: Embedded wallets are not supported on XAI testnet.

        Args:
            wallet_id: Embedded wallet ID
            password: Wallet password

        Raises:
            NotImplementedError: Embedded wallets are not supported
        """
        raise NotImplementedError(
            "Embedded wallets are not supported on XAI testnet."
        )
