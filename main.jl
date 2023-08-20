using JuMP
using GLPK
using Formatting

# Model init
m = Model(optimizer = GLPK.Optimizer)

# Decision variables
@variable(m, x[v in V], Bin)  # v is important to be removed
@variable(m, y[v in V], Bin)  # v will be removed

# Goal: Minimize the k-related subset size
@objective(m, Min, sum(y[v] for v in V))

# Constraints
@constraint(m, [v in V], x[v] + y[v] <= 1) # Each vertice are important or will be removed
@constraint(m, sum(x[v] for v in V) <= p) # Maximum people to be removed   

for S in subsets(V) # minimum degree k-related
  if length(S) > 0
      @constraint(m, sum(y[u] * (1 - x[v]) for u in V for v in S if u == v) >= k * length(S))
  end
end

# Solve
optimize!(m)

# Results 
