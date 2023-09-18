import csv
import json

# Function to convert csv to json
def csv_to_json(file_name): 
    with open(file_name , 'r') as csv_file:
        csv_data=csv.DictReader(csv_file)
        data_list=[row for row in csv_data]
        json_data = json.dumps(data_list, indent=4)
        
    with open('data.json','w') as json_file:
        json_file.write(json_data)

# main function
def main():
    file_name=input()
    csv_to_json(file_name)

if __name__ == '__main__':
    main()