# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
user.py
- Utility functions for managing users.
"""


from flask import current_app, session
from sweetrpg_COMPONENT_web.application import constants


def add_user_info(data: dict) -> dict:
    """Set user audit fields, such as `created_by` and `updated_by` with current user info.
    If the application is in debug mode, the system user ID is used.

    :param dict data: The data dictionary to update.
    :returns data: The data that was passed in, with user audit fields set.
    """
    if current_app.config['DEBUG']:
        data['updated_by'] = constants.SYSTEM_USER_ID
    elif session['user']:
        data['created_by'] = session['user']['id']

    if not data.get('created_by'):
        data['created_by'] = constants.SYSTEM_USER_ID

    return data
