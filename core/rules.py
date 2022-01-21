from .components import Linguistic
from .fuzzy_operation import Operation

class Rules:
    def __init__(self, variable,orders = None):
        """
        Rules Object attribute:
            rules: dict[String][String] - "lng1_name, lng2_name.." -> "lng_name"
            variable: the variable object of the consequence linguistic
        """
        self.rules = {}
        self.variable = variable
        self.op = Operation
        self.orders = orders

    def _parse_rule(self,rule):
        left, right = rule.strip().split("->")
        return left, right

    
    @staticmethod
    def shuffle(x,reference, key = None):
        if len(x) != len(reference):
            raise Exception("Can't shuffle | x: {}, reference: {}".format(x,reference))
        if not key:
            raise Exception("Define key | key: {}".format(key))
        re = []

        for ref in reference:
            for ele_x in x:
                if key(ele_x) == ref:
                    re.append(ele_x)
                    break

        return re

    @staticmethod    
    def rearange_vars(variable, order):
        order_var = list(order.items())
        order_var.sort(key = lambda x:x[0])
        var_names = [ele[1].name for ele in order_var]
        vars = Rules.shuffle(variable, var_names, key = lambda x:x.name)        

        return vars

    def set_rules(self, rules):
        """
        rules: [list[String]]
        ["x,y,z->y",..]        
        """
        for rule in rules:
            condition, result = self._parse_rule(rule)
            self.rules[condition] = result
    
        return self
    
    def get_result(self, condition):
        """
        conditon: String
        'a,b,c'
        """
        return self.rules[condition]
    
    

    def get_condition(self, fuzzy_set):
        """
        fuzzy_set: [FuzzySet]
        """

        if not self.orders:
            raise Exception('Error!')
        
        order_var = list(self.orders.items())
        order_var.sort(key = lambda x:x[0])
        var_names = [ele[1].name for ele in order_var]
        lngs = Rules.shuffle(fuzzy_set.linguistic, var_names, key = lambda x:x.variable.name)
        lng_names = [lng.name for lng in lngs]

        return ",".join(lng_names)

    def apply_rule(self, fuzzy_set) -> Linguistic:
        """
        fuzzy_set: [FuzzySet]
        """
        condition = self.get_condition(fuzzy_set)
        lng_out_name = self.get_result(condition)
        value_out = self.op.get_fuzzy_value(fuzzy_set, option='intersect')
        
        return Linguistic(lng_out_name, value_out, self.variable)
    
    



    
        

    

        
        