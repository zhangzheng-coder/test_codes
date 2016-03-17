#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Coal and gas procurement example for SWITCH-Pyomo workshop.

# Import
from __future__ import division
from pyomo.environ import *

#Create the Abstract Model
model = AbstractModel()

#Begin the optimization model


#Define Sets from the data
#SETS_ALL_CAPS

#As convention for this problem, we will enumerate scenarios as natural numbers.
model.SCENARIOS = Set(within = PositiveIntegers)


#Define Parameters
#params_lower_case_with_underscores

#Probabilities
def Scen_Prob_Validation(mod, val, ind):
	return val>=0 and val<=1
model.probability_of_scenario = Param(model.SCENARIOS, validate = Scen_Prob_Validation, default = 0)

#Demands
model.demand_0 = Param(within = NonNegativeReals)
model.demand_s = Param(model.SCENARIOS, within = NonNegativeReals)

#Prices
model.coal_price_0 = Param(within = NonNegativeReals)
model.coal_price_s =  Param(model.SCENARIOS, within = NonNegativeReals)
model.gas_price_0 = Param(within = NonNegativeReals)
model.gas_price_s =  Param(model.SCENARIOS, within = NonNegativeReals)


#Define Variables
#VarsCamelCase

model.CoalPurchase0 = Var(domain = NonNegativeReals)
model.CoalPurchaseS = Var(model.SCENARIOS, domain = NonNegativeReals)
model.GasPurchase0 = Var(domain = NonNegativeReals)
model.GasPurchaseS = Var(model.SCENARIOS, domain = NonNegativeReals)


#Define Constraints
#Constraints_Words_Capitalized_With_Underscores

#Demands
def First_Year_Demand_Rule(mod):
	return mod.CoalPurchase0 + mod.GasPurchase0 >= mod.demand_0
model.First_Year_Demand = Constraint(rule = First_Year_Demand_Rule)

def Total_Demand_Rule(mod, s):
	return mod.CoalPurchase0 + mod.GasPurchase0 + mod.CoalPurchaseS[s] + mod.GasPurchaseS[s] == \
	mod.demand_0 + mod.demand_s[s]
model.Total_Demand = Constraint(model.SCENARIOS, rule = Total_Demand_Rule)

#Minimum and maximum consumptions of coal and gas
def Min_Coal_Consum_Rule(mod,s):
	return mod.CoalPurchase0 + mod.CoalPurchaseS[s] <= (2/3)*(mod.demand_0 + mod.demand_s[s])
model.Min_Coal_Consum = Constraint(model.SCENARIOS, rule = Min_Coal_Consum_Rule)

def Max_Coal_Consum_Rule(mod,s):
	return mod.CoalPurchase0 + mod.CoalPurchaseS[s] >= (1/3)*(mod.demand_0 + mod.demand_s[s])
model.Max_Coal_Consum = Constraint(model.SCENARIOS, rule = Max_Coal_Consum_Rule)

def Min_Gas_Consum_Rule(mod,s):
	return mod.GasPurchase0 + mod.GasPurchaseS[s] <= (2/3)*(mod.demand_0 + mod.demand_s[s])
model.Min_Gas_Consum = Constraint(model.SCENARIOS, rule = Min_Gas_Consum_Rule)

def Max_Gas_Consum_Rule(mod,s):
	return mod.GasPurchase0 + mod.GasPurchaseS[s] >= (1/3)*(mod.demand_0 + mod.demand_s[s])
model.Max_Gas_Consum = Constraint(model.SCENARIOS, rule = Max_Gas_Consum_Rule)


#Define Objective Function
def Total_Cost_Rule(mod):
	return (mod.CoalPurchase0 * mod.coal_price_0 + mod.GasPurchase0 * mod.gas_price_0 +
			sum(mod.probability_of_scenario[s] *
			(mod.CoalPurchaseS[s]*mod.coal_price_s[s] + mod.GasPurchaseS[s]*mod.gas_price_s[s])
			for s in mod.SCENARIOS))
model.TotalCost = Objective(rule=Total_Cost_Rule, sense=minimize,
				  			doc='Define objective function')


def pyomo_postprocess(options=None, instance=None, results=None):
	model.CoalPurchaseS.display()
	model.GasPurchaseS.display()

# This is an optional code path that allows the script to be run outside of
# pyomo command-line.  For example:  python transport.py
# This emulates what the pyomo command-line tools does
if __name__ == '__main__':
	from pyomo.opt import SolverFactory
	# import pyomo.environ
	opt = SolverFactory("gurobi")
	model = model.create_instance('CoalGasProcurementExample.dat')
	results = opt.solve(model, tee=True)
# sends results to stdout
	results.write()
	print("\nDisplaying Solution\n" + '-' * 60)
	pyomo_postprocess(None, None, results)
