from book import book
from library import library
from library_log import library_log

ll = library()
ll.sign_in_duration = 10

print(ll.id, ll.sign_in_duration)

b = book()
library.books=[b]

print(library.books)


log =library_log()
log.library = ll
log.start_day = 1

print(log.getEndDaySignIn())

