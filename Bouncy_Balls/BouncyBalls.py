import pygame
import ballscript
import threading
import sliders
import random

restitution = 0.8
gravity = 30
friction = 0.97
airresistance = 0.995
explosionForce = 20
ballsize = 50
ballnum = 8
speedsens = 0.8
settingsopen = False

(width, height) = (1000, 800)

backcolour = (random.randint(0,2)*127,random.randint(0,2)*127,random.randint(0,2)*127)
while backcolour == (0,0,0):
    backcolour = (random.randint(0,2)*127,random.randint(0,2)*127,random.randint(0,2)*127)

running = True

pygame.init()
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption("Bouncy Balls")

first = True
balls = []

ballsize_slider = sliders.slider((255,255,255),(0,0,0),500,100,"Ball Size",10,100,55,800,50,15)
explosion_slider = sliders.slider((255,255,255),(0,0,0),500,200,"Explosion Power",0,100,50,800,50,15)
ballnum_slider = sliders.slider((255,255,255),(0,0,0),500,300,"Explosion Balls",5,25,10,800,50,15)
airres_slider = sliders.slider((255,255,255),(0,0,0),500,700,"Air Resistance",0,100,20,800,50,15)
grav_slider = sliders.slider((255,255,255),(0,0,0),500,400,"Gravity",-20,20,10,800,50,15)
restitution_slider = sliders.slider((255,255,255),(0,0,0),500,500,"Bounciness",0,100,80,800,50,15)
floor_friction_slider = sliders.slider((255,255,255),(0,0,0),500,600,"Floor Friction",10,100,55,800,50,15)
speed_slider = sliders.slider((255,255,255),(0,0,0),500,800,"Speed Sensitivity",0,100,50,800,50,15)

sliderslist = [ballsize_slider,explosion_slider,ballnum_slider,grav_slider,restitution_slider,floor_friction_slider,airres_slider,speed_slider]


def maingame(running,restitution,gravity,friction,airresistance,explosionForce,ballsize,backcolour,balls,speedsens,screen,settingsopen,ballnum):
    screen.fill(backcolour)
    ev = pygame.event.get()

    for event in ev:

        if event.type == pygame.MOUSEBUTTONDOWN:
            colour = (0,0,0)
            nextball = ballscript.ball(colour,ballsize,pygame.mouse.get_pos(),[0,0],False,gravity,airresistance,restitution,friction)   
            balls += [nextball]
            y = threading.Thread(target=nextball.calcspeed, args=(speedsens,))
            y.daemon = True
            y.start()
            
            x = threading.Thread(target=nextball.calculatepos, args=(screen,))
            x.daemon = True
            x.start()

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                explodeable = False
                if not pygame.mouse.get_pressed()[0] == 1:
                    for ball in balls:
                        if ball.alive:
                            explodeable = True
                        ball.explode(explosionForce,screen,ballnum)
                    if explodeable:
                        backcolour = (random.randint(0,2)*127,random.randint(0,2)*127,random.randint(0,2)*127)
                        while backcolour == (0,0,0):
                            backcolour = (random.randint(0,2)*127,random.randint(0,2)*127,random.randint(0,2)*127)
            if event.key == pygame.K_ESCAPE:
                settingsopen = not settingsopen

    for ball in balls:
        ball.gravity = gravity
        ball.airres = airresistance
        ball.res = restitution
        ball.friction = friction
        ball.drawball(screen)
        empty = True
        if ball.alive:
            empty = False
        for miniball in ball.miniballs:
            miniball.gravity = gravity
            miniball.airres = airresistance
            miniball.res = restitution
            miniball.friction = friction
            miniball.drawball(screen)
            if miniball.alive:
                empty = False
        if empty:
            balls.remove(ball)
    pygame.display.update()
    return backcolour, running, restitution,gravity,friction,airresistance,explosionForce,ballsize,backcolour,balls,screen,speedsens,settingsopen,ballnum


def settings(screen,running,backcolour,sliderslist,restitution,gravity,friction,airresistance,explosionForce,ballsize,balls,speedsens,settingsopen,ballnum):
    screen.fill(backcolour)
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                settingsopen = not settingsopen
    #size
    ballsize = sliderslist[0].draw_slider(screen)
    #explosion force
    expval = sliderslist[1].draw_slider(screen)
    explosionForce = expval/2
    #ballnum
    ballnum = sliderslist[2].draw_slider(screen)
    #gravity
    gravityval = sliderslist[3].draw_slider(screen)
    gravity = 3*gravityval
    #restitution
    resval = sliderslist[4].draw_slider(screen)
    restitution = resval/100
    #floor resistance
    floorresval = sliderslist[5].draw_slider(screen)
    friction = 1 - (floorresval/1500)
    #air resistance
    airresval = sliderslist[6].draw_slider(screen)
    airresistance = 1 - (airresval/3000)
    #sensitivity
    sensval = sliderslist[7].draw_slider(screen)
    speedsens = sensval*(0.8/50)

    pygame.display.update()
    return backcolour, running, restitution,gravity,friction,airresistance,explosionForce,ballsize,backcolour,balls,screen,speedsens,settingsopen,ballnum

while running:
    if settingsopen:
        backcolour, running, restitution,gravity,friction,airresistance,explosionForce,ballsize,backcolour,balls,screen,speedsens,settingsopen,ballnum = settings(screen,running,backcolour,sliderslist,restitution,gravity,friction,airresistance,explosionForce,ballsize,balls,speedsens,settingsopen,ballnum)
    else:
        backcolour, running, restitution,gravity,friction,airresistance,explosionForce,ballsize,backcolour,balls,screen,speedsens,settingsopen,ballnum = maingame(running,restitution,gravity,friction,airresistance,explosionForce,ballsize,backcolour,balls,speedsens,screen,settingsopen,ballnum)
