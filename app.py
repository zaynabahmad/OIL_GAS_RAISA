import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io


df = pd.read_csv("df_analysis.csv")

st.set_page_config(layout="wide")

st.title(" Feature vs Oil/Gas EUR with LOESS & Insights")

# Sidebar filters
formation_filter = st.sidebar.selectbox("Formation", ['All'] + list(df['FormationAlias'].unique()))
left_neigh_filter = st.sidebar.selectbox("Left Neighbour", ['All'] + list(df['LeftNeighbourType'].unique()))
right_neigh_filter = st.sidebar.selectbox("Right Neighbour", ['All'] + list(df['RightNeighbourType'].unique()))

filtered_df = df.copy()
if formation_filter != "All":
    filtered_df = filtered_df[filtered_df['FormationAlias'] == formation_filter]
if left_neigh_filter != "All":
    filtered_df = filtered_df[filtered_df['LeftNeighbourType'] == left_neigh_filter]
if right_neigh_filter != "All":
    filtered_df = filtered_df[filtered_df['RightNeighbourType'] == right_neigh_filter]

# Feature selection
features_all = [
    'TVD_imputed', 'NioGOR_imputed', 'FluidPerFoot_imputed','CodGOR_imputed',
    'ProppantPerFoot_imputed', 
    'BVHH_imputed' ,'LateralLength' ,
    'RightDistance_filled' , 'LeftDistance_filled', 'FormationAlias', 
    'LeftNeighbourType', 'RightNeighbourType'
]
features = [
    'BVHH_imputed', 'CodGOR_imputed', 'NioGOR_imputed',
    'LateralLength', 'FluidPerFoot_imputed', 'ProppantPerFoot_imputed',
    'TVD_imputed',
    'RightDistance_filled', 'LeftDistance_filled'
    # note: exclude categorical features 
]

st.markdown("## correlation between features ")

corr = df[features + ['NormalizedOilEUR', 'NormalizedGasEUR']].corr()

# Plot heatmap
fig_corr, ax_corr = plt.subplots(figsize=(12, 10))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": 0.75}, ax=ax_corr)
plt.title("Correlation Matrix", fontsize=14)

# Show the plot in Streamlit
st.pyplot(fig_corr)

st.markdown("## Distribution of Oil & Gas EUR by Categorical Features")

categorical_features = ['FormationAlias', 'LeftNeighbourType', 'RightNeighbourType']

selected_cat = st.radio("Select a Categorical Feature:", categorical_features, horizontal=True)

col1, col2 = st.columns(2)

with col1:
    fig_oil_cat, ax_oil_cat = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x=selected_cat, y='NormalizedOilEUR', ax=ax_oil_cat)
    ax_oil_cat.set_title(f'Oil EUR by {selected_cat}')
    ax_oil_cat.tick_params(axis='x', rotation=45)
    st.pyplot(fig_oil_cat)

with col2:
    fig_gas_cat, ax_gas_cat = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x=selected_cat, y='NormalizedGasEUR', ax=ax_gas_cat)
    ax_gas_cat.set_title(f'Gas EUR by {selected_cat}')
    ax_gas_cat.tick_params(axis='x', rotation=45)
    st.pyplot(fig_gas_cat)


st.markdown("## General Feature analysis on Gas and Oil with numerical Features  ")

feature = st.selectbox("Choose a numeric feature:", features)

# Plot with LOESS smoothing
col1, col2 = st.columns(2)

# Oil EUR
with col1:
    st.write("### Oil EUR vs", feature)
    fig_o, ax_o = plt.subplots()
    sns.regplot(
        x=feature, y='NormalizedOilEUR',
        data=filtered_df, lowess=True,
        scatter_kws={'s': 10}, line_kws={'color': 'red', 'label': 'LOESS'}
    )
    ax_o.legend()
    st.pyplot(fig_o)

# Gas EUR
with col2:
    st.write("### Gas EUR vs", feature)
    fig_g, ax_g = plt.subplots()
    sns.regplot(
        x=feature, y='NormalizedGasEUR',
        data=filtered_df, lowess=True,
        scatter_kws={'s': 10}, line_kws={'color': 'red', 'label': 'LOESS'}
    )
    ax_g.legend()
    st.pyplot(fig_g)

