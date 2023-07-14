from typing import List, Dict, Optional
from datetime import datetime


# Sample View from User's Perspective
'''Welcome to the Health Information System
 1. Display all patient data
 2. Display patient data by ID
 3. Add patient data
 4. Display patient statistics
 5. Find visits by year, month, or both
 6. Find patients who need follow-up
 7. Delete all visits of a particular patient
 8. Quit
 Enter your choice (1-8): '''

def readPatientsFromFile(patients):
    try:
        # Open the file for reading
        with open(patients, 'r') as f:
            # Create an empty dictionary to store the patient data
            patientData = {}
            # Read each line in the file
            for line in f:
                # Remove any whitespace and split the line into fields
                fields = line.strip().split(',')
                # Check if the line has the correct number of fields
                if len(fields) != 8:
                    print(f"Invalid number of fields ({len(fields)}) in line: {line.strip()}")
                    continue
                # Extract the patient ID from the first field
                try:
                    patientID = int(fields[0])
                except ValueError:
                    print(f"Invalid data type in line: {line.strip()}")
                    continue
                # Extract the visit data from the remaining fields
                try:
                    visitData = [fields[1], float(fields[2]), int(fields[3]), int(fields[4]), int(fields[5]), int(fields[6]), int(fields[7])]
                except (ValueError, IndexError):
                    print(f"Invalid data type in line: {line.strip()}")
                    continue
                # Check that the visit data is within the valid ranges
                if not (30 <= visitData[1] <= 43):
                    print(f"Invalid temperature value ({visitData[1]}) in line: {line.strip()}")
                    continue
                if not (30 <= visitData[2] <= 200):
                    print(f"Invalid heart rate value ({visitData[2]}) in line: {line.strip()}")
                    continue
                if not (5 <= visitData[3] <= 60):
                    print(f"Invalid respiratory rate value ({visitData[3]}) in line: {line.strip()}")
                    continue
                if not (50 <= visitData[4] <= 250):
                    print(f"Invalid systolic blood pressure value ({visitData[4]}) in line: {line.strip()}")
                    continue
                if not (30 <= visitData[5] <= 150):
                    print(f"Invalid diastolic blood pressure value ({visitData[5]}) in line: {line.strip()}")
                    continue
                if not (80 <= visitData[6] <= 100):
                    print(f"Invalid oxygen saturation value ({visitData[6]}) in line: {line.strip()}")
                    continue
                # Add the visit data to the patient's list of visits
                if patientID in patientData:
                    patientData[patientID].append(visitData)
                else:
                    patientData[patientID] = [visitData]
            return patientData
    except FileNotFoundError:
        print(f"The file '{patients}' could not be found.")
    except:
        print("An unexpected error occurred while reading the file.")


def displayPatientData(patients, patientId=0):
    """
    Displays patient data for a given patient ID or for all patients if patientId is 0.

    patients: A dictionary of patient dictionaries, where each patient has a list of visits.
    patientId: The ID of the patient to display data for. If 0, data for all patients will be displayed.
    """

    if not isinstance(patients, dict):
        print("Error: patients argument is not a dictionary")
        return

    if patientId != 0 and (not isinstance(patientId, int) or patientId < 0):
        print("Error: patientId must be a non-negative integer or 0")
        return

    if patientId != 0 and patientId not in patients:
        print(f"Patient with ID {patientId} not found.")
        return

    for patient_id, patient_data in patients.items():
        if patientId == 0 or patient_id == patientId:
            print("Patient ID:", patient_id)
            for visit in patient_data:
                print(" Visit Date:", visit[0])
                print("  Temperature:", "%.2f" % visit[1], "C")
                print("  Heart Rate:", visit[2], "bpm")
                print("  Respiratory Rate:", visit[3], "bpm")
                print("  Systolic Blood Pressure:", visit[4], "mmHg")
                print("  Diastolic Blood Pressure:", visit[5], "mmHg")
                print("  Oxygen Saturation:", visit[6], "%")

