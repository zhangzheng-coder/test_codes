# Single fleet optimizer

## Model description and assumptions
The aggregator model is implemented assuming that it has centralized control over a fleet of Electric Vehicles. The electric vehicles are dispatched (charged or discharged) depending on the flexibility requirements of the electric grid. From the commercial perspective, the aggregator is assumed to be a price taker and unable to affect energy prices.

The requirements of the grid for flexibility are normally reflected in the wholesale energy price, in the model the price is used as a control signal. The objective function includes the charging and discharging signals that manage the fleet and slack variables to guarantee feasibility when the changes in energy available in the fleet are larger than the power available. The slack variables are multiplied by a penalty to avoid their use unless is strictly necessary. 

The optimization objective function is maximized in order to obtain the largest profits from energy arbitraging in the grid subject to engineering constraints. For the proposed model the engineering constraints assume that all the cars in the each individual fleet are controlled at the same time. The first set of constraints limit the charging and discharging power of the fleet to the maximum power of the charger  multiplied by the factor  that represents the fleet availability. The slack terms are added to this equation in order to provide the aggregator with the capability to account for changes in the SoC related to fleet availability and not to energy accounting. The equations also contain the control variables  used to prevent simultaneous charging and discharging of the fleet. 


The mathematical model of the aggregator is as follows: 

![Model_multi](https://github.com/jdlara-berkeley/Julia_testcodes/blob/master/aggregator_model/Multiple_fleet/multi_fleet.png)

In order to model the requirements of the grid a representative price profile for California is used. The price profile is obtained from a system simulation of the WECC for year 2024 under 3 different scenarios. 

- Case0 - State-wide Electric Vehicle Fleet is small and has no effect on the prices. 
- Case1 - State-wide Electric Vehicle Fleet is large and unmanaged i.e., no smart charging. 
- Case2 - State-wide Electric Vehicle Fleet is large and operated with smart charging.