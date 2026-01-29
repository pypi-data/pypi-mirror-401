import time
import os

from . import utils
from ..log import log

    
    
def start_bot(bot_path: str):
    for i in range(3):
        log.info(f"第 *{i+1}* 次检查启动bot")
        try:
            ret = utils.check_bot_status()
        except Exception as e:
            log.exception("check_bot_status")
            ret = {"code": "2", "message": str(e)}
        log.info(f"机器人状态: {ret}")
        if ret['code'] == "2":
            if not os.path.exists(bot_path):
                raise FileNotFoundError(f"机器人文件不存在: {bot_path}")
            utils.open_bot(bot_path)
            time.sleep(6)
        elif ret['code'] == "3":
            time.sleep(3)
        else:
            return

    raise Exception(f"{bot_path} bot start fail!")
