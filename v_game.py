import pygame

tem = '123456'[0:0]
print(tem, len(tem))
exit()

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

squareLen = 74

pygame.init()
window_size = (width, height) = (720, 800)
playSurface = pygame.display.set_mode(window_size)
pygame.display.set_caption('中国象棋游戏')
picBoard = pygame.image.load('bmp/棋盘.png')

chessGroup = pygame.sprite.Group()             #sprite group
chessname = ["黑车", "黑马", "黑象", "黑仕", "黑将", "黑仕", "黑象", "黑马", "黑车", "黑卒", "黑炮",
             "红车", "红马", "红相", "红仕", "红帅", "红仕", "红相", "红马", "红车", "红兵", "红炮"]
imgs = [pygame.image.load('bmp/' + chessname[i] + '.png') for i in range(0, 22)]

chessmap = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1] for y in range(9)]
# 定义一个字典
dict_ChessName = {}     # sprite --> chess color and name

LocalPlayer = "红"  # LocalPlayer记录自己是红方还是黑方
first = True  # 区分第一次还是第二次选中的棋子
IsMyTurn = True
rect1 = 0
rect2 = 0
firstChessid = 0

class Chess(pygame.sprite.Sprite):
    def __init__(self, curimg):
        pygame.sprite.Sprite.__init__(self)
        self.image = curimg.convert_alpha()                 #converted type
        self.rect = self.image.get_rect()

    def update(self):
        playSurface.blit(self.image, self.rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def setPos(self, x, y):
        global chessmap
        chessmap[x][y] = self
        x, y = 60 + 75 * x, 58 + 76 * y
        self.rect.center = (x, y)

    def move(self, x, y):
        self.setPos(x, y)
        self.update()

def IsAbleToPut(id, x, y, oldx, oldy):  # 实现判断是否能走棋返回逻辑值，这代码最复杂。
    # oldx, oldy 棋子在棋盘原坐标
    # x, y       棋子移动到棋盘的新坐标
    print(id, "QQQ", dict_ChessName[id])
    qi_name = dict_ChessName[id][1]  # 取字符串第二个字符，"黑将"变成"将"
    # "将" "帅"走棋判断
    if (qi_name == "将" or qi_name == "帅"):
        if ((x - oldx) * (y - oldy) != 0):
            return False;
        if (abs(x - oldx) > 1 or abs(y - oldy) > 1):
            return False;
        if (x < 3 or x > 5 or (y >= 3 and y <= 6)):
            return False;
        return True;

    # "士"走棋判断
    if (qi_name == "士" or qi_name == "仕"):
        if ((x - oldx) * (y - oldy) == 0):
            return False;
        if (abs(x - oldx) > 1 or abs(y - oldy) > 1):
            return False;
        if (x < 3 or x > 5 or (y >= 3 and y <= 6)):
            return False;
        return True;

    # "象"走棋判断
    if (qi_name == "象" or qi_name == "相"):
        if ((x - oldx) * (y - oldy) == 0):
            return False;
        if (abs(x - oldx) != 2 or abs(y - oldy) != 2):
            return False;
        if (y < 5 and qi_name == "相"):  # 过河
            return False;
        if (y >= 5 and qi_name == "象"):  # 过河
            return False;
        i = 0;
        j = 0;  # i,j必须有初始值
        if (x - oldx == 2):
            i = x - 1;
        if (x - oldx == -2):
            i = x + 1;
        if (y - oldy == 2):
            j = y - 1;
        if (y - oldy == -2):
            j = y + 1;
        if (chessmap[i][j] != -1):  # 憋象腿
            return False;
        return True;

    # "马"走棋判断
    if (qi_name == "马" or qi_name == "马"):
        if (abs(x - oldx) * abs(y - oldy) != 2):
            return False;
        if (x - oldx == 2):
            if (chessmap[x - 1][oldy] != -1):  # 蹩马腿
                return False;
        if (x - oldx == -2):
            if (chessmap[x + 1][oldy] != -1):  # 蹩马腿
                return False;
        if (y - oldy == 2):
            if (chessmap[oldx][y - 1] != -1):  # 蹩马腿
                return False;
        if (y - oldy == -2):
            if (chessmap[oldx][y + 1] != -1):  # 蹩马腿
                return False;
        return True;

    # "车"走棋判断
    if (qi_name == "车" or qi_name == "车"):
        # 判断是否直线
        if ((x - oldx) * (y - oldy) != 0):
            return False;
        # 判断是否隔有棋子
        if (x != oldx):
            if (oldx > x):
                t = x;
                x = oldx;
                oldx = t;
            for i in range(oldx, x + 1):
                if (i != x and i != oldx):
                    if (chessmap[i][y] != -1):
                        return False;
        if (y != oldy):
            if (oldy > y):
                t = y;
                y = oldy;
                oldy = t;
            for j in range(oldy, y + 1):
                if (j != y and j != oldy):
                    if (chessmap[x][j] != -1):
                        return False;
        return True;

    # "炮"走棋判断
    if (qi_name == "炮" or qi_name == "炮"):
        swapflagx = False;
        swapflagy = False;
        if ((x - oldx) * (y - oldy) != 0):
            return False;
        c = 0;
        if (x != oldx):
            if (oldx > x):
                t = x;
                x = oldx;
                oldx = t;
                swapflagx = True;
            for i in range(oldx, x + 1):  # for (i = oldx; i <= x; i += 1):
                if (i != x and i != oldx):
                    if (chessmap[i][y] != -1):
                        c = c + 1;

        if (y != oldy):
            if (oldy > y):
                t = y;
                y = oldy;
                oldy = t;
                swapflagy = True;
            for j in range(oldy, y + 1):  # for (j = oldy; j <= y; j += 1):
                if (j != y and j != oldy):
                    if (chessmap[x][j] != -1):
                        c = c + 1;

        if (c > 1):
            return False;  # 与目标处间隔1个以上棋子
        if (c == 0):  # 与目标处无间隔棋子
            if (swapflagx == True):
                t = x;
                x = oldx;
                oldx = t;
            if (swapflagy == True):
                t = y;
                y = oldy;
                oldy = t;
            if (chessmap[x][y] != -1):
                return False;
        if (c == 1):  # 与目标处间隔1个棋子
            if (swapflagx == True):
                t = x;
                x = oldx;
                oldx = t;
            if (swapflagy == True):
                t = y;
                y = oldy;
                oldy = t;
            if (chessmap[x][y] == -1):  # 如果目标处无棋子，则不能走此步
                return False;
        return True;

    # "卒" "兵"走棋判断
    if (qi_name == "卒" or qi_name == "兵"):
        if ((x - oldx) * (y - oldy) != 0):  # 不是直线走棋
            return False;
        if (abs(x - oldx) > 1 or abs(y - oldy) > 1):  # 走多步，不符合兵仅能走一步
            return False;
        if (y >= 5 and (x - oldx) != 0 and qi_name == "兵"):  # 未过河且横向走棋
            return False;
        if (y < 5 and (x - oldx) != 0 and qi_name == "卒"):  # 未过河且横向走棋
            return False;
        if (y - oldy > 0 and qi_name == "兵"):  # 后退
            return False;
        if (y - oldy < 0 and qi_name == "卒"):  # 后退
            return False;
        return True;
    return True;

# ——————————————————————
def drawSquare(color, x, y):
    tem = pygame.draw.rect(playSurface, color, (60 + 75 * x - 40, 58 + 76 * y - 40, squareLen, squareLen), 1)
    return tem

def deleSquare(x, y):
    temRect = (60 + 75 * x - 40, 58 + 76 * y - 40, squareLen, squareLen)
    playSurface.blit(picBoard, temRect, temRect)

# ——————————————————————
def callback(event):  # 走棋picBoard_MouseClick
    global LocalPlayer
    global chessmap
    global rect1, rect2  # 选中框图像id
    global firstChessid, secondChessid, oldfirstChessid
    global x1, x2, y1, y2
    global first
    # print("clicked at", event.pos[0], event.pos[1], LocalPlayer)
    x = (event.pos[0] - 22) // 75  # 换算棋盘坐标
    y = (event.pos[1] - 20) // 76
    print("clicked at", x, y, LocalPlayer)

    if (first):  # 第1次单击棋子
        x1 = x;
        y1 = y;
        oldfirstChessid = firstChessid = chessmap[x1][y1]
        if not (chessmap[x1][y1] == -1):
            player = dict_ChessName[firstChessid][0]
            if (player != LocalPlayer):
                print("单击成对方棋子了!");
                return
            print("第1次单击", firstChessid, dict_ChessName[firstChessid])
            first = False;
            rect1 = drawSquare(red, x, y)       # 画选中标记框

    else:  # 第2次单击
        x2 = x;
        y2 = y;
        secondChessid = chessmap[x2][y2]
        if not (chessmap[x2][y2] == -1):        #目标处有棋子
            player = dict_ChessName[secondChessid][0]
            if (player == LocalPlayer):  # 目标处如果是自己的棋子,则更新firstChess
                firstChessid = chessmap[x2][y2]
                print("第2次单击", firstChessid, dict_ChessName[firstChessid])
                ##                cv.delete(rect1);  # 取消上次选择的棋子标记框
                playSurface.blit(picBoard, rect1, rect1)
                oldfirstChessid.update()

                x1 = x;
                y1 = y;
                # 设置选择的棋子颜色
                rect1 = drawSquare(red, x, y)  # 画选中标记框
                oldfirstChessid = firstChessid
                print("点到了自己的棋子", firstChessid, dict_ChessName[firstChessid])
                pygame.display.update()
                return;
            else:  # 在吃子目标处画框
                rect2 = drawSquare(yellow, x, y)      # 目标处画框;
        else:  # 目标处无棋子
            rect2 = drawSquare(yellow, x, y)      # 在移动棋子目标处画框
        ############
        pygame.display.update()         #一次刷新
        ###################
        # 目标处没棋子，移动棋子
        print("kkkkkkkkkkkkkkkkk", firstChessid, dict_ChessName[firstChessid])
        if (chessmap[x2][y2] == " " or chessmap[x2][y2] == -1):  # 目标处没棋子，移动棋子
            print("目标处没棋子，移动棋子", firstChessid, 'from:', x2, y2, 'to:', x1, y1)
            if (IsAbleToPut(firstChessid, x2, y2, x1, y1)):  # 判断是否可以走棋
                print("能移动棋子", '############  to:', x1, y1)
                ##################################
                deleSquare(x1, y1)
                deleSquare(x2, y2)
                firstChessid.move(x2, y2)
                chessmap[x1][y1] = -1

                first = True;
                SetMyTurn(False);  # 该对方了
            else:
                # 错误走棋
                print("不符合走棋规则");
                # showinfo(title="提示", message="不符合走棋规则")
                deleSquare(x2, y2)
                playSurface.blit(picBoard, rect2, rect2)
            pygame.time.delay(100)
            pygame.display.update()
            return;
        else:
            # 目标处有棋子，可以吃子
            if (not (chessmap[x2][y2] == -1) and IsAbleToPut(firstChessid, x2, y2, x1, y1)):  # 可以吃子
                first = True;
                print("能吃子", x1, y1)
                #################
                deleSquare(x1, y1)
                deleSquare(x2, y2)
                firstChessid.move(x2, y2)
                chessmap[x1][y1] = -1
                secondChessid.kill()
                pygame.display.update()

                if (dict_ChessName[secondChessid][1] == "将"):  # "将"
                    # showinfo(title="提示", message="红方你赢了")
                    return 1
                if (dict_ChessName[secondChessid][1] == "帅"):  # "帅"
                    # showinfo(title="提示", message="黑方你赢了")
                    return 1

                SetMyTurn(False);  # 该对方了
            else:  # 不能吃子
                print("不能吃子");
                # lable1['text'] = "不能吃子"
                #####################
                deleSquare(x2, y2)  # 删除目标标记框

    pygame.display.update()


# ——————————————————————
def SetMyTurn(flag):
    global LocalPlayer
    IsMyTurn = flag
    if LocalPlayer == "红":
        LocalPlayer = "黑"
        # lable1['text'] = "轮到黑方走"
    else:
        LocalPlayer = "红"
        # lable1['text'] = "轮到红方走"
# ——————————————————————
def DrawBoard():  # 画棋盘
    #p1 = cv.create_image((0, 0), image=img1)
    #cv.coords(p1, (360, 400))
    playSurface.blit(picBoard.convert(), (0, 0))
# ——————————————————————
def LoadChess():  # 初始化棋子的位置和图片，并绑定在初始位置上
    global chessmap
    # 黑方16个棋子
    for i in range(0, 9):
        img = imgs[i]
        id = Chess(img)                  # 75*76棋盘格子大小
        id.setPos(i, 0)              #set the center's position
        dict_ChessName[id] = chessname[i];  # 图像对应的是那种棋子
        chessGroup.add(id)

    for i in range(0, 5):
        img = imgs[9]  # 卒
        id = Chess(img)
        id.setPos(i * 2, 3)
        dict_ChessName[id] = "黑卒";  # 图像对应的是那种棋子
        chessGroup.add(id)
    img = imgs[10]  # 黑方炮
    id = Chess(img)
    id.setPos(1, 2)
    dict_ChessName[id] = "黑炮";  # 图像对应的是那种棋子
    chessGroup.add(id)

    id = Chess(img)
    id.setPos(7, 2)
    dict_ChessName[id] = "黑炮";  # 图像对应的是那种棋子
    chessGroup.add(id)

    # 红方16个棋子
    for i in range(0, 9):
        img = imgs[i + 11]
        id = Chess(img)
        id.setPos(i, 9)
        dict_ChessName[id] = chessname[i + 11];  # 图像对应的是那种棋子
        chessGroup.add(id)

    for i in range(0, 5):
        img = imgs[20]  # 兵
        id = Chess(img)
        id.setPos(i * 2, 6)
        dict_ChessName[id] = chessname[20];  # 图像对应的是那种棋子
        chessGroup.add(id)

    img = imgs[21]  # 红方炮
    id = Chess(img)
    id.setPos(1, 7)
    dict_ChessName[id] = "红炮";  # 图像对应的是那种棋子
    chessGroup.add(id)

    id = Chess(img)
    id.setPos(7, 7)
    dict_ChessName[id] = "红炮";  # 图像对应的是那种棋子
    chessGroup.add(id)

    return

def gameInit():
    LoadChess()
    DrawBoard()
    chessGroup.update()
    pygame.display.update()
    # print(dict_ChessName)       #for debug
# ——————————————————————
gameInit()
# print(dict_ChessName)
running = True
while (running):  # loop listening for end of game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print('#################################################   MOUSEBUTTONDOWN', event.pos, event.button)
            if (callback(event)):
                running = False



# loop over, quite pygame
pygame.quit()
exit()
