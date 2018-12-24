# Item Catalog Project
This project has been developed for Udacity to complete a Full Stack Web Developer Nanodegree.


## About
This project is a web application utilizing the Flask framework which accesses a SQL database "we using sqlalchemy database" that populates categories and their items.
we use the third party " google" for login in our web app.
OAuth2 provides authentication for further CRUD functionality on the application.
the web app is a catalog to show categories and it's items. with some of the CRUD functionality, and also we added endpoints JSON.


## Requirements Install
Python 3.7.1
vagrant 2.2.0
VirtualBox
Git bash - for Windows OS
pycodestyle-2.4.0
Flask
oauth2client
jsonify
requests

## How to Run
- Clone this repo:
$ git clone https://github.com/Alaa-1989/Item-Catalog-Project.git

- Run virtual machine:
 you need to bring the virtual machine by this command 'vagrant up' Then log into it with 'vagrant ssh'.

 - Clone the Udacity "Vagrantfile" from this link  [Click Here](https://github.com/udacity/fullstack-nanodegree-vm)

- 'cd /vagrant'

- 'cd catalog'

- if you make change in the database you need to run this command after delete "database_setup.db" and "novelscategories.db"
'python database_setup'

- then run the seeder file
' python seeder.py'

- For run the web app write this command in same direct.
'python catalogitem.py'

- Then Open http://localhost:8000 from your browser.

- Currently, OAuth2 is implemented for Google Accounts, you'll need a google accounts for "login" to the web app.

## Requirement Steps
Page implements a third-party authentication & authorization service, we implemented OAuth2 for Google Accounts.
- go to Google Developers Console [Click Here](https://console.developers.google.com)
- Sign up or Login
- Go to Credentials
- Select Create Credentials > OAuth Client ID
- Select Web application
- Enter name 'Item Catalog' or any name you want
- If you change the name you need to change it in 'catalogitem.py' line 20 , 'APPLICATION_NAME = "Item Catalog"'
- Select the app then In Authorized JavaScript origins add:
http://localhost:8000
- Select Authorized redirect URIs and add:
http://localhost:8000/gconnect
- Select Client ID and copy it and paste it into the 'login.html' line 21, 'data-clientid='
- Select Download JSON after Save your changing
- Rename JSON file to g_client_secrets.json
- Place JSON file in catalog directory that you cloned from here

## In your git bash/Terminal

- In your vagrant, install project requirements
'pip install -r requirements.txt'

- The code in this project conforms to the PEP8 style recommendations.
if you want to make a change in python file make sure to test	your	code quality, it's should	pass	the	style	standard	with	0	errors. You can install the pycodestyle tool to test this.
Run this code to install pycodestyle.
'pip install pycodestyle'


- 'cd' to catalog file and run this command to Checked your code.
'pycodestyle catalogitem.py'


## Snapshot

If you got a problem when you try to run 'vagrant up'
with the port, if there is another process run in same port.

you can try this solution for Window OS:

**In Windows PowerShell version 1 or later to stop a process on port 8000 type:**

'Stop-Process (,(netstat -ano | findstr :8000).split() | foreach {$[$.length-1]}) -Force'

**As suggested by @morganpdx here's a more PowerShell-ish, better version:**


'Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force'


- this solution take from this page [Click Here](https://stackoverflow.com/questions/39632667/how-to-kill-the-process-currently-using-a-port-on-localhost-in-windows)

- and for MAC OS see this page [Click Here](https://stackoverflow.com/questions/24387451/how-can-i-kill-whatever-process-is-using-port-8080-so-that-i-can-vagrant-up)


## JSON Endpoints
There is a Three endpoints in this project, you can view it in your browser by entering the path:

**categoriesMenuJSON**
- JSON APIs to view category and it's items Information
**path:**
'localhost:8000/categories/<int:categories_id>/menu/JSON'

**categoryItemJSON**
- JSON APIs to view Specific Category by id with its items Information by item id
**path:**
'localhost:8000/categories/<int:categories_id>/menu/<int:menu_id>/JSON'

**catalogsJSON**
- JSON APIs to view all categories with their id
**path:**
'localhost:8000/categories/JSON'

## Notes
you will find a comments in the code file described each command uses.

## Author
**Alaa Alaboud** - _GitHub Profile:_ [Alaa-1989](https://github.com/Alaa-1989)

## License
Licensed under the [MIT License](LICENSE)
