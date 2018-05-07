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
import smtplib

from email.message import EmailMessage
from email.headerregistry import Address

from loudml.api import (
    Hook,
    Plugin,
)

from voluptuous import (
    All,
    Any,
    Email,
    Invalid,
    Optional,
    Range,
    Required,
    Schema,
)

class MailPlugin(Plugin):
    """
    LoudML mail plug-in
    """

    CONFIG_SCHEMA = Schema({
        Required('smtp'): Schema({
            Required('host'): str,
            Optional('port', default=0): All(int, Range(min=0, max=65535)),
            Optional('tls', default=False): bool,
            Optional('user'): str,
            Optional('password', default=''): str,
        }),
    })


class MailHook(Hook):
    """
    Send e-mail notifications on anomaly detection
    """

    DEFAULT_SUBJECT = "[LoudML] anomaly detected! (model={model}, score={score})"
    DEFAULT_CONTENT = """
    Anomaly detected by LoudML!

    model={model}
    score={score}
    predicted={predicted}
    observed={observed}
    """

    CONFIG_SCHEMA = Schema({
        Required('from'): Schema({
            Optional('name', default=""): str,
            Required('address'): Email(),
        }),
        Required('to'): Schema({
            Optional('name', default=""): str,
            Required('address'): Email(),
        }),
        Optional('subject', default=DEFAULT_SUBJECT): str,
        Optional('content', default=DEFAULT_CONTENT): str,
    })

    def on_anomaly(self, model, timestamp, score, predicted, observed, *args, **kwargs):
        plugin_cfg = MailPlugin.instance.config

        if plugin_cfg is None:
            logging.error("mail plug-in is not configured")
            return
        smtp_cfg = plugin_cfg['smtp']

        msg = EmailMessage()

        fmt_args = {
            'model': model,
            'timestamp': timestamp,
            'score': score,
            'predicted': json.dumps(predicted),
            'observed': json.dumps(observed),
        }

        addr = self.config['from']['address'].split('@')
        msg['From'] = Address(
            self.config['from']['name'],
            addr[0],
            addr[1],
        )
        addr = self.config['to']['address'].split('@')
        msg['To'] = Address(
            self.config['to']['name'],
            addr[0],
            addr[1],
        )
        msg['Subject'] = self.config['subject'].format(**fmt_args)
        msg.set_content(self.config['content'].format(**fmt_args))

        if smtp_cfg['tls']:
            smtp_cls = smtplib.SMTP_SSL
        else:
            smtp_cls = smtplib.SMTP

        try:
            client = smtp_cls(
                host=smtp_cfg['host'],
                port=smtp_cfg['port'],
            )

            user = smtp_cfg.get('user')
            if user:
                password = smtp_cfg.get('password')
                client.login(user, password)

            client.send_message(msg)
        except smtplib.SMTPException as exn:
            logging.error("cannot execute %s.%s hook: %s",
                          model, self.name, str(exn))
