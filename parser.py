#!/usr/bin/python3.8

import sys
import re

class Parser:
    """
        parser contains lists of room info and links
        room is dic with keys {start_bool:bool, room_name:str, y:int , x:int}
        links is lists [room1, room2]
    """
    def __init__(self, args):
      
        self.check_args(args)
        self.get_data()
        
    def check_args(self, args):
        if len(args) == 1:
            self.error_exit("config file missing")
        self.file = args[1]
        if not self.file.endswith('.map'):
            self.error_exit("wrong file extension")
        self.map_file = self.file

    def get_data(self):
        with open(self.map_file, 'r') as reader:
            lines = reader.readlines()
        if len(lines) == 0:
            self.error_exit("file empty")
        lines = [x.strip('\n') for x in lines]
       


    #chyeck if anything after other than ##
    def create_dict(self, lines, i):
            #check if 3
            keys = ['room_name', 'y', 'x']
            vals = lines[i].split(" ")
            d = {key:val for key,val in zip(keys, vals)}
            return d

    def error_exit(self, error_msg):
        print(error_msg)
        sys.exit()



        #for line in lines[1:]:

            

        print("success")
        
        """"data = input()
        if not data.isdigit():
            print("1st input must be an int")
            sys.exit()"""
        

      
def intro():
    print("WELCOME TO LEM-IN PROGRAM")
    print("1) get info from map file with Parser class")
    help(Parser)


def main(args):

    #intro()
    parser1 = Parser(args)
    print(parser1.__dict__)
    
    


if __name__ == '__main__':
    main(sys.argv)