#Packages
using JuMP
using DataFrames


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
    agg = Model(solver=GurobiSolver(Presolve=1, InfUnbdInfo=1, DualReductions=0))
end  

prof_type = "multiple"
#data 
time = 8760  #[hrs]
data_p = readtable(joinpath(dirname(@__FILE__),"Price_profiles",ARGS[1]))
data_c = readtable(joinpath(dirname(@__FILE__),"car_profiles/car_profile_$(prof_type).csv"))
ini = 1
prices = convert(Array,data_p[ini:(ini+time-1),end])
println(size(prices))
car_availability = convert(Array,data_c)
fleet_types = size(car_availability)[2]
fleet_size = ones(fleet_types)*1000

#Parameters
k_SOC = car_availability #[0-1] 
k_power = car_availability #[0-1]
contract_limit = parse(Float64,ARGS[3]) #[%]
bat_size = 30 #[kWh], based on the Nissan Leaf 
charger_power = 7.2 #[kW], based on a 30 Amp Charger
eff_in = 0.85 #[%]
eff_out = 0.78 #[%]
P_max_in = repmat(fleet_size',time,1).*(charger_power*k_power[1:time, 1:fleet_types]) #[kW]
P_max_out = repmat(fleet_size',time,1).*(charger_power*k_power[1:time, 1:fleet_types]) #[kW]
SOC_max = bat_size*repmat(fleet_size',time,1).*k_SOC[1:time, 1:fleet_types] #[kWh]
SOC_min = bat_size*(1-contract_limit)*repmat(fleet_size',time,1).*k_SOC[1:time, 1:fleet_types] #[kWh]
SOC_ini = fleet_size.*bat_size #[kWh] 

@variables agg begin
    P_in[1:time, 1:fleet_types] >= 0
    P_out[1:time, 1:fleet_types] >= 0
    P_in_slack[1:time, 1:fleet_types] >= 0
    P_out_slack[1:time, 1:fleet_types] >= 0
    SOC_min[t, f] <= SOC[t = 1:time, f = 1:fleet_types] <= SOC_max[t, f]
    control[t = 1:time, f = 1:fleet_types],  Bin
end 

@constraints agg begin
    0 <= sum(sum(prices[t]/1000*(P_out[t,f] - P_in[t,f]) for t in 1:time) for f in 1:fleet_types)
    P_in[t = 1:time, f = 1:fleet_types] .<=  P_max_in[t,f].*control[t, f] 
    P_out[t = 1:time, f = 1:fleet_types] .<=  P_max_in[t,f].*(ones(time, fleet_types)-control[1:time, f])
    SOC[1, 1:fleet_types] .== SOC_ini[1:fleet_types] + (eff_in)*P_in[1, 1:fleet_types] - (1/eff_out)*P_out[1, 1:fleet_types] + (P_in_slack[t,f] - P_out_slack[t,f])
    SOC[2:time, 1:fleet_types] .== SOC[1:time-1, 1:fleet_types] + (eff_in)*P_in[2:time, 1:fleet_types] - (1/eff_out)*P_out[2:time, 1:fleet_types]
    #SOC[1:time, 1:fleet_types] .== (eff_in)*P_in[1:time, 1:fleet_types] - (1/eff_out)*P_out[1:time, 1:fleet_types]
end

@objective(agg, Max, sum(sum(prices[t]/1000*(P_out[t,f] - P_in[t,f]) for t in 1:time) for f in 1:fleet_types) - 
                     sum(sum(1000*(P_out_slack[t,f] + P_in_slack[t,f]) for t in 1:time) for f in 1:fleet_types));

writeLP(agg, "lp_file.lp", genericnames=false)
solve(agg)

writedlm(joinpath(dirname(@__FILE__),"results_multi/$(ARGS[2])P_out_$(ARGS[4])_$(prof_type)_$(contract_limit*100).txt"), getvalue(P_out))
writedlm(joinpath(dirname(@__FILE__),"results_multi/$(ARGS[2])P_in_$(ARGS[4])_$(prof_type)_$(contract_limit*100).txt"), getvalue(P_in))
writedlm(joinpath(dirname(@__FILE__),"results_multi/$(ARGS[2])SOC_$(ARGS[4])_$(prof_type)_$(contract_limit*100).txt"), getvalue(SOC))

writedlm(joinpath(dirname(@__FILE__),"results_multi/slack/$(ARGS[2])P_out_slack_$(ARGS[4])_$(prof_type)_$(contract_limit*100).txt"), getvalue(P_out_slack))
writedlm(joinpath(dirname(@__FILE__),"results_multi/slack/$(ARGS[2])P_in_slack_$(ARGS[4])_$(prof_type)_$(contract_limit*100).txt"), getvalue(P_in_slack))
