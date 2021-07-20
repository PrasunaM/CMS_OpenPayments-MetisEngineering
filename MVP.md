# Open Payments comparision between pre and post COVID

The aim of this project is to focus on payments from drug/device manufactures to healthcare providers pre and post COVID. 

## Data Acquisition 

Data was scraped from the website using Socrata API, for th purposes of MVP only 100,000 rows were obtained from 2019 and 2020. Scraped data was loaded onto SQL Lite database. SQL queries were utilized to retreive specific information necessary for visualizations. Data was cleaned and plotly was used for visualizations. Dash was utilized to construct a dashboard.

Google App Engine was used for deployment which can be found [here](https://cms-openpayments-dot-metis-engineering-319923.wl.r.appspot.com/). 

<img src="Screen Shot 2021-07-20 at 12.44.10 PM.png" alt="Payment_Speciality" width="600" height = "400"/>  <img src="Screen Shot 2021-07-20 at 12.44.24 PM.png" alt="Payment_month" width="600" height = "400"/> <img src="Screen Shot 2021-07-20 at 12.44.42 PM.png" alt="Payments_Drug" width="600" height = "400"/> 

Next steps, as you can see the graps still need to be formatted on plotly. CSS styling needs to be added and if time permits will add maps using geopandas on plotly.
