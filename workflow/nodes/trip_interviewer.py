import datetime
from typing import List, Optional

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

from models.llm import get_openai_llm
from workflow.TripPlannerState import TripPlannerState
from prompts.trip_interviewer import trip_interviewer_system_message, trip_interviewer_user_message
from workflow.nodes.utils import get_prompt_input_variables_from_state


class TripInterviewerOutput(BaseModel):
    question: str = Field(description="Next message to the user, containing a response to the previous message, and further questions if the previous ones are answered. Leave empty if no more questions to answer.")
    conversation_end: bool = Field(description="Flag to indicate the end of the conversation.")
    suggested_answers: List[str] = Field(description="Suggested 3-5 short answers to the question asked.")
    interview_summary: Optional[str] = Field(description="Summary of the interview with the user so far, and all the information gathered.")


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
    chain = prompt | llm.with_structured_output(TripInterviewerOutput)

    resp = chain.invoke(input=get_prompt_input_variables_from_state(state=state,
                                                                    prompt=prompt))
    question = resp['question']
    end_convo = resp['conversation_end']
    potential_answers = resp['suggested_answers'] or []
    try:
        interview_summary = resp['interview_summary']
    except KeyError:
        interview_summary = ""

    output = {'messages': [AIMessage(question)],
              'potential_answers': potential_answers}
    if end_convo:
        output['expectations'] = interview_summary
    return output


if __name__ == '__main__':
    state = TripPlannerState(messages=[],
                             start_date=datetime.date(2022, 1, 1),
                             end_date=datetime.date(2022, 2, 1),
                             origin_country='Singapore',
                             destination_country='Japan')
    x = interviewer_node(state)
    print(x)
