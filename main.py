# Copyright 2018 Google LLC
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

from flask import render_template, Response

from app import init_connection_pool, get_data

############ TABS vs. SPACES App for Cloud Functions ############

# initiate a connection pool to a Cloud SQL database
db = init_connection_pool()

def stocks(request):
    if request.method == "GET":
        return get_data(db)

    return Response(
        response="Invalid http request. Method not allowed, must be 'GET'",
        status=400,
    )
