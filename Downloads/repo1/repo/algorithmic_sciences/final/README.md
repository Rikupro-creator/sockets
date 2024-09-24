# What is the project about?
In its basic form, its creating a server that responds to queries from a client. 
Once given a query, it  performs a search in a txt file. 

# Installation
Dependencies: Install required packages using requirements.txt.

**pip install -r requirements.txt**

# Editing the configuration file

The file  config.py is used to generate the file config.ini which are essential for the basic setttings of the
server. from the config.py you can edit SSL, file path, and path to SSL certificate and key. 
all changes on the server are made via the config.py.

# Running the Server
To run the server simply move the server.py is and on the terminal type the following

**python server.py**

# running client.py
Move into the folder client and in there is client.py file.  In this folder open the terminal from here and
type the following

**python client.py**
It will prompt you for an input. If you put a single string, you  will get a response in  less than 1 millisecond.
Basically, I have set a variable minimum allowable length  of a line (string) to 10 characters.  Anything below that produces responses very fast. 
For the client.py you will have to run the above line if you want a new query. 

# Testing
All the functions that were used in each file were tested using pytest. To see if there are errors run a file as shown below. 

**pytest test-server.py** 

In total there are four test on the final folder and a single test on the client folder.

# SSL authentication
I have set SSL authentication to false as a default. TO change it go to the config file change the setting and run the config file. Ensure that you are in the same folder as the server.py  to begin with. 
Using SSL can be a bit complicated, so I included this to make it simple to use it locally. I have
included a file with the label localhost.cnf. This file makes it easy to create an SSL certificate
and key without needing a password or other configuration. Once you have the file in the same
folder as the server, you run the following line on the terminal.
**openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key -config localhost.cnf**
Note in the folder final, there is a **localhost.cnf**. This is a file that enables SSL certification on the same pc. 
This will create two files, **server.crt** and **server.key** in the folder where you have the server. Do
not forget to cd into the folder of the repository that I would send.
Finally, copy the **server.crt** to the client folder. This way turning SSL to true will work without
errors.

## Installing openssl
To install OpenSSl you can use various commands if you are on linux. For instance this one was written using fedora 40 linux distro.
The command to install openssl in fedora 40 is shown below.

**sudo dnf install openssl**
If you are on Arch linux the command is shown below
 **sudo pacman -S openssl**
 if you are in Ubuntu the following will work for you
 **sudo apt install openssl**

 Unfortunately, I do not have a windows pc which I can use to confirm the installation. Using the approach that I highlighted above I was able to create an SSL certificate and Key which  can be used on any pc. If you want to try it, you can go through the whole process. Otherwise, the code is a standalone. 

## Daemonizing
I have this code here.

"""
[Unit]
Description=Server Service

[Service]
Restart=always
WorkingDirectory=/your/working/directory
ExecStart=/usr/bin/python3 server.py

[Install]
WantedBy=multi-user.target
"""
For the above code here is hwo to edit it appropriately.
The working directory can  be edited to suit where you will save the folder with the server.py and the other files.
the **ExecStart** takes two arguments  the first is the path to the python bin and the second the name of the serverfile.
In this case, we have set it to server.py. If you cannot get the python bin folder use run the file **get_path.py** it will help you get
the path to python bin. 

Once you have edited it, you need to create a new file in this folder /etc/systemd/system/ with the extension .service. 
eg. server1.service. 

Now type the following commands in your terminal (assuming you used the name server1.service)

	1. sudo systemctl enable server1.service
	2. sudo systemctl start server1.service

if you are interested with knowing whether it started use the collowing command

**sudo systemctl status server1.service**

In case of any error, you will see after this command. And if, by any chance you wanted to stop the service run the following command.

**sudo systemctl stop server1.service**

# Other files in the  folder
In addition to pytest files, there are files 200k_download.py and generate.py. The latter generates data that  resembles the 200k provided as an example. The former, downloads the 200k files provided as an example. I recommend using the 200k_download to download other files.
 **Note, generate.py takes a very long time to produce outputs.**

There are also output files. They have different names. Those with the extension .csv are produces tables showing different speeds of different algorithms. The images are used for the report. 

The file **string_search.py** has all the algorithms used in the task. For speed testing of the algorithms I used **speed_testing_string_search.py**

The file **Algorithmic Sciences Final report.pdf** is my report. 
