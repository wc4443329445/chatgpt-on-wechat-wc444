import logging

from rich.console import Console

from chatgpt_tool_hub.apps import App
from chatgpt_tool_hub.common.constants import TRUE_VALUES_SET
from chatgpt_tool_hub.common.log import refresh
from chatgpt_tool_hub.common.utils import get_from_dict_or_env
from chatgpt_tool_hub.models import build_model_params
from chatgpt_tool_hub.tools import dynamic_tool_loader


class AppFactory:
    def __init__(self, console=Console()):
        self.default_tools_list = []
        self.console = console

    def init_env(self, **kwargs):
        """ 环境初始化 """
        # set log level
        nolog_flag = get_from_dict_or_env(kwargs, "nolog", "NOLOG", False)
        debug_flag = get_from_dict_or_env(kwargs, "debug", "DEBUG", False)
        if str(nolog_flag).lower() in TRUE_VALUES_SET:
            refresh(logging.CRITICAL)
        elif str(debug_flag).lower() in TRUE_VALUES_SET:
            refresh(logging.DEBUG)
        else:
            refresh(logging.INFO)

        # default tools
        no_default_flag = get_from_dict_or_env(kwargs, "no_default", "NO_DEFAULT", False)
        if str(no_default_flag).lower() in TRUE_VALUES_SET:
            self.default_tools_list = []
        else:
            self.default_tools_list = ["python", "terminal", "url-get", "meteo-weather"]

        # set proxy
        # _proxy = get_from_dict_or_env(kwargs, "proxy", "PROXY", "")
        # if not _proxy:
        #     os.environ["http_proxy"] = str(_proxy)
        #     os.environ["https_proxy"] = str(_proxy)

        # dynamic loading tool
        dynamic_tool_loader()

    def create_app(self, app_type: str = 'victorinox', tools_list: list = None, console=Console(quiet=True), **kwargs) -> App:
        tools_list = tools_list if tools_list else []

        # todo remove it
        if kwargs.get("openai_api_key"):
            kwargs["llm_api_key"] = kwargs.get("openai_api_key")
        if kwargs.get("open_ai_api_base"):
            kwargs["llm_api_base_url"] = kwargs.get("open_ai_api_base")

        self.init_env(**kwargs)

        if app_type == 'lite':
            from chatgpt_tool_hub.apps.lite_app import LiteApp
            app = LiteApp(**build_model_params(kwargs))
            app.create(tools_list, **kwargs)
            return app

        elif app_type == 'victorinox':
            from chatgpt_tool_hub.apps.victorinox import Victorinox

            for default_tool in self.default_tools_list:
                if default_tool not in tools_list:
                    tools_list.append(default_tool)

            # todo refactor
            if "browser" in tools_list:
                tools_list = list(filter(lambda tool: tool != "url-get", tools_list))

            app = Victorinox(console, **build_model_params(kwargs))
            app.create(tools_list, **kwargs)
            return app
        else:
            raise NotImplementedError
