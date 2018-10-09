import programStatus

test=programStatus.currentStatus()

test.setCurrFilename("ass")

x=55
y=897
punto1=programStatus.point()
punto2=programStatus.point()
punto3=programStatus.point()

punto1.setPoint(x,y)
punto2.setPoint(1,1)
print (test.currFilename)

if punto1.checkEmptyPoint():
    print("testato")
