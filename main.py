from read_xlxs import activate, read_csv, write_csv

if __name__ == '__main__':
    write_csv(activate(read_csv('output-mutmam.csv')))
