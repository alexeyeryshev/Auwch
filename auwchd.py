#!/usr/bin/python3

import time
import sys
from daemon import Daemon
from auwch import ImageRetriever, WallpaperChanger

class AUWCHDaemon(Daemon):
    PIDFILE = './auwch.pid'
    # LOGFILE = './auwch.log'
    
    delay = 3600
    
    def __init__(self):
        super(AUWCHDaemon, self).__init__(self.PIDFILE)     
    
    def run(self):
        while True:
            img_file_abs_path = ImageRetriever.desktopprImgRetrieve()
            WallpaperChanger.changeWallpaper(img_file_abs_path)
            time.sleep(AUWCHDaemon.delay)

def main():
    
    daemon = AUWCHDaemon()
    
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print('Starting ...')
            # try:
            daemon.start()
            # except:
            #     pass

        elif 'stop' == sys.argv[1]:
            print('Stopping ...')
            daemon.stop()

        elif 'restart' == sys.argv[1]:
            print('Restaring ...')
            daemon.restart()

        elif 'status' == sys.argv[1]:
            try:
                pf = open(AUWCHDaemon.PIDFILE,'r')
                pid = int(pf.read().strip())
                pf.close()
            except IOError:
                pid = None
            except SystemExit:
                pid = None

            if pid:
                print('Auwch is running as pid {}'.format(pid))
            else:
                print('Auwch is not running.')

        else:
            print("Unknown command")
            sys.exit(2)
            sys.exit(0)
    else:
        print("usage: {} start|stop|restart|status".format(sys.argv[0]))
        sys.exit(2)
    
if __name__ == '__main__':
    main()
    