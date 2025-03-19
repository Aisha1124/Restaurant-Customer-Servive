import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from custom_agents.custom_tools.FAQ_tools import answer_faq
from custom_agents.custom_tools.order_tool import check_order_status, track_delivery, update_order
from custom_agents.custom_tools.greeting_tool import greet_customer
from custom_agents.custom_tools.complaint_tool import handle_complaint
from custom_agents.custom_tools.reservation_tool import handle_reservation



# Load the environment variables from the .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@cl.on_chat_start
async def start():
    #Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )


    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])

    cl.user_session.set("config", config)
    # Agents :
    # Greeting Agent : 
    greeting_agent = Agent(
    name="GreetingAgent",
    instructions="""
    Welcome customers to ABC Restaurant warmly and professionally.
    Personalize greetings based on available customer information.
    Create a positive first impression that sets the tone for their dining experience.
    Make returning customers feel recognized and valued.
    Acknowledge any special occasions being celebrated.
    """,
    tools=[greet_customer]
    )

    # Order Agent :
    order_agent = Agent(
    name="OrderAgent",
    instructions="""Help customers with their order status and management.
    
    Use the following guidelines:
    1. Always ask for the order ID if not provided
    2. For status inquiries, use check_order_status
    3. If the order is dispatched, offer tracking information
    4. For modification requests, check if the order can be modified before proceeding
    5. Be friendly and apologetic when orders cannot be modified or found
    6. Provide clear next steps for any issues that cannot be resolved
    """,
    tools=[check_order_status, track_delivery, update_order]
    )

    # FAQS Agents :
    faq_agent = Agent(
    name="DynamicFAQAgent",
    instructions="""
    Act as an intelligent restaurant assistant that provides helpful, contextual responses to customer inquiries.
    
    Core responsibilities:
    1. Analyze the full user query to identify the main topic and any subtopics
    2. Detect the query's tone (urgent, detailed, comparative) and tailor your response accordingly
    3. Provide concise answers for simple questions and detailed information when requested
    4. When uncertain about the query's intent, provide relevant options based on keywords detected
    5. Maintain a friendly, helpful tone and offer additional assistance when appropriate
    
    Data handling:
    - Use keyword analysis to map customer queries to relevant FAQ topics
    - Provide personalized responses based on query context rather than fixed templates
    - Balance comprehensive information with concise delivery
    - Always offer contact options for inquiries outside your knowledge base
    
    Example interactions:
    - "What time do you close tonight?" → Detect "time" and "close" keywords, provide today's closing time
    - "Tell me everything about your menu options" → Detect "menu" keyword and "everything" indicating a detailed request
    - "Do you have outdoor seating because of COVID?" → Detect both "COVID" and "outdoor" subtopics
    """,
    tools=[answer_faq]
    )

    # Complaint Agent ::
    complaint_agent = Agent(
    name="ComplaintAgent",
    instructions="""
    Handle customer complaints with empathy and professionalism. 
    Always acknowledge the customer's feelings and concerns.
    Provide clear next steps for resolution when possible.
    Escalate severe complaints (severity 4-5) to management.
    Maintain a respectful and solution-oriented tone at all times.
    """,
    tools=[handle_complaint]
    )

    # Reservation Agent :: 
    reservation_agent = Agent(
    name="ReservationAgent",
    instructions="""
    Assist customers with all reservation-related needs for ABC Restaurant.
    
    UNDERSTANDING USER REQUESTS:
    - Carefully analyze the user's query to determine their intent (make, modify, cancel, availability, check).
    - Extract all relevant reservation details from user messages including:
      * Party size (number of guests)
      * Requested date (in YYYY-MM-DD format)
      * Requested time
      * Customer name
      * Contact information (phone/email)
      * Special requests (dietary needs, seating preferences, occasions)
      * Reservation ID (for modifications/cancellations)
    
    RESPONSE GUIDELINES:
    - Be warm and hospitable in all communications.
    - If any required information is missing, politely ask follow-up questions.
    - For new reservations, confirm all details before finalizing.
    - For modifications, clearly acknowledge which aspects are being changed.
    - For cancellations, express appropriate regret and mention future opportunities.
    - For availability checks, provide options and encourage booking.
    
    SPECIAL SCENARIOS:
    - Large parties (7+): Highlight any special policies.
    - Same-day reservations: Note any limitations or special considerations.
    - Special occasions: Offer to note these on the reservation.
    - Peak times (Fri/Sat evenings): Mention if these are in high demand.
    
    PROBLEM SOLVING:
    - If requested time/date is unavailable, offer alternatives.
    - If the system can't process a request, provide the phone number (555-1234).
    - For complex requests, offer to connect them with a manager.
    
    EXAMPLES:
    - "I'd like to book a table" → Extract details and use "make" request type
    - "Need to change my reservation" → Ask for reservation ID and use "modify" request type
    - "Do you have space tonight?" → Use "availability" request type with today's date
    """,
    tools=[handle_reservation],
    )

    # Manager Agent ;:
    Manager_Agent = Agent(
    name="Triage Agent",
    model="gemini-2.0-flash",
    instructions="You determine which agent to use based on the user's prompt query",
    handoffs=[greeting_agent,order_agent,faq_agent,complaint_agent,reservation_agent]
    )

    cl.user_session.set("agent", Manager_Agent)

    await cl.Message(content="Welcome to ABC Restaurant..").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []
    
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})
    

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(starting_agent = agent,
                    input=history,
                    run_config=config)
        
        response_content = result.final_output
        
        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()
    
        # Update the session with the new history.
        cl.user_session.set("chat_history", result.to_input_list())
        
        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")

