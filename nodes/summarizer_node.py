import datetime
from langchain_core.prompts import ChatPromptTemplate

from models.llm import get_openai_llm
from workflow.TripPlannerState import TripPlannerState
from prompts.trip_planner import trip_planner_system_message, trip_planner_user_message, trip_booker_system_message, \
    trip_booker_user_message

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

    resp = chain.invoke(input={
        'country': state.destination_country,
        'origin_country': state.origin_country,
        'start_date': state.start_date,
        'end_date': state.end_date,
        'expectations': state.expectations,
    })
    # Save content as an .md file in the 'outputs' folder
    with open(f'outputs/itinerary_{state.destination_country}_{state.start_date}_{state.end_date}.md', 'w') as f:
        f.write(resp.content)
    return {'itinerary': resp.content}

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
    r = chain.invoke(input={
        'country': state.destination_country,
        'origin_country': state.origin_country,
        'start_date': state.start_date,
        'end_date': state.end_date,
        'expectations': state.expectations,
        'itinerary': state.itinerary,
    })
    # Save content as an .md file in the 'outputs' folder
    with open(f'outputs/bookings_{state.destination_country}_{state.start_date}_{state.end_date}.md', 'w') as f:
        f.write(r.content)
    return {'bookings': r.content}


if __name__ == '__main__':
    state = TripPlannerState(messages=[],
                             start_date=datetime.date(2022, 1, 1),
                             end_date=datetime.date(2022, 2, 1),
                             origin_country='Singapore',
                             destination_country='Japan')
    x = itinerary_node(state)
    print(x)
