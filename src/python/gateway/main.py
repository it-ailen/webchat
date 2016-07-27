# coding: utf-8
import tornado.options
import tornado.web
import tornado.ioloop
import logging
import env
import signal
import sys
from entries import entries

def exit_handler(signal, frame):
    # 清理工作 或者 设置退出标记
    sys.exit(0)  # 会抛出 SystemExit 异常

# kill -s INT (等价 Ctrl+C）
signal.signal(signal.SIGINT, exit_handler)
# kill -s TERM （supervisor）
signal.signal(signal.SIGTERM, exit_handler)

tornado.options.define("config", default=None,
                       type=str, help="File for configuration.")

tornado.options.parse_command_line()

if __name__ == "__main__":
    env.init(tornado.options.options.config)
    try:
        port = env.configMgr.get("port")
        logging.info("Run with port %d", port)
        application = tornado.web.Application(entries)
        application.listen(port)
        tornado.ioloop.IOLoop.current().start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("exit")
    finally:
        env.finish()