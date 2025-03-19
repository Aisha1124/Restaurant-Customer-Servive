from agents import function_tool


@function_tool
def handle_complaint(complaint: str, severity: int = 1, category: str = "general") -> str:
    """
    Processes customer complaints and generates appropriate responses.
    
    Args:
        complaint: The customer's complaint in their own words
        severity: Complaint severity from 1 (minor) to 5 (severe)
        category: Category of complaint (general, food, service, cleanliness, etc.)
        
    Returns:
        A response addressing the customer's complaint
    """
    # Response templates based on severity and category
    responses = {
        "general": {
            "low": "We appreciate your feedback. We're sorry about your experience and will look into this matter.",
            "medium": "We sincerely apologize for your experience. Your feedback is important to us, and we'll address this issue promptly.",
            "high": "We deeply regret your negative experience. This is not the standard we aim for. A manager will contact you directly to resolve this matter."
        },
        "food": {
            "low": "We're sorry your meal wasn't up to our usual standards. We'll share your feedback with our kitchen team.",
            "medium": "We sincerely apologize about your dining experience. We take food quality very seriously and will address this with our chef immediately.",
            "high": "We deeply regret your unsatisfactory dining experience. This is unacceptable, and we'd like to make it right. A manager will contact you to offer a resolution."
        },
        "service": {
            "low": "We apologize for the service issues you experienced. We strive to provide excellent service and will address this with our staff.",
            "medium": "We're truly sorry about the service you received. This is not representative of our standards, and we'll be reviewing this with our team.",
            "high": "We're deeply concerned about the service you received. This falls well below our standards. Our manager will contact you directly to resolve this matter."
        },
        "cleanliness": {
            "low": "Thank you for bringing this cleanliness issue to our attention. We'll address it right away.",
            "medium": "We sincerely apologize for the cleanliness issues you encountered. This is not our standard, and we'll implement immediate corrective measures.",
            "high": "We're deeply sorry about the cleanliness issues you experienced. This is completely unacceptable. Our management team will investigate immediately and contact you with a resolution."
        }
    }
    
    # Set severity level
    if severity <= 2:
        level = "low"
    elif severity <= 4:
        level = "medium"
    else:
        level = "high"
    
    # If category doesn't exist, default to general
    if category not in responses:
        category = "general"
    
    # Generate response based on complaint analysis
    base_response = responses[category][level]
    
    # Add personalized elements based on complaint content
    if "refund" in complaint.lower() or "money back" in complaint.lower():
        base_response += " Please contact our customer service team at 555-1234 to discuss refund options."
    
    if "wait" in complaint.lower() or "slow" in complaint.lower():
        base_response += " We're reviewing our processes to improve our service times."
    
    if "manager" in complaint.lower() or "speak" in complaint.lower():
        base_response += " A manager will reach out to you within 24 hours."
    
    return base_response