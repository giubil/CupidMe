from cupidme import CupidMe

cupid_bot = CupidMe("Username", "Password")
cupid_bot.filter.set(who = "W4M", where = "10001", match_cutoff = 70, order_by = "MATCH", looking_for = ["new_friends", "short_term_dating"])
cupid_bot.filter.clear("match_cutoff")

cupid_bot.search(list_users=True)
print(cupid_bot.total_users)

cupid_bot.contact(cupid_bot.user_list[0], "How much does a polar bear weigh?", like = True)
cupid_bot.logout()