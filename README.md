# ImageJ-cvs-cutter

Simple tool for Calcium-imaging data preprocessing, based on timing-metadata from Olympus Fluoview sowtware
Given script reformats your ImageJ ROI cvs-multimeasurements, based on the events timing from Olympus Fluoview metadata.

Algorythm explanation:

1. Lists all of the .txt files (excluding .txt files that names starts with !) in all subdirectories of listed in DIRECTORIES pathes.
2. Collects event-timing metadata from correct-format metadatas (having T-dimentional axis)
3. lists all the .csv files, wich names starts the same as the collected metadata .txt file names and wich have the same full patch
4. creates subdirectories with the same names as each listed 'generic' .csv files
5. puts inside modified .csv files for each of listed 'generic' .csv files


List directories containing data (tiff + txt) to the 'settings.py', then simple run the script.


To Do:
- cut off columns by ROI area
-Done: do swich betwin dF/F0 and dF/F modes
