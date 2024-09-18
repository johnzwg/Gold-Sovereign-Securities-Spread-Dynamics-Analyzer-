import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path_gold = r'C:\Users\IoannisZografakis-Re\Downloads\Bulletin.csv'  # Adjust the file path accordingly
gold_df = pd.read_csv(file_path_gold)

# Step 1: Filter the Data
filtered_gold_df = gold_df[
    (gold_df['Gold_Ask_995'] >= 20) & (gold_df['Gold_Ask_995'] <= 50) &
    (gold_df['Sov_New_Post1974_Bid'] >= 70) & (gold_df['Sov_New_Post1974_Bid'] <= 270)
].copy()  # Explicitly create a copy to avoid SettingWithCopyWarning

# Step 2: Export the filtered data to CSV
output_file_path_gold = r'C:\Users\IoannisZografakis-Re\Documents\filtered_gold_data.csv'  # Adjust the path
filtered_gold_df.to_csv(output_file_path_gold, index=False)

# Step 3: Data Preprocessing - Convert 'Reference_Date' to datetime format using .loc[]
filtered_gold_df.loc[:, 'Reference_Date'] = pd.to_datetime(filtered_gold_df['Reference_Date'], format='%Y-%m-%d')

# Set 'Reference_Date' as the index of the DataFrame
filtered_gold_df.set_index('Reference_Date', inplace=True)

# Handle missing data by filling missing values with the column means
filtered_gold_df.fillna(filtered_gold_df.mean(), inplace=True)

# Step 4: Descriptive Statistics for 'Gold_Ask_995' and 'Gold_Bid_995'
summary_stats = filtered_gold_df[['Gold_Ask_995', 'Gold_Bid_995']].describe()

# Display the summary statistics
print(summary_stats)

# Step 5: Data Analysis - Calculate the rolling mean and standard deviation for a 30-day window for 'Gold_Ask_995'
filtered_gold_df.loc[:, 'Rolling_Mean_30'] = filtered_gold_df['Gold_Ask_995'].rolling(window=30).mean()
filtered_gold_df.loc[:, 'Rolling_Std_30'] = filtered_gold_df['Gold_Ask_995'].rolling(window=30).std()

# Calculate the correlation between 'Gold_Ask_995' and 'Gold_Bid_995'
correlation = filtered_gold_df[['Gold_Ask_995', 'Gold_Bid_995']].corr().iloc[0, 1]
print(f"Correlation between Gold_Ask_995 and Gold_Bid_995: {correlation}")

# Step 6: Visualization 1 - Time series plot for 'Gold_Ask_995' and 'Gold_Bid_995' with rolling mean and standard deviation

# Drop NaN values from rolling mean and std to avoid plotting issues
filtered_gold_df_clean = filtered_gold_df.dropna(subset=['Rolling_Mean_30', 'Rolling_Std_30'])

plt.figure(figsize=(12, 6))

# Plot Gold Ask 995
plt.plot(filtered_gold_df_clean.index, filtered_gold_df_clean['Gold_Ask_995'], label='Gold Ask 995', color='blue')

# Plot Gold Bid 995
plt.plot(filtered_gold_df_clean.index, filtered_gold_df_clean['Gold_Bid_995'], label='Gold Bid 995', color='orange')

# Plot 30-day rolling mean
plt.plot(filtered_gold_df_clean.index, filtered_gold_df_clean['Rolling_Mean_30'], label='30-day Rolling Mean (Gold Ask 995)', color='green', linestyle='--')

# Plot 30-day rolling standard deviation as shaded area
plt.fill_between(filtered_gold_df_clean.index,
                 filtered_gold_df_clean['Rolling_Mean_30'] - filtered_gold_df_clean['Rolling_Std_30'],
                 filtered_gold_df_clean['Rolling_Mean_30'] + filtered_gold_df_clean['Rolling_Std_30'],
                 color='green', alpha=0.2, label='30-day Rolling Std Dev')

# Customize plot
plt.title('Gold Ask 995 and Gold Bid 995 with 30-day Rolling Mean and Standard Deviation')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 7: Extract Year and Group Data by Year for Analysis
filtered_gold_df['Year'] = filtered_gold_df.index.year
grouped_by_year = filtered_gold_df.groupby('Year').agg(
    Gold_Ask_995_Mean=('Gold_Ask_995', 'mean'),
    Gold_Ask_995_Std=('Gold_Ask_995', 'std'),
    Gold_Bid_995_Mean=('Gold_Bid_995', 'mean'),
    Gold_Bid_995_Std=('Gold_Bid_995', 'std')
).reset_index()

# Step 8: Visualization 2 - Bar chart for average Gold_Ask_995 and Gold_Bid_995 prices per year with error bars
plt.figure(figsize=(12, 6))

# Bar chart for Gold Ask 995
plt.bar(grouped_by_year['Year'] - 0.15, grouped_by_year['Gold_Ask_995_Mean'], width=0.3, yerr=grouped_by_year['Gold_Ask_995_Std'], label='Gold Ask 995', color='blue')

# Bar chart for Gold Bid 995
plt.bar(grouped_by_year['Year'] + 0.15, grouped_by_year['Gold_Bid_995_Mean'], width=0.3, yerr=grouped_by_year['Gold_Bid_995_Std'], label='Gold Bid 995', color='orange')

# Customize plot
plt.title('Average Gold Ask and Bid Prices by Year with Standard Deviation')
plt.xlabel('Year')
plt.ylabel('Price')
plt.legend()
plt.tight_layout()
plt.show()

# Step 9: Resample Data to Monthly Frequency and Calculate Rolling Stats
monthly_gold_df = filtered_gold_df.resample('M').mean()

# Calculate 12-month rolling average and standard deviation
monthly_gold_df['Rolling_Mean_12'] = monthly_gold_df['Gold_Ask_995'].rolling(window=12).mean()
monthly_gold_df['Rolling_Std_12'] = monthly_gold_df['Gold_Ask_995'].rolling(window=12).std()

# Step 10: Visualization 3 - Line plot for monthly average Gold Ask 995 with rolling mean and std
plt.figure(figsize=(12, 6))

# Plot monthly average Gold Ask 995
plt.plot(monthly_gold_df.index, monthly_gold_df['Gold_Ask_995'], label='Monthly Average Gold Ask 995', color='blue')

# Plot 12-month rolling mean
plt.plot(monthly_gold_df.index, monthly_gold_df['Rolling_Mean_12'], label='12-Month Rolling Mean (Gold Ask 995)', color='green', linestyle='--')

# Plot 12-month rolling standard deviation as shaded area
plt.fill_between(monthly_gold_df.index,
                 monthly_gold_df['Rolling_Mean_12'] - monthly_gold_df['Rolling_Std_12'],
                 monthly_gold_df['Rolling_Mean_12'] + monthly_gold_df['Rolling_Std_12'],
                 color='green', alpha=0.2, label='12-Month Rolling Std Dev')

# Customize plot
plt.title('Monthly Average Gold Ask 995 with 12-Month Rolling Mean and Standard Deviation')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
