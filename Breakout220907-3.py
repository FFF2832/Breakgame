import tkinter as tk
# import numpy as np
import random

canvas_width=600
canvas_height=500
window=tk.Tk()
window.title('Breakout Game')
canvas = tk.Canvas(window, bg='white',width=canvas_width,height=canvas_height)
canvas.pack()


class Ball:
    def __init__(self,radius,x,y,speed,color):
        self.radius=radius
        self.x=x
        self.y=y
        self.speed=speed
        self.dx=speed
        self.dy=-speed
        self.color=color
        self.rect=[x-radius, y-radius, x+radius, y+radius]
        self.particles = []  #存放炫彩粒子
    
    #畫圓
    def drawBall(self):
        ball=canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, fill=self.color,width=0)
        # rect = canvas.coords(ball) #coords 這個函式可以幫你得到ball 外切矩形的左上與右下角點座標，即[x-radius, y-radius, x+radius, y+radius]

    #更新圓心位置
    def UpdateBallPos(self,paddle):
        if(paddle.fireIndex==False): 
            self.x=(paddle.rect[0]+paddle.rect[2])/2 #(paddleRect[0]+paddleRect[2])/2
        else:
            self.x += self.dx #即x=x+dx
            self.y += self.dy #即y=y+dx
        self.rect=[self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius]
        return self.rect

    def updateBallVelocity(self,paddle,game):
        if(self.rect[2]>canvas_width or self.rect[0]<0):
            self.dx = -self.dx
        if(self.rect[1]<0) : #if(self.rect[1]<0 or self.rect[3]>canvas_height) :
            self.dy = -self.dy
        elif(self.rect[3]>canvas_height-paddle.paddleHeight) : # elif(ballRect[3]+dy>canvas_height-paddleHeight) :
            collision=self.rectCollision(paddle.rect)
            if (collision):
                self.dy = -self.dy
            else :
                game.lives-=1
                if(game.lives>0): 
                    game.reset()
                else:
                    game.stop=True
            
    def rectCollision(self,rect2) :
        # rect1與rect2是儲存兩相互碰撞物件之外接矩形左上與右下角點座標的陣列
        # 以這個程式的ball為例，rect1=[x-radius, y-radius, x+radius, y+radius] #radius原本是全域變數，改成類別程式後刪掉了
        minXA = self.x-self.radius 
        maxXA = self.x+self.radius
        minYA = self.y-self.radius
        maxYA = self.y+self.radius

        minXB = rect2[0]
        maxXB = rect2[2]
        minYB = rect2[1]
        maxYB = rect2[3]
        if (maxXA >= minXB and maxXB >= minXA and maxYA >= minYB and maxYB >= minYA) :
            return True
        else:
            return False
    
    def randomValue(self,x,y):
        for i in range(15):
            self.effx=self.x+random.randrange(-10,10)
            self.effy=self.y+random.randrange(-10,10)
            self.effr = 4 + random.random() * 4 #產生4~8之間的隨機值作為半徑
            # #代表某種顏色之16進制值的字串(比如代表紅色的字串為'#ff0000')
            # R=int(random.random() * 255)
            # G=int(random.random() * 255)
            # B=int(random.random() * 255)
            self.effcolor = '#0095DD' #'#%02x%02x%02x' % (R, G, B) #color存的是16進制的字串
            self.effdx=-3+random.random()*6 #-3~6
            self.effdy=-3+random.random()*6 #-3~6
            self.effdr=0.25+random.random()
            self.particles.append([Ball(self.effr,self.effx,self.effy,0,self.effcolor),self.effdx,self.effdy,self.effdr]) #'#0095DD'

    def updateValue(self,value,i): 
        value[0].x+=value[1]
        value[0].y+=value[2]
        value[0].radius-=value[3]
        if(value[0].radius<=0):
            self,self.particles.remove(value)
            i-=1
        return i

    def drawParticles(self):
        i=0
        while(i<len(self.particles)):
            self.particles[i][0].drawBall()
            i=self.updateValue(self.particles[i],i)
            i+=1




class Paddle:
    def __init__(self,paddleWidth,paddleHeight,color):
        self.paddleHeight=paddleHeight #15 #球拍的高度
        self.paddleWidth=paddleWidth #95
        self.paddleX = (canvas_width-paddleWidth)/2
        self.paddleY = canvas_height-paddleHeight
        self.fireIndex=False
        self.action=0
        self.color=color
        #事件綁定或處理函式
        window.bind('<KeyPress>',self.keyDownHandler) #處理鍵盤按鍵是否按下的事件
        window.bind('<KeyRelease>',self.keyUpHandler) #處理鍵盤按鍵是否放開的事件
        window.bind('<Motion>',self.mouseMoveHandler) #處理滑鼠是否移動的事件
        window.bind('<ButtonPress>',self.mousePressed) #處理滑鼠左鍵是否按下的事件
        # # window.bind('<ButtonRelease>',mouseReleased) #處理滑鼠左鍵是否放開的事件
    def drawPaddle(self):
        canvas.create_rectangle(self.paddleX, self.paddleY, self.paddleX+self.paddleWidth, self.paddleY+self.paddleHeight, fill=self.color,width=0)

    def paddleUpdatePos(self):
        if self.action == 1 and self.paddleX < canvas_width-self.paddleWidth:   # right
            self.paddleX += 10
        elif self.action == 2 and self.paddleX > 0:   # left
            self.paddleX -= 10
        self.rect=[self.paddleX, self.paddleY, self.paddleX+self.paddleWidth, canvas_height]
        return self.rect

    def keyDownHandler(self,e) :
        if(e.keycode == 39) :
            self.action=1
        elif(e.keycode == 37) :
            self.action=2
        elif(e.keycode == 32): #32代表空白鍵
            self.fireIndex=True
            
    def keyUpHandler(self,e) :
        if(e.keycode == 39) :
            self.action=0
        elif(e.keycode == 37) :
            self.action=0

    def mouseMoveHandler(self,e) :
        # #控制滑鼠指標只有在畫布內移動，才可以改變球拍的X座標paddleX
        if(e.x > self.paddleWidth/2 and e.x < canvas_width-self.paddleWidth/2) :
            self.paddleX = e.x - self.paddleWidth/2

    def mousePressed(self,e):
        if(e.num==1): self.fireIndex=True



