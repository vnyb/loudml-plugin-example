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

import logging
import json

from loudml.api import Hook

from voluptuous import (
    All,
    Any,
    Invalid,
    Required,
    Schema,
)

CONFIG_SCHEMA = Schema({
    Required('message'): str,
})

class ExampleHook(Hook):
    @staticmethod
    def validate(config):
        try:
            CONFIG_SCHEMA(config)
        except Invalid as exn:
            raise ValueError(exn.error_message)

    def on_anomaly(self, model, timestamp, score, predicted, observed, **kwargs):
        # Deal with anomaly notification here
        logging.warning(
            "{}: {}, model={}, score={}, predicted={}, observed={}",
            self.config['message'],
            timestamp,
            score,
            json.dumps(predicted),
            json.dumps(observed),
        )
