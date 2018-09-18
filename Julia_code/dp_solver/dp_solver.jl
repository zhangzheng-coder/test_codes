module dp_solver

#The module exports the defined types and the dp related functions
#Currently the access to the auxiliary function definitions is not allowed. 

export DPmodel, DPsolution, DPsimulation
export dp_solve, dp_simulate

import FastGaussQuadrature
import Optim
import Distributions

#definition of the types 

"""

    DPmodel(x -> U(x),x-> M(x), β,(\\mu, \\sigma, n),(a,b),(c,d),k0,T)

The type DP model is used to store the information of a one-state, one-control stochastic dynamic programming problem (SDP)
with a random shock normally distributed. The solution process assumes that in every function the control is the first argument
in the functions. 

The problem structure is as follows: 

V^{t}(c_t, s_t) = max U(c_t, s_t) + \beta * V^{t-1}(M(c_t, s_t, \epsilon))

Where: 
U():        payoff equation 
M():        equation of motion 
\beta:      discount factor
c_t:        control variable
s_t:        state variable
\epsilon:   random shock realization of an i.i.d random variable. 
V^{t}():    value function in period t

Solving numerically the SDP problem requires bounds on the control and state variables defined as follows:
bounds on the control:  [a, b]
bounds on the state:    [c, d]

Also, the problem must have a frontier condition at time maximum simulation time.
k_0:        initial_state
T:          time horizon length 

# Arguments
*  `payoff_eq::Function`: Payoff equation.
*  `eq_motion::Function`: equation of motion.   
*  `β::Float64`: discount factor.
*  `dist_data::Tuple{Distributions.Normal,Int}`: Data of the random shock specified by 
                                                 Distributions.Normal(\mu, \sigma, number of interpolation nodes).
                                                 for details on the types included in Distributions refer to the 
                                                 module's documentation.
*  `bounds_control::Tuple{Float64,Float64}`: Bounds on the control variable. 
*  `bounds_state::Tuple{Float64,Float64}`: Bounds on the state variable.
*  `ini_state::Float64)`: Initial condition of the simulation, end condition of the problem.
*  `T::Int`: Length of the time horizon.

"""
type DPmodel 
    payoff_eq::Function
    eq_motion::Function
    β::Float64
    dist_data::Tuple{Distributions.Normal,Int}
    #dist_data::Tuple{Float64,Float64,Int}
    bounds_control::Tuple{Float64,Float64}
    bounds_state::Tuple{Float64,Float64}
    ini_state::Float64
    T::Int    
    
end


"""
    DPsolution(model,Vs,Ps)

The type DPsolution stores the result of one-state, one-control stochastic dynamic programming problem (SDP)
with a random shock normally distributed. 

The problem structure is as follows: 

V^{t}(c_t, s_t) = max U(c_t, s_t) + \beta * V^{t-1}(M(c_t, s_t, \epsilon)) 

The type contains the model that corresponds to the solution. 

The results of the DP are two arrays V_s and P_s that contain the value function and policy function approximations 
respectively for each period t. 

# Arguments
* `model::DPmodel`: Model data and structure.
* `V_s::Array`: Array with the value function approximations.
* `P_s::Array`: Array with the policy function approximations. 

"""
type DPsolution
    model::DPmodel
    V_s::Array
    P_s::Array
end

"""
    DPsimulation(s_dp,k_dp)

The type DPsolution stores the result of simulating a one-state, one-control stochastic dynamic programming problem (SDP)
with a random shock normally distributed which solution is stored in a variable of the type DPsolution.

The data stored corresponds to the simulation in the time domain of the state and control variables of the SDP problem. 

# Arguments 
* `state_variable::Matrix`: Matrix size [T x mc] storing the results of mc montecarlo simulations and T periods for s_t.
* `control_variable::Matrix`: Matrix size [T x mc] storing the results of mc montecarlo simulations and T periods for c_t.

"""
type DPsimulation
    control_variable::Matrix
    state_variable::Matrix
