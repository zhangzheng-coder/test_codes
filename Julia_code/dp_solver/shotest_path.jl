M = [0    60     9999  40   9999  9999; 
    60    0       30   9999 40    9999;
    9999  30      0    9999 9999  10;
    40    9999    9999 0    15    9999;
    9999  40      9999 15   0     30;
    9999  9999    10   9999 30    0 ]


function bellman_ford(M, o::Int)

    nodes = length(M[1,:])

    v = 9999*ones(nodes)
    p = nothing
    v[o] = 0;
    for i in 1:nodes-1
        println(v)
        for k in 1:nodes
            v(i) = min(M[i,:])           
        end
    end




end