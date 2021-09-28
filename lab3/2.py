import turtle as t
import math as m
t.shape('turtle')
t.color('blue')
t.penup()
t.goto(-200,0)
t.pendown
a0=[(90,1,100),(-90,1,50), (-90,1,100),(-90,1,50),(180,0,100)]
a1=[(90,0,50),(-135,1,50*m.sqrt(2)), (135,1,100),(-90,0,50),(-90,0,100),(90,0,0)]
a2=[(0,1,50),(90,1,50),(45,1,50*m.sqrt(2)),(-135,1,50),(-90,0,100),(90,0,50)]
a3=[(90,1,50),(135,1,50*m.sqrt(2)),(-135,1,50),(135,1,50*m.sqrt(2)),(-135,0,100),(-90,0,100)]
a4=[(90,1,50),(-90,1,50), (90,1,50),(-180,1,100),(90,0,50)]
a5=[(90,1,50),(-90,1,50), (90,1,50),(90,1,50),(90,0,100),(90,1,50),(90,0,50)]
a6=[(90,0,50),(0,1,50), (-90,1,50),(-90,1,50),(-90,1,50),(135,1,50*m.sqrt(2)),(45,0,50)]
a7=[(0,1,50),(135,1,50*m.sqrt(2)), (-45,1,50),(-90,0,100),(-90,0,100),(90,0,0)]
a8=[(0,1,50),(90,1,100), (90,1,50),(90,1,50),(90,1,50),(180,0,50),(90,1,50),(90,0,100)]
a9=[(0,1,50),(90,1,50), (45,1,50*m.sqrt(2)),(180,0,50*m.sqrt(2)),(-135,1,50),(90,1,50),(90,0,100)]
s=[a0,a1,a2,a3,a4,a5,a6,a7,a8,a9]
for i in [1,4,1,7,0,0]:
    for j in range (len(s[i])):
        if s[i][j][1]==0:
            t.penup()
            t.right(s[i][j][0])
            t.forward(s[i][j][2])
        else:
            t.pendown()
            t.right(s[i][j][0])
            t.forward(s[i][j][2])
t.done()