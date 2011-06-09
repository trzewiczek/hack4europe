HACK4EUROPE
===========
Repo for the first Europeana hackathon in Poznań.


HOW TO USE
==========
Go to scripts folder and run:

$ python get_data.py \<keyword\>

It will download the data from Europeana db and prepare it
the way they will be visible in the visualization.

Because there can be a loads of data for some general queries
there is a way to condition a download:

$ python get_data.py \<keyword\> ask

After the total number of records is known, the script will
ask if you want to continue. Be aware - download can take long...


LICENSE
=======
The code is licensed under BSD license.


AUTHORS
=======
Mikołaj

Marcin Korzekwa

Krzysztof Trzewiczek
