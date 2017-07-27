# Catalog App
Author: Ellen Liu
Last Edit: 6/28/2017

## Requirements for this project

### Git

If you need Git, go to http://git-scm.com/downloads.

### VirtualBox

If you need VM, you can download VirtualBox at https://www.virtualbox.org/wiki/Downloads.

### Vagrant

If you need Vagrant, go to https://www.vagrantup.com/downloads.

## Download the Source Code
From the terminal, run:

    'git clone https://github.com/ellenmliu/Catalog.git catalog'

## Run the Catalog App

In terminal, change directory to catalog then run the Vagrant to launch your virtual machine. Then we would log the terminal into the virtual machine. To do so you would run this in terminal:

    'cd catalog
    vagrant up
    vagrant ssh'

To log out you would run:
    'exit'

Once you are logged in your VM, you want to change the directory to /vagrant. Make sure you are in the right directory by typing in ls and it should show all the files and folders. You would then initialize the database.

    'cd /vagrant
    ls
    python database_setup.py'

I have provided categories and items already, so to add them you would run:

    'python categoriesanditems.py'

Lastly, to run the web server, run:

    'python views.py'

To view the catalog app, visit http://localhost:8000/. From there you can login in or view the public site. Once you login, you can add, edit, or delete items.
