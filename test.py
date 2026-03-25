def compte_a_rebourd(n):
    if n <= 0:
        print("decollage")
        return

    else:
        print(n)
        compte_a_rebourd(n - 1)


compte_a_rebourd(3)
