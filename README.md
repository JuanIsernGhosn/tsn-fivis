# TSN to Fivis
This tool read the log generated information from TSN nodes. This recorded information is sended to FIVIS.

#### Prerequisites
* To use it you should have `res/api_configuration.json`
    * Includes the following information:
        * api endpoint
        * token
        * partner
        
## Instructions
1. Download this repository.
2. Modify some data from the `res/api_configuration.json` if it is necessary.
3. Go to src directory `cd src`
4. Run `python tsn-fivis.py` inside a **screen**

You can change the working mode of the module using some parameters:

    `usage: tsn-fivis.py [-h] [--api_config APICONFIG]
                       [--time_between_measure TIME_BETWEEN_MEASURE]
                       [--send_every SEND_EVERY]`

    ´Record and send monitoring hardware data to FIVIS
    optional arguments:
      -h, --help                                        show this help message and exit
      --log_folder              SYSFILE                 Path of the folder that contains TSN data logs
      --api_config              APICONFIG               Path of the .json file with the Fivis api configuration
      --time_between_measure    TIME_BETWEEN_MEASURE    Interval of measurements in seconds
      --send_every              SEND_EVERY              Number of measures before sending it to FIVIS`