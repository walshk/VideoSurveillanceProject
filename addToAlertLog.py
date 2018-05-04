def addLog(message):
    from datetime import datetime
    now = datetime.now()

    day = now.day
    month = now.month
    year = now.year

    filename = "AlertLog_{2}_{1}_{0}.txt".format(day, month, year)

    f = open(filename, "a+")
    f.write("{0}\n".format(message))
    print("writing {0} to log".format(message))
    f.close()