def displayStats(patients, patientId=0):
    """
    Prints the average of each vital sign for all patients or for the specified patient.

    patients: A dictionary of patient IDs, where each patient has a list of visits.
    patientId: The ID of the patient to display vital signs for. If 0, vital signs will be displayed for all patients.
    """
    if not isinstance(patients, dict):
        print("Error: 'patients' should be a dictionary.")
        return
    if not patientId.isdigit():
        print("Error: 'patientId' should be an integer.")
        return
    patientId = int(patientId)

    if patientId == 0:
        temp_sum, hr_sum, rr_sum, sbp_sum, dbp_sum, os_sum, num_visits = 0, 0, 0, 0, 0, 0, 0
        for visits in patients.values():
            for visit in visits:
                print(visit)
                temp_sum += visit[1]
                hr_sum += visit[2]
                rr_sum += visit[3]
                sbp_sum += visit[4]
                dbp_sum += visit[5]
                os_sum += visit[6]
                num_visits += 1
        if num_visits == 0:
            print("No data found.")
            return
        print("Vital Signs for All Patients:")
    elif patientId in patients:
        temp_sum, hr_sum, rr_sum, sbp_sum, dbp_sum, os_sum, num_visits = 0, 0, 0, 0, 0, 0, 0
        for visit in patients[patientId]:
            temp_sum += visit[1]
            hr_sum += visit[2]
            rr_sum += visit[3]
            sbp_sum += visit[4]
            dbp_sum += visit[5]
            os_sum += visit[6]
            num_visits += 1
        if num_visits == 0:
            print("No data found for patient with ID {}.".format(patientId))
            return
        print("Vital Signs for Patient {}:".format(patientId))
    else:
        print("No data found for patient with ID {}.".format(patientId))
        return

    print("  Average temperature:", "%.2f" % (temp_sum / num_visits), "C")
    print("  Average heart rate:", "%.2f" % (hr_sum / num_visits), "bpm")
    print("  Average respiratory rate:", "%.2f" % (rr_sum / num_visits), "bpm")
    print("  Average systolic blood pressure:", "%.2f" % (sbp_sum / num_visits), "mmHg")
    print("  Average diastolic blood pressure:", "%.2f" % (dbp_sum / num_visits), "mmHg")
    print("  Average oxygen saturation:", "%.2f" % (os_sum / num_visits), "%")


def addPatientData(patients, patientId, date, temp, hr, rr, sbp, dbp, spo2, fileName):
    """
    Adds new patient data to the patient list by appending to the dictionary and by appending to the text file

    patients: The dictionary of patient IDs, where each patient has a list of visits, to add data to.
    patientId: The ID of the patient to add data for.
    date: The date of the patient visit in the format 'yyyy-mm-dd'.
    temp: The patient's body temperature.
    hr: The patient's heart rate.
    rr: The patient's respiratory rate.
    sbp: The patient's systolic blood pressure.
    dbp: The patient's diastolic blood pressure.
    spo2: The patient's oxygen saturation level.
    fileName: The name of the file to append new data to.
    """
    if temp < 35.0 or temp > 42.0:
        print("Invalid temperature. Please enter a temperature between 35.0 and 42.0 Celsius.")
        return

    # Check input values for errors
    try:
        patientId = int(float(patientId))
        temp = float(temp)
        hr = int(hr)
        rr = int(rr)
        sbp = int(sbp)
        dbp = int(dbp)
        spo2 = int(spo2)
    except ValueError:
        print(
            "Invalid input. Please enter numeric values for patient ID, temperature, heart rate, respiratory rate, systolic blood pressure, diastolic blood pressure, and oxygen saturation.")
        return

    if spo2 < 70 or spo2 > 100:
        print("Invalid oxygen saturation. Please enter an oxygen saturation between 70 and 100%.")
        return

    # Check date format and value
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date. Please enter a valid date in the format 'YYYY-MM-DD'.")
        return

    # Add new patient visit to the patient's visit history
    if patientId in patients:
        patients[patientId].append([date, temp, hr, rr, sbp, dbp, spo2])
    else:
        patients[patientId] = [[date, temp, hr, rr, sbp, dbp, spo2]]

    # Append the new data to the text file
    with open(fileName, 'a') as f:
        f.write(f"{patientId},{date},{temp:.1f},{hr},{rr},{sbp},{dbp},{spo2}\n")

    print(f"Visit is saved successfully for Patient #{patientId}")


def findVisitsByDate(patients, year=None, month=None):
    """
    Find visits by year, month, or both.

    patients: A dictionary of patient IDs, where each patient has a list of visits.
    year: The year to filter by.
    month: The month to filter by.
    return: A list of tuples containing patient ID and visit that match the filter.
    """
    visits = []
    for patient_id, patient_visits in patients.items():
        for visit in patient_visits:
            try:
                date = datetime.strptime(visit[0], '%Y-%m-%d')
                if year and date.year != year:
                    continue
                if month and date.month != month:
                    continue
                visits.append((patient_id, visit))
            except ValueError:
                pass

    return visits

