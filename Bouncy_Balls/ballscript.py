import random
from time import sleep
import pygame
import threading
class ball:
    def __init__(self,colour,size,pos,speed,mini,gravity,airres,bounce,friction):
        self.colour = colour
        self.size = size
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.speed = speed
        self.active = True
        self.hity = 0
        self.hitx = 0
        self.held = True
        self.floored = False
        self.roofed = False
        self.alive = True
        self.miniballs = []
        self.mini = mini
        self.gravity = gravity
        self.airres = airres
        self.res = bounce
        self.friction = friction
    def calcspeed(self,speedsens):
        while pygame.mouse.get_pressed()[0]:
            x1 = pygame.mouse.get_pos()[0]
            y1 = pygame.mouse.get_pos()[1]
            sleep(0.01)
            x2 = pygame.mouse.get_pos()[0]
            y2 = pygame.mouse.get_pos()[1]
            if not pygame.mouse.get_pressed()[0]:
                break
            self.speed = [(x2-x1)*speedsens,(y2-y1)*speedsens]
        self.held = False
    def calculatepos(self,screen):
        while pygame.mouse.get_pressed()[0]:
            self.xpos = min(max(pygame.mouse.get_pos()[0],self.size),screen.get_width()-self.size)
            self.ypos = min(max(pygame.mouse.get_pos()[1],self.size),screen.get_height()-self.size)
        while self.active and self.alive:

            if (self.xpos >= screen.get_width()-(self.size) or self.xpos <= self.size) and self.hitx <= 0:
                self.speed[0] = self.speed[0]*-1*self.res
                self.hitx = 2
            self.xpos = max(min(self.speed[0]+self.xpos,screen.get_width()-(self.size)),self.size)

            self.speed[0]*=self.airres
            self.speed[1]+=self.gravity/100
            self.speed[1]*=self.airres

            if (self.ypos >= screen.get_height()-(self.size)) and self.hity <0:
                if self.speed[1] > self.gravity*0.1 or self.speed[1]<=0:
                    self.speed[1] = self.speed[1]*-1*self.res
                else:
                    if self.gravity>=0:
                        self.speed[1] = 0
                        self.floored = True
                self.hity = 2

            if self.ypos <= self.size and self.hity < 0:
                if self.speed[1] < self.gravity*0.1 or self.speed[1]>0:
                    self.speed[1] = self.speed[1]*-1*self.res
                else:
                    if self.gravity<=0:
                        self.speed[1] = 0
                        self.roofed = True
                self.hity = 2
            if self.floored or self.roofed:
                if self.speed[0]>0.3 or self.speed[0]<-0.3:
                    self.speed[0] = self.speed[0]*self.friction
                else:
                    self.speed[0] = 0
                    if self.mini:
                        y = threading.Thread(target=self.destroymini, args=())
                        y.daemon = True
                        y.start()
            self.ypos = max(min(self.speed[1]+self.ypos,screen.get_height()-(self.size)),self.size)
            sleep(0.01)
            self.hity -=1
            self.hitx -=1
    def drawball(self,screen):
        if self.alive:
            pygame.draw.circle(screen,self.colour, (self.xpos,self.ypos), self.size)
    def explode(self,explosionForce,screen,ballsnum):
        explosionForce=int(explosionForce)
        self.balls = []
        if self.alive:
            numballs = max(2,random.randint(ballsnum-5,ballsnum))
            for i in range(numballs):
                smallball = ball(self.colour,min((self.size/(max(ballsnum,2)/3)),(self.size/1.3)),(self.xpos,self.ypos),[self.speed[0]+((random.randint(0,explosionForce*10)/10)-(explosionForce/2)),self.speed[1]+((random.randint(0,explosionForce*10)/10)-(explosionForce/2))],True,self.gravity,self.airres,self.res,self.friction)
                self.miniballs += [smallball]
                x = threading.Thread(target=smallball.calculatepos, args=(screen,))
                x.daemon = True
                x.start()
            self.alive = False
    def destroymini(self):
        sleep(2)
        self.alive = False

