# Policy Comparison and Normalisation

This code allows for the normalisation of ODRL policies containing Permissions and Prohibitions in order to check for policy containment, equivalence or overlap.
The data structures for ODRL policies come from the [UPCAST Policy Engine](https://github.com/EU-UPCAST/PolicyEngine.git)

## Features

- Normalisation of ODRL constraints and refinements. Unique normal forms can only be guaranteed for policies with only permissions and prohibitions.
- Compares ODRL policies for containment, equivalence and overlap.

## Requirements

- Python 3.8+
- RDFLib 7.0.0

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

demo.py exposes a simple command line interface that allows users to:
- normalise a policy by reformulating logical constraints and simple constraints.
- normalise, split intervals according to the constants in other policies, and remove prohibitions that match permissions.
- compare two ODRL policies by computing their overlap and containment in both directions.

```
usage: command file1 [file2...]
command is one of 'normalise', 'normalise_prohibitions', 'compare'
'normalise' requires exactly one argument. This will normalise simple and logical constraints, but will not split intervals or remove prohibitions. 
'normalise_prohibitions' requires at least one file. This will normalise, split intervals and remove prohibitions that match permissions.
'compare' requires exactly 2 arguments. This will compute the overlap between the two policies and two-way containment.
```

## Example

test.py runs a couple of examples.
This is an ODRL policy that declares a permission with a logical constraint (as seen in examples/example_logical_constraint.json): 
```
{
  "odrl:permission": [
    {
      "odrl:action": "http://www.w3.org/ns/odrl/2/appendTo",
      "odrl:assignee": "https://w3id.org/dpv/dpv-owl#Citizen",
      "odrl:target": ["http://example.org/datasets/climateChangeData", "http://example.org/datasets/climateChangeData2"],
      "odrl:constraint": [
        {
          "odrl:leftOperand": "purpose",
          "odrl:operator": "http://www.w3.org/ns/odrl/2/eq",
          "odrl:rightOperand": "https://w3id.org/dpv/dpv-owl#Personalisation"
        },
        {
          "odrl:and": [
            {
              "odrl:or": [
                {
                  "odrl:leftOperand": "A",
                  "odrl:operator": "http://www.w3.org/ns/odrl/2/lteq",
                  "odrl:rightOperand": 1
                },
                {
                  "odrl:leftOperand": "B",
                  "odrl:operator": "http://www.w3.org/ns/odrl/2/lteq",
                  "odrl:rightOperand": 3
                },
                {
                  "odrl:leftOperand": "C",
                  "odrl:operator": "http://www.w3.org/ns/odrl/2/lteq",
                  "odrl:rightOperand": 6
                }
              ]
            },
            {
              "odrl:or": [
                {
                  "odrl:leftOperand": "D",
                  "odrl:operator": "http://www.w3.org/ns/odrl/2/lteq",
                  "odrl:rightOperand": 10
                },
                {
                  "odrl:leftOperand": "E",
                  "odrl:operator": "http://www.w3.org/ns/odrl/2/lteq",
                  "odrl:rightOperand": 8
                },
                {
                  "odrl:leftOperand": "F",
                  "odrl:operator": "http://www.w3.org/ns/odrl/2/lteq",
                  "odrl:rightOperand": 4
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  "@id": "http://example.org/policy-79f7e6ba-daff-4919-940f-a1ad1344a97a",
  "@context": {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "odrl": "http://www.w3.org/ns/odrl/2/",
        "dpv": "https://w3id.org/dpv/owl#",
        "foaf": "http://xmlns.com/foaf/0.1/"
      },
  "@type": "http://www.w3.org/ns/odrl/2/Policy"
}

```
By running the following:
```
contract_parser = ContractParser()
contract_parser.load("examples/example_logical_constraint.json")
graph_parser = GraphParser(contract_parser.contract_graph)
policy = graph_parser.parse()
policy = policy.normalise()
```
We get a normalised policy comprised of 36 minimal permissions that contains no logical constraints.
The same result can be achieved through the command line by running:
`python demo.py normalise examples/example_logical_constraint.json`


The next example compares "simple_permissions.ttl" against "examples/simple_permissions+prohibition_2.ttl" by running the following:
```
comparer = PolicyComparer.compare("examples/simple_permissions.ttl", "examples/simple_permissions+prohibitions_2.ttl")
print(f"Number of overlapping permissions: {len(comparer[0])}")
print(f"Is (1) contained in (2)? {comparer[1]}")
print(f"Is (2) contained in (1)? {comparer[2]}")
print(f"Are (1) and (2) equivalent? {comparer[1] and comparer[2]}")
```
And outputs the following:
```
Number of overlapping permissions: 1042
Is (1) contained in (2)? False
Is (2) contained in (1)? True
Are (1) and (2) equivalent? False
```
## Development

To contribute to this project, feel free to submit pull requests. Make sure to test your changes thoroughly.

## License

This project is licensed under the MIT License.
