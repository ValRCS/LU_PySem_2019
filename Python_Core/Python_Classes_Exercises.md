# Exercises:Classes

## Exercise 1

Follow the steps:

* Create a class, Triangle. Its `__init__()` method should take self, angle1, angle2, and angle3 as arguments. Make sure to set these appropriately in the body of the `__init__()` method.

* Create a variable named number_of_sides and set it equal to 3.

* Create a method named check_angles. The sum of a triangle's three angles is It should return True if the sum of self.angle1, self.angle2, and self.angle3 is equal 180, and False otherwise.

* Create method isRightTriangle which works

* Create a variable named my_triangle and set it equal to a new instance of your Triangle class. Pass it three angles that sum to 180 (e.g. 90, 30, 60).
* Print out my_triangle.number_of_sides and print out my_triangle.check_angles().
* Print out my_triangle.isRightTriangle()

* create second_triangle which also is instance of Class but has the following angles (30, 75, 95)
* print out second_triangle.check_angles() and second_triangle.isRightTriangle()



## Exercise 2

* Define a class called Songs, it will show the lyrics of a song. Its `__init__()` method should have two arguments:selfanf lyrics.lyricsis a list. Inside your class create a method called sing_me_a_songthat prints each element of lyricson his own line. Define a varible:

* happy_bday = `Song(["May god bless you, ",
                   "Have a sunshine on you,",
                   "Happy Birthday to you !",
                   "LU Python Seminar is fun!")`
* Call the sing_me_songmehod on this variable.

## Exercise 3

* Define a class called Lunch.

* Its `__init__()` method should have two arguments:self and menu. Where menu is a string. 

* Add a method called menu_price.It will involve a if statement:
  1. if "menu 1" print "Your choice:", menu, "Price 12.00",
  2. if "menu 2" print "Your choice:", menu, "Price 13.40", 
  3. else print "Error in menu".

* To check if it works define: Paul=Lunch("menu 1") and call Paul.menu_price().

## Exercise 4

* Define a Point3D class that inherits from object Inside the Point3D class, 

* define an `__init__()` function that accepts self, x, y, and z, and assigns these numbers to the member variables self.x,self.y,self.z. * Define a `__repr__()` method that returns "(%d, %d, %d)" % (self.x, self.y, self.z). This tells Python to represent this object in the following format: (x, y, z). 

* Outside the class definition, create a variable named my_point containing a new instance of Point3D with x=1, y=2, and z=3.

* Finally, print my_point.


#### https://erlerobotics.gitbooks.io/erle-robotics-learning-python-gitbook-free/classes/exercisesclasses.html
