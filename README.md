# Open [Payments Data](https://www.cms.gov/OpenPayments/Data) before and after COVID

## Abstract

Centers for Medicare and Medicaid Services(CMS) offers a platform that allows the public to view data about transactions between pharmaceutical and drug device companies to hospitals and healthcare providers to provide transparency about financial relationships. Data for the year 2020 was released on June 30th 2021. 

App was developed to compare payments pre and post COVID. Please click here to find the [app](https://cms-openpayments-dot-metis-engineering-319923.wl.r.appspot.com/). 

## Design

Dataset is available for download from the [CMS Website](https://www.cms.gov/OpenPayments/Data/Dataset-Downloads). I plan to focus on general payments for the year 2019 and 2020. To reduce complexity in handling data only some zip codes were included. 100,000 rows each from 2020 and 2019 were scrapped. The data was imported into a SQL database and analyzed on jupyter notebooks. Visual studio code was utilized to organize my code for creating an app with Dash. App was deployed using the google app engine. 

## Data

Data has about 100,000 entries each from 2020 and 2019. It has 79 columns for each year describing hospital, physician and pharmaceutical company details.

## Algorithms

Machine learning algorithms were not utilized. A data pipeline was built that can display user information about open payments. Please review the below workflow diagram- 

<img src="Screen Shot 2021-07-22 at 4.05.56 PM.png" alt="Project_architecture" width="800" height = "600"/> 

## Tools
* SQLite
* Plotly
* Dash
* Google App Engine


