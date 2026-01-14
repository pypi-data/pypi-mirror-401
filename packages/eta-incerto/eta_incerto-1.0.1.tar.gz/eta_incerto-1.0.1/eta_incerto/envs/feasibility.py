import logging
from pathlib import Path

import gurobipy as gp
from gurobipy import GRB

log = logging.getLogger(__name__)

# Path to your LP file
lp_file = "C:/Git/eta-incerto/20250908_142307.lp"
# Create model and read LP file
model = gp.read(lp_file)

# Optimize the model
model.optimize()

# Write IIS to a file for inspection
out_dir = Path.cwd()
out_dir.mkdir(parents=True, exist_ok=True)
iis_file = out_dir / "20250908_142307.ilp"
sol_file = out_dir / "20250908_142307.sol"


if model.status == GRB.INF_OR_UNBD:
    log.warning("Model is infeasible or unbounded. Computing IIS...")
    model.computeIIS()
    model.write(str(iis_file))

elif model.status == GRB.INFEASIBLE:
    log.warning("Model infeasible. Computing IIS...")
    model.computeIIS()
    model.write(str(iis_file))

elif model.status == GRB.OPTIMAL:
    log.info("Model feasible and optimal. Obj = %f", model.objVal)

elif model.status == GRB.INTERRUPTED:
    log.warning("Solve interrupted.")
    if model.SolCount > 0:
        log.info("Best incumbent: %f, Best bound: %f", model.objVal, model.ObjBound)
        log.info("MIP gap: %f%%", 100 * (model.objVal - model.ObjBound) / abs(model.objVal))
        model.write(str(sol_file))
        log.info("Partial solution written to %s", sol_file)
    else:
        log.info("No feasible solutions found before interruption.")
