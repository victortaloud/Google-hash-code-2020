class library_log:
    def __init__(self, lib=None, start_day=0,list_scans=[]):
        self.library = lib
        self.start_day = start_day
        self.list_scans = list_scans

    def getEndDaySignIn(self):
        return self.start_day + self.library.sign_in_duration

    def get_list_book_ids(self):
        book_ids = []
        for book in self.list_scans:
            book_ids.append(book.id)
        return book_ids