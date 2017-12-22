determine member distance from tower 
    # wireless sta 0 signal      
    myKey["signal"] = wireless["sta"][0]["signal"]
    
    for key, value in wireless.items(): # (same for distance)
        if key == "distance":
            dis = value /1609.34 #convert to miles from meters
            myKey[key] = "About " + str(round(dis, 2)) + " miles"
        if key == "signal":
            if abs(int(value)) > 70:
                myKey[key] = str(value) + " (Weak signal) "
                myKey["signalint"] = abs(int(value))
            elif 70 >= abs(int(value)) > 65:
                myKey[key] = str(value) + " (Decent signal) "
                myKey["signalint"] = abs(int(value))
            elif abs(int(value)) < 65:
                myKey[key] = str(value) + " (Strong signal) "
                myKey["signalint"] = abs(int(value))
        if key == "sta":
            for key, value in sta.items():
                if key == "0":
                    for key, value in "0".items():
                        if abs(int(value)) > 70:
                            myKey[key] = str(value) + " (Weak signal) "
                            myKey["signalint"] = abs(int(value))
                        elif 70 >= abs(int(value)) > 65:
                            myKey[key] = str(value) + " (Decent signal) "
                            myKey["signalint"] = abs(int(value))
                        elif abs(int(value)) < 65:
                            myKey[key] = str(value) + " (Strong signal) "
                            myKey["signalint"] = abs(int(value))
