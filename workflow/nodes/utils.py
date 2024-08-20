def get_prompt_input_variables_from_state(state, prompt):
    return {k:v for k,v in state.__dict__.items() if k in prompt.input_variables}