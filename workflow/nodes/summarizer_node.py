# Standard library imports
import datetime
from datetime import datetime
from typing import List, Dict
# Third-party imports
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate

# Local imports
from models.llm import get_openai_llm
from prompts.trip_planner import (
    trip_planner_system_message,
    trip_planner_user_message,
    trip_booker_system_message,
    trip_booker_user_message
)
from workflow.TripPlannerState import TripPlannerState
from workflow.nodes.constants import bookings_generation_message, itinerary_generation_message
from workflow.nodes.utils import get_prompt_input_variables_from_state, search_flights

llm = get_openai_llm()


def itinerary_node(state: TripPlannerState):
    """
    Running a conversation with a user about their upcoming trip.
    :param state:
    :return:
    """
    itinerary_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", trip_planner_system_message),
            ("user", trip_planner_user_message),
        ]
    )
    chain = itinerary_prompt | llm
    resp = chain.invoke(input=get_prompt_input_variables_from_state(state=state,
                                                                    prompt=itinerary_prompt))

    # Save content as an .md file in the 'outputs' folder
    with open(f'outputs/itinerary_{state.destination_country}_{state.start_date}_{state.end_date}.md', 'w') as f:
        f.write(resp.content)
    return {'itinerary': resp.content,
            'messages': [AIMessage(itinerary_generation_message)]}



def bookings_node(state: TripPlannerState):
    """
    Running a conversation with a user about their upcoming trip.
    :param state:
    :return:
    """
    bookings_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", trip_booker_system_message),
            ("user", trip_booker_user_message),
        ]
    )
    chain = bookings_prompt | llm
    resp = chain.invoke(input=get_prompt_input_variables_from_state(state=state,
                                                                    prompt=bookings_prompt))
    # Save content as an .md file in the 'outputs' folder
    with open(f'outputs/bookings_{state.destination_country}_{state.start_date}_{state.end_date}.md', 'w') as f:
        f.write(resp.content)
    return {'bookings': resp.content,
            'messages': [AIMessage(bookings_generation_message)],
            # this cutoff is needed to exclude them in the further part of the interview.
            'messages_len_cutoff': len(state.messages) + 1}


def format_flight_results(flights: List[Dict]) -> str:
    """Format flight results for LLM input"""
    result = "Flight options:\n"
    for flight in flights:
        result += f"- {flight['website']} - {flight['airline']}: {flight['price']}, Duration: {flight['duration']}\n"
    return result


def enhanced_itinerary_node(state: TripPlannerState):
    """
    Enhanced version of itinerary_node that includes flight search results.
    """
    # Search for flights
    flights = search_flights(
        state.origin_country,
        state.destination_country,
        state.start_date
    )
    flight_info = format_flight_results(flights)

    # Prepare the enhanced prompt
    enhanced_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", trip_planner_system_message),
            ("user", trip_planner_user_message + "\n\nAvailable flight options:\n" + flight_info),
        ]
    )

    chain = enhanced_prompt | llm
    resp = chain.invoke(input=get_prompt_input_variables_from_state(state=state,
                                                                    prompt=enhanced_prompt))

    # Save content as an .md file in the 'outputs' folder
    with open(f'outputs/enhanced_itinerary_{state.destination_country}_{state.start_date}_{state.end_date}.md', 'w') as f:
        f.write(resp.content)

    return {'itinerary': resp.content,
            'messages': [AIMessage(itinerary_generation_message)],
            'flight_options': flights}

# Replace the original itinerary_node with the enhanced version
itinerary_node = enhanced_itinerary_node




if __name__ == '__main__':
    state = TripPlannerState(messages=[],
                             start_date=datetime.date(2022, 1, 1),
                             end_date=datetime.date(2022, 2, 1),
                             origin_country='Singapore',
                             destination_country='Japan')
    x = itinerary_node(state)
    print(x)
