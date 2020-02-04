class ReadTxtFiles(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), encoding='utf-8'):
                yield line

