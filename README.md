# DEI-Filler
This is a script which generates a PDF and an associated complaint about gender and diversity, to help with filling such forms in. It was entirely AI generated as a learning project.

It requires fpdf to function.

When one encounters such helpful forms as https://enddei.ed.gov/ one really feels the need to make sure they get as much information as possible. This script generates that content. It could do with a tweak to pull real school data - since the list is currently fictional. Also the size estimation is poor - it's targeting 9 mb but sometimes produces way less.

Gender_ramble2.py works as described above.

Gender_ramble3.py + it's associated school data file is an attempt to fully automate the process of generating complaints. It pulls from the much larger CSV files of schools. The zip codes in that file are random, but the school districts are pulled from a data source for US school districts. It is reliant on fpdf, selenium and chromedriver - you should replace its path to chromedriver with your path to chromedriver (if you don't have these then I'd install brew and then use pip3 to install fpdf and selenium, and brew to install chromedriver). Running it as is will show you the window as it fills it in. Uncomment line 117 to make it run headless.
