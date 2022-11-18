# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import logging
import os
from typing import Dict

import json
from flask import Flask, render_template, request, Response, jsonify, make_response

import sqlalchemy

from connect_connector import connect_with_connector
from connect_connector_auto_iam_authn import connect_with_connector_auto_iam_authn
from connect_tcp import connect_tcp_socket
from connect_unix import connect_unix_socket

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    # use a TCP socket when INSTANCE_HOST (e.g. 127.0.0.1) is defined
    #if os.environ.get("INSTANCE_HOST"):
    #    return connect_tcp_socket()

    # use a Unix socket when INSTANCE_UNIX_SOCKET (e.g. /cloudsql/project:region:instance) is defined
    if os.environ.get("INSTANCE_UNIX_SOCKET"):
        return connect_unix_socket()

    # use the connector when INSTANCE_CONNECTION_NAME (e.g. project:region:instance) is defined
    # if os.environ.get("INSTANCE_CONNECTION_NAME"):
    #     # Either a DB_USER or a DB_IAM_USER should be defined. If both are
    #     # defined, DB_IAM_USER takes precedence.
    #     return connect_with_connector_auto_iam_authn() if os.environ.get("DB_IAM_USER") else connect_with_connector()

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )

@app.before_first_request
def init_db() -> sqlalchemy.engine.base.Engine:
    global db
    db = init_connection_pool()

@app.route("/", methods=["GET"])
def test():
    return get_data(db)

def get_data(db: sqlalchemy.engine.base.Engine) -> Dict:
    data = []

    with db.connect() as conn:
        data_rows = conn.execute(
            "SELECT * from target ORDER BY ticker ASC;"
        ).fetchall()
    
        for row in data_rows:
            data.append({"ticker": row[0], "name": row[1], "target": row[2]})

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
