from ContractParser import ContractParser
from GraphParser import GraphParser
from PolicyComparer import PolicyComparer

file = "examples/example_logical_constraint.json"
filepath1 = "./examples/simple_permissions.ttl"
filepath2 = "./examples/simple_permissions+prohibition_2.ttl"

contract_parser = ContractParser()
contract_parser.load(file)
graph_parser = GraphParser(contract_parser.contract_graph)
policy = graph_parser.parse()
policy = policy.normalise()

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



