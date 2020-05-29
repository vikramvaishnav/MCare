# MedoCare
### 2020-05-13
## Database:
1. Database Connectivity done
2. created APIs for converting and storing csv data to database
3. medicineinventorymonthly and medicineinventoryweekly tables created

## Charts:
1. Data fetching apis pastinvapi, predictinvapi, pastweeklyinvapi, predictweeklyinvapi
2. Predicting medicine requirememts monthly and weekly created
3. Past inventory monthly and weekly created

## Map:
1. Api for map created mapapi
2. map function for folium map creation
3. map integrated with dashboard
4. Hospitals added in map

## Model:
1. LSTM model class LSTM_Model created
2. train and predict for monthly data
3. train and predict for weekly data

## Table:
1. Inventory table created
2. shows current month and next month comparison

## Dorm:


## Datasets:
1. Medicine inventory data 8 categories of medicine 60000 daily records divided into months and weeks
2. Hospitals geographical information data from data.gov.in
3. Hospitals region wise resource information from opendata Pune for Pune region.
4. Past disease data from idsp.nic.in
5. Disease outbreak (covid19)  data from covid19India.org and opendata.punecorporation.org

## Models
1. Neural Networks - seasonal disease prediction
2. LSTM/ARIMA - medical inventory prediction
3. SIR - disease outbreak resource management


## Medicine inventory dataset
1.Selected group of drugs from the dataset (57 drugs) is classified to the following Anatomical Therapeutic Chemical (ATC) Classification System categories: - M01AB - Anti-inflammatory and antirheumatic products, non-steroids, Acetic acid derivatives and related substances - M01AE - Anti-inflammatory and antirheumatic products, non-steroids, Propionic acid derivatives - N02BA - Other analgesics and antipyretics, Salicylic acid and derivatives - N02BE/B - Other analgesics and antipyretics, Pyrazolones and Anilides - N05B - Psycholeptics drugs, Anxiolytic drugs - N05C - Psycholeptics drugs, Hypnotics and sedatives drugs - R03 - Drugs for obstructive airway diseases - R06 - Antihistamines for systemic use 
2. 6 years (2014-2019)