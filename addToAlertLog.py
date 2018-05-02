def addLog(message):
    from datetime import datetime
    now = datetime.now()

    day = now.day
    month = now.month
    year = now.year

    filename = "Alert_Log_{0}_{1}_{2}.txt".format(day, month, year)

    f = open(filename, "a+")
    f.write("{0}\n".format(message))
    print("writing {0} to log".format(message))
    f.close()
