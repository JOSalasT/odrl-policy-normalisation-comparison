import rdflib

import Logic
import Parsers
import examples
from Logic import Rule
from Translators import LogicTranslator


def query_contains(rule1, rule2):
    graph = rdflib.Graph()
    n = rdflib.Namespace('http://example.org/')
    for atom in rule1.body:
        if len(atom.termList) == 2:
            subject = n[atom.termList[0].value]
            object_node = n[atom.termList[1].value]
            predicate = n[atom.predicate]
            graph.add((subject, predicate, object_node))
        elif len(atom.termList) == 1:
            subject = n[atom.termList[0].value]
            object_node = n[atom.predicate]
            predicate = rdflib.RDF.type
            graph.add((subject, predicate, object_node))
    query_string = """PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX dpv: <https://w3id.org/dpv/dpv-owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://example.org/>
SELECT * WHERE {\n"""
    for atom in rule2.body:
        if len(atom.termList) == 2:
            subject_string = str(atom.termList[0])
            predicate_string = str(atom.predicate)
            object_string = str(atom.termList[1])
            query_string += subject_string + " :" + predicate_string + " " + object_string + " .\n"
        elif len(atom.termList) == 1:
            subject_string = str(atom.termList[0])
            predicate_string = "a"
            object_string = str(atom.predicate)
            query_string += subject_string + " " + predicate_string + " :" + object_string + " .\n"
    query_string += "}"
    results = graph.query(query_string)
    if len(results) > 0:
        return True
    else:
        return False


def match_rule_to_policy(rule, policy_formula):
    for policy_rule in policy_formula:
        if query_contains(rule, policy_rule):
            return True
    return False


def match_policy_to_policy(policy_formula1, policy_formula2):
    answer = True
    for policy_rule in policy_formula1:
        answer = answer and match_rule_to_policy(policy_rule, policy_formula2)
    return answer


def logic_formula_to_rule(logic_formula):
    generic_head = "Q(x)"
    formula = logic_formula.replace(" ∧ ", ",")
    query = formula + " -> " + generic_head
    rule = Rule()
    rule.parseFromString(query)
    return rule


translator = LogicTranslator()
policy = translator.odrl.parse(examples.example_permission_policy)
policy1 = translator.odrl.parse(examples.example_permission_policy_2)
logic_list = translator.translate_policy([policy, policy1])
rule_list = []
for f in logic_list:
    rule_list.append(logic_formula_to_rule(f))
print(policy)
print(query_contains(rule_list[0], rule_list[0]))
print(query_contains(rule_list[0], rule_list[1]))
print(query_contains(rule_list[1], rule_list[0]))
