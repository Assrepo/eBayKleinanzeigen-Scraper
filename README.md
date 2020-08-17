# eBayKleinanzeigen-Scraper
 A small webscraper that keeps looking for new offers on www.ebay-kleinanzeigen.de and sends them to you via E-Mail.

## Setup
- The script requires an installation of python.
### Download
> Clone the repository by either using the button in the top right or execute the following line of code from your shell:
```shell
$ git clone https://github.com/Varsius/eBayKleinanzeigen-Scraper
```
### Installation
> Open up a terminal and go into the cloned directory
 ```shell
$ cd **path**/eBayKleinanzeigen-Scraper
```
> Install the required packages the script depends on
 ```shell
$ pip install -r requirements.txt
```
> Edit the configuration file with your favourite editor by following along the instructions. 
> For example:
```shell
$ nano config.py
```

### Execution
> Run the script.
```shell
$ python main.py
```
> Remember that this script will run forever, therefore you can not close the terminal.
> Exit the script with Ctrl + C.
> If you want to run this script in the background (If you want to close the terminal or if you are connected via ssh)
> use the following command:
```shell
$ nohup python -u main.py &
```
> Important: Don't forget the "&" at the end of the line. The output of the script will be written to
> to nohup.out. This can be customized with
```shell
$ nohup python -u main.py > custom_output_file.log &
```
---
## Problems and Questions
> There did not appear any problems in the testing phase.
> If the script does not work anymore or you have any questions, please contact me:
- E-Mail: varsius@gmail.com
---
## Screenshots
![Posteingang](https://imgur.com/mU4MS5o)
![E-Mail1](https://imgur.com/nDbRwbq)
![E-Mail2](https://imgur.com/NR06ujN)
