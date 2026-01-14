from numpy import full


def nsga2_tournament(pop, p, **kwargs):
    n_tournaments, n_competitors = p.shape
    s = full(n_tournaments, -1, dtype=int)

    for i in range(n_tournaments):
        a, b = p[i]

        rank_a, rank_b = pop[a].get("rank"), pop[b].get("rank")
        crowd_a, crowd_b = pop[a].get("crowding"), pop[b].get("crowding")

        # 1) check rank
        if rank_a < rank_b:
            s[i] = a
        elif rank_a > rank_b:
            s[i] = b
        # 2) tie: check crowding
        elif crowd_a > crowd_b:
            s[i] = a
        else:
            s[i] = b

    return s
