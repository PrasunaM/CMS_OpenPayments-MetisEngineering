# Analysis on [Open Payments Data](https://www.cms.gov/OpenPayments/Data) during COVID

### Question/need:
* What is the framing question of your analysis, or the purpose of the model/system you plan to build?

Centers for Medicare and Medicaid Services(CMS) offers a [platform] (https://www.cms.gov/OpenPayments/Data) that allows public to view data about trasactions between pharmaceutical and drug device companies to hospitals and healthcare providers to provide transparency about financial relationships. Data for the year 2020 was realeased on June 30th 2021. Comparing trends in payments across various states before and after the pandemic might reveal interesting facts about the pharmaceutical industry.    


* Who benefits from exploring this question or building this model/system?

The intention of creation of this portal was to build trust and openess in the healthcare system. Exploring this data in depth, I'm hoping to unveil impacts of a global pandemic on these payments.

### Data Description:

* What dataset(s) do you plan to use, and how will you obtain the data?

Dataset is available for download from the [CMS Website](https://www.cms.gov/OpenPayments/Data/Dataset-Downloads). I plan to focus on general payments for the year 2019 and 2020.
It has about 5783984 entries and 79 columns for each year describing hospital, physician and pharmaceutical company details.

* What is an individual sample/unit of analysis in this project? What characteristics/features do you expect to work with? 

Each row describe information 

* If modeling, what will you predict as your target?

None

#### Tools:
* How do you intend to meet the tools requirement of the project? 

SQL, Google cloud, Spark, streamlit

* Are you planning in advance to need or use additional tools beyond those required?

Tableau

#### MVP Goal:
* What would a [minimum viable product (MVP)](./mvp.md) look like for this project?

MVP with all the data cleaned and loaded onto a SQL database on google cloud. Tableau visualizations will be performed.


