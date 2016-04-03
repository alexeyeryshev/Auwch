#!/usr/bin/python3

import requests
import datetime
import os
import subprocess

class ImageRetriever():
    def desktopprImgRetrieve():
        image_base_dir = 'images'
        base_url = 'https://api.desktoppr.co'
        # requests.get('{}/{}'.format(base_url, '1/wallpapers/random?safe_filter=all'))
        img_data_url = '{}/{}'.format(base_url, '1/wallpapers/random')
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

class WallpaperChanger(): 
    def changeWallpaper(img_file_abs_path):
        command = 'gsettings'
        sub_command = 'set'
        schema = 'org.gnome.desktop.background'
        arg = 'picture-uri'
        file_uri = 'file://{}'.format(img_file_abs_path)
        subprocess.run([command, sub_command, schema, arg, file_uri])
       
def main(): 
    img_file_abs_path = ImageRetriever.desktopprImgRetrieve()
    WallpaperChanger.changeWallpaper(img_file_abs_path)

if __name__ == '__main__':
    main()
    