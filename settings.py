'''
ImageJ-csv-cutter

Simple tool for processing Ca-metry data recieved using Olympus Confocal or 2-photon microscopes.
Given script reformats your ImageJ ROI cvs-multimeasurements, based on the events timing in Olympus metadata.

Algorythm explanation:

1. Lists all of the .txt files (excluding .txt files that names starts with !) in all subdirectories of listed in DIRECTORIES pathes.
2. Collects event-timing metadata from correct-format metadatas (having T-dimentional axis)
3. lists all the .csv files, wich names starts the same as the collected metadata .txt file names and wich have the same full patch
4. creates subdirectories with the same names as each listed 'generic' .csv files
5. puts inside modified .csv files for each of listed 'generic' .csv files


List below directories containing data (tiff + txt), then simple run the script.

'''

TIME_BEFORE_TRIG = 10    # in sec.
TIME_AFTER_TRIG  = 30    # in sec.

DIRECTORIES = [
    # 'C:\\Users\\Lenin\\coding\\ImageJ-csv-cutter',
    # 'F:/Lab Work Files/2-photon/Pirt_GCamp3 x MCU-KO + DRS + Caps/',
    # 'F:/Lab Work Files/2-photon/Pirt GCamp3 x Thy1 RGeco SNI or SHAM + DRS  + PMX205 + Bicuculine/',
    
]
