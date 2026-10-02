day = 7

match day:
    case 1:
        print("1")
    case 2:
        print("2")
    case 3:
        print("3")
    case 4:
        print("4")
    case 5:
        print("5")
    case _:
        print("X")
    
month = 5
day2 = 3
match day2:
    case 1|2|3|4|5 if month == 4:
        print("4월")
    case 1|2|3|4|5 if month == 5:
        print("5월")
    case _:
        print("맞는 달이 없음")