import math
from datetime import datetime
import tkinter as tk
from Gui import HistogramApp
FILE_EXTENSION = ".csv"               #get datetime class in datetime library 

hanley_vehicle_count_byhour = {}
elm_vehicle_count_byhour = {}

#task A

def validate_date_input():
    while True:                                      #prompt the day by user
        validate_date_input = input("Please enter the day of the survey in the format dd: ")

        if not validate_date_input.isdigit():
            print("Integer required")
            continue

        day = int(validate_date_input)                                                            
        if not ( day >= 1 and day <= 31):
            print("Out of range = values must be in the range 1 and 31")
            continue
        
        return validate_date_input


def validate_month_input():
    while True:                                        #prompt the day by user
        validate_month_input = input("Please enter the month of the survey in the format mm: ")

        if not validate_month_input.isdigit():
            print("Integer required")
            continue

        month = int(validate_month_input)                                                            
        if not ( month >= 1 and month <= 12):
            print("Out of range = values must be in the range 1 and 12")
            continue

        return validate_month_input


def validate_year_input():
    while True:                                          #prompt the day by user
        validate_year_input = input("Please enter the day of the survey in the format yyyy: ")

        if not validate_year_input.isdigit():
            print("Integer required")
            continue

        year = int(validate_year_input)                                                            
        if not ( year >= 2000 and year <= 2024):
            print("Out of range = values must be in the range 2000 and 2024")
            continue

        return validate_year_input



#task B

def process_csv_data(filename):
        global hanley_vehicle_count_byhour,elm_vehicle_count_byhour
        file_path = filename +  FILE_EXTENSION
    
        #read csv file
        try:
            with open(file_path,"r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Error : The file {file_path} was not found.Try again!") 
            return None
    
        #extract the header[0] and, with split separate elements with commas and strip remove white spaces
        header = lines[0].strip().split(',')    #column names  
    
        data = []
        for line in lines[1:]:   #skip the 0 index and 1 to last row 
            data.append(line.strip().split(","))
    
        
        #find the index of each column
        junction_name_index = header.index("JunctionName")
        time_of_day_index = header.index("timeOfDay")
        travel_direction_in_index = header.index("travel_Direction_in")
        travel_direction_out_index = header.index("travel_Direction_out")
        weather_index = header.index("Weather_Conditions")
        juction_speed_limit_index = header.index("JunctionSpeedLimit")
        vehicle_speed_index = header.index("VehicleSpeed")
        vehicle_type_index = header.index("VehicleType")
        electric_hybrid_index = header.index("elctricHybrid")
    
        #Initialize counts
        total_no_of_vehicles = len(data)
        no_of_trucks = 0
        no_of_electric_vehicles = 0
        no_of_two_wheels = 0
        no_of_busses_headingto_north = 0
        no_of_vehicles_notturning = 0
        times = []
        no_of_bikes = 0
        no_of_vehicles_overthe_speed = 0
        vehicles_through_elm = 0
        vehicles_through_hanley = 0
        scooters_through_elm = 0
        
        rain_hours = set()      #set use to store unique values
    
    

        for row in data:

            #truck count
            if row[vehicle_type_index] == "Truck":
                no_of_trucks += 1

        
            #electric vehicle count
            if row[electric_hybrid_index] == "True":
                no_of_electric_vehicles += 1

        
            #two-wheeled vehicle count
            if row[vehicle_type_index] in ["Bicycle","Motorcycle","Scooter"]:
                no_of_two_wheels += 1

        
            #buses heading north
            if ((row[vehicle_type_index] == "Buss") &
                (row[travel_direction_out_index] == "N")):
                    no_of_busses_headingto_north += 1

        
            #vehicles not turning
            if row[travel_direction_in_index] == row[travel_direction_out_index]:
                no_of_vehicles_notturning += 1

        
            #datetime.strptime used to string into a datetime object 
            #take two arguments
            time = datetime.strptime(row[time_of_day_index],"%H:%M:%S")
            times.append(time)
    
        
            #bikes count
            if row[vehicle_type_index] == "Bicycle":
                no_of_bikes += 1


            #speed limit
            if float(row[juction_speed_limit_index]) < float(row[vehicle_speed_index]):
                no_of_vehicles_overthe_speed += 1

        
        
            #count per junction and scooter count in hanley
            if row[junction_name_index] == "Elm Avenue/Rabbit Road":
                vehicles_through_elm += 1
                hour = time.hour
                if hour not in elm_vehicle_count_byhour:
                    elm_vehicle_count_byhour[hour] = 0
                elm_vehicle_count_byhour[hour] += 1


            elif row[junction_name_index] == "Hanley Highway/Westway":
                vehicles_through_hanley += 1

                hour = time.hour
                if hour not in hanley_vehicle_count_byhour:
                    hanley_vehicle_count_byhour[hour] = 0
                hanley_vehicle_count_byhour[hour] += 1



            #scooter_count_through_elm
            if ((row[junction_name_index] == "Elm Avenue/Rabbit Road") &
                (row[vehicle_type_index] == "Scooter")):
                scooters_through_elm += 1
    


            #calculate percentage of trucks
            #ternary operater first you check if total_no_of_vehicles > 0 then percentage_of_trucks, if not, percentage_of_trucks = 0
            percentage_of_trucks = round(no_of_trucks / total_no_of_vehicles * 100) if total_no_of_vehicles > 0 else 0
    
 
 
            #calculate average bikes per hour
            total_h = ((max(times) - min(times)).total_seconds() / 3600 ) if times else 0
            average_bikes_per_hour = round(no_of_bikes / total_h ) if total_h > 0 else 0
    
 
 
            #calculate percentage of scooters_elm
            percentage_of_scooters_elm = math.floor(scooters_through_elm / vehicles_through_elm * 100) if vehicles_through_elm > 0 else 0
        
 
 
            #calculate higheset_no_of_vehicles_inanhour_hanley
            #check dictionary is nonempty
            if hanley_vehicle_count_byhour:
                #find the key dictionary with maxvalue
                max_hour = max(hanley_vehicle_count_byhour, key = hanley_vehicle_count_byhour.get)
                max_count = hanley_vehicle_count_byhour[max_hour]
                max_hour = f'{max_hour}:00 and {int(max_hour + 1)}:00'
            else:
                #if dictionary is empty
                max_hour = None
                max_count = 0
        
  
            #rain_hours
            if "rain" in row[weather_index].lower():
                rain_hours.add(time.hour)

            no_of_hours_rain = len(rain_hours)

    
        return {
            'data file selected is {}': filename,
            'The total vehicles recorded for this date is {}' : total_no_of_vehicles,
            'The total trucks recorded for this date is {}' : no_of_trucks,
            'The total electric vehicles recorded for this date is {}' : no_of_electric_vehicles,
            'The total two-wheeled recorded for this date is {}' : no_of_two_wheels,
            'The total Buses leaving Elm Avenue/Rabbit Road is {}' : no_of_busses_headingto_north,
            'The total Vehicles through both juction not turning left or right is is {}' : no_of_vehicles_notturning,
            'The percentage of total vehicles recorded that are trucks for this date is {}%' : percentage_of_trucks,
            'The average number of Bikesper hour for this date is {}' : average_bikes_per_hour,
            'The total number of vehicles  recorded as over the speed limit for this date is {}' : no_of_vehicles_overthe_speed,
            'The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {}' : vehicles_through_elm,
            'The total number of vehicles recorded through Hanley Highway/Westway junction is {}' : vehicles_through_hanley,
            '{}% of vehicles recorded through Elm Avenue/Rabbit Road are  scooters.' : percentage_of_scooters_elm,
            'The highest number of vehicles in an hour on Hanley Highway/Westway is {}' : max_count,
            'The most vehicles through Hanley Highway/Westway were recorded between {}' : max_hour,
            'The number of hours of rain for this date is {}' : no_of_hours_rain
            }
    


