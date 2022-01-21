# Steps:

# 1/ Define:
#     Variable
#     Domain
#     Entity

# 2/ Fuzzyfication
# 3/ DecisionMakinf
# 4/ Defuzzyfication


from core.components import Domain, Entity, Variable
from core.fuzzy import DeFuzzifiCation, DecisionMaking, Fuzzification
from core.membership_function import Trapzoid
from core.rules import Rules

class Geo:
    def __init__(self, name) -> None:
        self.name = name
        if name == "trapzoid":
            self.shape_class = Trapzoid
        else:
            raise Exception("Shape isn't exists")
        self.shape = None
    
    def set(self,params = []):
        if self.name == "trapzoid":
            if len(params) != 4: raise Exception("Invalid params | {}".format(params))
            self.shape = self.shape_class(
                params[0],
                params[1],
                params[2],
                params[3]
            )
            return self.shape 

class FuzzyRule:
    @staticmethod
    def combines(variables, orders):
        vars = Rules.rearange_vars(variables, orders)
        n = len(vars)
        def Try(i,tmp):
            if i == n:
                yield ",".join(tmp)
                return
                
                      
            for lng in vars[i].lng:
                tmp.append(lng)
                yield from Try(i+1, tmp[:])
                tmp.pop(-1)
                
        return Try(0,[])

class FuzzyManager:
    def __init__(self) -> None:
        pass
    
    def get(self,name):
        return 
    
    def define(self,**kwargs):
        return

class VariableManager(FuzzyManager):
    def __init__(self, variables) -> None:
        """
        Variable manager interacting with core module objects
        """
        super().__init__()
        self.variables = variables
    
    def get(self, name):
        var_list = [var for var in self.variables if var.name == name]
        if len(var_list) != 1:
            raise Exception("variables from FuzzyProblem got trouble | {}".format(
                [var.name for var in self.variables]
            ))
        return var_list[0]
    
    def define(self, **kwargs):
        return super().define(**kwargs)
    
    @staticmethod
    def make_variable(name, linguistic_mapper):
        lngs = list(linguistic_mapper.keys())
        shapes = [geo for geo in linguistic_mapper.values()]
        shape_mapper = dict(zip(lngs, shapes))

        var = Variable(name)
        var.get_linguistic(lngs)
        var.set_shape(shape_mapper)

        return var


class EntityManager(FuzzyManager):
    def __init__(self ,problems) -> None:
        """
        EntityManager:
        manager interacting with core module objects to get, create Entity, Domain
        """
        super().__init__()
        self.problem = problems

    
    def get(self, name):
        pass

    def define(self, name = None, value = None, **kwargs):
        """
        name: [String]
        value: [Numeric]
        """
        if not name or not value:
            raise Exception("Undefined name or value | name: {}, value: {}".format(name, value))
        var_manage = self.problem.get_variable_manager()
        var = var_manage.get(name)
        return Domain(name, value, var)
    
    @staticmethod
    def make_entity(domains):
        return Entity(domains)
                
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
    def __init__(self, variables = [], rules = None) -> None:
        self.variables = variables
        self.output_variables = None
        self.rules = rules
        self.orders = {}

    def add_variable(self, order, name = "", lngs_mapper = {}, consequence = False):
        """
        name: [String] variable name
        lngs_mapper: dict[String][String] | {"linguistic": "trapzoid"}
        option: [boolean] decide whether the variable is consequence or not
            default: False
            condition -> consequence
            * condition: left side variable
            * consequence: right side variable -> to define rule
        """
        if not name or not lngs_mapper:
            raise Exception("No parameters was passed")

        var = VariableManager.make_variable(name, lngs_mapper)
        
        if consequence: self.output_variables = var
        else: 
            self.variables.append(var)
            if self.orders.__contains__(order):
                raise Exception("Invalid order | {}".format(order))
            self.orders[order] = var
        
        return var

    def define_rules(self,rules):
        """
        rules: list[String]
        [lng1,lng2,lng3 -> lng4]
        lng1,lng2,lng3: condition linguistic
        lng4: consequencce linguistic
        """
        rule = Rules(self.output_variables, self.orders)
        rule.set_rules(rules)
        self.rules = rule
        return rule
    
    def get_variable_manager(self):
        if not self.variables:
            raise Exception("No variables to manage")
        if not self.output_variables:
            raise Exception("No consequence variables")

        vars = self.variables + [self.output_variables]
        return VariableManager(vars)
    
    def get_entity_manager(self):
        return EntityManager(self)

        
