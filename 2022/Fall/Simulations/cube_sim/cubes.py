from cube_naming import main as names

def seed_return(dis, dis_dims):
    a = names(dis, dis_dims)
    if a == False:
        return False
    else:
        seed = a

    return seed
