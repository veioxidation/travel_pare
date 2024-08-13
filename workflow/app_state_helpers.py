from langgraph.pregel import StateSnapshot

from workflow.graph_definition import Nodes, app


def has_messages(app_state_values: dict):
    return len(app_state_values['messages']) > 0


def has_started(app_state: StateSnapshot):
    return has_messages(app_state.values)


def has_finished(app_state: StateSnapshot):
    """
    Check if the app has finished running - it has no next node and has messages
    :param app_state:
    :return:
    """
    return len(app_state.next) == 0 and has_started(app_state)


def has_itinerary(app_state: StateSnapshot):
    """

    :param app_state:
    :return:
    """
    _itinerary = app_state.values.get('itinerary')
    return bool(_itinerary)


def has_bookings(app_state: StateSnapshot):
    """

    :param app_state:
    :return:
    """
    _bookings = app_state.values.get('bookings')
    return bool(_bookings)


def get_next_node(app_state: StateSnapshot):
    return app_state.next


def check_if_next_node_is(app_state: StateSnapshot,
                          node_name: str):
    return node_name in app_state.next


def get_writes(app_state: StateSnapshot):
    return app_state.metadata.get('writes')


def get_all_writes_messages(app_state: StateSnapshot):
    writes = get_writes(app_state)
    if isinstance(writes, dict):
        for node, writes_info in writes.items():
            if 'messages' in writes_info:
                return writes_info.get('messages')
    return []


def get_all_messages(app_state: StateSnapshot):
    return app_state.values.get('messages')


def is_human_node_next(app_state: StateSnapshot):
    return check_if_next_node_is(app_state, Nodes.human_input)


if __name__ == '__main__':
    config = {'configurable': {'thread_id': 'Israel'}}
    app_state = app.get_state(config)
    print(has_itinerary(app_state))
    print(has_started(app_state))
    print(has_finished(app_state))
    print(get_next_node(app_state))
    # print(get_all_writes_messages(app_state))
