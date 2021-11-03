import pygame
from random import randint
 
class robotgame:
    def __init__(self):
        pygame.init()
        self.loadimgs() #load images
        self.loop() #start looping
        
    def loadimgs(self):
        self.robot = pygame.image.load("robo.png")
        self.coin = pygame.image.load("kolikko.png")
        self.ghost = pygame.image.load("hirvio.png")
        
    def draw_screen(self):
        self.time+=1 #add to time

        if self.points<=65: #points affect darkness level
            darkness=150-2*self.points
            self.screen.fill((darkness,darkness,darkness))

        if self.points>65 and self.points<=100:
            self.screen.fill((20,20,20))
            self.screen.fill((darkness,darkness,darkness))

        if self.points>100:
            darkness=20-int((self.points-100)/5)
            self.screen.fill((darkness,darkness,darkness))
        
        text = self.font.render(f"Points: {self.points}", True, (0,255,0)) 
        self.screen.blit(text,(500,10))
        self.screen.blit(self.robot, (self.xrobot, self.yrobot))
        self.screen.blit(self.coin, (self.xcoin, self.ycoin))

        for ghost in range(len(self.ghosts)):            
            self.screen.blit(self.ghost, (self.ghosts[ghost][0], self.ghosts[ghost][1])) #draw ghosts

        if self.time<300:
            self.message("Collect as many coins as you can!",(0,255,0),1) #cheering(?) messages

        if self.points in [3,4]:
            self.message("A shady figure appears..",(255,0,0),2)

        if self.points in [10,11]:
            self.message("It seems to be getting darker..",(255,0,0),1)

        if self.points in [19,20]:
            self.message("Tip: you can outrun the ghosts",(255,0,0),1)

        if self.points in [40,41]:
            self.message("Where do they keep coming from?",(255,0,0),1)

        if self.points in [44,45]:
            self.message("Tip: when alot of ghosts spawn, the edges are safer",(255,0,0),3)

        if self.points in [80,81]:
            self.message("Nice going!",(255,0,0),1)

        if self.points in [100,101]:
            self.message("Now it's going to get really tough..",(255,0,0),1)
        
        pygame.display.flip()    
        self.clock.tick(60)
        
    def message(self,msg:str,color,pos:int): # choose positioning of drawn messages
        mesg = self.font.render(msg, True, color)

        if pos==1:
            self.screen.blit(mesg, (150, 20))

        if pos==2:
            self.screen.blit(mesg, (270, 220))

        if pos==3:
            self.screen.blit(mesg, (180, 220))

    def loop(self): #main game loop
        self.xrobot=0 
        self.yrobot = 480-self.robot.get_height()
        self.xcoin=randint(0,640-self.coin.get_width())
        self.ycoin=randint(0,480-self.coin.get_height())

        self.points=0
        self.speed=2

        self.right = False
        self.left = False
        self.up = False
        self.down = False

        self.time=0
        self.maxghosts=0
        self.ghostspeed=2
        self.ghosts=[]

        self.screen = pygame.display.set_mode((640, 480))
        self.font = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption(" "*60+"Robot game")
        self.clock = pygame.time.Clock()

        while True:
            self.examine_events()
            self.draw_screen()

    def moverobot(self, left:bool, up:bool, right:bool, down:bool):

        if down:
            if self.yrobot+self.speed+self.robot.get_height()<=480:
                self.yrobot += self.speed

        if up:
            if self.yrobot-self.speed>0:
                self.yrobot -= self.speed

        if right:
            if self.xrobot+self.speed+self.robot.get_width()<=640:
                self.xrobot += self.speed

        if left:
            if self.xrobot-self.speed>0:
                self.xrobot -= self.speed

    def moveghosts(self):
        for ghost in range(len(self.ghosts)):     
            
            if self.ghosts[ghost][2]==True:   #index 3 for +x, 4 for +y, 5 for -x and 6 for -y
                self.ghosts[ghost][0]+=self.ghostspeed

            if self.ghosts[ghost][3]==True:
                self.ghosts[ghost][1]+=self.ghostspeed

            if self.ghosts[ghost][4]==True:
                self.ghosts[ghost][0]-=self.ghostspeed

            if self.ghosts[ghost][5]==True:
                self.ghosts[ghost][1]-=self.ghostspeed

        #keep track of all ghosts
        self.ghosts=[self.ghosts[ghost] for ghost in range(len(self.ghosts)) if not (self.ghosts[ghost][0]>640 and self.ghosts[ghost][2]==True)]
        self.ghosts=[self.ghosts[ghost] for ghost in range(len(self.ghosts)) if not (self.ghosts[ghost][1]>480 and self.ghosts[ghost][3]==True)]
        self.ghosts=[self.ghosts[ghost] for ghost in range(len(self.ghosts)) if not (self.ghosts[ghost][0]<0 and self.ghosts[ghost][4]==True)]
        self.ghosts=[self.ghosts[ghost] for ghost in range(len(self.ghosts)) if not (self.ghosts[ghost][1]<0 and self.ghosts[ghost][5]==True)]

    def coinspawner(self):
        self.xcoin=randint(0,640-self.coin.get_width())
        self.ycoin=randint(0,480-self.coin.get_height())

    def ghostspawner(self):
        if len(self.ghosts)<self.maxghosts:
            side=randint(1,4) #ghost spawns on random side and travels towards the opposite side

            if side==1:
                self.ghosts.append([0-self.ghost.get_width(),randint(0-self.ghost.get_height(),480),True,False,False,False])
                
            if side==2:
                self.ghosts.append([randint(0-self.ghost.get_width(),640),0-self.ghost.get_height(),False,True,False,False])
                
            if side==3:
                self.ghosts.append([640,randint(0-self.ghost.get_height(),480),False,False,True,False])
                
            if side==4:
                self.ghosts.append([randint(0-self.ghost.get_width(),640),480,False,False,False,True])
                
    def difficulty(self):
        self.maxghosts=int(self.points/3)

        if self.points>=20:            
            if randint(1,int(50-self.points/7))==1: #spawnrate, adjustable
                self.ghostspawner()
        else:
            if randint(1,50):
                self.ghostspawner()

    def examine_events(self): 
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN: #key controls
                if event.key == pygame.K_LEFT:
                    self.left = True

                if event.key == pygame.K_RIGHT:                    
                    self.right = True

                if event.key == pygame.K_UP:
                    self.moverobot(0,1,0,0)
                    self.up = True

                if event.key == pygame.K_DOWN:
                    self.down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:                    
                    self.left = False

                if event.key == pygame.K_RIGHT:                    
                    self.right = False

                if event.key == pygame.K_UP:                    
                    self.up = False

                if event.key == pygame.K_DOWN:                    
                    self.down = False

            if event.type == pygame.QUIT:
                exit()
 
        xrobotmid=self.xrobot+self.robot.get_width()/2
        yrobotmid=self.yrobot+self.robot.get_height()/2

        xcoinmid=self.xcoin+self.coin.get_width()/2
        ycoinmid=self.ycoin+self.coin.get_height()/2

        xghostmid=[self.ghosts[ghost][0]+self.ghost.get_width()/2 for ghost in range(len(self.ghosts))]
        yghostmid=[self.ghosts[ghost][1]+self.ghost.get_width()/2 for ghost in range(len(self.ghosts))]
        
        if abs(yrobotmid-ycoinmid)<=(self.robot.get_height()+self.coin.get_height())/2:
            if abs(xrobotmid-xcoinmid)<=(self.robot.get_width()+self.coin.get_width())/2:
                self.points+=1
                self.coinspawner()


        for ghost in range(len(self.ghosts)):
            if abs(yrobotmid-yghostmid[ghost])+30<=(self.robot.get_height()+self.ghost.get_height())/2: #leniencies for touching a ghost
                if abs(xrobotmid-xghostmid[ghost])+30<=(self.robot.get_width()+self.ghost.get_width())/2:
                    gamelost=True
                    self.screen.fill((0,0,0))

                    while gamelost:
                        self.message("YOU DIED! Restart: R, Quit: Q",(255,0,0),1)
                        self.message(f"Score: {self.points}",(255,0,0),2)
                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    exit()

                                if event.key == pygame.K_r:
                                    self.loop()
        if self.points>=0:
            self.difficulty()

        if len(self.ghosts)>0:
            self.moveghosts()

        if self.down:
            self.moverobot(0,0,0,1)

        if self.up:
            self.moverobot(0,1,0,0)

        if self.right:
            self.moverobot(0,0,1,0)
                        
        if self.left:
            self.moverobot(1,0,0,0)
 
if __name__ == "__main__":
    robotgame()