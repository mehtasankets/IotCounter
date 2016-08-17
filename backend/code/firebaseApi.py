from firebase import firebase
import time
import sys
from threading import Thread

class FirebaseApi:

    def __init__(self, connection):
        self.firebase = firebase.FirebaseApplication(connection, None)

    def postAsync(self, apiPath, data):
        t = Thread(target=self.postRequest, args=(apiPath, data))
        t.daemon = True
        t.start()


    def postRequest(self, apiPath, data):
        try:
            result = self.firebase.patch(apiPath, data=data, params={'print': 'silent'})
        except:
             print('Exception while updating count at firebase: ', sys.exc_info()[0])

    def setTotal(self, total):
            currentDate = time.strftime("%Y%m%d")
            apiPath = '/phoenixBadmintonCounter/' + currentDate
            data = {'total' : total}
            self.postAsync(apiPath, data)
	    print 'set to', total

    def setCounter(self, count):
            currentDate = time.strftime("%Y%m%d")
            currentHour = time.strftime("%H")
            apiPath = '/phoenixBadmintonCounter/' + currentDate
            data = {str(currentHour) : count}
            self.postAsync(apiPath, data)
	    print 'set to', count
