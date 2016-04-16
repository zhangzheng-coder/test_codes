# Tariff Rates Example

# Components:
#   SETS_ALL_CAPS
#   VarsCamelCase
#   params_lower_case_with_underscores
#   Constraints_Words_Capitalized_With_Underscores
# SET_time_system

from __future__ import division
from pyomo.environ import *

model = ConcreteModel()

TimePeriods = ['T1', 'T2', 'T3', 'T4', 'T5']
model.TIME = Set(initialize=TimePeriods)

GeneratorTypes = ['Type1', 'Type2', 'Type3']
model.GENTYPE = Set(initialize=GeneratorTypes)

# Define the Parameters
min_output_l = {
    'Type1': 850,
    'Type2': 1250,
    'Type3': 1500
    }

model.min_output = Param(model.GENTYPE, initialize=min_output_l,
                         doc='Min Power of the Generator in MW')

max_output_l = {
    'Type1': 2000,
    'Type2': 1750,
    'Type3': 4000
    }

model.max_output = Param(model.GENTYPE, initialize=max_output_l,
                         doc='Min Power of the Generator in MW')

cost_hr_min_l = {
    'Type1': 1000,
    'Type2': 2600,
    'Type3': 3000
    }

model.cost_hr_min = Param(model.GENTYPE, initialize=cost_hr_min_l,
                          doc='Variable cost of the generation $/MW-period')

cost_incr_hr_l = {
    'Type1': 2,
    'Type2': 1.3,
    'Type3': 3
    }

model.cost_incr_hr = Param(model.GENTYPE, initialize=cost_incr_hr_l,
                           doc='Increasing cost of generation per hour')

cost_start_up_l = {
    'Type1': 2000,
    'Type2': 1000,
    'Type3': 500
    }

model.cost_start_up = Param(model.GENTYPE, initialize=cost_start_up_l,
                            doc='Startup Costs')

avail_generators_l = {
    'Type1': 12,
    'Type2': 10,
    'Type3': 5
    }

model.avail_generators = Param(model.GENTYPE, initialize=avail_generators_l,
                               doc='available units per type')

period_hrs_l = {
    'T1': 6,
    'T2': 3,
    'T3': 6,
    'T4': 3,
    'T5': 6
    }

model.period_hrs = Param(model.TIME, initialize=period_hrs_l)

demand_l = {
    'T1': 15000,
    'T2': 30000,
    'T3': 25000,
    'T4': 40000,
    'T5': 27000
    }

model.demand = Param(model.TIME, initialize=demand_l)

# Declare the variables
model.n = Var(model.I, model.J, domain=NonNegativeIntegers)
model.x = Var(model.I, model.J, domain=NonNegativeReals)
model.s = Var(model.I, model.J, domain=NonNegativeIntegers)
