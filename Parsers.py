"""
Author: Semih Yumuşak
Date: July 24, 2024
Description: This is the constraint package which has logical and arithmetic constraint implementations.

Contributors:

"""
import json

from rdflib import Graph

import examples
from Policy import Policy, Rule, Permission, Obligation, Duty, Prohibition


class PolicyObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class ODRLParser:
    def parse_file(self, file_name):
        if file_name is not None:
            file_name = file_name
        with open(file_name, 'r') as file:
            parsed_policy = json.load(file)

        # with open(file_name, 'r') as file:
        #     parsed_policy_object = json.load(file,object_hook = lambda d: Policy(**d))
        list_of_policies = []
        for p in parsed_policy:
            list_of_policies.append(self.parse(p))

        return list_of_policies

    def parse_list(self, parsed_policy):
        list_of_policies = []
        for p in parsed_policy:
            list_of_policies.append(self.parse(p))

        return list_of_policies

    def parse(self, parsed_policy):
        policy = Policy(parsed_policy["@id"], parsed_policy["@type"])
        for key, value in parsed_policy.items():
            if key == "odrl:prohibition":
                policy.prohibition = self.__parse_rule(key, value)
            if key == "odrl:permission":
                policy.permission = self.__parse_rule(key, value)
            if key == "odrl:duty":
                policy.duty = self.__parse_rule(key, value)
            if key == "odrl:obligation":
                policy.obligation = self.__parse_rule(key, value)
        return policy

    def __parse_rule(self, type, rule):
        ans = []
        for r in rule:
            action = r["odrl:action"]
            actor = r["odrl:assignee"]
            if "odrl:assigner" in r:
                assigner = r["odrl:assigner"]
            else:
                assigner = None
            if "odrl:target" in r:
                target = r["odrl:target"]
            else:
                target = None
            if "odrl:constraint" in r:
                constraint = r["odrl:constraint"]
            else:
                constraint = None
            if "odrl:remedy" in r:
                remedy = r["odrl:remedy"]
            else:
                remedy = None
            if "odrl:consequence" in r:
                consequence = r["odrl:consequence"]
            else:
                consequence = None
            if "odrl:duty" in r:
                duty = r["odrl:duty"]
            else:
                duty = None
            if type == "odrl:prohibition":
                ans.append(Prohibition(action=action, assigner=assigner, assignee=actor, target=target, constraint=constraint, remedy=remedy))
            if type == "odrl:permission":
                ans.append(Permission(action=action, duty=duty, assignee=actor, target=target, constraint=constraint))
            if type == "odrl:duty":
                ans.append(Duty(action=action, assignee=actor, target=target, constraint=constraint))
            if type == "odrl:obligation":
                ans.append(Obligation(action=action, assignee=actor, target=target, constraint=constraint, consequence=consequence))
        return ans

    def __parse_refinable(self, type, refinable):
        pass

    def __parse_constraint(self, type, constraint):
        pass

