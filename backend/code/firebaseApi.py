from firebase import firebase
import time
import sys

class FirebaseApi:

    def __init__(self, connection):
        self.firebase = firebase.FirebaseApplication(connection, None)

    def setCounter(self, count):
        try:
            currentDate = time.strftime("%Y%m%d")
            currentHour = time.strftime("%H")
            apiPath = '/phoenixBadmintonCounter/' + currentDate
            data = {str(currentHour) : count}
            result = self.firebase.patch(apiPath, data=data, params={'print': 'silent'})
        except:
             print('Exception while updating count at firebase: ', sys.exc_info()[0])
