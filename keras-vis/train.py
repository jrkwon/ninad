#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from drive_train import DriveTrain
    
#'../mir_torcs_drive_data/2017-05-31-20-49-09' 

###############################################################################
#       
def main():
    try:
        if (len(sys.argv) != 2):
            print('Give a folder name of drive data.')
            return
        
        drive_train = DriveTrain(sys.argv[1])
        drive_train.train(show_summary=False)    

    except KeyboardInterrupt:
        print ('\nShutdown requested. Exiting...')
       

###############################################################################
#       
if __name__ == '__main__':
    main()
