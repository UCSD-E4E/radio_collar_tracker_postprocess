import fileinput

def META_FILE_READER(path, tagVal):
        for line in fileinput.input(path):
            if tagVal == line.strip().split(':')[0].strip():
                fileinput.close()
                return line.strip().split(':')[1].strip()