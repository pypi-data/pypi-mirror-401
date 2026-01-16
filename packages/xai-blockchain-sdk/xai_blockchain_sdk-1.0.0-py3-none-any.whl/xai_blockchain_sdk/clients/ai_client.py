from __future__ import annotations

"""
AI Client for XAI SDK

Handles AI compute task pooling and trading operations on the XAI blockchain.

Available endpoints:
- POST /ai/tasks - Submit a compute task
- GET /ai/tasks/{id} - Get task status
- GET /ai/tasks - List tasks
- GET /ai/models - List available AI models
- GET /ai/models/{name} - Get model details
- POST /ai/match - Match task to AI provider
- GET /ai/task-types - List supported task types
- GET /ai/stats - Get AI compute statistics
"""

from typing import Any

from ..exceptions import APIError
from ..http_client import HTTPClient


class AIClient:
    """
    Client for AI compute operations on XAI blockchain.

    Provides access to AI task submission, model discovery, and
    task-to-provider matching for the XAI compute pooling network.
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """
        Initialize AI Client.

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    @staticmethod
    def is_available() -> bool:
        """
        Check if AI features are available.

        Returns:
            True - AI features are available on XAI testnet
        """
        return True

    def submit_task(
        self,
        submitter: str,
        task_type: str,
        description: str,
        complexity: str = "moderate",
        priority: str = "medium",
        estimated_tokens: int = 10000,
        prefer_cost_optimization: bool = False,
    ) -> dict[str, Any]:
        """
        Submit an AI compute task to the network.

        Args:
            submitter: Address of the task submitter
            task_type: Type of task (e.g., "inference", "training", "embedding")
            description: Human-readable task description
            complexity: Task complexity level ("low", "moderate", "high")
            priority: Task priority ("low", "medium", "high", "urgent")
            estimated_tokens: Estimated token count for the task
            prefer_cost_optimization: If True, prefer cheaper providers over faster ones

        Returns:
            Task submission result including task ID and status

        Raises:
            APIError: If task submission fails
        """
        payload = {
            "submitter": submitter,
            "task_type": task_type,
            "description": description,
            "complexity": complexity,
            "priority": priority,
            "estimated_tokens": estimated_tokens,
            "prefer_cost_optimization": prefer_cost_optimization,
        }
        return self.http_client.post("/ai/tasks", data=payload)

    def get_task(self, task_id: str) -> dict[str, Any]:
        """
        Get the status and details of a specific task.

        Args:
            task_id: Unique task identifier

        Returns:
            Task details including status, provider, and results

        Raises:
            APIError: If task not found or request fails
        """
        return self.http_client.get(f"/ai/tasks/{task_id}")

    def list_tasks(
        self,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """
        List AI compute tasks.

        Args:
            status: Filter by status (e.g., "pending", "running", "completed")
            limit: Maximum number of tasks to return

        Returns:
            List of task objects

        Raises:
            APIError: If request fails
        """
        params: dict[str, Any] = {"limit": limit}
        if status:
            params["status"] = status
        response = self.http_client.get("/ai/tasks", params=params)
        # Handle both list response and wrapped response
        if isinstance(response, list):
            return response
        return response.get("tasks", [])

    def list_models(self) -> dict[str, Any]:
        """
        List available AI models in the network.

        Returns:
            Dict of model objects keyed by model name, each with capabilities and pricing

        Raises:
            APIError: If request fails
        """
        response = self.http_client.get("/ai/models")
        # Extract data from wrapped response
        if isinstance(response, dict) and "data" in response:
            return response["data"]
        return response

    def get_model(self, model_name: str) -> dict[str, Any]:
        """
        Get details for a specific AI model.

        Args:
            model_name: Name of the model

        Returns:
            Model details including capabilities, pricing, and availability

        Raises:
            APIError: If model not found or request fails
        """
        return self.http_client.get(f"/ai/models/{model_name}")

    def match_task(
        self,
        task_type: str,
        complexity: str,
        priority: str,
        estimated_tokens: int,
        available_providers: list[str] | None = None,
        prefer_cost: bool = False,
    ) -> dict[str, Any]:
        """
        Match a task specification to the best available AI provider.

        This endpoint helps find the optimal provider for a task based on
        requirements, availability, and cost/performance preferences.

        Args:
            task_type: Type of task (e.g., "inference", "training")
            complexity: Task complexity ("low", "moderate", "high")
            priority: Task priority ("low", "medium", "high", "urgent")
            estimated_tokens: Estimated token count
            available_providers: Optional list of preferred provider addresses
            prefer_cost: If True, optimize for cost; if False, optimize for speed

        Returns:
            Matching result with recommended provider and estimated cost/time

        Raises:
            APIError: If matching fails
        """
        payload: dict[str, Any] = {
            "task_type": task_type,
            "complexity": complexity,
            "priority": priority,
            "estimated_tokens": estimated_tokens,
            "prefer_cost_optimization": prefer_cost,
        }
        if available_providers:
            payload["available_providers"] = available_providers
        return self.http_client.post("/ai/match", data=payload)

    def list_task_types(self) -> list[dict[str, Any]]:
        """
        List supported AI task types.

        Returns:
            List of task type objects with name, description, and requirements

        Raises:
            APIError: If request fails
        """
        response = self.http_client.get("/ai/task-types")
        # Extract data from wrapped response
        if isinstance(response, dict) and "data" in response:
            return response["data"]
        if isinstance(response, list):
            return response
        return response.get("task_types", [])

    def get_stats(self) -> dict[str, Any]:
        """
        Get AI compute network statistics.

        Returns:
            Statistics including total tasks, active providers, average costs, etc.

        Raises:
            APIError: If request fails
        """
        response = self.http_client.get("/ai/stats")
        # Extract data from wrapped response
        if isinstance(response, dict) and "data" in response:
            return response["data"]
        return response
