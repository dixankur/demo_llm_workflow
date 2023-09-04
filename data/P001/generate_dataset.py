
import pandas as pd

# Read the datasets
ticket_details = pd.read_csv('./data/P001/ticket_details.csv')
ticket_other_details = pd.read_csv('./data/P001/ticket_other_details.csv')
ticket_category_details = pd.read_csv('./data/P001/ticket_category_details.csv')
location_details = pd.read_csv('./data/P001/location_details.csv')

# Combine the datasets
final_dataset = pd.merge(ticket_details, ticket_other_details, on='number')
final_dataset = pd.merge(final_dataset, ticket_category_details, on='number')
final_dataset = pd.merge(final_dataset, location_details, on='number')

# Save the final dataset
final_dataset.to_csv('./data/P001/final_dataset.csv', index=False)
