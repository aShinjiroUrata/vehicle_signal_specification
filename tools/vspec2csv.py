#!/usr/bin/python

#
# Convert vspec file to CSV
#

import sys
import vspec
import json
import getopt
import csv
import re

def usage():
    print "Usage:", sys.argv[0], "[-I include_dir] ... [-i prefix:id_file:start_id] vspec_file csv_file"
    print "  -I include_dir              Add include directory to search for included vspec"
    print "                              files. Can be used multiple timees."
    print
    print "  -i prefix:id_file:start_id  Add include directory to search for included vspec"
    print "                              files. Can be used multiple timees."
    print
    print "  --nobranch                  Omit 'branches' and output 'leaves' only."
    print
    print "  --row1pos1only              Omit RowX, PosX items except for Row1 and Pos1"
    print "                              to reduce duplicative lines."
    print
    print " vspec_file                   The vehicle specification file to parse."
    print " csv_file                    The file to output the CSV data to."
    sys.exit(255)

def format_data(json_data):
    Id = '""'
    Type = '""'
    Unit = '""'
    Min = '""'
    Max = '""'
    Desc = '""'
    Enum = '""'
    if (json_data.has_key('id')):
        Id = '"' + str(json_data['id']) + '"'
    if (json_data.has_key('type')):
        Type = '"' + json_data['type'] + '"'
    if (json_data.has_key('unit')):
        Unit = '"' + json_data['unit'] + '"'
    if (json_data.has_key('min')):
        Min = '"' + str(json_data['min']) + '"'
    if (json_data.has_key('max')):
        Max = '"' + str(json_data['max']) + '"'
    if (json_data.has_key('description')):
        Desc = '"' + json_data['description'] + '"'
    if (json_data.has_key('enum')):
        Enum = '"' + ' / '.join(json_data['enum']) + '"'
    return Id + ","+ Type + ","+ Unit + ","+ Min + ","+ Max + ","+ Desc + ","+ Enum

def json2csv(json_data, file_out, parent_signal, _nobranch, _row1pos1only):
    for k in json_data.keys():
        if (_row1pos1only == True):
            pattern = r"Row[2-9]|Pos[2-9]"
            if (re.match(pattern, k)):
                continue

        if (len(parent_signal) > 0):
            signal = parent_signal + "." + k
        else:
            signal = k

        if (json_data[k]['type'] == 'branch'):
            if (_nobranch == False):
                file_out.write(signal + ',' + format_data(json_data[k]) + '\n')
            json2csv(json_data[k]['children'], file_out, signal, _nobranch, _row1pos1only)
        else:
            file_out.write(signal + ',' + format_data(json_data[k]) + '\n')

if __name__ == "__main__":
    # 
    # Check that we have the correct arguments
    #
    opts, args= getopt.getopt(sys.argv[1:], "I:i:", ['nobranch', 'row1pos1only'])
    nobranch = False
    row1pos1only = False

    # Always search current directory for include_file
    include_dirs = ["."]
    for o, a in opts:
        if o == "-I":
            include_dirs.append(a)
        elif o == "-i":
            id_spec = a.split(":")
            if len(id_spec) != 3:
                print "ERROR: -i needs a 'prefix:id_file:start_id' argument."
                usage()

            [prefix, file_name, start_id] = id_spec
            vspec.db_mgr.create_signal_db(prefix, file_name, int(start_id))
        elif o == "--nobranch":
            nobranch = True
        elif o == "--row1pos1only":
            row1pos1only = True
        else:
            usage()

    if len(args) < 2:
        usage()

    csv_out = open (args[1], "w")

    try:
        tree = vspec.load(args[0], include_dirs)
    except vspec.VSpecError as e:
        print "Error: {}".format(e)
        exit(255)

    json2csv(tree, csv_out, "", nobranch, row1pos1only)
    csv_out.write("\n")
    csv_out.close()
