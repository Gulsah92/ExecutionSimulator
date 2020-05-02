


class Binary:
    binl = []

    def __init__(self, file_path):
        # Keeps a flag for format errors, we set it to False when we find a formatting error
        # in given .asm file and break without creating .bin file
        format_check = True

        # Gets program name and file path as arguments
        # (Only the file name can be entered if the file is at the same directory)
        self.file_path = file_path

        # Removes extension and extracts file name from path
        file_name = file_path.split('.')[0].split('\\')[-1]

        # Reads the file if file cannot be opened throws 'File could not be found' exception
        try:
            binfile = open(file_path, 'r')
        except:
            print('File "' + file_name + '" could not be found!')
            format_check = False

        # For every line in code file, remove new line characters
        # append every line as string to binl list
        for line in binfile:
            line = line.split('\n')
            tmpl = [line[0][0:6], line[0][6:8], line[0][8:]]
            self.binl.append(tmpl)

        binfile.close()



