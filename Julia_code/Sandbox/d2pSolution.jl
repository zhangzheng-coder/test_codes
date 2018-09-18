function d2pSolution(a,b,c)
    DeltaSq = b*b - 4*a*c

# This condition takes care of the cases with solutions that include imaginary numbers
    if b == 0
        if c > 0
            r1 = sqrt(-complex(c/a))
            r2 = -1*sqrt(-complex(c/a))
        else
            r1 = sqrt(-c/a)
            r2 = -1*sqrt(-c/a)
        end

    elseif DeltaSq < 0 
        r1 = (-b + im*(sqrt(4*a*c-b*b)))/(2*a)
        r2 = (-b - im*(sqrt(4*a*c-b*b)))/(2*a)

# This condition takes care of loss of precision problems.         
    elseif DeltaSq > 0        
        if b >= 0
            r1 = -2*c/(b+sqrt(DeltaSq))
            r2 = (-b - (sqrt(DeltaSq)))/(2*a)
        elseif b < 0
            r1 = (-b + (sqrt(DeltaSq)))/(2*a)
            r2 = -2*c/(b-sqrt(DeltaSq))
        end
    end
    
    return r1, r2
end