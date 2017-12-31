__author__ = 'Aaron'

# Class Description:
#   Update our monsters.txt file and our images folder

from urllib3 import urllib3
import shutil
import os
import json

class image_updater():

    def __init__(self):

        # update monsters.txt here:

        self.json_file = open(os.path.realpath('./monsters.txt'), 'r')
        self.json_object = json.loads(self.json_file.read())

        path = os.path.realpath('images')

        team = ['Sparkling Goddess of Secrets, Kali', 'Holy Night Kirin Princess, Sakuya',
                'Soaring Dragon General, Sun Quan', 'divine law goddess, valkyrie rose']

        for x in range(len(self.json_object)):

        #for x in range(1):

            url = 'https://padherder.com'+self.json_object[x]["image60_href"]
            #print(url)
            name = self.json_object[x]["name"]

            if name in team:
                #if name.islower():
                #    name += 'chibi'

                request = urllib3.PoolManager().request('GET', url)

                #print(os.path.realpath('images2'))

                #is_accessible = os.access(path, os.F_OK)
                #print(is_accessible)

                # if the directory doesn't exist, create the directory - too risky
                #if is_accessible == False:
                #    os.makedirs(os.path.realpath('images2'))

                os.chdir(path)
                #print(path)
                #print(path+'\\'+name+'.png')
                if os.access(path+'/'+name+'.png', os.F_OK) == False:
                    with open(os.path.join(path+'/'+name+'.png'), 'wb') as file:
                        file.write(request.data)
                    request.release_conn()
                else:
                    print(name+'.png already exists.')

if __name__ == '__main__':
    updater = image_updater()