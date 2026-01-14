from __future__ import annotations

# ---- SYSTEM ----
SYSTEM_REGISTRY: dict[str, type[type, type]] = {}


def register_system(
    name: str,
    static_data_cls: type | None = None,
    investment_data_cls: type | None = None,
    distribution_data_cls: type | None = None,
):
    def decorator(cls):
        SYSTEM_REGISTRY[name] = (cls, static_data_cls, investment_data_cls, distribution_data_cls)
        return cls

    return decorator


def get_system(name: str):
    if name not in SYSTEM_REGISTRY:
        raise ValueError(f"Unknown system: {name}")
    return SYSTEM_REGISTRY[name]


# ---- ENVIRONMENT ----
ENVIRONMENT = {"stochastic": ("stochastic"), "robust": ("robust"), "regret": ("regret"), "antifragile": ("antifragile")}

# ---- REGISTRY MAP ----
REGISTRY_MAP = {"environement": ENVIRONMENT}

DIKT_PATH = {"environment": "eta_incerto.envs"}
