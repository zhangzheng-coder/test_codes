using OrdinaryDiffEq, Plots

#Constants
const g = 9.81
L = 1.0

#Initial Conditions
u₀ = [0,π/2]
tspan = (0.0,6.3)

struct pendulum 
    L::Float64
    g::Float64
    model::Function
    function pendulum(L,g) 
      dynamics =  (du, u, p, t) -> begin
                θ  = u[1]
                dθ = u[2]
                du[1] = dθ
                du[2] = -((g + p) /L)*sin(θ)                   
        end
        new(L,g,dynamics)
    end
end 

x = pendulum(L,g)

#Pass to solvers
prob = ODEProblem(x.model,u₀, tspan, 0.01)
sol = solve(prob,Tsit5())

#Plot
plot(sol,linewidth=2,title ="Simple Pendulum Problem", xaxis = "Time", yaxis = "Height", label = ["Theta","dTheta"])