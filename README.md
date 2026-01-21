# Policy Comparison and Normalisation

This code allows for the normalisation of ODRL policies containing Permissions and Prohibitions in order to check for policy containment, equivalence or overlap.
The data structures for ODRL policies come from the [UPCAST Policy Engine](https://github.com/EU-UPCAST/PolicyEngine.git)

## Features

- Normalisation of ODRL constraints and refinements. Unique normal forms can only be guaranteed for policies with only permissions and prohibitions.
- Compares ODRL policies for containment, equivalence and overlap.

## Requirements

- Python 3.8+

## Usage

A ContractParser element can be used to parse an ODRL policy in some RDF standard format and get an RDFLib graph.

```
parser = ContractParser()
parser.load(filename)
graph = parser.contract_graph
```

A map from left operands to sets of right operands can be extracted from a ContractParser using:
`values_per_constraints = parser.get_values_from_constraints()`

A GraphParser element can be used to parse an RDFLib graph to a Policy element.

```
graph_parser = GraphParser(graph)
policy = graph_parser.parse()
```

A Policy element can be normalised by using:
`normal_policy = policy.normalise()`

To split the intervals of a normalised policy:

`normal_split_policy = normal_policy.split_intervals(values_per_constraints)`

A PolicyComparer element can be used to compute the overlap or difference between sets of rules.


## Development

To contribute to this project, feel free to submit pull requests. Make sure to test your changes thoroughly.

## License

This project is licensed under the MIT License.
