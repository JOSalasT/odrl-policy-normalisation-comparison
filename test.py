import json

import Utils
import examples
from Constraint import LogicalConstraint
from ContractParser import ContractParser
from GraphParser import GraphParser
from Parsers import ODRLParser
from Policy import Prohibition, Permission, PolicyComparer

filepath1 = "./examples/simple_permissions.ttl"
filepath2 = "./examples/simple_permissions+prohibition_2.ttl"

comparer = PolicyComparer.compare(filepath1, filepath2)
print(f"Number of overlapping permissions: {len(comparer[0])}")
print(f"Is (1) contained in (2)? {comparer[1]}")
print(f"Is (2) contained in (1)? {comparer[2]}")
print(f"Are (1) and (2) equivalent? {comparer[1] and comparer[2]}")

filepath1 = "./examples/simple_permissions.ttl"
comparer = PolicyComparer.compare(filepath1, filepath1)
print(f"Number of overlapping permissions: {len(comparer[0])}")
print(f"Is (1) contained in (2)? {comparer[1]}")
print(f"Is (2) contained in (1)? {comparer[2]}")
print(f"Are (1) and (2) equivalent? {comparer[1] and comparer[2]}")
# for permission in normal_p.permission:
#     for constraint in permission.constraint:
#         c = constraint.split_intervals(values_per_constraints_2)
#         if isinstance(c, LogicalConstraint):
#             if c.operator == "or":
#                 for sub_c in c.constraints:
#                     if sub_c not in unique_constraints:
#                         unique_constraints.append(sub_c)
#
# for constraint in unique_constraints:
#     unique_permissions.append(Permission(target=p.permission[0].target, action=p.permission[0].action, assigner=p.permission[0].assigner, assignee=p.permission[0].assignee, constraint=[constraint]))
#
# for prohibition in normal_p.prohibition:
#     for constraint in prohibition.constraint:
#         c = constraint.split_intervals(f)
#         if isinstance(c, LogicalConstraint):
#             if c.operator == "or":
#                 for sub_c in c.constraints:
#                     p = Prohibition(target=prohibition.target, remedy=prohibition.remedy, action=prohibition.action, assigner=prohibition.assigner, assignee=prohibition.assignee,
#                            constraint=[sub_c])
#                     print(p)


# odrl = ODRLParser()
# with open(filepath) as json_file:
#     data = json.load(json_file)
#     policy = odrl.parse(data)
#     normal_policy = policy.normalise()
#     print(normal_policy)



