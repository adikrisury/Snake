import pygame as pg
from collections import deque
import random

#class definition
class Box:

    global field_ht
    global field_wd
    global width
    global height
    global vel

    def __init__(self, x, y, colors):
        self.x_pos = x
        self.y_pos = y
        self.dir = 0
        self.trail = deque([])
        win.fill((0, 0, 0))
        self.color = colors
        pg.draw.rect(win, self.color, (self.x_pos, self.y_pos, width, height))
        pg.display.update()

    def MoveLeft(self):
        self.x_pos = (self.x_pos % (field_wd - 2*width)) - vel

    def MoveRight(self):
        self.x_pos = (self.x_pos % (field_wd - 2*width)) + vel

    def MoveUp(self):
        self.y_pos = (self.y_pos % (field_ht - 2*height)) - vel

    def MoveDown(self):
        self.y_pos = (self.y_pos % (field_ht - 2*height)) + vel

    def Move(self):
        if self.dir==-1:
            self.MoveLeft()
        if self.dir==1:
            self.MoveRight()
        if self.dir==-2:
            self.MoveUp()
        if self.dir==2:
            self.MoveDown()

    def Draw(self):
        pg.draw.rect(win, self.color, (self.x_pos, self.y_pos, width, height))

    def UpdateDirection(self, direction):
        self.dir = direction

    def UpdateTrail(self):
        self.trail.append(self.dir)

    def ReturnCoord(self):
        return [self.x_pos, self.y_pos]

    def ReturnCurrentDirection(self):
        return self.dir

    def ReturnDirFromTrail(self):
        direction = self.trail.popleft()
        return direction
        
#function that returns the direction from keypress and checks if it is the opposite as the previous input. if it is the opposite, then it returns the old direction. this prevents
#the head from reversing direction
def KeyPressDirection():
    global head_old_dir
    head_direction = 0
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        head_direction = -1
    elif keys[pg.K_RIGHT]:
        head_direction = 1
    elif keys[pg.K_UP]:
        head_direction = -2
    elif keys[pg.K_DOWN]:
        head_direction = 2
    else:
        head_direction = head_old_dir

#condition to prevent reversing while moving
    if head_old_dir + head_direction == 0:
        head_direction = head_old_dir

    return head_direction

#food generator function
def MakeFood(food_x, food_y):
    pg.draw.rect(win, (128, 0, 0), (food_x, food_y, width, height))


#window parameters
field_wd = 450
field_ht = 250

# parameters of each box
width = 10
height = 10
vel = 10

pg.init()
win = pg.display.set_mode((field_wd, field_ht+100))
pg.display.set_caption("SNAKE")

#starting position of the head
head_x = random.randrange(0, field_wd, 10)
head_x = round(head_x)
head_y = random.randrange(0, field_ht, 10)
head_y = round(head_y)

#variables for main game
snake = []
head_new_dir = -1
head_old_dir = -1
run = True
steps = 0

#variable to store coordninates of each box (apart from head) to check if head coordinates match. if they match, game over
body_coords = []

#create snake with 3 boxes
head_box = Box(head_x, head_y, (255, 243, 123))
head_box.UpdateDirection(head_new_dir)
head_box.UpdateTrail()

box1 = Box(head_x+10, head_y, (0, 128, 0))
box1.UpdateDirection(head_box.trail[0])
box1.UpdateTrail()

snake = [box1]
follow_dir = head_box.trail[0]

score = 0
#font for score
font = pg.font.Font('freesansbold.ttf', 32)
text = font.render(str(score), True, (0,128,0))
textRect = text.get_rect()
textRect.center = (field_wd/2, field_ht+50)

win.blit(text, textRect)

for box in snake:
    body_coords.append(box.ReturnCoord())

food_x = random.randrange(0, field_wd - 10, 10)
food_x = round(food_x)
food_y = random.randrange(0, field_ht - 10, 10)
food_y = round(food_y)

while run:
    pg.time.delay(100)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

#on keypress, check directions and update head box direction with the new direction from keypress
        if event.type == pg.KEYDOWN:
            head_old_dir = head_new_dir
            head_new_dir = KeyPressDirection()

#collision condition. this is checked first so nothing else needs to run in collision has occurred
    head_coord = head_box.ReturnCoord()
    if head_coord in body_coords:
        run = False

#growth condition - head is in the same space as food
    if head_box.ReturnCoord()[0]==food_x and head_box.ReturnCoord()[1]==food_y:
        # pg.draw.rect(win, (0, 0, 0), (food_x, food_y, width, height))
        score+=1
        text = font.render(str(score), True, (0,128,0))
        food_x = random.randrange(0, field_wd, 10)
        food_y = random.randrange(0, field_ht, 10)
        # MakeFood(food_x, food_y)
        if snake[-1].ReturnCurrentDirection()==-1:
            box_add = Box((snake[-1].ReturnCoord()[0])+10, (snake[-1].ReturnCoord()[1]), (0, 128, 0))
            box_add.UpdateDirection(follow_dir)
            box_add.UpdateTrail()
            snake.append(box_add)
        elif snake[-1].ReturnCurrentDirection()==1:
            box_add = Box((snake[-1].ReturnCoord()[0])-10, (snake[-1].ReturnCoord()[1]), (0, 128, 0))
            box_add.UpdateDirection(follow_dir)
            box_add.UpdateTrail()
            snake.append(box_add)
        elif snake[-1].ReturnCurrentDirection()==-2:
            box_add = Box((snake[-1].ReturnCoord()[0]), (snake[-1].ReturnCoord()[1])+10, (0, 128, 0))
            box_add.UpdateDirection(follow_dir)
            box_add.UpdateTrail()
            snake.append(box_add)
        elif snake[-1].ReturnCurrentDirection()==2:
            box_add = Box((snake[-1].ReturnCoord()[0]), (snake[-1].ReturnCoord()[1])-10, (0, 128, 0))
            box_add.UpdateDirection(follow_dir)
            box_add.UpdateTrail()
            snake.append(box_add)

    win.fill((0, 0, 0))

    head_old_dir = head_new_dir
    head_box.UpdateDirection(head_new_dir)
    head_box.UpdateTrail()
    head_box.Move()
    head_box.Draw()
    follow_dir = head_box.trail.popleft()
    
#after moving head, body_coords is emptied for new coords
    body_coords = []

#movement loop for snake
    for box in snake:
        box.UpdateDirection(follow_dir)
        box.UpdateTrail()
        box.Move()
        box.Draw()
        body_coords.append(box.ReturnCoord())
        follow_dir = box.trail.popleft()

    MakeFood(food_x, food_y)
    win.blit(text, textRect)
    pg.display.update()
    steps+=1

pg.quit()