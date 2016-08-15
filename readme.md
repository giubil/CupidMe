# CupidMe

CupidMe (teehee) is a Python package allowing for simple, easy interaction with OKCupid.com. CupidMe is currently capable of searches, custom filters, outbound communication, and more. For complete documentation, see <a href="https://github.com/TSS88/CupidMe/wiki/CupidMe")>the wiki</a>.

### Prerequisities

CupidMe was written with Python 3.5 and uses the <a href="https://github.com/jmcarp/robobrowser">RoboBrowser</a> package.

### Example Usage

CupidMe makes it easy to automate finding matches and let them know you're interested.

```Python
from cupidme import CupidMe

cupid_bot = CupidMe("Username", "Password")
cupid_bot.filter.set(who = "W4M", where = "10001", match_cutoff = 70, order_by = "MATCH", looking_for = ["new_friends", "short_term_dating"])
cupid_bot.filter.clear("match_cutoff")

cupid_bot.search(list_users = True)
print(cupid_bot.total_users)

cupid_bot.contact(cupid_bot.user_list[0], "How much does a polar bear weigh?", like = True)
cupid_bot.logout()
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Although CupidMe was written independently, you may find several similar projects on GitHub. If CupidMe suits you best, feel free to use or contribute.
