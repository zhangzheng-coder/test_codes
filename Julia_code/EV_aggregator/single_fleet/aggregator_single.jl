#Packages
using JuMP
using DataFrames
using CSV

if is_linux()
    cplex_path = "../julia_cplex"
    push!(LOAD_PATH, cplex_path)
    using CPLEX
end 

if is_apple()
    using Gurobi
end    

# JuMP model 
if is_linux()
    agg = Model(solver=CplexSolver(CPX_PARAM_EPGAP=1e-04))
end 

if is_apple()
    agg = Model(solver=GurobiSolver(Presolve=1, InfUnbdInfo=1))
end  

#data 
time = 8750 #[hrs]
data_p = readtable(joinpath(dirname(@__FILE__),ARGS[1]));
data_c = readtable(joinpath(dirname(@__FILE__),"car_profile.csv"));
ini = 1;
prices = convert(Array,data_p[ini:(ini+time-1),end]);
car = convert(Array,data_c);

#Parameters
availability = car #[0-1]
contract_limit = 0.8 #[%]
fleet = 1000000 #[units]
bat_size = 30 #[kWh], based on the Nissan Leaf 
charger_power = 7.2 #[kW], based on a 30 Amp Charger
eff_in = 0.85 #[%]
eff_out = 0.78 #[%]
k_power = availability #[0-1]
P_max_in = fleet*charger_power #[kW]
P_max_out = fleet*charger_power #[kW]
SOC_max = fleet*bat_size #[kWh]
SOC_min = fleet*bat_size*(1-contract_limit) #[kWh]
SOC_ini = SOC_max #[kWh] 
k_SOC = availability #[0-1] 

@variables agg begin 
    P_in[t=1:time] >= 0
    P_out[t=1:time] >= 0
    SOC_min*k_SOC[t] <= SOC[t = 1:time] <= SOC_max*k_SOC[t]
    control[t=1:time], Bin
end 

@constraints agg begin
    0 <= sum(prices[t]/1000*(P_out[t] - P_in[t]) for t in 1:time)
    P_in[1:time] .<=  P_max_in*k_power[1:time].*control[1:time]
    P_out[1:time] .<=  P_max_out*k_power[1:time].*(1-control[1:time])
    SOC[1] == SOC_ini + (eff_in)*P_in[1] - (1/eff_out)*P_out[1]
    SOC[2:time] .== SOC[1:time-1] + (eff_in)*P_in[2:time] - (1/eff_out)*P_out[2:time]
end

@objective(agg, Max, sum(prices[t]/1000*(P_out[t] - P_in[t]) for t in 1:time));

solve(agg)

writedlm(joinpath(dirname(@__FILE__),"results/P_out$(ARGS[2]).txt"), getvalue(P_out))
writedlm(joinpath(dirname(@__FILE__),"results/P_in$(ARGS[2]).txt"), getvalue(P_in))
writedlm(joinpath(dirname(@__FILE__),"results/SOC$(ARGS[2]).txt"), getvalue(SOC))

