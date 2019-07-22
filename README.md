# ConsoGENCMIP6

<snippet>
  <content><![CDATA[
# ${1:ConsoGENCMIP6}

ConsoGENCMIP6 is the project where the monitorring of computing resources is done for the differents projects of IPSL on the National Super Computers (TGCC and IDRIS). 
There are two different monitoring done here : the cpu time consumption minotoring (whose code can be found in ./bin/consomation) and the cpu usage monitoring, depending on the number of jobs launched from IPSL and on the whole TGCC computer. These codes can be found on ./bin/jobs


Here is a brief overview of the computing chain (formerly) used to get the graphs for the GENCMIP6 project : 
Two cron are currently runing to follow the computing time ([Figure 1]) and the runing and pending jobs from CMIP6 teams on IRENE ([Figure 2] ) 




###### 1) Computing Time Monitoring
[//]: # (A cron is launched from the igcmg account on TGCC. It executes the ccc_myproject and ccc_mpp commands. Their output is stored and sent to ciclad. )
![Figure 1](UML/cron_consmation_description.png?raw=true)

Computing Time Monitoring is being revised from scratch to ensure better maintainability. 
First, ccc_myproject logs are being stored. Then a file parsers splits the logs between the differents projects. The projects log files are the parsed and the output is stored in structured files. 

These structured files will be used for data analysis an vizualization.

###### 2) Runing and Pending Jobs Monitoring
[//]: # (Python scripts are executed to plot the different graphs required to manage the CPU and memory usage on the computation centers. )
![Figure 2](UML/cron_job_description.png?raw=true)

## Usage
### Raw html graphs output : 
These scripts are to be launched by crons on the ciclad server ( ~/run_consoGENCMIP6.sh ). 
It will : 
- pull the data from the computing centers parse it, store it as a timeseries. (run_parser_to_timeseries.py)
- plot the data into bokeh graphs. (multi_plot_with_delay_bars.py)

An other script will copy the output html files to the igcmg account, so that the graphs can be seen online.

(https://vesg.ipsl.upmc.fr/thredds/fileServer/IPSLFS/igcmg/IRENE/ConsoGENCMIP6/index.html) 

### Bokeh app : 
An app is also being developped to visualize all the graphs from the same interface and improve plots interactivity. 

 Make sure that the timeseries Json File is on the proper folder.
 
 Then : 

 > cd $HOME/Documents/mesocentre/ConsoGENCMIP6_git/ConsoGENCMIP6/
 #(Path to git repository) 

 > bokeh serve --port 5006 --show bin/app/

## Contributing
No contribution need. 


## History

These scripts were written by the former person in charge of following computing time at IPSL.
The project has been rebooted in April 2019. 
They are now being modified to for maintenance and further development.


## Credits

TODO: Write credits

## License

TODO: Write license 

]]></content>
  <tabTrigger>readme</tabTrigger>
</snippet>
