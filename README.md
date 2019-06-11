# ConsoGENCMIP6

<snippet>
  <content><![CDATA[
# ${1:ConsoGENCMIP6}

ConsoGENCMIP6 is the project where the monitorring of computing resources is done for the differents projects of IPSL on the National Super Computers (TGCC and IDRIS). 
There are two different monitoring done here : the cpu time consumption minotoring (whose code can be found in ./bin/consomation) and the cpu usage monitoring, depending on the number of jobs launched from IPSL and on the whole TGCC computer. These codes can be found on ./bin/jobs


Here is a brief overview of the computing chain (formerly) used to get the graphs for the GENCMIP6 project : 
Two cron are currently runing to follow the computing time ([Figure 1]) and the runing and pending jobs from CMIP6 teams on IRENE ([Figure 2] ) 




###### 1) Computing Time Monitoring
[//]: # (A cron is launched by the from the igcmg account on TGCC. It executes the ccc_myproject and ccc_mpp commands. Their output is stored and sent to ciclad. )
![Figure 1](UML/cron_consmation_description.png?raw=true)

Computing Time Monitoring is being revised from scratch to ensure better maintainability. 
First, ccc_myproject logs are being stored. Then a file parsers splits the logs between the differents projects. The projects log files are the parsed and the output is stored in structured files. 

These structured files will be used for data analysis an vizualization.

###### 2) Runing and Pending Jobs Monitoring
[//]: # (Python scripts are executed to plot the different graphs required to manage the CPU and memory usage on the computation centers. )
![Figure 2](UML/cron_job_description.png?raw=true)

## Usage

These scripts are to be launched by crons on the ciclad server 

TODO: Write usage instructions
## Contributing
No contribution need for now. 

[//]: # (1. Fork it!
%2. Create your feature branch: `git checkout -b my-new-feature`
%3. Commit your changes: `git commit -am 'Add some feature'`
%4. Push to the branch: `git push origin my-new-feature`
%5. Submit a pull request :D ) 

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
