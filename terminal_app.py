from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
load_dotenv()

from workflow.TripPlannerState import TripPlannerState
from workflow.graph_definition import app, checkpointer, Nodes

dest = 'Namibia'
config = {'configurable': {'thread_id': dest}}
# Initial chat run
input_ = TripPlannerState(messages=[],
                          start_date='2024-09-01',
                          end_date='2022-09-07',
                          origin_country='Warsaw',
                          destination_country=dest,
                          traveler_info="I am a traveler that likes sports, adventures and coffee.")
while True:
    for event in app.stream(input=input_, config=config, stream_mode='values'):
        if len(event['messages']) == 0:
            continue
        app_state = app.get_state(config)
        writes = app_state.metadata.get('writes')
        if isinstance(writes, dict):
            for node_name, writes_info in writes.items():
                if 'messages' in writes_info:
                    for msg in writes_info['messages']:
                        print(msg.content)
                if 'potential_answers' in writes_info:
                    print(f"\nPotential answers: {', '.join(writes_info['potential_answers'])}")

    app_state = app.get_state(config)
    checkpoint = checkpointer.get(config)

    if not app_state.next:
        break
    input_ = None
    user_input = input(">>> ")
    app.update_state(config,
                     {"messages": [HumanMessage(user_input)]}, as_node=Nodes.human_input)
    if user_input == "exit":
        break
