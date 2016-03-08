# Tariff Rates Example

from __future__ import division
from pyomo.environ import *

model = AbstractModel()

# Sets
model.TimePeriods		= Set()
model.GeneratorTypes	= Set()


# Parameters
model.min_output 		= Param(model.GeneratorTypes)
model.max_output 		= Param(model.GeneratorTypes)
model.cost_hr_min 		= Param(model.GeneratorTypes)
model.cost_incr_hr 		= Param(model.GeneratorTypes)
model.cost_start_up 	= Param(model.GeneratorTypes)
model.avail_generators 	= Param(model.GeneratorTypes)
model.period_hrs		= Param(model.TimePeriods)
model.demand			= Param(model.TimePeriods)

# Variables
model.n = Var(model.GeneratorTypes, model.TimePeriods, within=NonNegativeIntegers)
model.x = Var(model.GeneratorTypes, model.TimePeriods, within=NonNegativeReals)
model.s = Var(model.GeneratorTypes, model.TimePeriods, within=NonNegativeIntegers)

# Objective
def obj_rule(mdl):
	return sum(mdl.n[I,J]*mdl.period_hrs[J]*mdl.cost_hr_min[I] 
	+(mdl.x[I,J]-(mdl.n[I,J]*mdl.min_output[I]))*mdl.period_hrs[J]*mdl.cost_incr_hr[I] 
	+mdl.s[I,J]*mdl.cost_start_up[I] 
	for I in mdl.GeneratorTypes for J in mdl.TimePeriods)
model.obj = Objective(rule=obj_rule, sense=minimize)

# Define Constraints
def demand_rule(mdl, j):
	return  sum(mdl.x[i,j] for i in mdl.GeneratorTypes) >= mdl.demand[j]  
model.DemandConstraint = Constraint(model.TimePeriods, rule = demand_rule)

def minimum_rule(mdl, i, j):
	return mdl.x[i,j] >= mdl.min_output[i]*mdl.n[i,j]	
model.MinimumConstraint = Constraint(model.GeneratorTypes, model.TimePeriods, rule = minimum_rule)

def maximum_rule(mdl, i, j):
	return mdl.x[i,j] <= mdl.max_output[i]*mdl.n[i,j]	
model.MaximumConstraint = Constraint(model.GeneratorTypes, model.TimePeriods, rule = maximum_rule)

def max_generator_rule(mdl, i, j):
	return mdl.n[i,j] <= mdl.avail_generators[i] 
model.Max_generatorConstraint = Constraint(model.GeneratorTypes, model.TimePeriods, rule = max_generator_rule)

def start_up_rule(mdl, i, j):
	kk = int(j[1])-1
	if kk == 0:
		kk = len(j)
	k = 'T' + str(kk)	
	return mdl.s[i,j] >= mdl.n[i,j]-mdl.n[i,k]
	return mdl.s[i,j] >= mdl.n[i,j]-mdl.n[i,k]
model.Start_up_rule = Constraint(model.GeneratorTypes, model.TimePeriods, rule = start_up_rule)

def reserve_rule(mdl, j):
	return sum(mdl.max_output[i]*mdl.n[i,j] for i in mdl.GeneratorTypes) >= 1.15*mdl.demand[j]
model.Reserve_rule = Constraint(model.TimePeriods, rule = reserve_rule)