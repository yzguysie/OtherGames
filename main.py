game = input("What would you like to play? (agar, pool, fidget, sorting, or evolve): ")
if game.lower() == "agar" or game.lower() == "a":
    import agar
elif game.lower() == "fidget" or game.lower() == "f": 
    import fidget
elif game.lower() == "evolve" or game.lower() == "e":
    import evolve
elif game.lower() == "pool" or game.lower() == "p":
    import pool
elif game.lower() == "sorting" or game.lower() == "sort" or game.lower() == "s":
    import sorting