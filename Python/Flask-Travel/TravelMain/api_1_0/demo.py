# coding:utf-8

from . import api
from TravelMain import db
# import logging
from flask import current_app


@api.route("/index")
def index():
    #print("hello")

    current_app.logger.error("error info")
    current_app.logger.warn("warn info")
    current_app.logger.info("info info")
    current_app.logger.debug("debug info")
    return "index page"


# logging.basicConfig(level=logging.ERROR)



