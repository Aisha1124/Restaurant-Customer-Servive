from agents import function_tool
@function_tool
def handle_reservation(
    request_type: str,
    party_size: int = 2,
    date: str = "",
    time: str = "",
    name: str = "",
    phone: str = "",
    email: str = "",
    special_requests: str = "",
    reservation_id: str = ""
) -> str:
    """
    Handles various reservation-related requests for ABC Restaurant.
    
    Args:
        request_type: Type of reservation request (make, modify, cancel, availability)
        party_size: Number of guests in the party
        date: Requested reservation date (YYYY-MM-DD format)
        time: Requested reservation time (HH:MM format)
        name: Customer name
        phone: Contact phone number
        email: Contact email address
        special_requests: Any special requests or notes
        reservation_id: Existing reservation ID (for modifications/cancellations)
        
    Returns:
        A response to the reservation request
    """
    import datetime
    
    # Validate request type
    valid_request_types = ["make", "modify", "cancel", "availability", "check"]
    if request_type.lower() not in valid_request_types:
        return "I'm not sure about that request. Please call us at 555-1234 for assistance with your reservation."
    
    # Current date/time for realistic responses
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M")
    
    # Parse date if provided
    if date:
        try:
            requested_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            is_weekend = requested_date.weekday() >= 5  # 5 and 6 are Saturday and Sunday
            is_future = requested_date.strftime("%Y-%m-%d") > current_date
        except ValueError:
            return f"The date format '{date}' is not valid. Please use YYYY-MM-DD format."
    else:
        is_weekend = False
        is_future = True
    
    # Handle large party size
    is_large_party = party_size > 6
    
    # Generate confirmation/reference code if needed
    if request_type.lower() in ["make", "modify"] and not reservation_id:
        import random
        import string
        reservation_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Handle different request types with more personalized and realistic responses
    if request_type.lower() == "make":
        # Check for required fields
        if not all([party_size, date, time, name]):
            missing = []
            if not party_size: missing.append("party size")
            if not date: missing.append("date")
            if not time: missing.append("time")
            if not name: missing.append("name")
            return f"To make a reservation, we need your {', '.join(missing)}. Please provide this information."
        
        # Check if restaurant can accommodate based on party size
        if party_size > 12:
            return f"For parties larger than 12, please call us directly at 555-1234 to discuss private dining options."
        
        # Generate different responses based on timing and party size
        if is_large_party:
            return f"Thank you, {name}. Your reservation request for {party_size} guests on {date} at {time} has been received (Ref: {reservation_id}). For parties of more than 6, we require a credit card to hold the reservation. Please call us at 555-1234 to complete your booking, or check your email for a secure payment link."
        
        # Weekend-specific messaging
        if is_weekend:
            return f"Thank you, {name}. Your reservation for {party_size} guests on {date} at {time} is confirmed (Ref: {reservation_id}). Weekend reservations are in high demand, so please call us at 555-1234 if you need to change or cancel. We look forward to serving you at ABC Restaurant!"
        
        # Standard confirmation
        special_note = f" We've noted your request: '{special_requests}'." if special_requests else ""
        return f"Thank you, {name}. Your reservation for {party_size} guests on {date} at {time} is confirmed (Ref: {reservation_id}).{special_note} A confirmation has been sent to {email or 'your contact information'}. We look forward to welcoming you to ABC Restaurant!"
    
    elif request_type.lower() == "modify":
        # Check for reservation ID
        if not reservation_id:
            return "To modify a reservation, we need your reservation reference number. Please provide this information."
        
        # Generate response for modification
        changes = []
        if party_size: changes.append(f"party size to {party_size} guests")
        if date: changes.append(f"date to {date}")
        if time: changes.append(f"time to {time}")
        if special_requests: changes.append(f"special requests to note '{special_requests}'")
        
        if not changes:
            return f"Your reservation ({reservation_id}) modification request has been received, but no changes were specified. Please indicate what you'd like to change."
        
        changes_text = ", ".join(changes)
        return f"Your request to modify reservation {reservation_id} has been received. We'll update your reservation with the following changes: {changes_text}. Please check your email shortly for confirmation of these changes. If you don't receive it within 15 minutes, please call us at 555-1234."
    
    elif request_type.lower() == "cancel":
        # Check for reservation ID
        if not reservation_id:
            return "To cancel a reservation, we need your reservation reference number. Please provide this information."
        
        # Generate cancellation response
        return f"Your reservation ({reservation_id}) has been canceled successfully. If this was a mistake, please call us at 555-1234 within the next hour to reinstate your reservation. We hope to welcome you to ABC Restaurant another time!"
    
    elif request_type.lower() == "check":
        # Check for reservation ID
        if not reservation_id:
            return "To check a reservation status, we need your reservation reference number. Please provide this information."
        
        # Simulate checking a reservation
        # In a real system, this would query a database
        return f"Your reservation ({reservation_id}) is confirmed for {date or '[date]'} at {time or '[time]'} for {party_size} guests. If you need to make any changes, please let us know at least 24 hours in advance."
    
    elif request_type.lower() == "availability":
        # Check for required date
        if not date:
            return "To check availability, please provide a desired date in YYYY-MM-DD format."
        
        # Generate dynamic availability based on date
        if not is_future:
            return f"We cannot make reservations for past dates. Please select a future date."
        
        # Weekend vs weekday availability differences
        if is_weekend:
            lunch_slots = ["11:30 AM", "12:00 PM", "1:30 PM"]
            dinner_slots = ["5:00 PM", "7:30 PM", "8:45 PM"]
            busy_message = "Weekend reservations fill quickly. We recommend booking at least one week in advance."
        else:
            lunch_slots = ["11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM"]
            dinner_slots = ["5:00 PM", "5:30 PM", "6:00 PM", "7:00 PM", "8:00 PM", "8:30 PM"]
            busy_message = "Weekday reservations are typically available with 1-2 days' notice."
        
        # Adjust based on party size
        if is_large_party:
            large_party_msg = f"For your party of {party_size}, we have limited availability. "
            lunch_slots = lunch_slots[:2]  # Fewer options for large parties
            dinner_slots = dinner_slots[:3]
        else:
            large_party_msg = ""
        
        # Format available times
        available_lunch = ", ".join(lunch_slots)
        available_dinner = ", ".join(dinner_slots)
        
        return f"For {date}, we have the following availability: \n\nLunch: {available_lunch}\nDinner: {available_dinner}\n\n{large_party_msg}{busy_message}\n\nTo make a reservation, please reply with 'make' and your preferred time, or call us at 555-1234."
    
    # Fallback response
    return "I'm not sure about that request. Please call us at 555-1234 for assistance with your reservation."