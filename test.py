from andfuzzy import AndFuzzy, FuzzyProblem, EntityManager, FuzzyRule, Geo
from core.membership_function import trapezoid

problem = FuzzyProblem()

v1 = problem.add_variable(1,"E", {
    "L": Geo('trapzoid').set([1,2,3,4]),
    "M": Geo('trapzoid').set([1+1,2+1,3+1,4+1]),
    "H": Geo('trapzoid').set([1+3,2+3,3+3,4+3])
})

v2 = problem.add_variable(2,"p", {
    "L": Geo('trapzoid').set([10,20,30,40]),
    "M": Geo('trapzoid').set([10*1.5,20*1.5,30*1.5,40*1.5]),
    "H": Geo('trapzoid').set([10*2.5,20*2.5,30*2.5,40*2.5])
})
v3 = problem.add_variable(3,"d", {
    "C": Geo('trapzoid').set([1,2,3,4]),
    "M": Geo('trapzoid').set([1*1.5,2*1.5,3*1.5,4*1.5]),
    "F": Geo('trapzoid').set([1*2.5,2*2.5,3*2.5,4*2.5])
})

v4 = problem.add_variable(-1,"pw",{
    "L": Geo('trapzoid').set([0.1,0.2,0.3,0.4]),
    "M": Geo('trapzoid').set([0.4,0.5,0.6,0.7]),
    "H": Geo('trapzoid').set([0.6,0.7,0.8,0.9])
},
consequence=True)

print([
    v1.__str__(),
    v2.__str__(),
    v3.__str__(),
    v4.__str__()
])
names = [v1.name, v2.name, v3.name]
conditions = list(FuzzyRule.combines(problem.variables, problem.orders))
consequences = ["L"] * 9 + ["M"] * 9 + ["H"] * 9
rules = [conditions[i] + "->" + consequences[i] for i in range(len(conditions))]

problem.define_rules(rules)

entity_manager = problem.get_entity_manager()
domains = [
    entity_manager.define("E",3),
    entity_manager.define("p",10),
    entity_manager.define("d",9)
]
entity = entity_manager.make_entity(domains)
print(entity.__str__())
fuzz = AndFuzzy(problem)
for rule in rules:
    print(rule)
print(fuzz.act(entity))
# problem.define_rules([
#     "L,L,C->L",
# ])