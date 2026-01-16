from __future__ import annotations

"""
Mining Client for XAI SDK

Handles mining operations, bonuses, referrals, and reward management.
"""

from typing import Any

from ..exceptions import MiningError, ValidationError
from ..http_client import HTTPClient
from ..models import MiningStatus


class MiningClient:
    """Client for mining operations."""

    def __init__(self, http_client: HTTPClient) -> None:
        """
        Initialize Mining Client.

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    # ==========================================================================
    # Auto-Mining Control
    # ==========================================================================

    def start(self) -> dict[str, Any]:
        """
        Start automatic mining.

        Returns:
            Mining status response

        Raises:
            MiningError: If mining start fails
        """
        try:
            return self.http_client.post("/auto-mine/start", data={})
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to start mining: {str(e)}") from e

    def stop(self) -> dict[str, Any]:
        """
        Stop automatic mining.

        Returns:
            Mining status response

        Raises:
            MiningError: If mining stop fails
        """
        try:
            return self.http_client.post("/auto-mine/stop", data={})
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to stop mining: {str(e)}") from e

    def mine_block(self) -> dict[str, Any]:
        """
        Mine pending transactions (single block).

        Returns:
            Block mining result

        Raises:
            MiningError: If block mining fails
        """
        try:
            return self.http_client.post("/mine", data={})
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to mine block: {str(e)}") from e

    # ==========================================================================
    # Miner Registration & Stats
    # ==========================================================================

    def register(self, address: str, **kwargs: Any) -> dict[str, Any]:
        """
        Register as a miner.

        Args:
            address: Miner wallet address
            **kwargs: Additional registration parameters

        Returns:
            Registration response

        Raises:
            MiningError: If registration fails
        """
        if not address:
            raise ValidationError("address is required")

        try:
            payload = {"address": address, **kwargs}
            return self.http_client.post("/mining/register", data=payload)
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to register miner: {str(e)}") from e

    def get_stats(self) -> dict[str, Any]:
        """
        Get mining bonus statistics.

        Returns:
            Mining statistics including bonus info

        Raises:
            MiningError: If stats retrieval fails
        """
        try:
            return self.http_client.get("/mining/stats")
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to get mining stats: {str(e)}") from e

    def get_leaderboard(self) -> dict[str, Any]:
        """
        Get mining bonus leaderboard.

        Returns:
            Leaderboard data

        Raises:
            MiningError: If leaderboard retrieval fails
        """
        try:
            return self.http_client.get("/mining/leaderboard")
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to get leaderboard: {str(e)}") from e

    # ==========================================================================
    # Address-Specific Mining Data
    # ==========================================================================

    def get_streak(self, address: str) -> dict[str, Any]:
        """
        Get mining streak for an address.

        Args:
            address: Wallet address

        Returns:
            Streak information

        Raises:
            MiningError: If streak retrieval fails
        """
        if not address:
            raise ValidationError("address is required")

        try:
            return self.http_client.get(f"/mining/streak/{address}")
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to get mining streak: {str(e)}") from e

    def get_achievements(self, address: str) -> dict[str, Any]:
        """
        Get mining achievements for an address.

        Args:
            address: Wallet address

        Returns:
            Achievement data

        Raises:
            MiningError: If achievement retrieval fails
        """
        if not address:
            raise ValidationError("address is required")

        try:
            return self.http_client.get(f"/mining/achievements/{address}")
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to get achievements: {str(e)}") from e

    def get_user_bonuses(self, address: str) -> dict[str, Any]:
        """
        Get user bonuses for an address.

        Args:
            address: Wallet address

        Returns:
            User bonus information

        Raises:
            MiningError: If bonus retrieval fails
        """
        if not address:
            raise ValidationError("address is required")

        try:
            return self.http_client.get(f"/mining/user-bonuses/{address}")
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to get user bonuses: {str(e)}") from e

    # ==========================================================================
    # Bonus & Referral System
    # ==========================================================================

    def claim_bonus(self, address: str, bonus_type: str, **kwargs: Any) -> dict[str, Any]:
        """
        Claim a social bonus.

        Args:
            address: Wallet address claiming the bonus
            bonus_type: Type of bonus to claim
            **kwargs: Additional claim parameters

        Returns:
            Claim result

        Raises:
            MiningError: If bonus claim fails
        """
        if not address:
            raise ValidationError("address is required")
        if not bonus_type:
            raise ValidationError("bonus_type is required")

        try:
            payload = {"address": address, "bonus_type": bonus_type, **kwargs}
            return self.http_client.post("/mining/claim-bonus", data=payload)
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to claim bonus: {str(e)}") from e

    def create_referral(self, address: str) -> dict[str, Any]:
        """
        Create a referral code.

        Args:
            address: Wallet address to create referral for

        Returns:
            Referral code information

        Raises:
            MiningError: If referral creation fails
        """
        if not address:
            raise ValidationError("address is required")

        try:
            payload = {"address": address}
            return self.http_client.post("/mining/referral/create", data=payload)
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to create referral: {str(e)}") from e

    def use_referral(self, address: str, referral_code: str) -> dict[str, Any]:
        """
        Use a referral code.

        Args:
            address: Wallet address using the referral
            referral_code: Referral code to use

        Returns:
            Referral use result

        Raises:
            MiningError: If referral use fails
        """
        if not address:
            raise ValidationError("address is required")
        if not referral_code:
            raise ValidationError("referral_code is required")

        try:
            payload = {"address": address, "referral_code": referral_code}
            return self.http_client.post("/mining/referral/use", data=payload)
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to use referral: {str(e)}") from e

    # ==========================================================================
    # Convenience Methods
    # ==========================================================================

    def get_status(self) -> MiningStatus:
        """
        Get mining status.

        Returns:
            Mining status object

        Raises:
            MiningError: If status retrieval fails
        """
        try:
            response = self.http_client.get("/mining/stats")

            return MiningStatus(
                mining=response.get("mining", False),
                threads=response.get("threads", 1),
                hashrate=response.get("hashrate", 0.0),
                blocks_found=response.get("blocks_found", 0),
                current_difficulty=response.get("current_difficulty", 1),
                uptime=response.get("uptime", 0),
                last_block_time=response.get("last_block_time"),
            )
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise MiningError(f"Failed to get mining status: {str(e)}") from e

    def is_mining(self) -> bool:
        """
        Check if mining is active.

        Returns:
            True if mining is active

        Raises:
            MiningError: If check fails
        """
        try:
            status = self.get_status()
            return status.mining
        except MiningError:
            raise
        except (KeyError, ValueError, TypeError, AttributeError) as e:
            raise MiningError(f"Failed to check mining status: {str(e)}") from e
