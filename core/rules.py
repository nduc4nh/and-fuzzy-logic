from components import Linguistic
from fuzzy_operation import Operation

class Rules:
    def __init__(self, variable):
        """
        Rules Object attribute:
            rules: dict[String][String] - "lng1_name, lng2_name.." -> "lng_name"
            variable: the variable object of the consequence linguistic
        """
        self.rules = {}
        self.variable = variable
        self.op = Operation

    def _parse_rule(self,rule):
        left, right = rule.strip().split("->")
        return left, right

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
        return ",".join([lng.name for lng in fuzzy_set.lngs])

    def apply_rule(self, fuzzy_set) -> Linguistic:
        """
        fuzzy_set: [FuzzySet]
        """
        condition = self.get_condition(fuzzy_set)
        lng_out_name = self.get_result(condition)
        value_out = self.op.get_fuzzy_value(fuzzy_set, option='intersect')
        
        return Linguistic(lng_out_name, value_out, self.variable)



    
        

    

        
        