def findPatientsWhoNeedFollowUp(patients):
    """
    Find patients who need follow-up visits based on abnormal vital signs.

    patients: A dictionary of patient IDs, where each patient has a list of visits.
    return: A list of patient IDs that need follow-up visits due to abnormal health stats.
    """
    followup_patients = []
    for patient_id in patients:
        for visit in patients[patient_id]:
            heart_rate = visit[2]
            systolic = visit[4]
            diastolic = visit[5]
            oxygen_sat = visit[6]
            if heart_rate > 100 or heart_rate < 60 or systolic > 140 or diastolic > 90 or oxygen_sat < 90:
                followup_patients.append(patient_id)
                break
    return followup_patients

def deleteAllVisitsOfPatient(patients, patientId, filename):

    """ Delete all visits of a particular patient.

    patients: The dictionary of patient IDs, where each patient has a list of visits, to delete data from.
    patientId: The ID of the patient to delete data for.
    filename: The name of the file to save the updated patient data.
    return: None
    """
    # check if patientId exists in patients dictionary
    if patientId not in patients:
        print(f"No data found for patient with ID {patientId}")
        return

    # delete patient's visits from patients dictionary
    patients[patientId] = []

    # update patient data file
    with open(filename, "w") as file:
        for id, visits in patients.items():
            for visit in visits:
                line = f"{id},{visit['date']},{visit['temp']},{visit['hr']},{visit['rr']},{visit['sbp']},{visit['dbp']},{visit['spo2']}\n"
                file.write(line)

    print(f"Data for patient {patientId} has been deleted.")


def main():
    patients = readPatientsFromFile('patients.txt')
    while True:
        print("\n\nWelcome to the Health Information System\n\n")
        print("1. Display all patient data")
        print("2. Display patient data by ID")
        print("3. Add patient data")
        print("4. Display patient statistics")
        print("5. Find visits by year, month, or both")
        print("6. Find patients who need follow-up")
        print("7. Delete all visits of a particular patient")
        print("8. Quit\n")

        choice = input("Enter your choice (1-8): ")
        if choice == '1':
            displayPatientData(patients)
        elif choice == '2':
            patientID = int(input("Enter patient ID: "))
            displayPatientData(patients, patientID)
        elif choice == '3':
            patientID = int(input("Enter patient ID: "))
            date = input("Enter date (YYYY-MM-DD): ")
            try:
                temp = float(input("Enter temperature (Celsius): "))
                hr = int(input("Enter heart rate (bpm): "))
                rr = int(input("Enter respiratory rate (breaths per minute): "))
                sbp = int(input("Enter systolic blood pressure (mmHg): "))
                dbp = int(input("Enter diastolic blood pressure (mmHg): "))
                spo2 = int(input("Enter oxygen saturation (%): "))
                addPatientData(patients, patientID, date, temp, hr, rr, sbp, dbp, spo2, 'patients.txt')
            except ValueError:
                print("Invalid input. Please enter valid data.")
        elif choice == '4':
            patientID = input("Enter patient ID (or '0' for all patients): ")
            displayStats(patients, patientID)
        elif choice == '5':
            year = input("Enter year (YYYY) (or 0 for all years): ")
            month = input("Enter month (MM) (or 0 for all months): ")
            visits = findVisitsByDate(patients, int(year) if year != '0' else None,
                                      int(month) if month != '0' else None)
            if visits:
                for visit in visits:
                    print("Patient ID:", visit[0])
                    print(" Visit Date:", visit[1][0])
                    print("  Temperature:", "%.2f" % visit[1][1], "C")
                    print("  Heart Rate:", visit[1][2], "bpm")
                    print("  Respiratory Rate:", visit[1][3], "bpm")
                    print("  Systolic Blood Pressure:", visit[1][4], "mmHg")
                    print("  Diastolic Blood Pressure:", visit[1][5], "mmHg")
                    print("  Oxygen Saturation:", visit[1][6], "%")
            else:
                print("No visits found for the specified year/month.")
        elif choice == '6':
            followup_patients = findPatientsWhoNeedFollowUp(patients)
            if followup_patients:
                print("Patients who need follow-up visits:")
                for patientId in followup_patients:
                    print(patientId)
            else:
                print("No patients found who need follow-up visits.")
        elif choice == '7':
            patientID = input("Enter patient ID: ")
            deleteAllVisitsOfPatient(patients, int(patientID), "patients.txt")
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == '__main__':
    main()