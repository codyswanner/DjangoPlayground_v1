import re
from time import sleep

"""
The purpose of this program is to take an input .csv file (here named input.csv) that was downloaded from Google Sheets and
reformat it into the output file (here named output.txt).  The program replaces Google Sheets' default field separator (comma)
with a new custom separator (semicolon), working under the assumption that new fields will begin with a character that is not
a space, double quote, or newline.

Note that the file format must be changed to .txt for python to accept it.
You may change the files back to .csv after the program has finished.

This works as expected for the library catalog I am currently building, and facilitates transfer of data from
Google Sheets to MySQL.

An example of an input and output line for this program

this,line,is,separated,by,commas,but,should,be,semicolons
this;line;is;separated;by;commas;but;should;be;semicolons


Following blank spaces escape this rule, such as in

this,line, has,an,exception
this;line, has;an;exception

and double quotes are removed with prejudice, such as

this,"line includes",double,quotes
this;line includes;double;quotes



The specific book title presenting bugs when exporting from Google Sheets (and thus inspriring this program) is
31,"Will Grayson, Will Grayson",David,,Levithan,Realistic Fiction,Young Adult Fiction,,English,1A,John,,Green,,,,0,

Which becomes
31;Will Grayson, Will Grayson;David;;Levithan;Realistic Fiction;Young Adult Fiction;;English;1A;John;;Green;;;;0;

which is much easier for me to import into MySQL.
"""

new_data = open('output.csv', 'w')

with open('input.csv', 'r+') as load_data:
    load_data.seek(0)

    for line in load_data.readlines():
        contents = line

        # This while block converts commas acting as field separators into semicolons.
        while re.search(r',[^\s]', contents):
            for i in range(0, len(contents)):
                if i + 1 < len(contents):
                    if contents[i] == "," and contents[i + 1] != " ":
                        substring1 = contents[:i]
                        substring2 = contents[i + 1:]
                        contents = substring1 + ";" + substring2
        # This version of the program uses print statements to track progress and aid in debugging.
        # sleep function is used to enable human reading of print statements in real time (they go real fast otherwise).
        # tbh... the debugging part is done, I just enjoy watching the print statements, and that's why they're still here.
        print("completed first loop")
        sleep(.1)

        # This while block strips double quotes with prejudice.
        while re.search(r';".+";', contents):
            print("entering loop")
            sleep(.2)
            for i in range(0, len(contents)):
                if i < len(contents):
                    if contents[i] == "\"":
                        print("double quote found at index" + str(i))
                        substring1 = contents[:i]
                        print(substring1)
                        substring2 = contents[i + 1:]
                        print(substring2)
                        contents = substring1 + substring2
                        print(contents)
                    else:
                        print("not a double quote at index " + str(i))
                        sleep(.1)
        print("completed second loop")
        sleep(.1)

        # Write the data to the new file (output.csv)
        new_data.write(contents)
