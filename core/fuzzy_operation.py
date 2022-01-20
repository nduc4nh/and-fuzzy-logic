from msilib.schema import Error
from components import Linguistic


class Operation:
    @staticmethod
    def union(ling1,ling2):
        if ling1.name == ling2.name and ling1.varable.name == ling2.variable.name:
            new_ling = Linguistic(ling1.name, None, ling1.variable)
            new_ling.value = max(ling1.value, ling2.value)
            return [new_ling] 
        return [ling1,ling2]
    
    @staticmethod
    def get_max_value(list_of_lngs):
        return max(list_of_lngs, lambda x:x.value)

    @staticmethod
    def get_min_value(list_of_lngs):
        return min(list_of_lngs, lambda x:x.value)

    @staticmethod
    def get_fuzzy_value(fuzzy_set, option = 'union'):
        if option == 'union':
            return Operation.get_max_value(fuzzy_set.lngs)
        elif option == 'intersect':
            return Operation.get_min_value(fuzzy_set.lngs)
            
    @staticmethod
    def union_many(list_of_lngs) -> list:
        """
            fuzzy_set: [FuzzySet] the fuzzyset after rules application
        """
        names = list(set([lng.name for lng in list_of_lngs]))
        var_names = list(set([lng.variable.name for lng in list_of_lngs]))

        if not len(list_of_lngs):
            raise Exception("Invalid input | {}".format(list_of_lngs))
        if len(names) != 1:
            raise Exception("Encounter more than 1 linguistics for union! | {}".format(names))
        if len(var_names) != 1:
            raise Exception("Encounter more than 1 types of variable for union! | {}".format(var_names))

        re = Linguistic(
            names[0],
            Operation.get_max_value(list_of_lngs),
            list_of_lngs[0].variable
        )

        return re
        
    