import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine("sqlite:///cms.db")
engine.connect()

def load_cms_data(year):

    cms_payments = pd.read_sql(f'SELECT Teaching_Hospital_Name as Hopsital_Name,Physician_Profile_ID,Recipient_City,Recipient_Zip_Code,Physician_Specialty, Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name as Paying_Entity,Total_Amount_of_Payment_USDollars as Total_payment,Date_of_Payment, Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_1 as DrugName, nature_of_payment_or_transfer_of_value FROM cms_payments_{year};', engine)
    cms_payments['date_of_payment'] = pd.to_datetime(cms_payments['date_of_payment'])
    cms_payments['Payment_month'] = cms_payments['date_of_payment'].dt.strftime('%b')
    cms_payments['Total_payment'] = cms_payments.Total_payment.astype(float)


    if year == 2019:
        i = cms_payments[((cms_payments.Payment_month == 'Oct') &( cms_payments.Total_payment == cms_payments['Total_payment'].max()))].index
        cms_payments = cms_payments.drop(i)

    return cms_payments

    


    




    return cms_payments



