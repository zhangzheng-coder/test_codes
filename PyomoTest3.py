#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import
from pyomo.environ import *
 
# Creation of a Concrete Model
model = ConcreteModel()
 
## Define sets ##
#  Sets
#       i   canning plants   / seattle, san-diego /
#       j   markets          / new-york, chicago, topeka / ;
cit1=['seattle','san-diego']
model.i = Set(initialize=cit1, doc='Canning plans')
model.j = Set(initialize=['new-york','chicago', 'topeka'], doc='Markets')
 
## Define parameters ##
#   Parameters
#       a(i)  capacity of plant i in cases
#         /    seattle     350
#              san-diego   600  /
#       b(j)  demand at market j in cases
#         /    new-york    325
#              chicago     300
#              topeka      275  / ;
model.a = Param(model.i, initialize={'seattle':350,'san-diego':600}, doc='Capacity of plant i in cases')
model.l = Param(model.i, initialize={'seattle':18,'san-diego':18}, doc='Earning from plant i in cases')
model.k = Param(model.j, initialize={'new-york':10,'chicago':10,'topeka':12}, doc='Cost of demand j in cases')
#  Table d(i,j)  distance in thousands of miles
#                    new-york       chicago      topeka
#      seattle          2.5           1.7          1.8
#      san-diego        2.5           1.8          1.4  ;
dtab = {
    ('seattle',  'new-york') : 2.5,
    ('seattle',  'chicago')  : 1.7,
    ('seattle',  'topeka')   : 1.8,
    ('san-diego','new-york') : 2.1,
    ('san-diego','chicago')  : 1.8,
    ('san-diego','topeka')   : 1.4,
    }
model.d = Param(model.i, model.j, initialize=dtab, doc='Distance in thousands of miles')
#  Scalar f  freight in dollars per case per thousand miles  /90/ ;
model.f = Param(initialize=90, doc='Freight in dollars per case per thousand miles')
#  Parameter c(i,j)  transport cost in thousands of dollars per case ;
#            c(i,j) = f * d(i,j) / 1000 ;
def c_init(model, i, j):
  return model.f * model.d[i,j] / 1000
model.c = Param(model.i, model.j, initialize=c_init, doc='Transport cost in thousands of dollar per case')
 
## Define variables ##
#  Variables
#       x(i,j)  shipment quantities in cases
#		b(j) Demand in each market
#       z       total transportation costs in thousands of dollars ;
#  Positive Variable x ;
model.x = Var(model.i, model.j, bounds=(0.0,None), doc='Shipment quantities in case')
model.b = Var(model.j, bounds=(0.0,300), doc='Demand quantities') 
model.q = Var(model.i, bounds=(0.0,9999), doc='Supply quantities')
 
## Define contrains ##
# supply(i)   observe supply limit at plant i
# supply(i) .. sum (j, x(i,j)) =l= a(i)
def supply_rule(model, i):
  return sum(model.x[i,j] for j in model.j) <= model.a[i]
model.supply_rule = Constraint(model.i, rule=supply_rule, doc='Observe supply limit at plant i')
# demand(j)   satisfy demand at market j ;  
# demand(j) .. sum(i, x(i,j)) =g= b(j);

def supply_amount(model,i):
	return sum(model.x[i,j] for j in model.j) == model.q[i]
model.supply_amount=Constraint(model.i, rule=supply_amount, doc='Total supply')	

def demand_rule(model, j):
  return sum(model.x[i,j] for i in model.i) >= model.b[j]  
model.demand = Constraint(model.j, rule=demand_rule, doc='Satisfy demand at market j')

def balance(model):
  return sum(model.b[j] for j in model.j) == sum(model.q[i] for i in model.i)
model.demand = Constraint(model.j, rule=balance, doc='Energy Balance in the system') 
 
## Define Objective and solve ##
#  cost        define objective function
#  cost ..        z  =e=  sum((i,j), c(i,j)*x(i,j)) + sum(j,90*b(j)-sum(i,120*x(i));
#  Model transport /all/ ;
#  Solve transport using lp minimizing z ;
def objective_rule(model):
  return  sum(model.k[j]*model.b[j] for j in model.j) + sum(model.c[i,j]*model.x[i,j] for i in model.i for j in model.j) - sum(model.l[i]*model.q[i] for i in model.i)
model.objective = Objective(rule=objective_rule, sense=minimize, doc='Define objective function')
 
 
## Display of the output ##
# Display x.l, x.m ;
def pyomo_postprocess(options=None, instance=None, results=None):
  model.x.display()
  model.b.display()
  model.q.display()
 
# This is an optional code path that allows the script to be run outside of
# pyomo command-line.  For example:  python transport.py
if __name__ == '__main__':
    # This emulates what the pyomo command-line tools does
    from pyomo.opt import SolverFactory
    import pyomo.environ
    opt = SolverFactory("gurobi")
    results = opt.solve(model)
    #sends results to stdout
    results.write()
    print("\nDisplaying Solution\n" + '-'*60)
    pyomo_postprocess(None, None, results)