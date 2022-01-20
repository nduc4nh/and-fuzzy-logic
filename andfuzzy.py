# Steps:

# 1/ Define:
#     Variable
#     Domain
#     Entity

# 2/ Fuzzyfication
# 3/ DecisionMakinf
# 4/ Defuzzyfication


from core.fuzzy import DeFuzzifiCation, DecisionMaking, Fuzzification


class AndFuzzy:
    def __init__(self, problem) -> None:
        self.problem = problem
        self.fuzzify_module = Fuzzification(problem.variables)
        self.decision_module = DecisionMaking(None,problem.rules)
        self.defuzzifu_module = DeFuzzifiCation([])
    
    def act(self,entity):
        fuzzify_out = self.fuzzify_module.act(entity)
        self.decision_module.input_ = fuzzify_out
        fuzzyset_out = self.decision_module.process()
        self.defuzzifu_module.input_ = fuzzyset_out
        return self.defuzzifu_module.cog()

class FuzzyProblem:
    def __init__(self, variables, rules) -> None:
        self.variables = variables
        self.rules = rules
