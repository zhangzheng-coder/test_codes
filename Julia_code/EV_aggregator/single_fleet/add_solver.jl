#Use the current directory to store the deps.jl file

depsfile = joinpath(dirname(@__FILE__),"julia_cplex/deps.jl")
path_to_bin = joinpath(dirname(@__FILE__),"cplex/bin/x86-64_linux/")
if isfile(depsfile)
    rm(depsfile)
end

#Write the deps.jl file
function write_depsfile(path)
    open(depsfile,"w") do f
        print(f,"const libcplex = ")
        show(f, path) # print with backslashes excaped on windows
        println(f)
    end
end

cpxvers = ["1263"]

libnames = String["cplex"]
for v in reverse(cpxvers)
    push!(libnames, join([path_to_bin,"libcplex$v.so"]))
end

write_depsfile(libnames[2])
