import smartscore_gip as gip
import smartscore_driver as driver
import time

while True:
    if(driver.gameInProgress()):
        gip.main()
    else:
        print(f"Next game in {driver.secondsUntilNextGame()}. ")
        time.sleep(1800)
