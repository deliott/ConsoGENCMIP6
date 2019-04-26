# ConsoGENCMIP6

<snippet>
  <content><![CDATA[
# ${1:ConsoGENCMIP6}


These are the codes used and formerly used to check the computing ressources use in TGCC for the CMIP6 projects

Here is a brief overview of the computing chain used to get the graphs for the GENCMIP6 project : 
Two cron are currently runing to follow the computing time ([Figure 1]) and the runing and pending jobs from CMIP6 teams on IRENE ([Figure 2] ) 

![Figure 1](UML/cron_consmation_description.png?raw=true)

![Figure 2](UML/cron_job_description.png?raw=true)

###### 1) Data acquisition
A cron is launched by the from the igcmg account on TGCC. It executes the ccc_myproject and ccc_mpp commands. Their output is stored and sent to ciclad. 

###### 1) Data analysis
Python scripts are executed to plot the different graphs required to manage the CPU and memory usage on the computation centers. 

## Usage

These scripts are to be launched by crons on the irene server 

TODO: Write usage instructions
## Contributing
No contribution need for now. 

%1. Fork it!
%2. Create your feature branch: `git checkout -b my-new-feature`
%3. Commit your changes: `git commit -am 'Add some feature'`
%4. Push to the branch: `git push origin my-new-feature`
%5. Submit a pull request :D

## History

These scripts were written by the former person in charge of following computing time at IPSL.
They are now being modified to for maintenance and further development.


## Credits

TODO: Write credits

## License

TODO: Write license 

]]></content>
  <tabTrigger>readme</tabTrigger>
</snippet>
