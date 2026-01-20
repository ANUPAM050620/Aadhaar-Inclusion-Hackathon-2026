import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Professional Data Aggregation Script for UIDAI Hackathon
def run_analysis():
    # 1. Load and Clean Data
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    def aggregate_data(keyword):
        files = [f for f in csv_files if keyword in f]
        dfs = [pd.read_csv(f) for f in files]
        if not dfs: return pd.DataFrame()
        df = pd.concat(dfs, ignore_index=True)
        df.columns = [c.strip().lower() for c in df.columns]
        df['state'] = df['state'].str.upper()
        df['district'] = df['district'].str.upper()
        return df

    enrol = aggregate_data('enrolment')
    bio = aggregate_data('biometric')
    demo = aggregate_data('demographic')

    # 2. Join Datasets
    master = enrol.groupby(['state', 'district']).sum().reset_index()
    master = master.merge(bio.groupby(['state', 'district']).sum().reset_index(), on=['state', 'district'], how='outer')
    master = master.merge(demo.groupby(['state', 'district']).sum().reset_index(), on=['state', 'district'], how='outer').fillna(0)

    # 3. Create Key Metrics
    master['total_enrol'] = master['age_0_5'] + master['age_5_17'] + master['age_18_greater']
    master['total_updates'] = master['bio_age_5_17'] + master['bio_age_17_'] + master['demo_age_5_17'] + master['demo_age_17_']
    master['vulnerability_score'] = (master['total_updates'] / (master['total_enrol'] + 1))

    # 4. Generate Visuals
    plt.figure(figsize=(10,6))
    top_10 = master.sort_values('total_enrol', ascending=False).head(10)
    sns.barplot(data=top_10, x='district', y='vulnerability_score')
    plt.title('District-wise Service Intensity Score')
    plt.xticks(rotation=45)
    plt.savefig('visual_insight.png')
    
    master.to_csv('processed_aadhaar_data.csv', index=False)
    print("Analysis Complete. Results saved to processed_aadhaar_data.csv")

if __name__ == "__main__":
    run_analysis()
