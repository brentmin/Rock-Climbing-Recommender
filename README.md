
# Rock Climbing Recommender Title [TODO]

Description of project [TODO]

## How To Run

* To just use the project, visit https://dsc180b-rc-rec.herokuapp.com/. Note that this project runs on a free dyno, so when traffic to the site is low, response times will be very slow. Be patient!
* To run on the command line, clone the repository, then run the command "pip install -r requirements.txt" from the project home.

### Running the Project on the Command Line

To run the project, every command must start with "python run.py" from the root directory of the project. By default, "python run.py" will not download data, will use the default data/model parameters, will not use cuda, will not run any benchmarks, and will train and evaluate SASRec on the Beauty dataset. The base command can be modified with a couple of different flags:

|Flag|Type|Default Value|Description|
|-|-|-|-|
|-d, --data|bool|False|Use this flag to run all data scraping code. Be warned that using this flag will first delete **ALL** raw and cleaned data, before downloading new raw data.|
|-c, --clean|bool|False|Use this flag to run all data cleaning code. Be warned that using this flag will first delete **ALL** raw and cleaned data, before processing raw data into cleaned data.|
|-p, --top_pop|bool|False|Use this flag to return the top 10 most popular/well received as a csv.|
|-\-data-config|str|"config/data_params.json"|The location at which data parameters can be found|
|-\-test|bool|False|Use this flag to run the data pipeline and top pop on a small sample. This will override all other flags|

### Description of Parameters

#### Data Parameters

|Parameter Name|Type|Default Value|Description|
|-|-|-|-|
|raw_data_folder|str|data/raw/|The location at which raw data will be saved. Note that this path is relative to the project root.|
|clean_data_folder|str|data/cleaned/|The location at which clean data will be saved. Note that this path is relative to the project root.|

#### Model Parameters

|Parameter Name|Type|Default Value|Description|
|-|-|-|-|
|TODO|TODO|TODO|TODO|

There are none so far
