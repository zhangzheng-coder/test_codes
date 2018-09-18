
include("dp_solver.jl")
using dp_solver
using Plots
using Distributions
gr() 

# Problem Data
T = 100 # Time horizon
β = 0.97 # Discount factor
γ = 0.1 # Capital deprecation rate
α = 0.3 # Output elasticity of capital
k0 = 1. # Initial capital stock
μ = 1. # Mean of the shock
σ = 0.1 # STD of the shock
distribution = Normal(μ, σ)
s_bounds = (0,1) #bounds for the savings
k_bounds = (0,4) #bounds for the capital 
dist_data = (distribution,3) #Data of the shock 
n_mc = 1000 #number of montecarlo runs

#Problem functions 
U(S_t, k_t) = log((1-S_t)*k_t^α) #Payoff function
M(S_t, k_t, ϵ) = (1-γ)*k_t +ϵ*S_t*k_t^α #Equation of motion 

#Step 1: Create Model of the problem from the data. 
model = DPmodel(U,M,β,dist_data,k_bounds,s_bounds,k0,T)

#Step 2: Calculate the solution to the DP problem 
solution = dp_solve(model,15)

#Step 3: Perform the simulations 
simulation = dp_simulate(solution, n_mc)

#Step 4: Produce the plots with the results 
plot(vec(mean(simulation.state_variable,1)), label = "Average of the state")
plot!([quantile(simulation.state_variable[:,t],0.05) for t=1:100],label="5% quantile")
plot!([quantile(simulation.state_variable[:,t],0.95) for t=1:100],label="95% quantile")
plot!(  xlims = (0, 100), 
        xlabel = "Time [years]",    
        ylims = (0, 4), 
        ylabel = "s_t value")
savefig("plot_state")
plot(vec(mean(simulation.control_variable,1)), label = "control")
plot!(  xlims = (0, 100), 
        xlabel = "Time [years]",    
        ylims = (0, 1), 
        ylabel = "c_t value")
savefig("plot_control")
plot(simulation.state_variable[1,:], color=:black, alpha = 0.2, leg=false)
plot!(xlims = (0, 100), ylims = (0, 4))
for i = 2:n_mc
    plot!(simulation.state_variable[i,:], color=:black, alpha = 0.2, leg=false)
end
plot!(vec(mean(simulation.state_variable,1)), color=:red, label = "average of the state")
plot!(  xlims = (0, 100), 
        xlabel = "time [years]",    
        ylims = (0, 4), 
        ylabel = "s_t value")
savefig("plot_mc_state")