from __future__ import annotations

"""
Blockchain Client for XAI SDK

Handles blockchain querying and synchronization operations.
"""

from datetime import datetime
from typing import Any

from ..exceptions import ValidationError, XAIError
from ..http_client import HTTPClient
from ..models import Block, BlockchainStats


class BlockchainClient:
    """Client for blockchain operations."""

    def __init__(self, http_client: HTTPClient) -> None:
        """
        Initialize Blockchain Client.

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    def get_block(self, block_number: int) -> Block:
        """
        Get block details.

        Args:
            block_number: Block number

        Returns:
            Block details

        Raises:
            XAIError: If block retrieval fails
        """
        if block_number < 0:
            raise ValidationError("block_number must be non-negative")

        try:
            response = self.http_client.get(f"/blocks/{block_number}")

            # Map testnet API fields to SDK model fields
            # API returns: index, previous_hash, transactions (array)
            # SDK expects: number, parent_hash, transactions (count)
            tx_list = response.get("transactions", [])
            tx_count = len(tx_list) if isinstance(tx_list, list) else 0
            tx_hashes = (
                [tx.get("hash", tx.get("id", "")) for tx in tx_list]
                if isinstance(tx_list, list)
                else []
            )

            return Block(
                index=response.get("index", response.get("number", 0)),
                hash=response["hash"],
                previous_hash=response.get("previous_hash", response.get("parent_hash", "")),
                timestamp=response["timestamp"],
                miner=response["miner"],
                difficulty=response.get("difficulty", 0),
                gas_limit=response.get("gas_limit"),
                gas_used=response.get("gas_used"),
                transactions=tx_list,
                transaction_hashes=tx_hashes,
                merkle_root=response.get("merkle_root"),
                miner_pubkey=response.get("miner_pubkey"),
                nonce=response.get("nonce"),
                signature=response.get("signature"),
                version=response.get("version", 1),
            )
        except XAIError:

            raise

        except (KeyError, ValueError, TypeError) as e:

            raise XAIError(f"Failed to get block: {str(e)}") from e

    def list_blocks(self, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        """
        List recent blocks.

        Args:
            limit: Number of blocks to retrieve
            offset: Offset for pagination

        Returns:
            List of blocks with metadata

        Raises:
            XAIError: If block list retrieval fails
        """
        if limit > 100:
            limit = 100

        try:
            response = self.http_client.get(
                "/blocks",
                params={"limit": limit, "offset": offset},
            )

            blocks = []
            for b in response.get("blocks", []):
                # Map testnet API fields to SDK model fields
                tx_list = b.get("transactions", [])
                tx_count = len(tx_list) if isinstance(tx_list, list) else 0

                blocks.append(
                    Block(
                        index=b.get("index", b.get("number", 0)),
                        hash=b["hash"],
                        previous_hash=b.get("previous_hash", b.get("parent_hash", "")),
                        timestamp=b["timestamp"],
                        miner=b["miner"],
                        difficulty=b.get("difficulty", 0),
                        gas_limit=b.get("gas_limit"),
                        gas_used=b.get("gas_used"),
                        transactions=tx_list,
                        merkle_root=b.get("merkle_root"),
                        nonce=b.get("nonce"),
                        version=b.get("version", 1),
                    )
                )

            return {
                "blocks": blocks,
                "total": response.get("total", 0),
                "limit": response.get("limit", limit),
                "offset": response.get("offset", offset),
            }
        except XAIError:

            raise

        except (KeyError, ValueError, TypeError) as e:

            raise XAIError(f"Failed to list blocks: {str(e)}") from e

    def get_block_transactions(self, block_number: int) -> list[dict[str, Any]]:
        """
        Get transactions in a block.

        Args:
            block_number: Block number

        Returns:
            List of transactions

        Raises:
            XAIError: If transaction retrieval fails
        """
        if block_number < 0:
            raise ValidationError("block_number must be non-negative")

        try:
            response = self.http_client.get(
                f"/blocks/{block_number}/transactions"
            )
            return response.get("transactions", [])
        except XAIError:

            raise

        except (KeyError, ValueError, TypeError) as e:

            raise XAIError(f"Failed to get block transactions: {str(e)}") from e

    def get_sync_status(self) -> dict[str, Any]:
        """
        Get blockchain synchronization status.

        Returns:
            Sync status information

        Raises:
            XAIError: If sync status retrieval fails
        """
        try:
            return self.http_client.get("/sync")
        except XAIError:

            raise

        except (KeyError, ValueError, TypeError) as e:

            raise XAIError(f"Failed to get sync status: {str(e)}") from e

    def is_synced(self) -> bool:
        """
        Check if blockchain is synchronized.

        Returns:
            True if blockchain is synced

        Raises:
            XAIError: If check fails
        """
        try:
            status = self.get_sync_status()
            return not status.get("syncing", False)
        except XAIError:

            raise

        except (KeyError, ValueError, TypeError) as e:

            raise XAIError(f"Failed to check sync status: {str(e)}") from e

    def get_stats(self) -> BlockchainStats:
        """
        Get blockchain statistics.

        Returns:
            Blockchain statistics

        Raises:
            XAIError: If stats retrieval fails
        """
        try:
            response = self.http_client.get("/stats")

            # Map testnet API fields to SDK model fields
            return BlockchainStats(
                chain_height=response.get("chain_height", 0),
                difficulty=response.get("difficulty", 0),
                is_mining=response.get("is_mining", False),
                latest_block_hash=response.get("latest_block_hash"),
                miner_address=response.get("miner_address"),
                node_uptime=response.get("node_uptime", 0.0),
                orphan_blocks_count=response.get("orphan_blocks_count", 0),
                peers=response.get("peers", 0),
                pending_transactions_count=response.get("pending_transactions_count", 0),
                total_circulating_supply=response.get("total_circulating_supply", 0.0),
                network=response.get("network", "testnet"),
            )
        except XAIError:

            raise

        except (KeyError, ValueError, TypeError) as e:

            raise XAIError(f"Failed to get blockchain stats: {str(e)}") from e

    def get_node_info(self) -> dict[str, Any]:
        """
        Get blockchain node information.

        Returns:
            Node information

        Raises:
            XAIError: If node info retrieval fails
        """
        try:
            return self.http_client.get("/")
        except XAIError:

            raise

        except (KeyError, ValueError, TypeError) as e:

            raise XAIError(f"Failed to get node info: {str(e)}") from e

    def get_health(self) -> dict[str, Any]:
        """
        Get node health status.

        Returns:
            Health information

        Raises:
            XAIError: If health check fails
        """
        try:
            return self.http_client.get("/health")
        except XAIError:

            raise

        except (KeyError, ValueError, TypeError) as e:

            raise XAIError(f"Failed to check node health: {str(e)}") from e
