
def assertEqual(x, y):
    if(x != y):
        print("FAILED assertEqual : "+str(x)+" != "+str(y))
    assert x == y