equilateral = [
    [0,0,0,1,0,0,0],
    [0,0,1,1,1,0,0],
    [0,1,1,1,1,1,0],
    [1,1,1,1,1,1,1]
    ]
for point in equilateral:
    for image in point:
        if(image):
            print('*',end="")
        else:
            print(' ',end="")
    print('')
