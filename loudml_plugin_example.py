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

from loudml.api import (
    Hook,
    Plugin,
)

from voluptuous import (
    All,
    Any,
    Invalid,
    Optional,
    Required,
    Schema,
)


class ExamplePlugin(Plugin):
    """
    LoudML example plug-in
    """

    # Optional class to be defined if the plug-in requires an initialization
    # on LoudML start up. If no initialization is needed, get rid of it.

    CONFIG_SCHEMA = Schema({
        Required('foo'): str,
        Optional('bar'): int,
    })

    def __init__(self, name, config_dir, *args, **kwargs):
        # Load and validate plug-in configuration from
        # /etc/loudml/plugins.d/<plugin name>.yml
        super().__init__(name, config_dir, *args, **kwargs)

        # ... put here additional initialization actions ...

    @classmethod
    def validate(cls, config):
        """
        Validate and sanitize plug-in static configuration
        """

        # Validate configuration against the schema
        config = super().validate(config)

        # ... put here additional validation if needed ...

        # Return sanitized configuration
        return config


class ExampleHook(Hook):
    CONFIG_SCHEMA = Schema({
        Required('message'): str,
    })

    @classmethod
    def validate(cls, config):
        """
        Validate and sanitize hook configuration
        """

        # Validate configuration against the schema
        config = super().validate(config)

        # ... put here additional validation if needed ...

        # Return sanitized configuration
        return config

    def on_anomaly(
        self,
        model,
        dt,
        score,
        predicted,
        observed,
        *args,
        **kwargs
    ):
        # Deal with anomaly notification here
        logging.warning(
            "%s: %s, model=%s, score=%.2f, predicted=%s, observed=%s",
            self.config['message'],
            str(dt.astimezone()),
            model,
            score,
            json.dumps(predicted),
            json.dumps(observed),
        )
