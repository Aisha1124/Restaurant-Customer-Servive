from agents import function_tool
from typing import Dict, List, Optional, Any
@function_tool
def check_order_status(order_id: str):
    """Check the status of an order with the given order ID.
    
    Args:
        order_id (str): The unique identifier for the order
        
    Returns:
        str: Status message with details about the order
    """
    # Expanded database with more orders and detailed status information
    order_statuses: Dict[str, Dict[str, Any]] = {
        "12345": {
            "status": "preparing",
            "eta_minutes": 20,
            "items": ["Pizza Margherita", "Garlic Bread"],
            "last_update": "2025-03-19T14:30:00"
        },
        "67890": {
            "status": "dispatched",
            "eta_minutes": 10,
            "items": ["Chicken Burger", "Fries", "Soda"],
            "last_update": "2025-03-19T14:35:00"
        },
        "11121": {
            "status": "processing",
            "eta_minutes": 30,
            "items": ["Pasta Carbonara", "Tiramisu"],
            "last_update": "2025-03-19T14:25:00"
        },
        "22222": {
            "status": "delivered",
            "delivery_time": "2025-03-19T14:00:00",
            "items": ["Vegetable Soup", "Caesar Salad"],
            "last_update": "2025-03-19T14:05:00"
        },
        "33333": {
            "status": "cancelled",
            "reason": "Customer request",
            "items": ["Sushi Platter"],
            "last_update": "2025-03-19T13:45:00"
        }
    }

    
    if order_id not in order_statuses:
        return "Order ID not found. Please check and try again."
    
    order = order_statuses[order_id]
    
    # Format response based on status
    if order["status"] == "preparing":
        return f"Your order {order_id} is being prepared and will be delivered in {order['eta_minutes']} minutes. Items: {', '.join(order['items'])}."
    elif order["status"] == "dispatched":
        return f"Your order {order_id} has been dispatched and will arrive in {order['eta_minutes']} minutes. Items: {', '.join(order['items'])}."
    elif order["status"] == "processing":
        return f"Your order {order_id} is still being processed. Estimated delivery in {order['eta_minutes']} minutes. Items: {', '.join(order['items'])}."
    elif order["status"] == "delivered":
        return f"Your order {order_id} was delivered at {order['delivery_time']}. Items: {', '.join(order['items'])}."
    elif order["status"] == "cancelled":
        return f"Your order {order_id} was cancelled. Reason: {order['reason']}. Items: {', '.join(order['items'])}."
    else:
        return f"Your order {order_id} status: {order['status']}. Please contact customer service for more information."


@function_tool
def track_delivery(order_id: str):
    """Get real-time tracking information for a dispatched order.
    
    Args:
        order_id (str): The unique identifier for the order
        
    Returns:
        str: Tracking details with location and ETA
    """
    # Simulated delivery tracking data
    tracking_info = {
        "67890": {
            "driver_name": "Michael",
            "current_location": "2 blocks away",
            "eta_minutes": 8,
            "contact": "555-0123"
        },
        "12345": {
            "driver_name": "Sarah",
            "current_location": "In the kitchen",
            "eta_minutes": 18,
            "contact": "555-0124"
        }
    }
    
    if order_id not in tracking_info:
        return "Tracking information not available for this order. Either the order hasn't been dispatched yet or tracking is not supported."
    
    info = tracking_info[order_id]
    return f"Driver {info['driver_name']} is currently {info['current_location']}. Expected arrival in {info['eta_minutes']} minutes. Driver contact: {info['contact']}"


@function_tool
def update_order(order_id: str, update_type: str, details: str = None):
    """Modify an existing order if it hasn't been dispatched.
    
    Args:
        order_id (str): The unique identifier for the order
        update_type (str): Type of update (add_item, remove_item, change_address, cancel)
        details (str, optional): Additional information for the update
        
    Returns:
        str: Confirmation message or error
    """
    # Simulated order update logic
    modifiable_orders = ["11121", "12345"]
    
    if order_id not in modifiable_orders:
        return "This order cannot be modified. It may have already been dispatched or delivered."
    
    if update_type == "cancel":
        return f"Order {order_id} has been cancelled successfully."
    elif update_type == "add_item":
        return f"Added '{details}' to order {order_id}."
    elif update_type == "remove_item":
        return f"Removed '{details}' from order {order_id}."
    elif update_type == "change_address":
        return f"Delivery address for order {order_id} updated to: {details}"
    else:
        return "Invalid update type. Supported types: add_item, remove_item, change_address, cancel"