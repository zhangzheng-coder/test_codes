# Tariff Rates Example

from __future__ import division
from pyomo.environ import *

model = ConcreteModel()

TimePeriods = ['T1', 'T2', 'T3', 'T4', 'T5']
model.J = Set(initialize=TimePeriods)

GeneratorTypes = ['Type1', 'Type2', 'Type3']
model.I = Set(initialize=GeneratorTypes)

HydroGeneratorType = ['TypeA', 'TypeB']
model.HydroGeneratorTypes = Set(initialize=HydroGeneratorType)

# Define the Parameters
min_output_l = {
('Type1'): 850,
('Type2'): 1250,
('Type3'): 1500
}

max_output_l = {
('Type1'): 2000,
('Type2'): 1750,
('Type3'): 4000
}

cost_hr_min_l = {
('Type1'): 1000,
('Type2'): 2600,
('Type3'): 3000
}

cost_incr_hr_l = {
('Type1'): 2,
('Type2'): 1.3,
('Type3'): 3
}

cost_start_up_l = {
('Type1'): 2000,
('Type2'): 1000,
('Type3'): 500
}

avail_generators_l = {
('Type1'): 12,
('Type2'): 10,
('Type3'): 5
}

#period_hrs_l = [6, 3, 6, 3, 6]
period_hrs_l = {
('T1'): 6,
('T2'): 3,
('T3'): 6,
('T4'): 3,
('T5'): 6
}

demand_l = {
('T1'): 15000,
('T2'): 30000,
('T3'): 25000,
('T4'): 40000,
('T5'): 27000
}

hydro_operating_level_l = {
('TypeA'): 900,
('TypeB'): 1400
}

hydro_cost_hr_l = {
('TypeA'): 90,
('TypeB'): 150
}

hydro_reservoir_reduction_hr_l = {
('TypeA'): 0.31,
('TypeB'): 0.47
}

hydro_cost_start_up_l = {
('TypeA'): 1500,
('TypeB'): 1200
}

model.min_output 	= Param(model.I, initialize=min_output_l)
model.max_output 	= Param(model.I, initialize=max_output_l)
model.cost_hr_min 	= Param(model.I, initialize=cost_hr_min_l)
model.cost_incr_hr 	= Param(model.I, initialize=cost_incr_hr_l)
model.cost_start_up = Param(model.I, initialize=cost_start_up_l)
model.avail_generators = Param(model.I, initialize=avail_generators_l)
model.period_hrs	= Param(model.J, initialize=period_hrs_l)
model.demand 		= Param(model.J, initialize=demand_l)

model.hydro_operating_level	= Param(model.HydroGeneratorTypes, initialize=hydro_operating_level_l)
model.hydro_cost_hr			= Param(model.HydroGeneratorTypes, initialize=hydro_cost_hr_l)
model.hydro_reservoir_reduction_hr	= Param(model.HydroGeneratorTypes, initialize=hydro_reservoir_reduction_hr_l)
model.hydro_cost_start_up	= Param(model.HydroGeneratorTypes, initialize=hydro_cost_start_up_l)

# Declare the variables
model.n = Var(model.I, model.J, domain=NonNegativeIntegers)
model.x = Var(model.I, model.J, domain=NonNegativeReals)
model.s = Var(model.I, model.J, domain=NonNegativeIntegers)

model.h = Var(model.HydroGeneratorTypes, model.J, domain=Binary)
#model.t = Var(model.HydroGeneratorTypes, model.J, domain=Binary)
model.t = Var(model.HydroGeneratorTypes, model.J, domain=NonNegativeIntegers)
model.l = Var(model.J, bounds = (15, 20))
model.p = Var(model.J, domain=NonNegativeIntegers)

