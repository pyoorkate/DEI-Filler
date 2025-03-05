# DEI-Filler
This is a script which generates a PDF and an associated complaint about gender and diversity, to help with filling forms like https://enddei.ed.gov/ in. 

It was entirely AI generated as a learning project. Obviously you definitely shouldn't use it to fill the DEI Form with nonsense complaints. That would be bad and wrong.

To use it you need gender_ramble3.py - and the school data file. It attempts to fully automate the process of generating complaints. 

It pulls from the CSV files of school districts. The zip codes in that file are random, but the school districts are pulled from a data source for US school districts (I couldn't find a source with zip codes, if you have one, please update the file!).

It is reliant on fpdf, selenium and chromedriver - you should replace its path to chromedriver with your path to chromedriver (if you don't have these then I'd install brew and then use pip3 to install fpdf and selenium, and brew/snap to install chromedriver).

Running it as is will show you the window as it fills it in. Uncomment line 117 to make it run headless.

- The script as configured will probably work unmodified on a Mac (assuming default locations).

- On ubuntu 24.0X if you use the default location for a snap install of chromium (to get chomedriver) it is at: /snap/bin/chromium.chromedriver (which is the location you should put on line 119).


It requires fpdf to function.

Gender_ramble2.py was my first stab at the process - it used fictional school districts and produced files for you to manually copy/paste and attach.
