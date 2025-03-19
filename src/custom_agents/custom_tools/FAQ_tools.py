from agents import function_tool

@function_tool
def answer_faq(query: str) -> str:
    """
    Provides dynamic responses to frequently asked questions about the restaurant.
    Analyzes the query to determine the topic and returns relevant, contextualized information.
    
    Args:
        query: The customer's question or request in full form
        
    Returns:
        A contextual response addressing the customer's question
    """
    # Core FAQ information with expanded details
    faq_data = {
        "hours": {
            "weekday": "Monday to Friday: 10 AM to 11 PM",
            "weekend": "Saturday and Sunday: 9 AM to 12 AM",
            "holiday": "Holiday hours may vary, please check our website for updates",
            "kitchen_closes": "Our kitchen stops taking orders 30 minutes before closing"
        },
        "menu": {
            "regular": "Our full menu is available at restaurant.com/menu",
            "seasonal": "We offer seasonal specials that change monthly",
            "dietary": "We have vegetarian, vegan, and gluten-free options clearly marked on our menu",
            "kids": "Kids menu available for children under 12",
            "drinks": "Full bar with signature cocktails, local craft beers, and wine selection"
        },
        "location": {
            "address": "123 Main Street, Cityville",
            "parking": "Free parking available in the rear lot",
            "public_transport": "Accessible via bus routes 10 and 15, two blocks from Central Station",
            "landmarks": "Located across from City Park, next to the Public Library"
        },
        "contact": {
            "phone": "555-1234",
            "email": "support@restaurant.com",
            "social": "Follow us on Instagram and Facebook @RestaurantName",
            "manager": "For urgent matters, ask to speak with the manager on duty"
        },
        "reservation": {
            "online": "Book online at restaurant.com/reservations",
            "phone": "Call 555-1234 for same-day reservations",
            "large_groups": "For parties of 8+, please call at least 48 hours in advance",
            "special_events": "We offer private dining for special events with custom menus"
        },
        "delivery": {
            "platforms": "Available on Uber Eats, DoorDash, and GrubHub",
            "direct": "Order directly through our website for a 10% discount",
            "radius": "We deliver within a 5-mile radius",
            "minimum": "Minimum order of $20 for delivery",
            "time": "Average delivery time is 30-45 minutes depending on location and time of day"
        },
        "allergies": {
            "policy": "We take allergies seriously and can accommodate most dietary restrictions",
            "kitchen": "Our kitchen can prepare meals avoiding common allergens upon request",
            "cross_contamination": "Please note we cannot guarantee zero cross-contamination",
            "notification": "Please inform your server about allergies when ordering"
        },
        "specials": {
            "daily": "We offer daily chef's specials not listed on the regular menu",
            "happy_hour": "Happy Hour from 4-6 PM weekdays with discounted drinks and appetizers",
            "brunch": "Weekend brunch served 9 AM - 2 PM with bottomless mimosas"
        },
        "covid": {
            "safety": "We follow all current health guidelines to ensure customer safety",
            "staff": "All staff members are fully vaccinated and undergo regular health checks",
            "cleaning": "Enhanced cleaning protocols between seatings",
            "options": "Outdoor seating and contactless pickup options available"
        }
    }
    
    # Analyze query to determine topic
    query = query.lower()
    
    # Dictionary to map keywords to their respective topics
    keyword_mapping = {
        # Hours related keywords
        "hour": "hours", "open": "hours", "close": "hours", "time": "hours", 
        "when": "hours", "schedule": "hours", "operation": "hours", "timing": "hours",
        
        # Menu related keywords
        "menu": "menu", "food": "menu", "dish": "menu", "eat": "menu", "cuisine": "menu",
        "special": "specials", "vegetarian": "menu", "vegan": "menu", "gluten": "menu",
        "drink": "menu", "cocktail": "menu", "beer": "menu", "wine": "menu",
        
        # Location related keywords
        "location": "location", "address": "location", "where": "location", 
        "direction": "location", "find": "location", "map": "location",
        "parking": "location", "transit": "location", "bus": "location", "train": "location",
        
        # Contact related keywords
        "contact": "contact", "phone": "contact", "call": "contact", "email": "contact",
        "reach": "contact", "talk": "contact", "social": "contact", "instagram": "contact",
        "facebook": "contact", "manager": "contact",
        
        # Reservation related keywords
        "reservation": "reservation", "book": "reservation", "table": "reservation", 
        "party": "reservation", "seat": "reservation", "group": "reservation",
        "private": "reservation", "event": "reservation", "celebrate": "reservation",
        
        # Delivery related keywords
        "delivery": "delivery", "takeout": "delivery", "take-out": "delivery", 
        "pickup": "delivery", "order": "delivery", "doordash": "delivery", 
        "ubereats": "delivery", "grubhub": "delivery", "bring": "delivery",
        
        # Allergies related keywords
        "allergy": "allergies", "allergic": "allergies", "dietary": "allergies", 
        "restriction": "allergies", "gluten-free": "allergies", "nut": "allergies",
        "dairy": "allergies", "vegan": "allergies", "vegetarian": "allergies",
        
        # Specials related keywords
        "special": "specials", "deal": "specials", "discount": "specials", 
        "happy hour": "specials", "promotion": "specials", "offer": "specials",
        "brunch": "specials", "event": "specials",
        
        # COVID related keywords
        "covid": "covid", "safety": "covid", "protocol": "covid", "outdoor": "covid",
        "distance": "covid", "mask": "covid", "vaccination": "covid", "cleaning": "covid"
    }
    
    # Determine the most relevant topic based on keyword matching
    identified_topic = None
    for keyword, topic in keyword_mapping.items():
        if keyword in query:
            identified_topic = topic
            break
    
    # If no topic was identified, try a more sophisticated analysis
    if not identified_topic:
        # Check each topic directly
        for topic in faq_data.keys():
            if topic in query:
                identified_topic = topic
                break
    
    # Default fallback if no topic identified
    if not identified_topic:
        return "I'm not sure what information you're looking for. You can ask about our hours, menu, location, contact information, reservations, delivery options, or accommodations for allergies. You can also call our helpline at 555-1234 for assistance."
    
    # Analyze query sentiment/tone to customize response
    is_urgent = any(word in query for word in ["urgent", "emergency", "immediately", "right now", "asap"])
    is_detailed = any(word in query for word in ["exactly", "specific", "detail", "explain", "tell me more"])
    is_comparing = any(word in query for word in ["compare", "difference", "versus", "vs", "or"])
    
    # Determine specific subtopics based on query
    subtopic_data = faq_data[identified_topic]
    relevant_subtopics = []
    
    # Check for specific subtopics in the query
    for subtopic in subtopic_data.keys():
        # Convert underscores to spaces for matching
        search_term = subtopic.replace("_", " ")
        if search_term in query:
            relevant_subtopics.append(subtopic)
    
    # If detailed information requested or specific subtopics identified, provide comprehensive response
    if is_detailed or is_comparing or relevant_subtopics:
        if relevant_subtopics:
            # Provide information about specific subtopics
            response = f"Regarding our {identified_topic}:\n\n"
            for subtopic in relevant_subtopics:
                response += f"• {subtopic_data[subtopic]}\n"
            return response
        else:
            # Provide all information about the topic
            response = f"Here's detailed information about our {identified_topic}:\n\n"
            for subtopic, info in subtopic_data.items():
                response += f"• {info}\n"
            return response
    
    # For urgent queries, provide direct and concise information
    if is_urgent:
        # Determine most important subtopic for urgent requests
        if identified_topic == "hours":
            return subtopic_data["weekday"] + " " + subtopic_data["weekend"]
        elif identified_topic == "contact":
            return f"For urgent matters, please call us at {subtopic_data['phone']}."
        elif identified_topic == "location":
            return subtopic_data["address"]
        elif identified_topic == "reservation":
            return f"For immediate reservations, please call {subtopic_data['phone']}."
        elif identified_topic == "delivery":
            return f"Fastest delivery options: {subtopic_data['platforms']} or {subtopic_data['direct']}"
        else:
            # For other topics, provide the first piece of information
            first_key = list(subtopic_data.keys())[0]
            return subtopic_data[first_key]
    
    # Standard response - provide main information about the topic
    if identified_topic == "hours":
        return f"{subtopic_data['weekday']}. {subtopic_data['weekend']}."
    elif identified_topic == "menu":
        return f"{subtopic_data['regular']}. {subtopic_data['seasonal']}."
    elif identified_topic == "location":
        return f"{subtopic_data['address']}. {subtopic_data['parking']}."
    elif identified_topic == "contact":
        return f"Call us at {subtopic_data['phone']} or email {subtopic_data['email']}."
    elif identified_topic == "reservation":
        return f"{subtopic_data['online']} or {subtopic_data['phone']}."
    elif identified_topic == "delivery":
        return f"{subtopic_data['platforms']}. {subtopic_data['direct']}."
    elif identified_topic == "allergies":
        return f"{subtopic_data['policy']}. {subtopic_data['notification']}."
    elif identified_topic == "specials":
        return f"{subtopic_data['daily']}. {subtopic_data['happy_hour']}."
    elif identified_topic == "covid":
        return f"{subtopic_data['safety']}. {subtopic_data['options']}."
    else:
        return "I'm not sure what information you're looking for. Please call our helpline at 555-1234 for assistance."