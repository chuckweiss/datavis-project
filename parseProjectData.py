from os import walk, path

def parseProjectData(pathname):
    def list_files(dirpath, files = []):
        for (curdir, dirs, filenames) in walk(dirpath):
            for file in filenames:
                files.append((file, curdir))
            if(len(dirs) > 0):
                for dir in dirs:
                    list_files(dir, files)
        return files

    def parse_data(files, keyword):
        data = {}
        for filename, dirpath in files:
            if filename == keyword:
                subject_id = path.basename(dirpath)
                if subject_id in data:
                    data[subject_id].append(dirpath)
                else:
                    data[subject_id] = [dirpath]
        return data

    files = list_files(pathname)

    return parse_data(files, 'summary.csv')
