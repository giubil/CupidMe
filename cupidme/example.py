from cupidme import CupidMe

cupid_bot = CupidMe("THScraper", "W3@kP@ssw0rd")
cupid_bot.filter.set(where = "10001", religion = ["agnosticism"])
print(cupid_bot.filter.current_filter["religion"])
print(cupid_bot.total_users)