# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 18:18:40 2024

@author: BBS
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 17:30:53 2024

@author: vhopp
"""

import cv2
import numpy as np 

class Person:
    selected_colors = []
    order = {'starter': 'x', 'main course': 'x', 'snack': 'x', 'desert': 'x'}
    MainMenuCounter = 0
    StarterCounter = 0

    def __init__(self, name):
        self.name = name
        self.colordetector=[]
    def Dishdetector(self, color, shape):
        
        
        if color == "red" and not color in self.colordetector:
            Person.StarterCounter += 1
            if Person.StarterCounter == 1:
                if shape == "triangle":
                    dish = "Soup"
                    Person.order['starter'] = dish
                elif shape == "rectangle":
                    dish = "Cheese Platter"
                    Person.order['starter'] = dish
                elif shape == "circle":
                    dish = "Garlic Bread"
                    Person.order['starter'] = dish
        elif color == "green" and not color in self.colordetector:
       
            if shape == "triangle":
                dish = "Crispy Chicken"
                Person.order['snack'] = dish
            elif shape == "rectangle":
                dish = "Fish & Chips"
                Person.order['snack'] = dish
            elif shape == "circle":
                dish = "Omelet"
                Person.order['snack'] = dish

        elif color == "blue" and not color in self.colordetector:
            Person.MainMenuCounter += 1
            if Person.MainMenuCounter == 1:
                if shape == "triangle":
                    dish = "Meatballs"
                    Person.order['main course'] = dish
                elif shape == "rectangle":
                    dish = "Casseroles"
                    Person.order['main course'] = dish
                elif shape == "circle":
                    dish = "Fajitas"
                    Person.order['main course'] = dish

        elif color == "yellow" and not color in self.colordetector:
            if shape == "triangle":
                dish = "Souffle"
                Person.order['desert'] = dish
            elif shape == "rectangle":
                dish = "Tiramisu"
                Person.order['desert'] = dish
            elif shape == "circle":
                dish = "Cheesecake"
                Person.order['desert'] = dish
        
        
        else:
            raise Exception("Only One Of Same Color Object You Can Select")
        
        self.colordetector.append(color)
    def isEnable(self):
        if Person.StarterCounter==1 and Person.MainMenuCounter==1:
            return True
    def getMenu(self):
        if self.isEnable():
            self.approve=str(input(f"Your Order: {Person.order} \n Do you confirm ?\n Yes or No\n"))
            if self.approve=="yes":
                print("Your Order is Prepared")
                print(f"The Total Amount You Have To Pay {self.price()} Tl")
            else:
                raise Exception("Canceled")
        else:
            raise Exception("You Should Select Starter or Main Course")
    def price(self):
         self.price=0
         self.personmeal=[]
         self.prices = {
             'Soup' :65 ,
             'Cheese Platter': 75,
             'Garlic Bread':55,
             
             'Crispy Chicken':80,
             'Fish & Chips':100,
             'Omelet':70,
             
             'Meatballs':100,
             'Casseroles':150,
             'Fajitas':125,
             
             'Souffle':90,
             'Tiramisu':125,
             'Cheesecake':90 }
         
         for i in Person.order.values():
             self.personmeal.append(i)
         for x, y in self.prices.items():
             for i in self.personmeal:
                 if x==i:
                     self.price+=y
         return self.price
                     
class MenuDetector:
    def __init__(self, person, imageurl):
        self.person = person
        self.imageurl = imageurl

        self.detectcolor()

    def detectcolor(self):
        self.image = cv2.imread(self.imageurl, cv2.IMREAD_COLOR)
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
       
        self.red_lower = np.array([160, 50, 50], np.uint8) 
        self.red_upper = np.array([180, 255, 255], np.uint8) 
        self.red_mask = cv2.inRange(self.hsv, self.red_lower, self.red_upper) 
                
        self.green_lower = np.array([35, 100, 100]) 
        self.green_upper = np.array([75, 255, 255]) 
        self.green_mask = cv2.inRange(self.hsv, self.green_lower, self.green_upper) 
        
        self.blue_lower = np.array([75, 100, 100], np.uint8) 
        self.blue_upper = np.array([130, 255, 255], np.uint8) 
        self.blue_mask = cv2.inRange(self.hsv, self.blue_lower, self.blue_upper)
        
        self.yellow_lower = np.array([20, 100, 100])
        self.yellow_upper = np.array([30, 255, 255])
        self.yellow_mask = cv2.inRange(self.hsv, self.yellow_lower, self.yellow_upper)
        
        

        
        
        self.kernel = np.ones((5, 5), np.uint8) 
        self.red_mask=cv2.dilate(self.red_mask,self.kernel)
        self.green_mask=cv2.dilate(self.green_mask,self.kernel)
        self.blue_mask=cv2.dilate(self.blue_mask,self.kernel)

        self.contourred, _ = cv2.findContours(self.red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contourgreen, _ = cv2.findContours(self.green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contourblue, _ = cv2.findContours(self.blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contouryellow, _ = cv2.findContours(self.yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        self.counter = 0
        self.color = 'x'
        
        for i in range(len(self.contourred)):
            if cv2.contourArea(self.contourred[i]) > 1000:
                self.contour = self.contourred[0]
                self.color = "red"
                self.detectshape()

        for i in range(len(self.contourgreen)):
            if cv2.contourArea(self.contourgreen[i]) > 1000:
                self.contour = self.contourgreen[0]
                self.color = "green"
                self.detectshape()

        for i in range(len(self.contourblue)):
            if cv2.contourArea(self.contourblue[i]) > 1000:
                self.contour = self.contourblue[0]
                self.color = "blue"
                self.detectshape()

        for i in range(len(self.contouryellow)):
            if cv2.contourArea(self.contouryellow[i]) > 1000:
                self.contour = self.contouryellow[0]
                self.color = "yellow"
                self.detectshape()

    def detectshape(self):
        self.counter += 1
        self.shape = "x"
        self.peri = cv2.arcLength(self.contour, True)
        self.approx = cv2.approxPolyDP(self.contour, 0.04 * self.peri, True)
        if self.counter == 1:
            if len(self.approx) == 3:
                self.shape = "triangle"
            elif len(self.approx) == 4:
                self.shape = "rectangle"
            else:
                self.shape = "circle"

            self.person.Dishdetector(self.color, self.shape)
       
ahmet=Person("Ahmet")    
menu=MenuDetector(ahmet, "C:/Users/BBS/Desktop/yellowtriangle.jpeg")

menu2=MenuDetector(ahmet, "C:/Users/BBS/Desktop/bluecircle.png")
menu3=MenuDetector(ahmet, "C:/Users/BBS/Desktop/redrectangle.jpg")
ahmet.getMenu()




