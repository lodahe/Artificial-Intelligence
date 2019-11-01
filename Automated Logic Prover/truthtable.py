
from abc import ABCMeta, abstractmethod
import copy

class KnowledgeBase:  # the knowledge bsae with a Dict of Symbols and Compound Sentences
    def __init__(self):
        self.Sentences = {}
        self.SymbolTable = []
        self.modelList = []
        self.Target = ""

    def buildModels(self, symbolList, model):

        if len(symbolList) == 0:
            self.modelList.append(model)
            return

        sym = symbolList[0]
        modelA = copy.deepcopy(model)

        model.setEntry(sym.name, False)
        modelA.setEntry(sym.name, True)

        self.buildModels(symbolList[1:], model)
        self.buildModels(symbolList[1:], modelA)

    def calcKB(self, model=None):
        isSat = True
        for key in sorted(self.Sentences.keys()):
            if type(self.Sentences[key]) is CompoundSentence:
                if (self.Sentences[key].KB_state):
                    if (model == None):
                        print(self.Sentences[key].name, "\t\t", end="")
                    else:
                        print(self.Sentences[key].checkSatisfied(model), "\t", end="")
                        if not (self.Sentences[key].checkSatisfied(model)):
                            isSat = False

    def checkEntailment(self, TargetName):
        isEntailed = True
        for model in self.modelList:
            kbSat = True
            for key in sorted(self.Sentences.keys()):
                if (type(self.Sentences[key]) is CompoundSentence) and (self.Sentences[key].KB_state) and (
                not self.Sentences[key].checkSatisfied(model)):
                    kbSat = False
                    break
            if (kbSat and not model.symbolMap[TargetName]):
                isEntailed = False
        return isEntailed

    def printSymbols(self):
        for i in self.SymbolTable:
            print(i.name, "\t\t", end="")

class Sentence:
    __metaclass__ = ABCMeta

    @abstractmethod  # this is pythons abstract class implementation if you werent aware
    def checkSatisfied(self, model):
        pass

class Model:
    # assigns symbols truth or false values
    def __init__(self):
        self.symbolMap = {}  # this maps all symbols to booleans

    def setEntry(self, name, b):
        self.symbolMap[name] = b

    def printEntries(self, KB):
        for i in KB.SymbolTable:
            print(self.symbolMap[i.name], "\t", end="")

class CompoundSentence(Sentence):
    def __init__(self, name, left, right, op, KB, KB_state):
        if left is not None:
            self.left = KB.Sentences[left]
        else:
            self.left = None
        self.right = KB.Sentences[right]
        self.op = op  # operators like and, or, not
        self.name = name
        self.KB_state = KB_state
        self.KB = KB
        KB.Sentences[name] = self

    def checkSatisfied(self, model):  # switch case over the possible operators

        if self.left is None:  # This is the format of a unary sentence
            if self.op == "not":
                return not (self.right.checkSatisfied(model))
                # notice that checkSatisfied will evaluate to a True or False if right is a Symbol,
                # but it will be recursive if right is a Sentence.
                # This works because both classes have the checkSatisfied
                # method from the abstract class Sentence
            else:
                return self.right.checkSatisfied(model)
        elif self.op == "and":
            return self.left.checkSatisfied(model) and self.right.checkSatisfied(model)
        elif self.op == "or":
            return self.left.checkSatisfied(model) or self.right.checkSatisfied(model)
        elif self.op == "imp":
            return (not self.left.checkSatisfied(model)) or self.right.checkSatisfied(model)
        elif self.op == "bicond":
            return self.left.checkSatisfied(model) == self.right.checkSatisfied(model)

class Symbol(Sentence):
    # Symbols are just atomic Trues or Falses
    def __init__(self, name, KB):
        self.KB = KB
        self.name = name
        KB.Sentences[name] = self
        KB.SymbolTable.append(self)

    def checkSatisfied(self, model):
        return model.symbolMap[self.name]

def parser(fileName, KB):
    with open(fileName) as f:
        s = f.readline()
        # print(s)
        if s != "Symbols:\n":
            raise (IOError("Uncorrected Format"))
        s = f.readline()
        while s != "Compounds:\n":
            s = s.split()  # cutoff the newline
            # print(s)
            sym = Symbol(s[0], KB)
            s = f.readline()
        s = f.readline()
        while s != "Target:\n":
            s = s.split()
            name = s[0]  # a string name for the compound(like 1,2,3...)
            left = s[1]  # a string name for the left symbol
            op = s[2]
            right = s[3]  # a string name for the right symbol
            KB_state = s[4]
            if left == "null":
                left = None
            if op == "null":
                op = None
            newCompound = CompoundSentence(name, left, right, op, KB, (KB_state == "true"))
            s = f.readline()
        s = f.readline()
        s = s.split()[0]
        KB.Target = s

KB = KnowledgeBase()
parser("Door2.txt", KB)
model = Model()
print("Truthtable:")
KB.buildModels(KB.SymbolTable, model)
KB.printSymbols()
print("||\t", end="")
KB.calcKB()
print("")
for i in KB.modelList:
    i.printEntries(KB)
    print("||\t", end="")
    KB.calcKB(i)
    print("")
print("Result of Truthtable: ", KB.Target, 'is', KB.checkEntailment(KB.Target))
