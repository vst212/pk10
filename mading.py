import random

from pycparser.ply.cpp import xrange

WIN  = 1
LOSE = 0

def gambling_50_percent(pocket, pay):
    result = random.randint(0, 1)
    if result == WIN:
        pocket += pay
    else:
        pocket -= pay
    return result, pocket

def play_a_round(win_time_to_stop, pocket, pay, n):
    money_when_start = pocket
    root_pay = pay

    for i in xrange(win_time_to_stop):
        win_or_lose, pocket = gambling_50_percent(pocket, pay)
        if win_or_lose == WIN:
            pay *= n
        else:
            pay = root_pay
            break
    # print(pocket, pay)
    return pocket - money_when_start, pocket > money_when_start

mymoney = 0
for i in range(200):
    mymoney += play_a_round(4,2000,100,2)[0]

print(mymoney)