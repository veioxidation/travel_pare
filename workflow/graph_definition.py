from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from pydantic import BaseModel

from database.memory_db import pool
from workflow.nodes.summarizer_node import itinerary_node, bookings_node
from workflow.TripPlannerState import TripPlannerState
from workflow.nodes.trip_interviewer import interviewer_node


class Trip(BaseModel):
    origin: str
    destination: str
    price: float
    duration: int

class Nodes:
    interview = 'interviewer_node'
    human_input = 'human_interview_input'
    itinerary = 'summarizer_node'
    booking = 'booking_node'

graph = StateGraph(TripPlannerState)
graph.add_node(Nodes.interview, interviewer_node)
graph.add_node(Nodes.human_input, RunnablePassthrough())
graph.add_node(Nodes.itinerary, itinerary_node)
graph.add_node(Nodes.booking, bookings_node)


def interview_ended(state: TripPlannerState, config: dict):
    """
    Check if the interview has ended, or if the maximum number of messages has been reached.
    :param state:
    :param config:
    :return:
    """
    max_messages = config['configurable'].get('max_messages', 10)
    if state.expectations or len(state.messages) >= max_messages:
        return Nodes.itinerary
    else:
        return Nodes.human_input


# begin the graph
graph.add_edge(START, Nodes.interview)
# add conditional edges
graph.add_conditional_edges(Nodes.interview, interview_ended)
graph.add_edge(Nodes.human_input, Nodes.interview)
graph.add_edge(Nodes.itinerary, Nodes.booking)
graph.add_edge(Nodes.booking, END)

# Initialize memory to persist state between graph runs
with pool.connection() as conn:
    checkpointer = PostgresSaver(conn)
    # NOTE: you need to call .setup() the first time you're using your checkpointer
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer,
                        interrupt_before=[Nodes.human_input])


if __name__ == '__main__':
    config = {'configurable': {'thread_id': "6"}}
    # Initial chat run
    input_ = TripPlannerState(messages=[],
                              start_date='2022-01-01',
                              end_date='2022-02-01',
                              origin_country='Singapore',
                              destination_country='Japan')
    while True:
        for event in app.stream(input=input_, config=config, stream_mode='values'):
            if len(event['messages']) == 0:
                continue
            last_message = event['messages'][-1]
            print(last_message.content)
        app_state = app.get_state(config)
        if not app_state.next:
            break
        input_ = None
        user_input = input(">>> ")
        app.update_state(config,
                         {"messages": [HumanMessage(user_input)]}, as_node=Nodes.human_input)
        if user_input == "exit":
            break

