#!/usr/bin/python3

import requests
import datetime
import os
import subprocess
import json
import sys
import logging

class ConfService:
    def __init__(self, conf_uri): 
        self.conf_dict = json.load(open(conf_uri, 'r'))
        
    def get_conf(self):
        return self.conf_dict

class ImageRetriever:
    def desktopprImgRetrieve(conf_service):
        conf = conf_service.get_conf() 
        image_base_dir = conf['image_base_dir']
        base_url = conf['desktoppr']['base_url']
        safe = conf['desktoppr']['safe']
        img_data_url = '{}/{}'.format(base_url, conf['desktoppr']['safe_path']) if safe else '{}/{}'.format(base_url, conf['desktoppr']['not_safe_path'])
        logging.info('api url to call {}'.format(img_data_url))
        img_data_resp = requests.get(img_data_url)
        img_data = img_data_resp.json()
        img_url = img_data['response']['image']['url']
        img_resp = requests.get(img_url)
        cur_time = datetime.datetime.now().isoformat()
        img_file_rel_path = '{}/{}.jpg'.format(image_base_dir, cur_time)
        
        if not os.path.exists(image_base_dir):
            os.makedirs(image_base_dir)
        with open(img_file_rel_path, 'wb') as img_file:
            img_file.write(img_resp.content)
        
        img_file_abs_path = os.path.abspath('{}/{}'.format(os.path.curdir, img_file_rel_path))
        return img_file_abs_path

class WallpaperChanger: 
    def changeWallpaper(img_file_abs_path):
        command = 'gsettings'
        sub_command = 'set'
        schema = 'org.gnome.desktop.background'
        arg = 'picture-uri'
        file_uri = 'file://{}'.format(img_file_abs_path)
        subprocess.run([command, sub_command, schema, arg, file_uri])
       
def main(): 
    conf_uri = ''
    if (len(sys.argv) == 2):
        conf_uri = sys.argv[1]
    else:
        conf_uri = 'application.conf'
        
    conf_service = ConfService(conf_uri)
    conf = conf_service.get_conf()
    logging.basicConfig(filename = conf['log_file_path'], level = logging.INFO)
    
    img_file_abs_path = ImageRetriever.desktopprImgRetrieve(conf_service)
    WallpaperChanger.changeWallpaper(img_file_abs_path)

if __name__ == '__main__':
    main()
    