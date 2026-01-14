# ---- OPTIONAL: ALGORITHMS ----
ALGORITHMS = {"AGEMOEA": "age", "AGEMOEA2": "age2", "SMSEMOA": "sms"}

# ---- SAMPLING ----
SAMPLING = {
    "lhs": ("LatinHypercubeSampling", "LHS"),
    "rnd": ("FloatRandomSampling", "BinaryRandomSampling", "IntegerRandomSampling", "PermutationRandomSampling"),
}

# ---- SELECTION ----
SELECTION = {
    "rnd": ("RandomSelection"),
    "tournament": ("TournamentSelection"),
}

# ---- CROSSOVER ----
CROSSOVER = {
    "binx": ("BinomialCrossover", "BX"),
    "dex": ("DEX"),
    "erx": ("EdgeRecombinationCrossover", "ERX"),
    "expx": ("ExponentialCrossover"),
    "hux": ("HalfUniformCrossover", "HUX"),
    "nox": ("NoCrossover"),
    "ox": ("OrderCrossover"),
    "pcx": ("ParentCentricCrossover", "PCX"),
    "pntx": ("PointCrossover", "SinglePointCrossover", "TwoPointCrossover"),
    "sbx": ("SimulatedBinaryCrossover", "SBX"),
    "spx": ("SPX"),
    "ux": ("UniformCrossover", "UX"),
}

# ---- MUTATION ----
MUTATION = {
    "bitflip": ("BitflipMutation", "BFM"),
    "gauss": ("GaussianMutation", "GM"),
    "inversion": ("InversionMutation"),
    "nom": ("NoMutation"),
    "pm": ("PolynomialMutation", "PM"),
    "rm": ("ChoiceRandomMutation"),
}

# ---- REGISTRY MAP ----
REGISTRY_MAP = {
    "algorithm": ALGORITHMS,
    "sampling": SAMPLING,
    "selection": SELECTION,
    "crossover": CROSSOVER,
    "mutation": MUTATION,
}

DIKT_PATH = {"algorithm": "pymoo.algorithms.moo", "parameters": "pymoo.operators"}
