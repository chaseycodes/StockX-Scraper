

import os
import json
import urllib
import time
import random

PATH = 'path_to_images'
BRANDS = ['nike','jordan','adidas','other']
PLACEHOLDER_PATH = 'path_to_placeholder_image'

def img_dwnldr():
    for b in BRANDS:
        with open('{}.json'.format(b)) as file:
            data = json.load(file)
            for key, value in data.items():
                #clean name to save for jpg
                name = key.replace('/','-').replace('?','').strip()
                img_link = data[key]['image']
                if name+'.jpg' in os.listdir(PATH):
                    #no duplicates
                    print 'Already Saved: '+str(counter)
                    pass
                else:
                    """save to static"""
                    #replace placeholder images with own
                    if 'Placeholder' in img_link.split('-'):
                        placeholder = open(PLACEHOLDER_PATH)
                        f = open('static/{}.jpg'.format(name),'wb')
                        f.write(placeholder.read())
                        f.close()
                        print 'Placeholder'
                    else:
                        #download image url
                        f = open('static/{}.jpg'.format(name),'wb')
                        f.write(urllib.urlopen(img_link).read())
                        f.close()   
                        print key
        
                    time.sleep(1/(random.randint(1,100)*10000))

if __name__ == "__main__":
    img_dwnldr()