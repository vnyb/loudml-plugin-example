#!/usr/bin/env python3

# This file is part of LoudML HTTP plug-in. LoudML HTTP plug-in is free software:
# you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Red Mint Network

"""
Setup mail plug-in for LoudML
"""

from setuptools import setup

setup(
    name='loudml-plugin-mail',

    version='1.3.0',

    description="Make LoudML send e-mail notifications on anomaly detection",

    py_modules = [
        'loudml_plugin_mail',
    ],

    install_requires=[
        'loudml',
        'loudml-api',
    ],

    entry_points={
        'loudml.plugins': [
            'mail=loudml_plugin_mail:MailPlugin',
        ],
        'loudml.hooks': [
            'mail=loudml_plugin_mail:MailHook',
        ],
    },
)
