from plyer import notification
from cowin_api import CoWinAPI
import datetime
import time
import csv
import os



class VaccineTracker:
    '''Tracks Vaccine Slots for the given state and districts'''
    def __init__(self,state_id=9):
        '''Default State ID is set to Delhi i.e. 9. 
        To check your State's ID call the class without any parameters and run the get_state_id function'''
        self.cowin=CoWinAPI()
        self.states=self.cowin.get_states()
        self.districts=self.cowin.get_districts(state_id)
        
    def create_notification(self,notification_title,content,icon='',no_of_seconds=10):
        notification.notify(title=notification_title,message=content,app_icon=icon,timeout=no_of_seconds)
    
    def get_state_id(self,state_name):

        for state in self.states['states']:
            if state['state_name'].lower()==state_name.lower():
                return state['state_id']

    def get_district_id(self,district_name):

        for district in self.districts['districts']:
            if district['district_name'].lower()==district_name.lower():
                return district['district_id']



    def check_availability_by_district(self,district_name,age=None,location_list=[]):
        '''Gives the Number of Slots available in a district with the age that is specified'''

        dis_id=self.get_district_id(district_name)

        # Checks the Availabilty for next 45 days
        for no in range(45):
            date_for_vaccine=(datetime.datetime.today() + datetime.timedelta(no)).strftime('%d-%m-%Y')
            available_location=self.cowin.get_availability_by_district(district_id=str(dis_id),min_age_limt=age,date=date_for_vaccine)['centers']
            
            # Iterating through available locations
            for location in available_location:

                # Checking if there are available slots. i.e. available_capacity not equal to 0
                if location['sessions'][0]['available_capacity'] !=0:
                    location_list.append({'Date':date_for_vaccine,'District':district_name.upper(),'Location':location['name'],'Pincode':location['pincode'],'Availability':location['sessions'][0]['available_capacity'],'Vaccine':location['sessions'][0]['vaccine']})
        
        # Returning list of locations where slots are available
        return location_list


def get_states_with_id():
    '''Returns Nested List with ID and STATE'''

    records=[]
    records.append('{:>3} | {:>3}'.format('ID','STATE'))

    for state in CoWinAPI().get_states()['states']:
        records.append('{:>3} | {:>3}'.format(state['state_id'],state['state_name']))
        
    return records                

        
        
if __name__=='__main__':
    
    tracker=VaccineTracker()
    locations=[]
    while True:
        areas=['bangalore rural','bangalore urban','bbmp']

        for area in areas:
            records=tracker.check_availability_by_district(area,18,locations)
        fieldnames=records[0].keys()
        with open('Vaccine.csv','a',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
            f.close()
        
        with open('Vaccine.csv','r') as f:
            reader=csv.DictReader(f)
            for record in reader:
                if int(record['Availability'])>5:
                    tracker.create_notification(notification_title='Slot Found',content='Date: {}\nDistrict: {}\nLocation: {}\nPincode: {}\nAvailable Slots : {}\nVaccine:{}'.format(record['Date'],record['District'],record['Location'],record['Pincode'],record['Availability'],record['Vaccine']),no_of_seconds=3)
                    
            f.close()
        os.remove('Vaccine.csv')
        
    
        
        
    