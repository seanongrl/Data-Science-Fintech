class Song(object):

    def __init__(self, lyrics):
        self.lyrics = lyrics

    def singmeasong(self):
        for line in self.lyrics:
            print(line)
