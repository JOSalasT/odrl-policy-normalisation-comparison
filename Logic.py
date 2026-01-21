import sys
import os

# parser = argparse.ArgumentParser
def parse(path, query):
    ruleList = []
    with open(path + "/queries/iqaros/Q" + query + ".txt") as file:
        for line in file:
            r = Rule()
            r.parseFromString(line, "<-")
            r.addAnonVariable()
            print(r)
            print("@export " + r.head[0].predicate + " :- csv{resource = \"" + "Q" + query + ".csv\"} .")
    with open(path + "/dependencies/oneToOne-t-tgds.txt") as file:
        w = 0
        for line in file:
            r = Rule()
            r.parseFromString(line)
            w = max(w, r.getMaxBodyArity())
            r.convertToNemoSyntax()
            r.addCounters()
            ruleList.append(r)
        s = len(ruleList)
        upperBound = s * (2 * w) ** w
        for rule in ruleList:
            rule.addUpperBound(upperBound)
        for rule in ruleList:
            print(rule)


def parseSources(path, size="small"):
    path = path + "/data/oneToOne/" + size
    for file in os.listdir(path):
        if file.startswith("src"):
            sourceName = file.replace("_", "")
            sourceName = sourceName[0:sourceName.find(".")]
            print("@import " + sourceName + " :- csv{resource = \"" + path + "/" + file + "\"} .")
            with open(path + "/" + file) as f:
                line = f.readline().strip("\n")
                arity = len(line.split(","))
                varList = []
                for i in range(arity):
                    varList.append(Variable("X" + str(i)))
                headAtom = Atom(sourceName[3:], varList)
                headAtom.termList.append(Term(0))
                r = Rule([headAtom], [Atom(sourceName, varList)])
                print(r)


def constructNemoProgram(path):
    ruleList = []
    dataList = []
    with open(path + "/dependencies/oneToOne-st-tgds.txt") as file:
        offset = 0
        for line in file:
            r = Rule()
            r.parseFromString(line)
            headAtom = r.head[0]
            predicate = headAtom.predicate
            arity = len(headAtom.termList)
            newTermList = []
            for i in range(arity):
                newTermList.append(Term("\"" + "c" + str(i + offset) + "\""))
            newTermList.append(Term(0))
            offset += arity
            dataList.append(Atom(predicate, newTermList))

    with open(path + "/dependencies/oneToOne-t-tgds.txt") as file:
        w = 0
        for line in file:
            r = Rule()
            r.parseFromString(line)
            w = max(w, r.getMaxBodyArity())
            r.convertToNemoSyntax()
            r.addCounters()
            ruleList.append(r)
        s = len(ruleList)
        upperBound = s * (2 * w) ** w
        for rule in ruleList:
            rule.addUpperBound(upperBound)
        for rule in ruleList:
            print(rule)
        for atom in dataList:
            print(str(atom) + " .")


class Rule:
    def __init__(self, head=None, body=None):
        if head is None:
            self.head = []
        else:
            self.head = head
        if body is None:
            self.body = []
        else:
            self.body = body

    def parseFromString(self, string, separator="->"):
        splitList = string[0:string.find(".")].split(separator)
        if separator == "->":
            head = splitList[1].strip()
            body = splitList[0].strip()
        elif separator == "<-":
            head = splitList[0].strip()
            body = splitList[1].strip()
        elif separator == ":-":
            head = splitList[0].strip()
            body = splitList[1].strip()
        headList = head.split("),")
        bodyList = body.split("),")
        for atom in headList:
            if not atom[len(atom) - 1] == ")":
                atom = atom + ")"
            self.head.append(Atom(atom))
        for atom in bodyList:
            if not atom[len(atom) - 1] == ")":
                atom = atom + ")"
            self.body.append(Atom(atom))

    def __str__(self):
        ansHead = ""
        ansBody = ""
        for atom in self.head:
            ansHead = ansHead + str(atom) + ","
        ansHead = ansHead[0:len(ansHead) - 1]
        for atom in self.body:
            ansBody = ansBody + str(atom) + ","
        ansBody = ansBody[0:len(ansBody) - 1]
        return ansHead + " :- " + ansBody + " ."

    def convertToNemoSyntax(self):
        ansHead = ""
        ansBody = ""
        bodyVars = set()
        for atom in self.body:
            for term in atom.termList:
                if isinstance(term, Variable):
                    bodyVars.add(term)
        for atom in self.head:
            for i in range(len(atom.termList)):
                term = atom.termList[i]
                if isinstance(term, Variable) and term not in bodyVars:
                    term.makeExistential()

    def addCounters(self):
        self.head[0].addIncreasingCounter()
        self.body[0].addCounter()

    def addAnonVariable(self):
        for atom in self.body:
            atom.termList.append(Term("_"))

    def getMaxBodyArity(self):
        highestArity = 0
        for atom in self.body:
            highestArity = max(highestArity, len(atom.termList))
        return highestArity

    def addUpperBound(self, upperBound):
        self.body.append(Expr(Variable("N"), Term("<="), Term(upperBound)))


class Atom:
    def __init__(self, predicate, terms=None):
        self.predicate = predicate
        self.termList = []
        if terms is None:
            self.buildFromString(predicate)
        else:
            for term in terms:
                self.termList.append(term)

    def __str__(self):
        ans = ""
        for term in self.termList:
            ans = ans + str(term) + ","
        ans = self.predicate + "(" + ans[0:len(ans) - 1] + ")"
        return ans

    def buildFromString(self, string):
        self.predicate = string[0:string.find("(")]
        for term in string[string.find("(") + 1:string.find(")")].split(","):
            if "?" in term:
                self.termList.append(Variable(term[term.find("?") + 1:]))
            elif "!" in term:
                v = Variable(term[term.find("!") + 1:])
                v.makeExistential()
                self.termList.append(v)
            else:
                self.termList.append(Term(term))

    def buildFromString(self, string):
        self.predicate = string[0:string.find("(")]
        for term in string[string.find("(") + 1:string.find(")")].split(","):
            if "?" in term:
                self.termList.append(Variable(term[term.find("?") + 1:]))
            elif "!" in term:
                v = Variable(term[term.find("!") + 1:])
                v.makeExistential()
                self.termList.append(v)
            else:
                self.termList.append(Term(term))

    def addCounter(self):
        self.termList.append(Variable("N"))

    def addIncreasingCounter(self):
        self.termList.append(Expr(Variable("N"), Term("+"), Term(1)))


class Term:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, Term):
            return self.value == other.value
        return False

    def __hash__(self):
        return str(self).__hash__()


class Variable(Term):
    def __init__(self, value):
        super().__init__(value)
        self.isExistential = False

    def __str__(self):
        if self.isExistential:
            return "!" + self.value
        return "?" + self.value

    def makeExistential(self):
        self.isExistential = True


class Expr:
    def __init__(self, left, op, right):
        self.leftOp = left
        self.op = op
        self.rightOp = right

    def __str__(self):
        return str(self.leftOp) + " " + str(self.op) + " " + str(self.rightOp)


# parseSources(sys.argv[1],sys.argv[2])
# parse(sys.argv[1],sys.argv[3])
