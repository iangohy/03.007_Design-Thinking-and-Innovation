def readBarcode():
    try:
        fp = open('/dev/hidraw0', 'rb')

        res = ""
        while True:
            # Read barcode scan
            buffer = fp.read(8)
            shift = False
            for c in buffer:
                if c > 0:
                    if c == 2:
                        shift = True
                        continue
                    if shift == True:
                        res += hid2[int(c)]
                    else:
                        if c == 40:
                            logging.info("Barcode scanned: " + res)
                            return(res)    
                        else:
                            res += hid[int(c)]
    except FileNotFoundError:
        logging.error("[ERROR] Unable to connect to barcode scanner! Is it plugged in?")
        logging.info("Recyclace software quitting...")
        input("Press any enter to continue...")
        quit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def getBarcodeData():
    res = readBarcode() 
    # Check shutdown
    if res == "SHUTDOWN":
        os.system("sudo shutdown -h now")
        quit()
    # Check against database
    with open("data.csv") as data:
        reader = csv.reader(data)
        item = []
        for row in reader:
            if row[0] == res:
                item = row
                logging.info(f">>> name: {item[1]} | type: {item[2]} | barcode: {item[0]}")
                return item[2]
        if not item:
            logging.info(f"Barcode {res} not found! Classifying as waste")
            return "waste"