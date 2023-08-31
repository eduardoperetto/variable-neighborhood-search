using JuMP
using GLPK
import Formatting

# Define the edges and parameters
edges = [
    [1, 2], [1, 10], [1, 9], [1, 3], [1, 8],
    [2, 11], [2, 3], [3, 11], [3, 4], [4, 12],
    [4, 5], [5, 12], [5, 6], [6, 12], [6, 13],
    [6, 7], [7, 13], [7, 14], [7, 8], [8, 9],
    [8, 14], [9, 10], [10, 11], [10, 13],
    [10, 14], [11, 12], [11, 13], [12, 13],
    [13, 14]
]
verticesNumber = 14
edgesNumber = 29
k = 3
p = 1

# Model init
m = Model()
set_optimizer(m, GLPK.Optimizer);

# Decision variables
@variable(m, x[1:verticesNumber], Bin) # v selected 
@variable(m, y[1:verticesNumber], Bin) # v to be removed

# Goal: Minimize the k-related subset size
@objective(m, Min, sum(x))

# Constraints

# Limit the number of removed vertices to p
@constraint(m, sum(y) == p)

# A vertice be removed and selected at the same time
@constraint(m, [v in verticesNumber], x[v] + y[v] <= 1)

# Subgraph formed by selected vertices must be at least k-related


@time begin
    # Solve
    optimize!(m)
end

# Results
println("Objective value: ", objective_value(m))
println("Selected Vertices:")
for v in 1:verticesNumber
    if value(x[v]) > 0.5
        println(v)
    end
end





