import datetime

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate

from models.llm import get_openai_llm
from workflow.TripPlannerState import TripPlannerState
from prompts.trip_planner import trip_planner_system_message, trip_planner_user_message, trip_booker_system_message, \
    trip_booker_user_message
from workflow.nodes.constants import bookings_generation_message, itinerary_generation_message
from workflow.nodes.utils import get_prompt_input_variables_from_state

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


if __name__ == '__main__':
    state = TripPlannerState(messages=[],
                             start_date=datetime.date(2022, 1, 1),
                             end_date=datetime.date(2022, 2, 1),
                             origin_country='Singapore',
                             destination_country='Japan')
    x = itinerary_node(state)
    print(x)
