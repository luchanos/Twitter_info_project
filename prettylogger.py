import logging


class PrettyLogger:
    """
    Просто логер.
    """
    log_sett = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL}

    def __init__(self, logpath, conf, name: str):
        self.logpath = logpath
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level=conf.get('logger_settings', 'log_level'))
        self.handler = logging.FileHandler(filename=self.logpath)
        self.handler.setLevel(level=conf.get('logger_settings', 'log_level'))
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def log_level(self, level: str) -> None:
        if level in self.log_sett.keys():
            self.logger.setLevel(level=level)
        else:
            print('wrong level')
