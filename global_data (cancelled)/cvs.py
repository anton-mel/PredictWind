import csv
import sys
import os
import glob
CRED = '\033[91m'
CEND = '\033[0m'

# Check if the correct number of arguments is provided
if len(sys.argv) != 4:
    print("Usage: python script.py <main_folder> <replacement_string> <column_index>")
    sys.exit(1)

main_folder = sys.argv[1]
replacement_string = sys.argv[2]
column_index = int(sys.argv[3])

# INFO TABLE
print(f"Developed by Anton Melnychuk")
print("Table Usage Info-Table\n\n#1    True Wind Speed\n#2    True Wind Direction\n#9    Wave Height\n#10   Wave Direction\n#11   Wave Period\n#18   Wind Gust")
print(CRED+f"Used #: {column_index}"+CEND)

# Iterate over subdirectories in the main folder
for subdirectory in os.listdir(main_folder):
    subdirectory_path = os.path.join(main_folder, subdirectory)

    if not os.path.isdir(subdirectory_path):
        continue

    true_data_files = glob.glob(os.path.join(subdirectory_path, "TrueData", f"*{replacement_string}*.csv"))
    predicted_data_folder = os.path.join(subdirectory_path, "Predicted")

    if len(true_data_files) != 1 or not os.path.isdir(predicted_data_folder):
        continue

    true_data_file = true_data_files[0]
    print("\n") #gap btw

    # Iterate over subfolders in the predicted data folder
    for subfolder in os.listdir(predicted_data_folder):
        subfolder_path = os.path.join(predicted_data_folder, subfolder)

        if not os.path.isdir(subfolder_path):
            continue

        predicted_data_files = glob.glob(os.path.join(subfolder_path, f"*{replacement_string}*.csv"))

        if len(predicted_data_files) != 1:
            continue

        predicted_data_file = predicted_data_files[0]

        with open(true_data_file, 'r') as trueData, open(predicted_data_file, 'r') as predictedData:
            reader1 = csv.reader(trueData)
            reader2 = csv.reader(predictedData)

            # Skip the first four lines in both files
            for _ in range(4):
                next(reader1)
                next(reader2)

            initial_speed = None
            total_difference = 0
            count = 0

            for row1, row2 in zip(reader1, reader2):
                try:
                    tws1 = float(row1[column_index])
                    tws2 = float(row2[column_index])

                    if initial_speed is None:
                        initial_speed = tws1  # Set initial speed from true data file

                    # Calculate the difference and divide by initial speed
                    difference = abs(tws1 - tws2) / initial_speed * 100

                    total_difference += difference
                    count += 1

                except (ValueError, IndexError):
                    pass

            if count > 0:
                average_difference = total_difference / count
                formatted_difference = '{:.2f}'.format(average_difference)
                print("Folder:", subdirectory, "| Subfolder:", subfolder, "| Average Percentage Difference:", formatted_difference,"%")
            else:
                print("Folder:", subdirectory, "| Subfolder:", subfolder, "| No valid data points found.")
