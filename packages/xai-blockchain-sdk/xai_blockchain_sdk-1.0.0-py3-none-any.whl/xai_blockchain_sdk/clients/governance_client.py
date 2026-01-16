from __future__ import annotations

"""
Governance Client for XAI SDK

Handles governance and voting operations.
"""

from datetime import datetime
from typing import Any

from ..exceptions import GovernanceError, ValidationError
from ..http_client import HTTPClient
from ..models import Proposal, ProposalStatus


class GovernanceClient:
    """Client for governance operations."""

    def __init__(self, http_client: HTTPClient) -> None:
        """
        Initialize Governance Client.

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    def list_proposals(
        self,
        status: str | None = None,
    ) -> dict[str, Any]:
        """
        List governance proposals.

        Args:
            status: Filter by proposal status

        Returns:
            List of proposals with metadata

        Raises:
            GovernanceError: If proposal list retrieval fails
        """
        try:
            params: dict[str, Any] = {}
            if status:
                params["status"] = status

            response = self.http_client.get("/governance/proposals", params=params)

            # Extract data from wrapped response
            data = response.get("data", response) if isinstance(response, dict) else response
            proposal_list = data if isinstance(data, list) else data.get("proposals", [])

            proposals = [
                Proposal(
                    id=p["id"],
                    title=p["title"],
                    description=p["description"],
                    creator=p.get("submitter", p.get("creator", "")),
                    status=ProposalStatus(p.get("status", "pending")),
                    created_at=datetime.fromisoformat(p["created_at"])
                    if p.get("created_at")
                    else None,
                    voting_ends_at=datetime.fromisoformat(p["voting_ends_at"])
                    if p.get("voting_ends_at")
                    else None,
                    votes_for=p.get("votes_for", 0),
                    votes_against=p.get("votes_against", 0),
                    votes_abstain=p.get("votes_abstain", 0),
                )
                for p in proposal_list
            ]

            return {
                "proposals": proposals,
                "total": response.get("total", len(proposals)),
            }
        except GovernanceError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise GovernanceError(f"Failed to list proposals: {str(e)}") from e

    def get_proposal(self, proposal_id: int) -> Proposal:
        """
        Get proposal details.

        Args:
            proposal_id: Proposal ID

        Returns:
            Proposal details

        Raises:
            GovernanceError: If proposal retrieval fails
        """
        if proposal_id < 0:
            raise ValidationError("proposal_id must be non-negative")

        try:
            response = self.http_client.get(f"/governance/proposals/{proposal_id}")

            return Proposal(
                id=response["id"],
                title=response["title"],
                description=response["description"],
                creator=response.get("submitter", response.get("creator", "")),
                status=ProposalStatus(response.get("status", "pending")),
                created_at=datetime.fromisoformat(response["created_at"])
                if response.get("created_at")
                else None,
                voting_starts_at=datetime.fromisoformat(response["voting_starts_at"])
                if response.get("voting_starts_at")
                else None,
                voting_ends_at=datetime.fromisoformat(response["voting_ends_at"])
                if response.get("voting_ends_at")
                else None,
                votes_for=response.get("votes_for", 0),
                votes_against=response.get("votes_against", 0),
                votes_abstain=response.get("votes_abstain", 0),
            )
        except GovernanceError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise GovernanceError(f"Failed to get proposal: {str(e)}") from e

    def submit_proposal(
        self,
        title: str,
        description: str,
        proposal_type: str,
        submitter: str,
        payload: dict[str, Any] | None = None,
    ) -> Proposal:
        """
        Submit a governance proposal.

        Args:
            title: Proposal title
            description: Proposal description
            proposal_type: Type of proposal
            submitter: Address of submitter
            payload: Optional proposal data/payload

        Returns:
            Created proposal

        Raises:
            GovernanceError: If proposal submission fails
        """
        if not title or not description or not submitter:
            raise ValidationError("title, description, and submitter are required")

        if not proposal_type:
            raise ValidationError("proposal_type is required")

        try:
            request_body: dict[str, Any] = {
                "submitter": submitter,
                "title": title,
                "description": description,
                "proposal_type": proposal_type,
            }

            if payload:
                request_body["proposal_data"] = payload

            response = self.http_client.post("/governance/proposals", data=request_body)

            return Proposal(
                id=response["id"],
                title=response["title"],
                description=response["description"],
                creator=response.get("submitter", response.get("creator", submitter)),
                status=ProposalStatus(response.get("status", "pending")),
                created_at=datetime.fromisoformat(response["created_at"])
                if response.get("created_at")
                else None,
                votes_for=response.get("votes_for", 0),
                votes_against=response.get("votes_against", 0),
            )
        except GovernanceError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise GovernanceError(f"Failed to submit proposal: {str(e)}") from e

    def vote(self, proposal_id: int, voter: str, vote: str) -> dict[str, Any]:
        """
        Vote on a proposal.

        Args:
            proposal_id: Proposal ID
            voter: Voter address
            vote: Vote choice (yes, no, abstain)

        Returns:
            Vote confirmation

        Raises:
            GovernanceError: If voting fails
        """
        if proposal_id < 0:
            raise ValidationError("proposal_id must be non-negative")

        if not voter:
            raise ValidationError("voter is required")

        if vote not in ["yes", "no", "abstain"]:
            raise ValidationError("vote must be 'yes', 'no', or 'abstain'")

        try:
            request_body = {
                "voter": voter,
                "vote": vote,
            }

            return self.http_client.post(
                f"/governance/proposals/{proposal_id}/vote", data=request_body
            )
        except GovernanceError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise GovernanceError(f"Failed to vote: {str(e)}") from e

    def execute_proposal(self, proposal_id: int, executor: str) -> dict[str, Any]:
        """
        Execute a passed proposal.

        Args:
            proposal_id: Proposal ID
            executor: Address of executor

        Returns:
            Execution confirmation

        Raises:
            GovernanceError: If execution fails
        """
        if proposal_id < 0:
            raise ValidationError("proposal_id must be non-negative")

        if not executor:
            raise ValidationError("executor is required")

        try:
            request_body = {
                "executor": executor,
            }

            return self.http_client.post(
                f"/governance/proposals/{proposal_id}/execute", data=request_body
            )
        except GovernanceError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise GovernanceError(f"Failed to execute proposal: {str(e)}") from e

    def get_voting_power(self, address: str) -> dict[str, Any]:
        """
        Get voting power for an address.

        Args:
            address: Wallet address

        Returns:
            Voting power information

        Raises:
            GovernanceError: If retrieval fails
        """
        if not address:
            raise ValidationError("address is required")

        try:
            return self.http_client.get(f"/governance/voting-power/{address}")
        except GovernanceError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise GovernanceError(f"Failed to get voting power: {str(e)}") from e

    def get_stats(self) -> dict[str, Any]:
        """
        Get governance statistics.

        Returns:
            Governance stats

        Raises:
            GovernanceError: If retrieval fails
        """
        try:
            response = self.http_client.get("/governance/stats")
            # Extract data from wrapped response
            if isinstance(response, dict) and "data" in response:
                return response["data"]
            return response
        except GovernanceError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise GovernanceError(f"Failed to get governance stats: {str(e)}") from e

    def get_active_proposals(self) -> list[Proposal]:
        """
        Get active proposals.

        Returns:
            List of active proposals

        Raises:
            GovernanceError: If retrieval fails
        """
        try:
            result = self.list_proposals(status="active")
            return result["proposals"]
        except GovernanceError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise GovernanceError(f"Failed to get active proposals: {str(e)}") from e

    def get_proposal_votes(self, proposal_id: int) -> dict[str, Any]:
        """
        Get vote details for a proposal.

        Args:
            proposal_id: Proposal ID

        Returns:
            Vote information

        Raises:
            GovernanceError: If retrieval fails
        """
        try:
            proposal = self.get_proposal(proposal_id)
            return {
                "proposal_id": proposal.id,
                "votes_for": proposal.votes_for,
                "votes_against": proposal.votes_against,
                "votes_abstain": proposal.votes_abstain,
                "total_votes": proposal.total_votes,
            }
        except GovernanceError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise GovernanceError(f"Failed to get proposal votes: {str(e)}") from e

    @classmethod
    def is_available(cls) -> bool:
        """
        Check if governance features are available.

        Returns:
            True - governance is now available
        """
        return True
