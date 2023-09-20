import sys
import os
import csv
import glob

# CHECK ARGS
if len(sys.argv) < 3:
    print("Please provide the folder path and the word as command-line arguments.")
else:
    # Extract folder path, word, and inp from command-line arguments
    folder_path = sys.argv[1]
    word = sys.argv[2]
    inp = sys.argv[3]

    # SUBFOLDERS
    subfolders = glob.glob(os.path.join(folder_path, "*"))

    # Store average results for each unique name
    name_averages = {}

    # Iterate over each subfolder
    for subfolder in subfolders:
        # Construct path to "True" folder and find CSV files containing the specified word
        true_folder_path = os.path.join(subfolder, "True")
        true_files = glob.glob(os.path.join(true_folder_path, f"*{word}*.csv"))

        # Initialize lists for matching rows
        folder_matching_rows = []
        true_matching_rows = []

        # Iterate over each true file found (there is only one)
        for true_file in true_files:

            # find prediction file by going to subfolder (prediction date)
            folder_file = glob.glob(os.path.join(subfolder, f"*{word}*.csv"))

            # open other dependencies for the program to work
            with open(folder_file[0], 'r') as csv_file, open(true_file, 'r') as td_data, \
                    open("./names", 'r') as names_file, \
                    open("./loc8", 'r') as loc8_file, \
                    open("./loc7", 'r') as loc7_file:

                csv_reader = csv.reader(csv_file)
                td_reader = csv.reader(td_data)

                # Read lines from additional files
                names_lines = names_file.readlines()
                loc8_lines = loc8_file.readlines()
                loc7_lines = loc7_file.readlines()

                # Skip the first 5 rows in CSV files
                for _ in range(5):
                    next(csv_reader)
                    next(td_reader)

                # Store rows from CSV and true data files in separate lists
                csv_rows = list(csv_reader)
                td_rows = list(td_reader)

                # Iterate over lines from additional files
                for i in range(18):
                    loc8_line = loc8_lines[i].rstrip()
                    loc7_line = loc7_lines[i].rstrip()
                    name = names_lines[i].rstrip()

                    # Find matching rows in CSV file based on loc7 and loc8 values
                    for row_csv in csv_rows:
                        if row_csv[8].startswith(loc8_line) and row_csv[7].startswith(loc7_line):
                            if (row_csv[18] == ''):
                                break
                            folder_matching_rows.append({
                                'loc7': row_csv[7],
                                'loc8': row_csv[8],
                                'speed': float(row_csv[1]),
                                'gust': float(row_csv[18]),
                                'dir': float(row_csv[2]),
                                'name': name
                            })
                            break

                    # Find matching rows in true data file based on loc7 and loc8 values
                    for row_td in td_rows:
                        if row_td[8].startswith(loc8_line) and row_td[7].startswith(loc7_line):
                            if (row_csv[18] == ''):
                                break
                            true_matching_rows.append({
                                'loc7': row_td[7],
                                'loc8': row_td[8],
                                'speed': float(row_td[1]),
                                'gust': float(row_td[18]),
                                'dir': float(row_td[2]),
                                'name': name
                            })
                            break

        # Create pairs of matching rows
        pairs = []
        folder_names = {}
        true_names = {}

        for row in folder_matching_rows:
            name = row['name']
            if name in folder_names:
                folder_names[name].append(row)
            else:
                folder_names[name] = [row]

        for row in true_matching_rows:
            name = row['name']
            if name in true_names:
                true_names[name].append(row)
            else:
                true_names[name] = [row]

        for name, folder_rows in folder_names.items():
            if name in true_names:
                true_rows = true_names[name]
                for folder_row in folder_rows:
                    for true_row in true_rows:
                        pair = (folder_row, true_row)
                        pairs.append(pair)

        # Calculate result and store average results for each name

        for folder_row, true_row in pairs:
            result = abs(folder_row[inp] - true_row[inp])

            if (inp == 'dir'):
                diff = abs(folder_row[inp] - true_row[inp]) % 360
                if diff > 180:
                    diff = 360 - diff
                result = (diff / 3.6)

            if folder_row['name'] in name_averages:
                name_averages[folder_row['name']].append(result)
            else:
                name_averages[folder_row['name']] = [result]


    # Print average results for each unique name
    print("\n--- Average Results ---")
    for name, results in name_averages.items():
        avg_result = sum(results) / len(results)
        print("{:.2f}".format(avg_result))
