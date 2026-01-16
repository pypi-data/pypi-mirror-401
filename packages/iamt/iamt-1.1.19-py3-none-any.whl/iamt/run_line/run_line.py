from prompt_toolkit import prompt

from ..client_config.client_config import ClientConfig
from ..completers.customCompleter import CustomCompleter, CustomValidator
from ..modules.runlinetask.runlinetask import run_line


class RunLine:

    def x(self):
        """交互式选择并执行命令"""
        # region 合并命令字典并创建补全器
        all_commands = {**python_pkgs, **node_pkgs}
        completer = CustomCompleter(all_commands)
        validator = CustomValidator(completer, error_msg="无效的命令，请从补全列表中选择")
        # endregion

        # region 交互式选择命令
        try:
            selected_cmd = prompt(
                "请选择要执行的命令 (Tab补全, 支持模糊搜索): ",
                completer=completer,
                validator=validator
            ).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n已取消选择")
            return

        if not selected_cmd or selected_cmd not in all_commands:
            print(f"无效的选择: {selected_cmd}")
            return
        # endregion

        # region 连接服务器并执行命令
        config = ClientConfig()
        conn = config.connect()
        if conn is None:
            return
        print(f"\n执行命令: {selected_cmd}\n")
        run_line(conn, selected_cmd)
        # endregion





python_pkgs={
    "uv tool install -U dlght":"免代理 gitub下载工具 dlght",
    "uv tool install -U envvm":"环境变量管理工具 envvm",
    "uv tool install -U ali-ops":"aliyun命令行工具"
}

node_pkgs={
    "npm install -g opencode-ai@latest":"opencode"
}