end

#The following set of function definitions are auxiliary functions required to solve and stochastic dynamic programming problem,
#namely the functions are used to define the following:
#           - Gauss - Hermite approximator of a N(\mu, \sigma) randomly distributed shock
#           - Chebyshev polynomial approximator of the value function.
#               + Calculation of Chebyshev nodes
#               + Chebyschev recurrence function 
#               + Chebyschev basis function
#               + Chebyschev interpolation matrix
#               + Function approximator. 


"""
    gauss_approx(data)

# Arguments 
*`data::tuple` :Tuple that contains the desired normal distribution moments and the degree of the approximation

# Returns
* `weights_adj::Float64` : Weights of the approximation adjusted for the normal distribution. 
* `nodes_adj::Float64`   : Nodes (samples of the support) of the approximation adjusted for the normal distribution.   

"""
function gauss_approx(dist_data::Tuple{Distributions.Normal,Int})

    nodes, weights = FastGaussQuadrature.gausshermite(dist_data[2])
    nodes_adj = sqrt(2.) .* dist_data[1].σ .* nodes .+ dist_data[1].μ
    weights_adj = weights ./ sqrt(π)
    return weights_adj, nodes_adj
end

"""
chebyshev_nodes calculation

# Arguments 
*`n::Int` : Number of nodes required
*`bounds::Tuple`: Bounds of approximation range. 

# Returns 
*`##::Array{Float64,1}`: Array containing N Chebyschev nodes
"""
function chebyshev_nodes(n::Int,bounds::Tuple)
    return [(bounds[1]+bounds[2])/2+(bounds[2]-bounds[1])/2*cos((n-i+0.5)/n*π) for i = 1:n]
end

"""
Chebyshev polynomials of the first kind recurrent generators. This function is used later in the 
basis function. Usually the approximator is not used 

# Arguments
*`x::Number`: Argument of the polynomial to be evaluated 
*`n:Int` : Polynomial degree
"""
function chebyshev_recurrence(x::Number,n::Int)
    if n == 0
        return 1
        elseif n ==1
        return x
    else
        return 2*x*chebyshev_recurrence(x,n-1)-chebyshev_recurrence(x,n-2)
    end
end


"""
Chebyshev basis function definition. Doesn't require a return because it runs ```chebyshev_recurrence```

# Arguments 
*`x::Number`: Argument to be evaluated in the basis
*`n:Int` : Polynomial degree
*`bounds::Tuple`: Bounds of approximation range. 
"""
function chebyshev_basis(x::Number,n::Int,bounds::Tuple)
    z = 2*(x-bounds[1])/(bounds[2]-bounds[1])-1
    chebyshev_recurrence(z,n-1)
end

"""
Calculation of the interpolation matrix for function approximation. 
This function estimates the interpolation function for any generic basis function 
and applicable nodes. 

This module only has Chebyschev polynomial approximators available. 

# Arguments 
*`f_basis::Function` : Applicable basis function
*`nodes_adj::Float64`   : Nodes for the approximation
*`bounds::Tuple`: Bounds of approximation range.

#Returns
*`Φ::Matrix{Float64,2}` : Interpolation Matrix   
"""
function interpolation_matrix(f_basis::Function, nodes::Array{Float64,1}, bounds::Tuple)
    n = length(nodes)
    Φ = [f_basis(nodes[i],j,bounds) for i in 1:n, j in 1:n]
    return Φ
end

"""
The function returns a function approximation based on a particular basis function, interpolation nodes and matrix. 
The implementation is general for any function approximation method. In this code the only available is Chebyschev 
polynomials 

# Arguments
*`V_func::Function` : function to be approximated 
*`B_func::Function` : Basis function
*`interpolation_nodes::Array{Float64,1}` :
*`Φ::Matrix{Float64,2}` : Interpolation Matrix 
*`bounds::Tuple`: Bounds of approximation range.
"""
function f_approx(V_func::Function, B_func::Function, interpolation_nodes::Array{Float64,1}, Φ::Matrix, bounds::Tuple)
    y = V_func.(interpolation_nodes)
    c = Φ\y
