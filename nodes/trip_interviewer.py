import datetime

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from models.llm import get_openai_llm
from workflow.TripPlannerState import TripPlannerState
from prompts.trip_interviewer import trip_interviewer_system_message, trip_interviewer_user_message


def interviewer_node(state: TripPlannerState):
    """
    Running a conversation with a user about their upcoming trip.
    :param state:
    :return:
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", trip_interviewer_system_message),
            ("human", trip_interviewer_user_message),
            MessagesPlaceholder('messages'),
        ]
    )
    llm = get_openai_llm()
    chain = prompt | llm
    # TODO - structure the response

    resp = chain.invoke(input={
        'country': state.destination_country,
        'start_date': state.start_date,
        'end_date': state.end_date,
        'messages': state.messages,
    })
    output = {'messages': [resp]}
    if "EXIT_TAG" in resp.content:
        output['expectations'] = resp.content
    return output


if __name__ == '__main__':
    state = TripPlannerState(messages=[],
                             start_date=datetime.date(2022, 1, 1),
                             end_date=datetime.date(2022, 2, 1),
                             origin_country='Singapore',
                             destination_country='Japan')
    x = interviewer_node(state)
    print(x)
