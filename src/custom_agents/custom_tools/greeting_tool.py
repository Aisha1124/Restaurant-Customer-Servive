from agents import function_tool
@function_tool
def greet_customer(
    name: str = "",
    time_of_day: str = "",
    is_returning: bool = False,
    reservation: bool = False,
    special_occasion: str = ""
) -> str:
    """
    Generates a personalized greeting for customers at ABC Restaurant.
    
    Args:
        name: Customer's name (if available)
        time_of_day: Time period (morning, afternoon, evening)
        is_returning: Whether the customer has visited before
        reservation: Whether the customer has a reservation
        special_occasion: Any special occasion being celebrated (birthday, anniversary, etc.)
        
    Returns:
        A personalized greeting message
    """
    # Base greeting components
    restaurant_name = "ABC Restaurant"
    
    # Time-based greeting
    if not time_of_day:
        time_greeting = "Welcome"
    elif time_of_day.lower() == "morning":
        time_greeting = "Good morning"
    elif time_of_day.lower() == "afternoon":
        time_greeting = "Good afternoon"
    elif time_of_day.lower() == "evening":
        time_greeting = "Good evening"
    else:
        time_greeting = "Welcome"
    
    # Name personalization
    if name:
        name_greeting = f"{time_greeting}, {name}!"
    else:
        name_greeting = f"{time_greeting}!"
    
    # Base greeting
    greeting = f"{name_greeting} Thanks for choosing {restaurant_name}."
    
    # Add returning customer recognition
    if is_returning:
        greeting += " It's wonderful to see you back with us again."
    else:
        greeting += " We're delighted to have you join us today."
    
    # Add reservation acknowledgment
    if reservation:
        greeting += " Your table is ready as reserved."
    
    # Add special occasion recognition
    if special_occasion:
        greeting += f" We understand you're celebrating your {special_occasion} today, and we'll do our best to make it special."
    
    # Add closing
    greeting += " Our staff is here to ensure you have an exceptional dining experience. Please let us know if there's anything specific you need."
    
    return greeting