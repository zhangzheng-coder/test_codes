# Multiple fleet optimizer

## Model description and assumptions
The aggregator model is implemented assuming that it has centralized control over a fleet of Electric Vehicles. The electric vehicles are dispatched (charged or discharged) depending on the flexibility requirements of the electric grid. From the commercial perspective, the aggregator is assumed to be a price taker and unable to affect energy prices.

In order to model the requirements of the grid a representative price profile for California is used. The price profile is obtained from a system simulation of the WECC for year 2024 under 3 different scenarios. 

- Case0 - State-wide Electric Vehicle Fleet is small and has no effect on the prices. 
- Case1 - State-wide Electric Vehicle Fleet is large and unmanaged i.e., no smart charging. 
- Case2 - State-wide Electric Vehicle Fleet is large and operated with smart charging.

The mathematical model of the aggregator is as follows:

![Math Model](https://github.com/jdlara-berkeley/Julia_testcodes/blob/master/aggregator_model/Multiple_fleet/multi_fleet.png)  

