import pygame
pygame.init()

class slider():
    def __init__(self,slidercolour1,slidercolour2,xpos,ypos,title,min,max,startpos,width,toggleheight,togglewidth):
        self.title = title
        self.xpos = xpos
        self.ypos = ypos
        self.slidercolour2 = slidercolour2
        self.slidercolour1 = slidercolour1
        self.max = max
        self.min = min
        self.sliderpos = startpos
        self.width = width
        self.togheight = toggleheight
        self.togglewidth = togglewidth
        self.sliderrect = pygame.Rect(0,0,0,0)
        self.togglerect = pygame.Rect(0,0,0,0)
        self.selected = False
        self.otherselected = False

        self.sliderrect = pygame.Rect(0,0,0,0)
        self.togglerect = pygame.Rect(0,0,0,0)
    def draw_slider(self,screen):

        sheight = screen.get_height()
        swidth = screen.get_width()
        width = swidth*self.width/1000
        xpos = (swidth*self.xpos/1000)-width/2
        ypos = sheight*self.ypos/1000

        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:
            if self.togglerect.collidepoint(pos):
                if not self.otherselected:
                    self.selected = True
            else:
                self.otherselected = True
        else:
            self.selected = False
            self.otherselected = False

        if self.selected:

            spacing = width/(self.max-self.min)

            self.sliderpos = ((pos[0]-xpos)/spacing)+self.min
            self.sliderpos = round(self.sliderpos)
            self.sliderpos = min(max(self.min,self.sliderpos),self.max)

        toggleheight = self.togheight*sheight/1000
        togglewidth = self.togglewidth*swidth/1000
        toggleposx = ((self.sliderpos-self.min)*width/(self.max-self.min))+xpos-(togglewidth/2)
        toggleposy = ypos - ((toggleheight/2) - 2)

        font = pygame.font.Font(None,int(toggleheight))
        toptext = (self.title + " - " + str(self.sliderpos))
        text_surface1 = font.render(toptext,True,self.slidercolour2)
        text_surface2 = font.render(self.title,True,self.slidercolour2)
        titlewidth = text_surface2.get_width()
        titleheight = text_surface1.get_height()
        screen.blit(text_surface1, ((xpos+(width/2)-(titlewidth/2)), (self.togglerect.top-(2+titleheight))))

        self.sliderrect = pygame.Rect(xpos,ypos,width,4)
        self.togglerect = pygame.Rect(toggleposx,toggleposy,togglewidth,toggleheight)
        
        pygame.draw.rect(screen,self.slidercolour1, self.sliderrect)
        pygame.draw.rect(screen,self.slidercolour2, self.togglerect)

        return self.sliderpos


