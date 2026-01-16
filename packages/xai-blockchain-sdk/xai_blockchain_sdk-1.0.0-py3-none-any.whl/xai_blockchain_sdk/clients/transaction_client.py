from __future__ import annotations

"""
Transaction Client for XAI SDK

Handles all transaction-related operations.

Testnet API Endpoints:
- POST /send - Submit a new transaction
- GET /transaction/{txid} - Get transaction details
- GET /transactions - Get pending transactions (paginated)
- GET /history/{address} - Get transaction history for address (paginated)
"""

import time
from typing import Any

from ..exceptions import TransactionError, ValidationError
from ..http_client import HTTPClient
from ..models import Transaction, TransactionStatus


class TransactionClient:
    """Client for transaction operations."""

    def __init__(self, http_client: HTTPClient) -> None:
        """
        Initialize Transaction Client.

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    def send(
        self,
        sender: str,
        recipient: str,
        amount: float | int | str,
        *,
        fee: float | int | str | None = None,
        public_key: str | None = None,
        signature: str | None = None,
        nonce: int | None = None,
        tx_type: str | None = None,
        timestamp: float | None = None,
        txid: str | None = None,
        metadata: dict[str, Any] | None = None,
        inputs: list[dict[str, Any]] | None = None,
        outputs: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Send a transaction.

        Submits a signed transaction to the XAI testnet via POST /send.

        Args:
            sender: Sender address
            recipient: Recipient address
            amount: Transaction amount
            fee: Transaction fee (optional)
            public_key: Sender's public key for signature verification
            signature: Transaction signature
            nonce: Transaction nonce for replay protection
            tx_type: Transaction type (default: "transfer")
            timestamp: Transaction timestamp (defaults to current time)
            txid: Pre-computed transaction ID (validated against hash)
            metadata: Optional transaction metadata
            inputs: UTXO inputs (for UTXO-based transactions)
            outputs: UTXO outputs (for UTXO-based transactions)

        Returns:
            Response containing txid and success message

        Raises:
            ValidationError: If required fields are missing
            TransactionError: If transaction submission fails
        """
        if not sender or not recipient or amount is None:
            raise ValidationError("sender, recipient, and amount are required")

        if not public_key:
            raise ValidationError("public_key is required for transaction verification")

        if not signature:
            raise ValidationError("signature is required")

        if nonce is None:
            raise ValidationError("nonce is required for replay protection")

        try:
            payload: dict[str, Any] = {
                "sender": sender,
                "recipient": recipient,
                "amount": amount,
                "public_key": public_key,
                "signature": signature,
                "nonce": nonce,
            }

            if fee is not None:
                payload["fee"] = fee
            if tx_type:
                payload["tx_type"] = tx_type
            if timestamp is not None:
                payload["timestamp"] = timestamp
            else:
                payload["timestamp"] = time.time()
            if txid:
                payload["txid"] = txid
            if metadata:
                payload["metadata"] = metadata
            if inputs:
                payload["inputs"] = inputs
            if outputs:
                payload["outputs"] = outputs

            response = self.http_client.post("/send", data=payload)
            return response
        except TransactionError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise TransactionError(f"Failed to send transaction: {e}") from e

    def get(self, txid: str) -> Transaction:
        """
        Get transaction details.

        Retrieves transaction details via GET /transaction/{txid}.

        Args:
            txid: Transaction ID (hash)

        Returns:
            Transaction object with details

        Raises:
            ValidationError: If txid is empty
            TransactionError: If transaction retrieval fails
        """
        if not txid:
            raise ValidationError("txid is required")

        try:
            response = self.http_client.get(f"/transaction/{txid}")

            if not response.get("found", False):
                raise TransactionError(f"Transaction not found: {txid}")

            tx_data = response.get("transaction", {})
            status_str = response.get("status", "confirmed")
            if status_str == "pending":
                status = TransactionStatus.PENDING
            else:
                status = TransactionStatus.CONFIRMED

            return Transaction(
                hash=tx_data.get("txid", txid),
                from_address=tx_data.get("sender", ""),
                to_address=tx_data.get("recipient", ""),
                amount=str(tx_data.get("amount", "0")),
                timestamp=tx_data.get("timestamp"),
                status=status,
                fee=str(tx_data.get("fee", "0")),
                block_number=response.get("block"),
                confirmations=response.get("confirmations", 0),
            )
        except TransactionError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise TransactionError(f"Failed to get transaction: {e}") from e

    def get_pending(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Get pending transactions.

        Retrieves pending (unconfirmed) transactions via GET /transactions.

        Args:
            limit: Maximum number of transactions to return (default: 50, max: 500)
            offset: Number of transactions to skip for pagination (default: 0)

        Returns:
            Response containing:
                - count: Total number of pending transactions
                - limit: Applied limit
                - offset: Applied offset
                - transactions: List of pending transaction objects

        Raises:
            TransactionError: If retrieval fails
        """
        try:
            params = {"limit": limit, "offset": offset}
            return self.http_client.get("/transactions", params=params)
        except TransactionError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise TransactionError(f"Failed to get pending transactions: {e}") from e

    def get_history(
        self,
        address: str,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Get transaction history for an address.

        Retrieves paginated transaction history via GET /history/{address}.

        Args:
            address: Blockchain address to query
            limit: Maximum transactions to return (default: 50, max: 500)
            offset: Number of transactions to skip (default: 0)

        Returns:
            Response containing:
                - address: The queried address
                - transaction_count: Total transactions for this address
                - limit: Applied limit
                - offset: Applied offset
                - transactions: List of transaction objects

        Raises:
            ValidationError: If address is empty
            TransactionError: If retrieval fails
        """
        if not address:
            raise ValidationError("address is required")

        try:
            params = {"limit": limit, "offset": offset}
            return self.http_client.get(f"/history/{address}", params=params)
        except TransactionError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise TransactionError(f"Failed to get transaction history: {e}") from e

    def is_confirmed(self, txid: str, min_confirmations: int = 1) -> bool:
        """
        Check if transaction is confirmed.

        Args:
            txid: Transaction ID (hash)
            min_confirmations: Minimum required confirmations (default: 1)

        Returns:
            True if transaction has at least min_confirmations

        Raises:
            TransactionError: If check fails
        """
        try:
            tx = self.get(txid)
            return tx.confirmations >= min_confirmations
        except TransactionError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise TransactionError(f"Failed to check confirmation: {e}") from e

    def wait_for_confirmation(
        self,
        txid: str,
        min_confirmations: int = 1,
        timeout: int = 600,
        poll_interval: int = 5,
    ) -> Transaction:
        """
        Wait for transaction confirmation.

        Polls the transaction status until it reaches the required
        number of confirmations or times out.

        Args:
            txid: Transaction ID (hash)
            min_confirmations: Required number of confirmations (default: 1)
            timeout: Maximum time to wait in seconds (default: 600)
            poll_interval: Polling interval in seconds (default: 5)

        Returns:
            Confirmed transaction object

        Raises:
            TransactionError: If confirmation times out or fails
        """
        start_time = time.time()

        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TransactionError(
                    f"Transaction confirmation timeout after {timeout}s"
                )

            try:
                tx = self.get(txid)
                if tx.confirmations >= min_confirmations:
                    return tx
            except TransactionError as e:
                if "not found" in str(e).lower():
                    pass
                else:
                    raise

            time.sleep(poll_interval)
