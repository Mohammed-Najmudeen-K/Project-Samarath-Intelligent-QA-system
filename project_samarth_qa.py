import pandas as pd
import re

# -------------------------------
# 1️⃣ Load the datasets
# -------------------------------
agri_path = "datafile (1).csv"              # Crop data
rain_path = "Sub_Division_IMD_2017.csv"     # Rainfall data

agri = pd.read_csv(agri_path)
rain = pd.read_csv(rain_path)

# -------------------------------
# 2️⃣ Clean and prepare data
# -------------------------------
# Normalize column names
agri.columns = agri.columns.str.strip().str.replace("`", "", regex=False).str.replace("(", "", regex=False).str.replace(")", "", regex=False)
rain.columns = rain.columns.str.strip()

# Select relevant columns (fixed column name)
agri = agri[['Crop', 'State', 'Yield Quintal/ Hectare']]
agri.columns = ['Crop', 'State', 'Yield']

rain = rain[['SUBDIVISION', 'YEAR', 'ANNUAL']]
rain.columns = ['State', 'Year', 'Rainfall']

# Clean text
agri['State'] = agri['State'].str.strip().str.title()
rain['State'] = rain['State'].str.strip().str.title()

# -------------------------------
# 3️⃣ Define QA functions
# -------------------------------

def compare_rainfall(state1, state2, year):
    """Compare average annual rainfall between two states"""
    df1 = rain[(rain['State'].str.contains(state1, case=False, na=False)) & (rain['Year'] == year)]
    df2 = rain[(rain['State'].str.contains(state2, case=False, na=False)) & (rain['Year'] == year)]

    if df1.empty or df2.empty:
        return f"Data not found for {state1} or {state2} in {year}."

    r1 = df1['Rainfall'].mean()
    r2 = df2['Rainfall'].mean()

    return (f"Average annual rainfall in {state1} ({year}): {r1:.2f} mm\n"
            f"Average annual rainfall in {state2} ({year}): {r2:.2f} mm\n"
            f"Source: Sub_Division_IMD_2017.csv")

def top_crop_by_yield(state, n=3):
    """List top N crops by yield in a state"""
    df = agri[agri['State'].str.contains(state, case=False, na=False)]
    if df.empty:
        return f"No crop data found for {state}."
    top_crops = df.groupby('Crop')['Yield'].mean().nlargest(n)
    return f"Top {n} crops in {state} by yield:\n{top_crops.to_string()}\nSource: datafile (1).csv"

def correlation_crop_rain(crop, year):
    """Correlate yield and rainfall for a given crop and year"""
    df_crop = agri[agri['Crop'].str.contains(crop, case=False, na=False)]
    df_year = rain[rain['Year'] == year]

    merged = pd.merge(df_crop, df_year, on='State', how='inner')
    if merged.empty:
        return f"No matching data found for crop {crop} in {year}."

    corr = merged['Yield'].corr(merged['Rainfall'])
    return (f"Correlation between rainfall and yield for {crop} in {year}: {corr:.2f}\n"
            f"Source: datafile (1).csv + Sub_Division_IMD_2017.csv")

# -------------------------------
# 4️⃣ Simple question parser
# -------------------------------
def answer_question(q):
    q = q.lower()

    if "compare" in q and "rainfall" in q:
        m = re.findall(r"between (.+) and (.+) in (\d{4})", q)
        if m:
            s1, s2, year = m[0]
            return compare_rainfall(s1.strip(), s2.strip(), int(year))
        return "Try: Compare rainfall between Tamil Nadu and Kerala in 2017."

    elif "top" in q and "crop" in q:
        m = re.findall(r"top (\d+) crops? in (.+)", q)
        if m:
            n, state = m[0]
            return top_crop_by_yield(state.strip(), int(n))
        return "Try: Top 3 crops in Maharashtra."

    elif "correlation" in q or "impact" in q:
        m = re.findall(r"for (.+) in (\d{4})", q)
        if m:
            crop, year = m[0]
            return correlation_crop_rain(crop.strip(), int(year))
        return "Try: Correlation between rainfall and yield for Wheat in 2017."

    else:
        return "I can answer questions about rainfall, crops, or correlation."

# -------------------------------
# 5️⃣ Example run
# -------------------------------
if __name__ == "__main__":
    print("🌾 Project Samarth — Intelligent Q&A System 🌦️")
    print("Ask natural questions like:")
    print(" • Compare rainfall between Tamil Nadu and Kerala in 2017")
    print(" • Top 3 crops in Maharashtra")
    print(" • Correlation between rainfall and yield for Rice in 2017\n")

    while True:
        q = input("Your question (or 'exit'): ")
        if q.lower() in ['exit', 'quit']:
            break
        print("\nAnswer:")
        print(answer_question(q))
        print("\n" + "-"*50 + "\n")