# Add insights
descriptions = {
'BVHH_imputed': """
**Rock Quality Insight (BVHH):**  

**Correlation with Gas:** Shows a moderate linear correlation of **+0.41** with NormalizedGasEUR.

**Relationship Type:** Exhibits a **non-linear positive relationship** with gas production — especially at higher BVHH values, indicating that better rock quality significantly enhances gas output.  

**With Oil:** Only a slight increase is observed, suggesting a weaker impact on oil compared to gas.  

**In general**, higher BVHH (rock quality) is a valuable predictor for **gas EUR**, particularly in formations with favorable geologic characteristics.
""",

'NioGOR_imputed': """  
**Gas/Oil Ratio in Niobrara Rock:**  

**NioGOR** is not a strong predictor for oil, and the impact is minimal and nearly flat.  

Initially, high GOR is a good sign for gas productivity, but extremely high values may indicate gas breakthrough, inefficiency, or reservoir limitations.

the rock could becomes less productive at very high GOR.  
""",

'CodGOR_imputed': """

**Gas/Oil Ration in Codell Rock:**

in general has a direct positive relation with gas produce and not very informative to oil

"""
,
'LateralLength':"""
**Lateral Length:**

slightly positive linear relation with oil (0.29)

in general has no direct relation neither with oil nor gas.

""",

'FluidPerFoot_imputed': """
**Fluid Per Foot:** 
fluid has positive relationwith oil

the gas increases as the fluid increase until a threshold at 1000 and then no change

""",

'ProppantPerFoot_imputed':"""
**Proppant Per Foot:** 
 
proppant has a slightly non linear effect on oil with positive

has positive linearity effect on oil with 0.23

and negative effect as it increases on gas

"""
,
'TVD_imputed':"""
**True Vertical Depth of the Well:**

not direct linear relationship with gas or oil

Increasing Gas EUR with Depth (up to ~7500) Deeper wells often tap into more mature rock layers with more hydrocarbons.

Decreasing Gas EUR after 8000 ft After (sweet spot curve ) a certain point:

* Reservoir quality may decline (tighter rock, less permeability).

* Higher pressure & temperature can lead to gas migration, meaning gas may have escaped over geological time.
""",


    'RightDistance_filled': "there is no relation with spacing at their own on oil and gas",
    'LeftDistance_filled': "there is no relation with spacing at their own on oil and gas."
}



st.markdown(f"**Insights :** {descriptions.get(feature, '')}")


# Binning selected features
binned_features = ['BVHH_imputed', 'TVD_imputed', 'FluidPerFoot_imputed', 'CodGOR_imputed', 'ProppantPerFoot_imputed' , 'NioGOR_imputed','LateralLength']
for feat in binned_features:
    bin_col = feat.replace('_imputed', '') + '_bin'
    df[bin_col] = pd.qcut(df[feat], q=3, labels=['low', 'medium', 'high'])


# Feature Interactions
st.markdown("##  Interactions Between Features and Their Impact on Oil & Gas")

st.markdown("### Custom Interaction Analysis")

# Custom interaction controls
selected_bin_feature = st.selectbox("Choose a feature to bin (categorize):", binned_features)
target_interact_feature = st.selectbox(
    "Choose a numeric feature to interact with:", 
    [f for f in features if f != selected_bin_feature]
)

# Generate bin column
bin_col = selected_bin_feature.replace('_imputed', '') + '_bin'
if bin_col not in df.columns:
    df[bin_col] = pd.qcut(df[selected_bin_feature], q=3, labels=['low', 'medium', 'high'])

st.markdown(f"### Interaction between **{selected_bin_feature} (binned)** and **{target_interact_feature}**")

col1, col2 = st.columns(2)

with col1 : 
    # Gas EUR plot
    st.markdown("####  Gas EUR")
    fig_custom_gas = sns.lmplot(
        data=filtered_df,
        x=target_interact_feature,
        y='NormalizedGasEUR',
        hue=bin_col,
        lowess=True,
        aspect=1.5,
        height=5,
        scatter_kws={'s': 20}
    )
    st.pyplot(fig_custom_gas.fig)


