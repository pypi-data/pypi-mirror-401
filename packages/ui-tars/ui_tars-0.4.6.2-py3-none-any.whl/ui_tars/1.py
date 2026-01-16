from ui_tars.action_parser import parse_xml_action_65
from ui_tars.formatter_xml02 import make_assistant_responses

if __name__ == "__main__":

    response = "<seed:tool_call><function name=\"doubao_code_interpreter\"><parameter name=\"code\" string=\"false\">{\"name\": \"code\", \"value\": \"print('Hello,\\n\\n\\\\n World!')\"}</parameter><parameter name=\"language\" string=\"false\">true</parameter><parameter name=\"index\" string=\"false\">1</parameter><parameter name=\"text\" string=\"true\">this is a test</parameter><parameter name=\"chunks\" string=\"false\">[\"block1\", \"block2\"]</parameter></function></seed:tool_call>"
    print(response)
    
    tool_calls = parse_xml_action_65(response)
    test_calls = [{"type": "function", "function": {"name": call["function"], "arguments": call["parameters"]}} for call in tool_calls]
    
    # 校验
    assert len(test_calls) > 0
    print(test_calls)
    
    response = make_assistant_responses(test_calls)
    print(response)
    
# 输出：
# <seed:tool_call_never_used_51bce0c785ca2f68081bfa7d91973934><function_never_used_51bce0c785ca2f68081bfa7d91973934=doubao_code_interpreter><parameter_never_used_51bce0c785ca2f68081bfa7d91973934=code>{"name": "code", "value": "print('Hello,\n\n\\n World!')"}</parameter_never_used_51bce0c785ca2f68081bfa7d91973934><parameter_never_used_51bce0c785ca2f68081bfa7d91973934=language>True</parameter_never_used_51bce0c785ca2f68081bfa7d91973934><parameter_never_used_51bce0c785ca2f68081bfa7d91973934=index>1</parameter_never_used_51bce0c785ca2f68081bfa7d91973934><parameter_never_used_51bce0c785ca2f68081bfa7d91973934=text>this is a test</parameter_never_used_51bce0c785ca2f68081bfa7d91973934><parameter_never_used_51bce0c785ca2f68081bfa7d91973934=chunks>["block1", "block2"]</parameter_never_used_51bce0c785ca2f68081bfa7d91973934></function_never_used_51bce0c785ca2f68081bfa7d91973934></seed:tool_call_never_used_51bce0c785ca2f68081bfa7d91973934>