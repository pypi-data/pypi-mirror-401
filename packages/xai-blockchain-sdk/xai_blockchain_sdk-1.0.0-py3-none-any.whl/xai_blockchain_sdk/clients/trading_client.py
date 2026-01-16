from __future__ import annotations

"""
Trading Client for XAI SDK

Handles exchange trading and order management via the testnet exchange API.

Available testnet endpoints:
- GET /exchange/orders - List all orders
- POST /exchange/place-order - Place a new order
- POST /exchange/cancel-order - Cancel an order
- GET /exchange/trades - Get trade history
- GET /exchange/balance/{address} - Get exchange balance
- GET /exchange/my-orders/{address} - Get orders for an address
- GET /exchange/price-history - Get price history
- GET /exchange/stats - Get exchange statistics
"""

from datetime import datetime
from typing import Any

from ..exceptions import ValidationError, XAIError
from ..http_client import HTTPClient
from ..models import TradeOrder


class TradingClient:
    """Client for exchange trading operations."""

    def __init__(self, http_client: HTTPClient) -> None:
        """
        Initialize Trading Client.

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    def list_orders(self) -> list[TradeOrder]:
        """
        List all active trade orders on the exchange.

        Returns:
            List of trade orders

        Raises:
            XAIError: If order list retrieval fails
        """
        try:
            response = self.http_client.get("/exchange/orders")

            orders_data = response if isinstance(response, list) else response.get("orders", [])

            orders = []
            for o in orders_data:
                orders.append(
                    TradeOrder(
                        id=o.get("id", o.get("order_id", "")),
                        from_address=o.get("from_address", o.get("maker", "")),
                        to_address=o.get("to_address", o.get("taker", "")),
                        from_amount=str(o.get("from_amount", o.get("amount", o.get("price", "0")))),
                        to_amount=str(o.get("to_amount", o.get("total", "0"))),
                        created_at=datetime.fromisoformat(o["created_at"])
                        if o.get("created_at")
                        else datetime.now(),
                        status=o.get("status", "pending"),
                        expires_at=datetime.fromisoformat(o["expires_at"])
                        if o.get("expires_at")
                        else None,
                    )
                )

            return orders
        except XAIError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise XAIError(f"Failed to list trade orders: {str(e)}") from e

    def get_my_orders(self, address: str) -> list[TradeOrder]:
        """
        Get orders for a specific address.

        Args:
            address: Wallet address

        Returns:
            List of orders for the address

        Raises:
            XAIError: If order retrieval fails
        """
        if not address:
            raise ValidationError("address is required")

        try:
            response = self.http_client.get(f"/exchange/my-orders/{address}")

            orders_data = response if isinstance(response, list) else response.get("orders", [])

            orders = []
            for o in orders_data:
                orders.append(
                    TradeOrder(
                        id=o.get("id", o.get("order_id", "")),
                        from_address=o.get("from_address", o.get("maker", "")),
                        to_address=o.get("to_address", o.get("taker", "")),
                        from_amount=str(o.get("from_amount", o.get("amount", o.get("price", "0")))),
                        to_amount=str(o.get("to_amount", o.get("total", "0"))),
                        created_at=datetime.fromisoformat(o["created_at"])
                        if o.get("created_at")
                        else datetime.now(),
                        status=o.get("status", "pending"),
                        expires_at=datetime.fromisoformat(o["expires_at"])
                        if o.get("expires_at")
                        else None,
                    )
                )

            return orders
        except XAIError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise XAIError(f"Failed to get orders for address: {str(e)}") from e

    def place_order(
        self,
        address: str,
        order_type: str,
        side: str,
        amount: str,
        price: str | None = None,
    ) -> dict[str, Any]:
        """
        Place a new order on the exchange.

        Args:
            address: Wallet address placing the order
            order_type: Order type ("limit" or "market")
            side: Order side ("buy" or "sell")
            amount: Amount to trade
            price: Price per unit (required for limit orders)

        Returns:
            Order placement result

        Raises:
            XAIError: If order placement fails
        """
        if not address or not order_type or not side or not amount:
            raise ValidationError("address, order_type, side, and amount are required")

        if side not in ["buy", "sell"]:
            raise ValidationError("side must be 'buy' or 'sell'")

        if order_type not in ["limit", "market"]:
            raise ValidationError("order_type must be 'limit' or 'market'")

        if order_type == "limit" and not price:
            raise ValidationError("price is required for limit orders")

        try:
            payload: dict[str, Any] = {
                "address": address,
                "order_type": order_type,
                "side": side,
                "amount": amount,
            }

            if price:
                payload["price"] = price

            return self.http_client.post("/exchange/place-order", data=payload)
        except XAIError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise XAIError(f"Failed to place order: {str(e)}") from e

    def cancel_order(self, order_id: str, address: str | None = None) -> dict[str, Any]:
        """
        Cancel an order on the exchange.

        Args:
            order_id: Order ID to cancel
            address: Address that placed the order (for verification)

        Returns:
            Cancellation confirmation

        Raises:
            XAIError: If cancellation fails
        """
        if not order_id:
            raise ValidationError("order_id is required")

        try:
            payload: dict[str, Any] = {"order_id": order_id}
            if address:
                payload["address"] = address

            return self.http_client.post("/exchange/cancel-order", data=payload)
        except XAIError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise XAIError(f"Failed to cancel order: {str(e)}") from e

    def get_trades(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get trade history from the exchange.

        Args:
            limit: Maximum number of trades to return
            offset: Offset for pagination

        Returns:
            List of trades

        Raises:
            XAIError: If trade retrieval fails
        """
        try:
            params: dict[str, Any] = {}
            if limit is not None:
                params["limit"] = limit
            if offset is not None:
                params["offset"] = offset

            response = self.http_client.get("/exchange/trades", params=params if params else None)

            return response if isinstance(response, list) else response.get("trades", [])
        except XAIError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise XAIError(f"Failed to get trades: {str(e)}") from e

    def get_balance(self, address: str) -> dict[str, Any]:
        """
        Get exchange balance for an address.

        Args:
            address: Wallet address

        Returns:
            Balance information

        Raises:
            XAIError: If balance retrieval fails
        """
        if not address:
            raise ValidationError("address is required")

        try:
            return self.http_client.get(f"/exchange/balance/{address}")
        except XAIError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise XAIError(f"Failed to get balance: {str(e)}") from e

    def get_price_history(
        self,
        period: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get price history from the exchange.

        Args:
            period: Time period (e.g., "1h", "24h", "7d")
            limit: Maximum number of data points

        Returns:
            Price history data

        Raises:
            XAIError: If price history retrieval fails
        """
        try:
            params: dict[str, Any] = {}
            if period:
                params["period"] = period
            if limit is not None:
                params["limit"] = limit

            response = self.http_client.get(
                "/exchange/price-history",
                params=params if params else None,
            )

            return response if isinstance(response, list) else response.get("history", [])
        except XAIError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise XAIError(f"Failed to get price history: {str(e)}") from e

    def get_stats(self) -> dict[str, Any]:
        """
        Get exchange statistics.

        Returns:
            Exchange statistics including volume, price, etc.

        Raises:
            XAIError: If stats retrieval fails
        """
        try:
            return self.http_client.get("/exchange/stats")
        except XAIError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise XAIError(f"Failed to get exchange stats: {str(e)}") from e

    # Legacy methods for backwards compatibility

    def register_session(
        self,
        wallet_address: str,
        peer_id: str,
    ) -> dict[str, Any]:
        """
        Register a trading session.

        NOTE: This is a legacy method. The testnet exchange does not require
        session registration. This method is kept for API compatibility but
        returns a mock success response.

        Args:
            wallet_address: Wallet address
            peer_id: Peer identifier

        Returns:
            Session information (mock)
        """
        if not wallet_address or not peer_id:
            raise ValidationError("wallet_address and peer_id are required")

        # Return mock success for API compatibility
        return {
            "status": "ok",
            "message": "Session registration not required on testnet exchange",
            "wallet_address": wallet_address,
            "peer_id": peer_id,
        }

    def create_order(
        self,
        from_address: str,
        to_address: str,
        from_amount: str,
        to_amount: str,
        timeout: int | None = None,
    ) -> TradeOrder:
        """
        Create a trade order (legacy P2P method).

        NOTE: This is a legacy method for P2P trading. For the testnet exchange,
        use place_order() instead. This method will attempt to create a limit
        order with the equivalent parameters.

        Args:
            from_address: Sender address
            to_address: Recipient address (ignored on exchange)
            from_amount: Amount to sell
            to_amount: Amount to receive (used to calculate price)
            timeout: Order timeout in seconds (ignored on exchange)

        Returns:
            Created trade order

        Raises:
            XAIError: If order creation fails
        """
        if not from_address or not from_amount or not to_amount:
            raise ValidationError(
                "from_address, from_amount, and to_amount are required"
            )

        try:
            # Calculate price from amounts
            from_val = float(from_amount)
            to_val = float(to_amount)
            price = str(to_val / from_val) if from_val > 0 else "0"

            # Place as a limit sell order
            result = self.place_order(
                address=from_address,
                order_type="limit",
                side="sell",
                amount=from_amount,
                price=price,
            )

            return TradeOrder(
                id=result.get("order_id", result.get("id", "")),
                from_address=from_address,
                to_address=to_address or "",
                from_amount=from_amount,
                to_amount=to_amount,
                created_at=datetime.now(),
                status=result.get("status", "pending"),
            )
        except XAIError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise XAIError(f"Failed to create trade order: {str(e)}") from e

    def get_order_status(self, order_id: str) -> dict[str, Any]:
        """
        Get trade order status.

        NOTE: This queries the exchange orders to find the order status.
        For better performance, consider using get_my_orders() with your address.

        Args:
            order_id: Order ID

        Returns:
            Order status

        Raises:
            XAIError: If status retrieval fails
        """
        if not order_id:
            raise ValidationError("order_id is required")

        try:
            # Get all orders and find the matching one
            orders = self.list_orders()
            for order in orders:
                if order.id == order_id:
                    return {
                        "order_id": order.id,
                        "status": order.status,
                        "from_address": order.from_address,
                        "from_amount": order.from_amount,
                        "to_amount": order.to_amount,
                        "created_at": order.created_at.isoformat() if order.created_at else None,
                    }

            # Order not found in active orders - may be completed or cancelled
            return {
                "order_id": order_id,
                "status": "unknown",
                "message": "Order not found in active orders. It may have been completed or cancelled.",
            }
        except XAIError:
            raise
        except (KeyError, ValueError, TypeError) as e:
            raise XAIError(f"Failed to get order status: {str(e)}") from e
