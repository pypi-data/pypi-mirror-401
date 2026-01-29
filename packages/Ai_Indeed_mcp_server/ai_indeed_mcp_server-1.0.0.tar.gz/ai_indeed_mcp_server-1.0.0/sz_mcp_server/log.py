import logging
import os
import datetime


ROAMING_DIR = os.getenv('APPDATA')
log_dir = os.path.join(ROAMING_DIR, 'Z-Factory', 'logs', f'{datetime.datetime.now().strftime("%Y-%m-%d")}', 'mcp')
print(log_dir)
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'sz_mcp.log'),
    level=logging.DEBUG,
    encoding='utf-8',
    format='|%(asctime)s|%(levelname)5s|pid:%(process)5d|%(filename)s:%(lineno)4d|%(message)s|',
    force=True
)


log = logging.getLogger('sz_mcp')