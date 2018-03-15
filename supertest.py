class A(object):
    def __init__(self):
            self.test = "Hi!"   
            self.z = ""
    def x(self):
            self.z = "Okay"
 
class B(A):
    def __init__(self):
            self.test = "Nope!"
            self.z = ""
    def x(self):
            super(B,self).x()
            self.z += ", but ..."
            
b = B()
b.x()
print b.z