def display_outcomes(outcomes):
    for key, value in outcomes.items():
        print(key.format(value))



#save to a textfile
def save_outcomes_to_file(outcomes,filename = "result.txt"):
    with open(filename, "a") as file:
        #write a new line to file
        for key,value in outcomes.items():
            file.write(key.format(value) + "\n")
            
        file.write("\n*****************\n")

    print()
    print("Text has been appended to the file. ")


#clear vehicle counts in dictionaries (task E)
def clear_vehiclecount():
    global hanley_vehicle_count_byhour,elm_vehicle_count_byhour
    hanley_vehicle_count_byhour.clear()
    elm_vehicle_count_byhour.clear()
    return("vehicle counts has been cleared. ")


while True:

    day = validate_date_input()
    month = validate_month_input()
    year = validate_year_input()

    #data = process_csv_data("traffic_data15062024.csv")
    #display_outcomes(data)
    
    #save_outcomes_to_file(data) 
    
    csv_file_name = "traffic_data" + day + month + year
    csv_data = process_csv_data(csv_file_name)
    if csv_data is not None:
        display_outcomes(csv_data)
        save_outcomes_to_file(csv_data) 
    
        #tkinter use
        root = tk.Tk()
        date = "{}/{}/{}".format(day, month, year)
        app = HistogramApp(root, elm_vehicle_count_byhour, hanley_vehicle_count_byhour, date)    #data_1,data_2
        root.mainloop()
    
    
    user_input_another_round =  input("Do you want to select another data file for a different data? Y/N  ").lower()
    if user_input_another_round == "y":
       clear_vehiclecount()
       continue
    elif user_input_another_round == "n":
        print("End of the run")
        break
    else:
        print("Invalid! Please enter 'Y' or 'N' ")

    