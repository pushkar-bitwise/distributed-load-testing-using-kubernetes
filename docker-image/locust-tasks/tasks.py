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
import random
from datetime import datetime
from locust import HttpLocust, TaskSet, task
import json


def read_rules_requests():
    with open('/inputdata.json') as json_file:
        return json.load(json_file)


rules_requests = read_rules_requests()


class MetricsTaskSet(TaskSet):


    def on_start(self):
        self._deviceid = str(uuid.uuid4())

    @task(1)
    def login(self):
        rule_req = random.choice(rules_requests)
        headers = {'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4='}
        response = self.client.post(
            '/rest/server/containers/instances/discover_pm_2.2.1', data=json.dumps(
                dict(lookup="DimsStatelessSession", commands=[{"insert": {"object": {
                    "com.globalpayments.dims.rule.common.model.CaseDataInput": {
                        "reasonCode": rule_req['reasonCode'],
                        "gracePeriodFlag": rule_req['gracePeriodFlag'],
                        "salesDraftAttached": rule_req['salesDraftAttached'],
                        "merchantDocumentsAttached": rule_req['merchantDocumentsAttached'],
                        "retrievalReqFulfilled": rule_req['retrievalReqFulfilled'],
                        "merchantCategoryCode": rule_req['merchantCategoryCode'],
                        "creditIssued": rule_req['creditIssued'],
                        "previousRetrievalRequestPresent": rule_req['previousRetrievalRequestPresent'],
                        "creditInstance": rule_req['creditInstance'],
                        "salesInstance": rule_req['salesInstance'],
                        "acquirerName": rule_req['acquirerName'],
                        "previousReasonCode": rule_req['previousReasonCode'],
                        "caseStage": rule_req['caseStage'],
                        "stripOffMerchantFlag": rule_req['stripOffMerchantFlag']}},
                    "out-identifier": "fact0",
                    "return-object": "true"}},
                    {"fire-all-rules": {
                        "out-identifier": "rulesFired"}},
                    {"get-objects": {
                        "out-identifier": "fact0"}}]))
            , headers=headers, name="Execute Rule")

        print(response)


class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
