import csv
import re

def look_for_ip(variable,v_type):

    with open('./hosts.csv') as data:
        data = csv.reader(data, delimiter=',')
        line_count=0
        for row in data:
            if v_type == 'IP' and variable == row[1]:
                line_count+=1
                return row[1]

            elif v_type == 'MAC' and variable == row[2]:
                line_count+=1
                return row[1]

            elif v_type == 'HOST' and str(variable)== row[0]:
                line_count+=1
                return row[1]

            elif v_type == 'ID' and str(variable)==str(line_count):
                line_count+=1
                return row[1]
            else:
                line_count+=1

def look_for_host(variable,v_type):

    with open('./hosts.csv') as data:
        data = csv.reader(data, delimiter=',')
        line_count=0
        for row in data:
            if v_type == 'IP' and variable == row[1]:
                line_count+=1
                return row[0]

            elif v_type == 'MAC' and variable == row[2]:
                line_count+=1
                return row[0]

            elif v_type == 'HOST' and str(variable)== row[0]:
                line_count+=1
                return row[0]

            elif v_type == 'ID' and str(variable)==str(line_count):
                line_count+=1
                return row[0]
            else:
                line_count+=1


def look_for_var(variable,v_type):

    with open('./hosts.csv') as data:
        data = csv.reader(data, delimiter=',')
        line_count=0
        for row in data:
            if v_type == 'IP' and variable == row[1]:
                #print('Found database entry: '+row[1]+' ('+str(line_count)+')')
                line_count+=1
                return True

            elif v_type == 'MAC' and variable == row[2]:
                #print('Found database entry: '+row[2]+' ('+str(line_count)+')')
                line_count+=1
                return True

            elif v_type == 'ID' and str(variable)==str(line_count):
                #print('Found device ID: '+str(line_count))
                line_count+=1
                return True

            elif v_type == 'HOST' and str(variable)==row[0]:
                #print('Found database entry: '+str(line_count))
                line_count+=1
                return True

            else:
                line_count+=1

def look_for_mac(variable,v_type):

    with open('./hosts.csv') as data:
        data = csv.reader(data, delimiter=',')
        line_count=0
        for row in data:
            if v_type == 'IP' and variable == row[1]:
                #print('Found database entry: '+row[1]+' ('+str(line_count)+')')
                line_count+=1
                return row[2]

            elif v_type == 'MAC' and variable == row[2]:
                #print('Found database entry: '+row[2]+' ('+str(line_count)+')')
                line_count+=1
                return row[2]

            elif v_type == 'HOST' and str(variable)== row[0]:
                line_count+=1
                return row[2]

            elif v_type == 'ID' and str(variable)==str(line_count):
                #print('Found device ID: '+str(line_count))
                line_count+=1
                return row[2]
            else:
                line_count+=1


def look_for_var_s(variable):

    with open('./hosts.csv') as data:
        data = csv.reader(data, delimiter=',')
        line_count=0
        for row in data:
            if variable == row[1]:
                #print('Found database entry: '+row[1]+' ('+str(line_count)+')')
                line_count+=1
                return True

            elif variable == row[2]:
                #print('Found database entry: '+row[2]+' ('+str(line_count)+')')
                line_count+=1
                return True

            elif str(variable)==str(line_count):
                #print('Found device ID: '+str(line_count))
                line_count+=1
                return True

            elif str(variable)==row[0]:
                #print('Found database entry: '+str(line_count))
                line_count+=1
                return True

            else:
                line_count+=1


