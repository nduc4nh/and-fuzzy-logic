from membership_function import Shape, Trapzoid


class Variable:
    def __init__(self, name) -> None:
        """
        Variable Object:
        - name: [String] variable name
        
        + other attributes:
            lng: list[String]
            membership_function: Dict[[String][func]]
        """
        self.name = name
        self.lng = None
        self.membership_function = None
        self.shape = None

    def _exists_lng(self, lng):
        return self.membership_function.__contains__(lng)

    def get_linguistic(self, lngs):
        self.lng = lngs
        self.membership_function = dict(
            zip(self.lng, [None for ele in self.lng]))

    def _define_membership_function(self, lng, func):
        if not self._exists_lng(lng):
            raise Exception("{} is not defined")

        self.membership_function[lng] = func

    def set_membership_function(self, function_mapper):
        """
        function_mapper: [dict(String, Object Function)] 
        e.g: 
            {"lng":function}
        """

        for lng, func in function_mapper.items():
            self._define_membership_function(lng, func)

        return self.membership_function
    
    def set_shape(self, shape_mapper):
        """
        function_mapper: [dict(String, Object Shape)] 
        e.g: 
            {"lng":shape}
        """
        self.shape = self.shape = dict(
            zip(self.lng, [None for ele in self.lng]))
        
        for lng, shape in shape_mapper.items():
            self.shape[lng] = shape
    

class Domain:
    """
        A domain incluces Variale name going along with a specific value
    """

    def __init__(self, name, value, variable):
        self.name = name
        self.value = value
        self.variable = variable
    
    def get_fuzzy_value(self,lng):
        return self.var.shape[lng].get_fuzzy_value()


class Linguistic(Domain):
    """
        Linguistic value
    """

    def __init__(self, name, value, variable):
        super().__init__(name, value, variable)
        self.modified_shape = None
    
    def fit_shape(self) -> Shape:
        self.modified_shape = self.variable.shape[self.name].fit_shape()
        return self.modified_shape

    def get_area(self):
        if not self.modified_shape:
            raise Exception("Shape for linguistic is undefined")
        return self.modified_shape.get_area()
    
    def get_centroid(self):
        if not self.modified_shape:
            raise Exception("Shape for linguistic is undefined")
        return self.modified_shape.get_centroid()
    
class Entity:
    """
        An entity posesses a set of Domains
    """

    def __init__(self, domains):
        self.domains = domains


class FuzzySet:
    def __init__(self, lngs):
        self.linguistic = lngs
    
    
    
