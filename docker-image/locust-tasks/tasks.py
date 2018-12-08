#!/usr/bin/env python

# Copyright 2015 Google Inc. All rights reserved.
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


import uuid
import time
import random
import json

from datetime import datetime
from locust import HttpLocust, TaskSet, task


class MetricsTaskSet(TaskSet):
    _deviceid = None

    def on_start(self):
        self._deviceid = str(uuid.uuid4()).replace('-', '')

    @task(1)
    def post_metrics(self):
        data = {
            "metric": "operational.australia.nem.ec.meter.real_power",
            "timestamp": int(time.time()),
            "value": random.uniform(0, 2),
            "tags": {
                "DEPL_ID": self._deviceid,
                "phase": 'blue'
            }
        }

        headers = {'Content-Type': 'application/json'}

        r = self.client.post('/api/put?details', data=json.dumps(data), headers=headers)

#    @task(999)
#    def post_metrics(self):
#        self.client.post(
#            "/metrics", {"deviceid": self._deviceid, "timestamp": datetime.now()})


class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
