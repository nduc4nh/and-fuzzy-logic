from .components import FuzzySet, Linguistic
from .fuzzy_operation import Operation

#Variabe -> Domains, Linguistic -> Entity -> Fuzzyfication -> FuzzySet -> DecisionMaking -> FuzzySet -> Defuzzification

class Fuzzification:
    """
        var: list[String] Variable name
        lng: list[String] Linguistic variable
    """

    def __init__(self, variables):
        self.variables = variables

    def _get_variable(self, name):
        """
        Refer to a Variable Object given its name
            name: name of variable
        """
        for variable in self.variables:
            if variable.name == name:
                return variable
        return None

    def _compute_fuzzy(self, variable, domain):
        """
        Compute fuzzy value for each respected linguistic value
        variable: [Variable] object
        domain: [Domain] oject 
        """
        re = []
        for lng in variable.lng:
            re.append((lng, variable.shape[lng].get_fuzzy_value(domain.value)))
        return re

    def _make_set(self, discrete_fuzzy):
        """
        Aggregate permutation of linguistic values among variables
        """
        vars_name = list(discrete_fuzzy.keys()) #order
        n = len(discrete_fuzzy)

        def Try(i, tmp):
            if i == n:
                yield tmp
                return
            variable = self._get_variable(vars_name[i])
            for lng in variable.lng:
                tmp.append(lng)
                yield from Try(i+1, tmp[:])
                tmp.pop(-1)

        lng_sets = list(Try(0, []))
        fuzzy_sets = []
        for lng_set in lng_sets:
            lngs = [Linguistic(e,
                               discrete_fuzzy[vars_name[i]][e],
                               self._get_variable(vars_name[i]))
                    for i, e in enumerate(lng_set)]
            fuzzy_sets.append(FuzzySet(lngs))
        
        # for fuzzy_set in fuzzy_sets:
        #     print(fuzzy_set.__str__())
        return fuzzy_sets

    def act(self, entity) -> FuzzySet:
        discrete_fuzzy = {}
        for domain in entity.domains:
            variable = self._get_variable(domain.name)
            discrete_fuzzy[domain.name] = {}
            lngs_with_value = self._compute_fuzzy(variable, domain)
            for lng,value in lngs_with_value:
                discrete_fuzzy[domain.name][lng]=value
        
        return self._make_set(discrete_fuzzy)


class DecisionMaking:
    def __init__(self,input_, rules) -> None:
        """
            fuzzy_set: List[FuzzySet]
            rules: [Rule]
        """
        self.input_ = input_
        self.op = Operation
        self.rules = rules
        self.output_ = None
    
    def _fit_rules(self):
        """
            get consequence based on given Rules
        """
        out_lngs = []
        for fuzzy_set in self.input_:
            out_lngs.append(self.rules.apply_rule(fuzzy_set))
        return out_lngs

    def _shrink(self, fuzzy_set):
        lng_names = list(set([lng.name for lng in fuzzy_set]))
        
        re = []
        for lng_name in lng_names:
            re.append(self.op.union_many([lng for lng in fuzzy_set if lng.name == lng_name]))
            
        return re
        
    def process(self) -> FuzzySet:
        linguistic_after_rules = self._fit_rules()
        linguistic_output = self._shrink(linguistic_after_rules)
        self.output_ = FuzzySet(linguistic_output) 
        print(self.output_.__str__())
        return self.output_
    
    def get_output(self):
        if self.output_: return self.output_
        


class DeFuzzifiCation:
    def __init__(self, input_) -> None:
        """
            input_: List[FuzzySet]
        """
        self.input_ = input_

    def cog(self):
        sub_cog = 0
        total_region = 0
        for lng in self.input_.linguistic:
            tmp_lng = lng.fit_shape()
            xi = tmp_lng.get_centroid()
            Ai = tmp_lng.get_area()
            sub_cog += xi * Ai
            total_region += Ai
        
        return sub_cog / total_region
        
