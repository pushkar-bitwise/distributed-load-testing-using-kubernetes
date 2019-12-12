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

from datetime import datetime
from locust import HttpLocust, TaskSet, task
import json


class MetricsTaskSet(TaskSet):
    _deviceid = None

    def on_start(self):
        self._deviceid = str(uuid.uuid4())

    @task(1)
    def login(self):
        headers = {'content-type': 'application/json', 'Authorization':'Basic YWRtaW46YWRtaW4='}
        self.client.post(
            '/rest/server/containers/instances/discover_pm_2.2.1', data= json.dumps({ "lookup": "DimsStatelessSession", "commands": [ { "insert": { "object": { "com.globalpayments.dims.rule.common.model.CaseDataInput": { "reasonCode" : "01", "gracePeriodFlag": "false", "salesDraftAttached": "false", "merchantDocumentsAttached": "true", "retrievalReqFulfilled": "true", "merchantCategoryCode": "5712", "creditIssued": "false", "previousRetrievalRequestPresent": "true", "creditInstance": 2, "salesInstance": 2, "acquirerName": "GPN", "previousReasonCode": "02", "caseStage" : "Chargeback", "stripOffMerchantFlag": "false" } }, "out-identifier": "fact0", "return-object":"true" } }, { "fire-all-rules": { "out-identifier": "rulesFired" } }, { "get-objects": { "out-identifier": "fact0" } } ] })
,headers=headers,   name = "Execute Rule")

class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
