from langchain_core.messages import AIMessage, HumanMessage


def message_to_streamlit_role(message):
    """
    If message is an AI message - return 'ai', if Human message - 'human'. otherwise - 'system'
    :param message:
    :return:
    """
    if isinstance(message, AIMessage):
        return 'ai'
    elif isinstance(message, HumanMessage):
        return 'human'
    else:
        return 'system'


def strip_markdown_markings(text: str):
    """
    Strip the markings from GPT using regex - sometimes GPT outputs the data with ```markdown tabs
    :param text:
    :return:
    """
    if "```markdown" in text:
        return text[12:-3]
    else:
        return text
