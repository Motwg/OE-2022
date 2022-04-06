def bounce(x, x_range):
    # TODO: Make it bounce
    if x < x_range[0]:
        return x_range[0]
    elif x > x_range[1]:
        return x_range[1]
    else:
        return x
