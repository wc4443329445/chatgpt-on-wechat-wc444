from chatgpt_tool_hub.tools.base_tool import BaseTool
from chatgpt_tool_hub.tools.web_requests import BaseRequestsTool, _parse_input


class RequestsPutTool(BaseRequestsTool, BaseTool):
    """Tool for making a PUT request to an API endpoint."""

    name = "requests_put"
    description = """Use this when you want to PUT to a website.
    Input should be a json string with two keys: "url" and "data".
    The value of "url" should be a string, and the value of "data" should be a dictionary of 
    key-value pairs you want to PUT to the url.
    Be careful to always use double quotes for strings in the json string.
    The output will be the text response of the PUT request.
    """

    def _run(self, text: str) -> str:
        """Run the tool."""
        try:
            data = _parse_input(text)
            return self.requests_wrapper.put(data["url"], data["data"])
        except Exception as e:
            return repr(e)

    async def _arun(self, text: str) -> str:
        """Run the tool asynchronously."""
        try:
            data = _parse_input(text)
            return await self.requests_wrapper.aput(data["url"], data["data"])
        except Exception as e:
            return repr(e)