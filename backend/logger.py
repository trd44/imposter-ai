"""
logger.py

Author: Christian Welling
Date: 12/5/2023
Company: ImposterAI
Contact: csw73@cornell.edu

Manage logging within flask application. Uses single logging instance created in
app startup.
"""

import logging

LOGGER = logging.getLogger(name="app")