# Define Objective
def obj(mdl):
	return sum(mdl.n[I,J]*mdl.period_hrs[J]*mdl.cost_hr_min[I]
	+(mdl.x[I,J]-(mdl.n[I,J]*mdl.min_output[I]))*mdl.period_hrs[J]*mdl.cost_incr_hr[I]
	+mdl.s[I,J]*mdl.cost_start_up[I] for I in mdl.I for J in mdl.J)
	+sum(mdl.hydro_cost_hr[HydroGeneratorTypes]*mdl.period_hrs[J]*mdl.h[HydroTypes,J]
	+mdl.hydro_cost_start_up[HydroTypes]*mdl.t[HydroTypes,J]
	for HydroTypes in mdl.HydroGeneratorTypes for J in mdl.J)
model.CostTotal = Objective(rule=obj, sense=minimize)

# Define Constraints
def demand_rule(mdl, j):
	return  (sum(mdl.x[i,j] for i in mdl.I) + sum(mdl.h[HydroTypes,j]*mdl.hydro_operating_level[HydroTypes] for HydroTypes in mdl.HydroGeneratorTypes) - mdl.p[j]) >= mdl.demand[j]
model.DemandConstraint = Constraint(model.J, rule = demand_rule)

def minimum_rule(mdl, i, j):
	return mdl.x[i,j] >= mdl.min_output[i]*mdl.n[i,j]
model.MinimumConstraint = Constraint(model.I, model.J, rule = minimum_rule)

def maximum_rule(mdl, i, j):
	return mdl.x[i,j] <= mdl.max_output[i]*mdl.n[i,j]
model.MaximumConstraint = Constraint(model.I, model.J, rule = maximum_rule)

def max_generator_rule(mdl, i, j):
	return mdl.n[i,j] <= mdl.avail_generators[i]
model.Max_generatorConstraint = Constraint(model.I, model.J, rule = max_generator_rule)

def start_up_rule(mdl, i, j):
	kk = int(j[1])-1
	if kk == 0:
		kk = len(j)
	k = 'T' + str(kk)
	return mdl.s[i,j] >= mdl.n[i,j]-mdl.n[i,k]
model.Start_up_rule = Constraint(model.I, model.J, rule = start_up_rule)

def hydro_start_up_rule(mdl, HydroTypes, j):
	kk = int(j[1])-1
	if kk == 0:
		kk = len(j)
	k = 'T' + str(kk)
	return mdl.t[HydroTypes,j] >= mdl.h[HydroTypes,j]-mdl.h[HydroTypes,k]
model.hydro_start_up_rule = Constraint(model.HydroGeneratorTypes, model.J, rule = hydro_start_up_rule)

def reserve_rule(mdl, j):
	return sum(mdl.max_output[i]*mdl.n[i,j] for i in mdl.I) >= (1.15*mdl.demand[j] - sum(mdl.hydro_operating_level[HydroTypes] for HydroTypes in mdl.HydroGeneratorTypes))
model.Reserve_rule = Constraint(model.J, rule = reserve_rule)

def hydro_reservoir_rule(mdl, j):
	kk = int(j[1])-1
	if kk == 0:
		kk = len(j)
	k = 'T' + str(kk)
	return mdl.l[j] - mdl.l[k] - (mdl.period_hrs[j]*mdl.p[j]/3000) + sum(mdl.period_hrs[j]*mdl.hydro_reservoir_reduction_hr[HydroTypes]*mdl.h[HydroTypes,j] for HydroTypes in mdl.HydroGeneratorTypes) ==0
model.Hydro_reservoir_rule = Constraint(model.J, rule = hydro_reservoir_rule)

def hydro_midnight_rule(mdl):
	return mdl.l['T1'] ==16
model.Hydro_midnight_rule = Constraint(rule = hydro_midnight_rule)

def pyomo_postprocess(options=None, instance=None, results=None):
	model.x.display()
	model.n.display()
	model.s.display()
	model.h.display()
	model.t.display()
	model.l.display()
	model.p.display()

# This is an optional code path that allows the script to be run outside of
# pyomo command-line.  For example:  python transport.py
if __name__ == '__main__':
	from pyomo.opt import SolverFactory
	# import pyomo.environ
	opt = SolverFactory("gurobi")
	instance = model.create_instance()
	results = opt.solve(instance)
# sends results to stdout
	results.write()
	print("\nDisplaying Solution\n" + '-' * 60)
	pyomo_postprocess(None, instance, results)