return x -> begin 
                res = 0.0
                for i = 1:length(interpolation_nodes)
                    res += c[i]*B_func(x,i,bounds)
                end
            return res
            end
end

# This portion of the code contains the main routines to solve and simulate the SDP problem. It contains two functions
#   - dp_solve: Application of value function iteration 

"""
The main solution algorith of the stochastic dynamic programming problem (SDP) using backward time recursion. 

# Arguments 
*`model::DPmodel`: Information of and SDP problem 
*`cheb_nodes_number::Int = 5`: Number of Chebyschev nodes used for the approximation, default 5. 

# Returns 
*`result:DPsolution`: Solution of the SDP problem. Contains a copy of the original problem 
                      and 2 vectors size T with the value functions and policy functions. 
"""

function dp_solve(model::DPmodel, cheb_nodes_number::Int = 5)

    #Algorithm initialization. 
    Ps = Array{Function, 1}(model.T)
    Vs = Array{Function, 1}(model.T+1);
    Vs[model.T + 1] = k -> 0.

    #Calculation of the estimations for Random Shock and Value Function. 
    shock_approx = gauss_approx(model.dist_data)
    print("Shock appoximation done\n")
    interpolation_nodes = chebyshev_nodes(cheb_nodes_number, model.bounds_control)
    print("Interpolation nodes done\n")
    Φ = interpolation_matrix(chebyshev_basis, interpolation_nodes, model.bounds_control);
    print("Interpolation Matrix done\n")
    
    print("starting main loop\n")
    for t=model.T:-1:1
    println(t)
    P = s_t -> begin 
        f_obj = c_t -> begin 
            continuation_value = 0.0
            for i in 1:model.dist_data[2]
                continuation_value += shock_approx[1][i]*model.β*Vs[t+1](model.eq_motion(c_t,s_t,shock_approx[2][i]))
            end
            return model.payoff_eq(c_t,s_t)+continuation_value
        end
        r = Optim.optimize(c_t -> -f_obj(c_t),model.bounds_state[1],model.bounds_state[2])
        if !Optim.converged(r)
            error("Didn't converge.")
        end
        c_opt = Optim.minimizer(r)[1]
        return c_opt
    end

    Ps[t] = P
    V = s_t -> begin 
        f_obj = c_t -> begin 
            continuation_value = 0.0
            for i in 1:model.dist_data[2]
                continuation_value += shock_approx[1][i]*model.β*Vs[t+1](model.eq_motion(c_t,s_t,shock_approx[2][i]))
            end
            return model.payoff_eq(c_t,s_t) + continuation_value
        end
            c_opt = Ps[t](s_t)
            return f_obj(c_opt)
    end
    Vs[t] = f_approx(V, chebyshev_basis, interpolation_nodes, Φ, model.bounds_control)   
    
    end
    result = DPsolution(model,Vs,Ps)
    return result
end    

"""
MonteCarlo Simulation of the SDP problem solution. 

# Arguments 
*`solution:DPsolution`: 
*`mc::Int=50`: Number of MonteCarlo iteration   

"""
function dp_simulate(solution::DPsolution, mc::Int=50)
    c_dp = zeros(mc,solution.model.T)
    s_dp = zeros(mc,solution.model.T)

    s_dp[:,1] = solution.model.ini_state

    d = solution.model.dist_data[1]

    for i in 1:mc
        for t = 1:solution.model.T
            ϵ=Distributions.rand(d)
            c_dp[i,t] = solution.P_s[t](s_dp[i,t])
            if t < solution.model.T
                s_dp[i,t+1] =  solution.model.eq_motion(c_dp[i,t],s_dp[i,t],ϵ)
            end
        end
    end
    result = DPsimulation(c_dp,s_dp)
    return result
end

end