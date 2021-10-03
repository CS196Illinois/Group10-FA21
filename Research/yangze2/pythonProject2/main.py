# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pygame


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

print("1")


pygame.init()

window = pygame.display.set_mode((1000,600))
#设置游戏名字：
pygame.display.set_caption("卢本伟牛逼！")


#延长运行时间
# gameloop:死循环（里面要检测event）
while True:
    #检测事件
    for event in pygame.event.get():
        #检测事件：关闭按钮
        if event.type == pygame.QUIT:
            #退出程序，一般来说是退出一个进程，但是这里的话因为进程只有一个，所以说我们这样直接就可以退出这个游戏。
            exit()



