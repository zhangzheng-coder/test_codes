```
This code shows how use JuMP to solve a one dimensional, user defined non-linear equation. 
For the example the equation is x^2 - sqrt(x) = 0
```

using JuMP
using Ipopt
solver = IpoptSolver()

function foo(x)
    return x^2 - sqrt(x)
end

m = Model(solver = solver)

y = @variable(m, y >= 0.01, start = 0.6) #give a better initial guess to avoid bad solutions. 
ϵ = @variable(m, ϵ)

JuMP.register(m, :foo, 1, foo, autodiff=true)

@NLconstraint(m, foo(y) == ϵ)

@objective(m, Min, ϵ^2)

solve(m)

getobjectivevalue(m)

getvalue(y)