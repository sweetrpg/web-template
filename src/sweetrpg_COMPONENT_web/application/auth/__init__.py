# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
"""

from flask_oauthlib.provider import OAuth2Provider
# from authlib.integrations.flask_client import OAuth
from flask import current_app
import logging
from sweetrpg_COMPONENT_web.application import constants
import os
