# -*- coding: utf-8 -*-
import logging
from logging import config


class Frustum:

    levels = ['critical', 'error', 'warning', 'info', 'debug']

    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.events = {}
        self.config = {'version': 1}

    def _number_to_level(self, number):
        if number >= len(self.levels):
            return self.levels[-1]
        return self.levels[number]

    def real_level(self, level):
        """
        Finds the real level from a numeric or string level
        """
        if type(level) is int:
            level = self._number_to_level(level)
        return getattr(logging, level.upper())

    def start_logger(self):
        """
        Enables the root logger and configures extra loggers.
        """
        logging.basicConfig(level=self.level)
        self.set_logger(self.name, self.level)
        config.dictConfig(self.config)
        self.logger = logging.getLogger(self.name)

    def set_logger(self, logger_name, level):
        """
        Sets the level of a logger
        """
        if 'loggers' not in self.config:
            self.config['loggers'] = {}
        real_level = self.real_level(level)
        self.config['loggers'][logger_name] = {'level': real_level}

    def add_handler(self, level, output):
        if output != 'stdout':
            handler = logging.FileHandler(output)
            handler.setLevel(level)
            self.logger.addHandler(handler)

    def register_event(self, event_name, event_level, message):
        """
        Registers an event so that it can be logged later.
        """
        self.events[event_name] = (event_level, message)

    def log(self, event, *args):
        message = event
        level = logging.INFO
        if event in self.events:
            level = getattr(logging, self.events[event][0].upper())
            message = self.events[event][1]
        self.logger.log(level, message.format(*args))
