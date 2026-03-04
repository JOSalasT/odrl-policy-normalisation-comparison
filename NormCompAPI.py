# TODO these dummy functions still need to be completed

def normalise_policies(graphs, only_first=False):
    """
    Normalise a list of ODRL policies with respect to each other
    :param graphs: a list of rdflib graph objects containing ODRL policies OR a list of RDF files containing ODRL policies
    :return: if only_first is False, a list A, of the same length as graphs, where A[i] contains ODRL policy x,
    normalised version of policy y, with respect to all the policies in graphs, if and only if graphs[i] contains policy y;
    else only the first element of list A will be returned
    """
    return None

def contains(policy_1, policy2):
    """
    Check if the first policy contains the second
    :param policy_1: an rdflib graph object, or an RDF file, containing a single ODRL policy
    :param policy2: an rdflib graph object, or an RDF file, containing a single ODRL policy
    :return: True if policy_1 contains policy2, else False
    """
    return None

def equals(policy_1, policy_2):
    """
    Check if the two policies are identical
    :param policy_1: an rdflib graph object, or an RDF file, containing a single ODRL policy
    :param policy2: an rdflib graph object, or an RDF file, containing a single ODRL policy
    :return: True if policy_1 is semantically equivalent to policy_2, else False
    """
    return contains(policy_1, policy_2) and contains(policy_2, policy_1)