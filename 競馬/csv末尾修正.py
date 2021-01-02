with open('Database_Horse_Race20201129015523.csv',mode='r',encoding='utf-8') as f:
    with open('Database_Horse_Race20201129015523_reformat.csv', mode='w', encoding='utf-8') as rf:

        f_lines = (f_line.rstrip(',') for f_line in f.readlines())
        print(f_lines)
        #rf.write(f_lines)
        rf.writelines(f_lines)