import sys

import Utils
from ContractParser import ContractParser
from GraphParser import GraphParser
from PolicyComparer import PolicyComparer

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print("No command specified.")
        print("usage: command file1 [file2...]")
        print("command is one of 'normalise', 'normalise_prohibitions', 'compare'")
        print("'normalise' requires exactly one argument. This will normalise simple and logical constraints, but will not split intervals or remove prohibitions. ")
        print("'normalise_prohibitions' requires at least one file. This will normalise, split intervals and remove prohibitions that match permissions.")
        print("'compare' requires exactly 2 arguments. This will compute the overlap between the two policies and two-way containment.")
        sys.exit(1)
    if args[0] == 'normalise':
        if len(args) < 2:
            print("No file specified")
            sys.exit(1)
        contract_parser = ContractParser()
        contract_parser.load(args[1])
        graph_parser = GraphParser(contract_parser.contract_graph)
        policy = graph_parser.parse()
        normal_policy = policy.normalise()
        print(normal_policy)
    elif args[0] == 'normalise_prohibitions':
        args = sys.argv[2:]
        if len(args) < 2:
            print("No file(s) specified")
            sys.exit(1)
        contract_parser = ContractParser()
        contract_parser.load(args[1])
        values_per_constraints = contract_parser.get_values_from_constraints()
        graph_parser = GraphParser(contract_parser.contract_graph)
        policy = graph_parser.parse()
        normal_policy = policy.normalise()
        if len(args) > 2:
            for file in args[2:]:
                contract_parser = ContractParser()
                contract_parser.load(file)
                values_per_constraints = Utils.merge_key_multisets(values_per_constraints,
                                                                   contract_parser.get_values_from_constraints())
            normal_policy = normal_policy.split_intervals(values_per_constraints)
        print(normal_policy)
    elif args[0] == 'compare':
        if len(args) < 3:
            print("Not enough arguments")
            sys.exit(1)
        comparer = PolicyComparer.compare(args[1], args[2])
        print(f"Number of overlapping permissions: {len(comparer[0])}")
        print(f"Is (1) contained in (2)? {comparer[1]}")
        print(f"Is (2) contained in (1)? {comparer[2]}")
        print(f"Are (1) and (2) equivalent? {comparer[1] and comparer[2]}")
    else:
        print("No valid command specified.")
        print("usage: command file1 [file2...]")
        print("command is one of 'normalise', 'normalise_prohibitions', 'compare'")
        print("'normalise' requires exactly one argument. This will normalise simple and logical constraints, but will not split intervals or remove prohibitions. ")
        print("'normalise_prohibitions' requires at least one file. This will normalise, split intervals and remove prohibitions that match permissions.")
        print("'compare' requires exactly 2 arguments. This will compute the overlap between the two policies and two-way containment.")