with col2 : 
    # Oil EUR plot
    st.markdown("####  Oil EUR")
    fig_custom_oil = sns.lmplot(
        data=filtered_df,
        x=target_interact_feature,
        y='NormalizedOilEUR',
        hue=bin_col,
        lowess=True,
        aspect=1.5,
        height=5,
        scatter_kws={'s': 20}
    )
    st.pyplot(fig_custom_oil.fig)


if (
    (target_interact_feature.lower() == 'niogor_imputed') and 
    (selected_bin_feature.lower() == 'bvhh_imputed')
):
    st.markdown("###  Insight Summary")
    
    st.markdown("""
    ####  **Gas EUR**
    - **Increases strongly** with NioGOR, especially at **higher BVHH**.
    - For all BVHH bins, as NioGOR increases, **Gas EUR increases** — but **dramatically** in the *high BVHH* bin.
    - This reflects that **better rock quality (high BVHH)** combined with **gas-rich reservoir (high NioGOR)** leads to significantly more **Gas EUR**.

    ####  **Oil EUR**
    - Shows a **non-linear trend**:
        - Peaks at **medium BVHH + low NioGOR** (~21.52).
        - Then **declines** as NioGOR increases, even in better rocks.
        - At **high BVHH + high NioGOR**, Oil EUR drops to around **18.45**.
    - This suggests that **higher NioGOR** indicates **more gas-dominant flow**, which might **reduce oil production**.
    - Possibly the **fluid composition (GOR)** dominates what gets produced from the well.
    """)

if target_interact_feature == 'ProppantPerFoot_imputed' and selected_bin_feature == 'BVHH_imputed':
    st.markdown("###  Insight Summary: Proppant Use vs Rock Quality (BVHH)")
    
    st.markdown(
        """
        **Gas EUR Trends:**

        - In **low to medium BVHH (poor to average rock)**: increasing proppant leads to **higher gas EUR**, as expected.
        - In **high BVHH (high rock quality)**:
            - Gas EUR initially increases with proppant, but eventually **plateaus** or **declines**.
            - This suggests **diminishing returns** or even **damage** from excessive stimulation.
            - **Codell and high-quality Niobrara** may benefit from **less aggressive proppant strategies**.

        **Oil EUR Trends:**

        - In **low and medium BVHH**, more proppant leads to a **slight increase** in oil EUR.
        - In **high BVHH**, oil production becomes **less responsive** to added proppant.

        **Takeaway:** 
        Completion design should be **rock-aware** — using too much proppant in high-quality zones can be **counterproductive**.
        """
    )




st.markdown("##  Export & Downloads")

# Create report
report = io.StringIO()
report.write(" Feature Insights Report\n\n")
report.write(f"Selected Feature: {feature}\n\n")
report.write(descriptions.get(feature, "No insight available.") + "\n\n")
report.write("Filters Applied:\n")
report.write(f"- Formation: {formation_filter}\n")
report.write(f"- Left Neighbour: {left_neigh_filter}\n")
report.write(f"- Right Neighbour: {right_neigh_filter}\n")
report.write("\n---\n\nCorrelation Matrix:\n")
report.write(corr.to_string())
report_text = report.getvalue()

# Download report
st.download_button("Download Report", report_text, file_name="feature_insights_report.txt")

# Download figures
heatmap_buf = io.BytesIO()
fig_corr.savefig(heatmap_buf, format="png")
st.download_button(" Download Correlation Heatmap", heatmap_buf.getvalue(), file_name="correlation_heatmap.png", mime="image/png")

oil_buf = io.BytesIO()
fig_o.savefig(oil_buf, format="png")
st.download_button(" Download Oil EUR Plot", oil_buf.getvalue(), file_name="oil_loess_plot.png", mime="image/png")

gas_buf = io.BytesIO()
fig_g.savefig(gas_buf, format="png")
st.download_button(" Download Gas EUR Plot", gas_buf.getvalue(), file_name="gas_loess_plot.png", mime="image/png")