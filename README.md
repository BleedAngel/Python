import calendar
while True:
    try:
        t=int(input())
        for i in range(t):
            x=int(input())
            ans=calendar.isleap(x)
            if(ans):
                print("a leap year")
            else:
                print("a normal year")
    except:
        break
