import sys,os, argparse,time
from datetime import timedelta
import logging
import csv

def argsParser():
    parser = argparse.ArgumentParser(description='Python 3  -- split large csv file into smaller files')
    parser.add_argument('--csv_large_file_input', '-i', required = True, help = "CSV large file input path.")
    parser.add_argument('--file_rows', '-r', required = True,type=int, help = "File rows to record in smaller files.")
    return parser.parse_args()

def main():
    arguments = argsParser()
    output_folder = os.path.dirname(arguments.csv_large_file_input)
    filename = os.path.basename(arguments.csv_large_file_input)
    (file, ext) = os.path.splitext(filename)
    output_file_prefix = file + "_SPLIT"
    split_csv(arguments.csv_large_file_input,output_folder,output_file_prefix,arguments.file_rows)
    print("CSV smaller files output path = {}".format(output_folder))
        
 
def split_csv(source_filepath, dest_folder, split_file_prefix, records_per_file):

    if records_per_file <= 0:
        raise Exception('records_per_file must be > 0')

    with open(source_filepath, 'r') as source:
        reader = csv.reader(source)
        headers = next(reader)
        file_idx = 0
        records_exist = True
    
        while records_exist:
            i = 0
            target_filename = f'{split_file_prefix}_{file_idx}.csv'
            target_filepath = os.path.join(dest_folder, target_filename)

            with open(target_filepath, 'w', newline='') as target:
                writer = csv.writer(target)

                while i < records_per_file:
                    if i == 0:
                        writer.writerow(headers)
                    try:
                        writer.writerow(next(reader))
                        i += 1
                    except:
                        records_exist = False
                        break

            if i == 0:
                # if has only header, the file will be deleted.
                os.remove(target_filepath)

            file_idx += 1

if __name__ == '__main__':
    sys.exit(main())