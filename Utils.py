CTRL_SCALE = 1

def changeSuffix(jntname, currsuffix, suffix, separator):
    temp = jntname.split(separator)
    newtemp = [t.replace(currsuffix, suffix) for t in temp]

    result = separator.join(newtemp)
    return result