class Bricks:
    def __init__(self,brickRowCount,brickWidth,brickColumnCount,brickHeight,brickPadding,brickOffsetTop,color):
        self.brickRowCount = brickRowCount #8
        self.brickWidth = brickWidth #30
        self.brickColumnCount = brickColumnCount #16 #round(canvas_width/brickWidth)
        self.brickHeight = brickHeight #10
        self.brickPadding = brickPadding #5
        self.brickOffsetTop = brickOffsetTop #50
        self.brickOffsetLeft = (canvas_width-brickWidth*brickColumnCount-brickPadding*(brickColumnCount-1))/2
        self.color=color
        self.bricksData = []
        for r in range(brickRowCount) :
            self.bricksData.append([])
            for c in range(brickColumnCount) :
                brickX = (c*(brickWidth+brickPadding))+self.brickOffsetLeft
                brickY = (r*(brickHeight+brickPadding))+brickOffsetTop
                rect = [brickX, brickY, brickX+brickWidth, brickY+brickHeight]
                # R=int(random.random() * 255)
                # G=int(random.random() * 255)
                # B=int(random.random() * 255)
                # color = '#%02x%02x%02x' % (R, G, B)
                self.bricksData[r].append({ 'x': brickX, 'y': brickY, 'status':1, 'color':self.color, 'rect': rect })

    def drawBricks(self):
        for r in range(self.brickRowCount) :
            for c in range(self.brickColumnCount) :
                b = self.bricksData[r][c]
                if(b['status']==1): #
                    canvas.create_rectangle(b['x'], b['y'], b['x']+self.brickWidth, b['y']+self.brickHeight, fill=b['color'],width=0)

    def updateBricks(self,game):
        for r in range(self.brickRowCount) :
            for c in range(self.brickColumnCount) :
                b = self.bricksData[r][c]
                if(b['status']==1):
                    if (game.ball.rectCollision(b['rect'])) :
                        game.ball.randomValue(b['x']+self.brickWidth/2, b['y']+self.brickHeight/2)
                        game.ball.dy = -game.ball.dy
                        b['status']=0 #設為0，代表被撞的該磚塊不存在了，下次也就不再做碰撞檢測
                        game.score+=1
                        if(game.score == self.brickRowCount*self.brickColumnCount) :
                            game.stop=True


class Breakout:
    def __init__(self):
        self.lives=3
        self.score=0
        self.stop=False
        self.paddle=Paddle(95,15,'#0095DD')
        self.ball=Ball(12.5,canvas_width/2,canvas_height-12.5-self.paddle.paddleHeight,5,'#0095DD')
        self.bricks=Bricks(8,30,16,10,5,50,'#0095DD')

    def drawScore(self) :
        return canvas.create_text(60,20,text='Score: '+str(self.score),font=('Arial',16),fill='blue')

    def drawLives(self) :
        return canvas.create_text(canvas_width-60, 20,text='Lives: '+str(self.lives),font=('Arial',16),fill='blue')

    def reset(self):
        self.ball.x=canvas_width/2
        self.ball.y=canvas_height-self.ball.radius-self.paddle.paddleHeight
        self.ball.dx=self.ball.speed
        self.ball.dy=-self.ball.speed
        self.paddle.paddleX = (canvas_width-self.paddle.paddleWidth)/2
        self.paddle.fireIndex=False

    def step(self):
        self.paddle.paddleUpdatePos()
        self.ball.UpdateBallPos(self.paddle)
        self.bricks.updateBricks(self)
        self.ball.updateBallVelocity(self.paddle,self)
        return self.stop

    def draw(self):
        canvas.delete("all") #delete(ALL)
        self.ball.drawBall()
        self.paddle.drawPaddle()
        self.bricks.drawBricks()
        self.ball.drawParticles()
        self.drawScore()
        self.drawLives()

    def render(self):
        self.draw()
        self.stop=self.step()
        myAfter=window.after(10, self.render)#即幀率為100FPS(一秒更新100次) #間隔多少時間(這裡是設10ms)就執行什麼動作一次
        if self.stop: 
            window.after_cancel(myAfter)
            self.draw()
            if(self.lives==0): canvas.create_text(canvas_width/2,canvas_height/2,text='GAME OVER',font=('Arial',50),fill='red')
            else: canvas.create_text(canvas_width/2,canvas_height/2,text='YOU WIN',font=('Arial',50),fill='green')



game=Breakout()
game.render()

window.mainloop()