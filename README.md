# attendance-tool
Attendance tool for GPSG

# Usage
This tutorial assumes the use of [gitbash](https://git-scm.com/downloads) or a Unix-like terminal with github command line usage.
1. This project utilizes conda to manage environments and ensure consistent results. Download [miniconda](https://docs.conda.io/en/latest/miniconda.html) and ensure you can activate it from your terminal by running `$conda activate` 
    * Depending on system configuration, this can be an involved process [here](https://discuss.codecademy.com/t/setting-up-conda-in-git-bash/534473) is a recommended thread.
2. Clone the repository using `$git clone https://github.com/CU-Boulder-GPSG/attendance-tool.git`
3. Change to the current working directory using `$cd <insert_path>/attendance-tool`
4. Active the gpsg environment using `$conda activate gpsg`
    * If this is your first time running, you will need to install the environment using `$conda env create -f environment.yml`
5. Download the Qualtrics survey data by clicking 'Data & Analysis' then 'Export & Import'.
6. Extract and copy the survey csv file into the `attendance_data` folder.
7. Run the analysis by running `$python attendance.py --date YYYY-MM-DD`
    * For example a meeting happening November 1 2021 would be `$python attendance.py --date 2021-11-01`
8. A minutes table will be generated in the directory with the name `YYYY-MM-DD_minutes.csv`

# Contents
```
attendance-tool
│   .gitignore
│   attendance.py: Source code for tool
│   environment.yml: Conda environment specs
│   LICENSE
│   README.md
│
├───attendance_data: Location to put downloaded attendance data
│       place_attendence_here.txt
│
└───role_information
        roles.csv: Officer and Exec role information (to be updated whenever personnel changes happen)
```
