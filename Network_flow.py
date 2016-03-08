# Import
from pyomo.environ import *

# Components:
#   SETS_ALL_CAPS
#   VarsCamelCase
#   params_lower_case_with_underscores
#   Constraints_Words_Capitalized_With_Underscores
# SET_time_system

cities = ['boston', 'chicago', 'dallas', 'kansas-cty', 'losangeles',
          'memphis', 'portland', 'salt-lake', 'wash-dc']
model = ConcreteModel()
model.nodes = Set(initialize=cities)
model.routes = Set(initialize=model.nodes*model.nodes)

# Parameters
distances = {
    ('boston', 'chicago'): 58,
    ('kansas-cty', 'memphis'): 27,
    ('boston', 'wash-dc'): 25,
    ('kansas-cty', 'salt-lake'): 66,
    ('chicago', 'kansas-cty'): 29,
    ('kansas-cty', 'wash-dc'): 62,
    ('chicago', 'memphis'): 32,
    ('losangeles', 'portland'): 58,
    ('chicago', 'portland'): 130,
    ('losangeles', 'salt-lake'): 43,
    ('chicago', 'salt-lake'): 85,
    ('memphis', 'wash-dc'): 53,
    ('dallas', 'kansas-cty'): 29,
    ('portland', 'salt-lake'): 48,
    ('dallas', 'losangeles'): 85,
    ('dallas', 'memphis'): 28,
    ('dallas', 'salt-lake'): 75,
}

model.distances = Param(model.routes, initialize=distances, doc='Distances')

demand = {'boston': 8,
          'chicago': 10,
          'dallas': 0,
          'kansas-cty': 25,
          'losangeles': 15,
          'memphis': 0,
          'portland': 0,
          'salt-lake': 0,
          'wash-dc': 30,
          }

supply = {'boston': 0,
          'chicago': 0,
          'dallas': 40,
          'kansas-cty': 0,
          'losangeles': 0,
          'memphis': 9,
          'portland': 19,
          'salt-lake': 20,
          'wash-dc': 0,
          }

model.demand = Param(model.nodes, initialize=demand, doc='Demand')
model.supply = Param(model.nodes, initialize=supply, doc='Supply')
model.cost = Param(initialize=90, doc='Uniform Freight cost')

# variables
model.flow = Var(model.routes, within=NonNegativeReals)


def cost_rule(mdl):
    return sum(mdl.cost*mdl.flow[i, j]
               for (i, j) in mdl.routes)
model.costTotal = Objective(rule=cost_rule)


def flow_rule(mdl, k):
    inFlow = sum(mdl.flow[i, j] for (i, j) in mdl.routes if j == k)
    outFlow = sum(mdl.flow[i, j] for (i, j) in mdl.routes if i == k)
    return inFlow+mdl.supply[k] == outFlow+mdl.demand[k]
model.flowconstraint = Constraint(model.nodes, rule=flow_rule)

# Display of the output ##
# Display x.l, x.m ;
def pyomo_postprocess(options=None, instance=None, results=None):
    model.flow.display()

# This is an optional code path that allows the script to be run outside of
# pyomo command-line.  For example:  python transport.py
if __name__ == '__main__':
    # This emulates what the pyomo command-line tools does
    from pyomo.opt import SolverFactory
    import pyomo.environ
    opt = SolverFactory("gurobi")
    results = opt.solve(model)
# sends results to stdout
    results.write()
    print("\nDisplaying Solution\n" + '-'*60)
    pyomo_postprocess(None, None, results)
