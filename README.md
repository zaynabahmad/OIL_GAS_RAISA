# Oil & Gas EUR Analysis & Visualization

This project provides a detailed end-to-end analysis of factors affecting **Normalized Oil and Gas EUR** (Estimated Ultimate Recovery) using engineering and geological features. The analysis includes **data preprocessing**, **feature engineering**, and **interactive visualization** via a **Streamlit web application**.

---

## Project Structure

- **Data Understanding**
- **Data Cleaning**
  - Handling zeros
  - Outliers in numerical features
  - Bad values in categorical features
- **Missing Data Imputation**
- **Exploratory Data Analysis (EDA)**
  - Individual feature analysis
  - Categorical feature distributions
  - Interactions between features
- **Feature Engineering**
  - Creating binned versions of key features
  - Imputation columns
- **Visualization**
  - Heatmap correlation matrix
  - LOESS smoothing plots
  - Interactive feature interaction analysis
  - Streamlit dashboard with filters, insights, and download options

---

## 1. Data Understanding

Initial exploration and knowing the features such as:

- **Rock quality**: `BVHH`
- **Well depth**: `TVD`
- **Gas-oil ratios**: `CodGOR`, `NioGOR`
- **Fracture stimulation inputs**: `FluidPerFoot`, `ProppantPerFoot`
- **Well spacing**: `Left/RightNeighbourType`, `Left/RightDistance`

Categorical features like `FormationAlias`, `NeighbourTypes`.

###### started by exploring the dataset to get an overall understanding of its structure and quality.

- i used `df.describe()`, `df.info()`, and `.shape` to check the basic stats, data types, and dataset size.
- I found that several columns had **missing values**, especially in key numerical features like `BVHH`, `GOR`, `TVD`, and `FluidPerFoot`, so I calculated the percentage of missing data to assess its impact.
- Then, i visualized the **distributions** of numerical features using histograms to detect **outliers** and skewed data.
- I also plotted **boxplots** for the main categorical variables (`FormationAlias`, `LeftNeighbourType`, and `RightNeighbourType`) to see how they affect both oil and gas EUR.
- To understand which features are most useful, I built **Random Forest models** for both `NormalizedOilEUR` and `NormalizedGasEUR`, and extracted **feature importance scores**.

![understanding data ](images/image%20evaluation.png)


###  Outcome:
I found that:
- Some features had strong influence, like `BVHH`, `TVD`, and `ProppantPerFoot`.
- There’s a lot of missing and noisy data that I need to clean and impute properly.

![understanding data ](images/image.png)


---

## 2. Dealing with Zeros

I explored the features `ProppantPerFoot` and `FluidPerFoot`, where I found several wells with **zero values**, which raised concern.

#### Initial Investigation
- Plotted **histograms and boxplots** to inspect distributions and detect suspicious values.
- Found a noticeable number of **wells with Proppant = 0**, which seemed unrealistic at first.

####  Domain Research
- While analyzing, I found **Proppant = 0** can **technically occur** in certain completion strategies — so I couldn't discard zeros immediately without further analysis.

####  Clustering & PCA for Validation
To assess whether the zero entries were **outliers or valid patterns**, I:
- Applied **KMeans clustering** on zero-proppant wells using features like `TVD`, EURs, GORs, etc.
- Used **PCA for dimensionality reduction** to visualize clusters.
- Identified **minority clusters as suspicious** and flagged them for further review.

####  Result
- Replaced only the **suspicious zero values** in `ProppantPerFoot` with `NaN` to be handled later.
- Left **valid zeros** untouched based on domain reasoning and cluster behavior.

> This approach ensured that **true engineering cases weren't discarded**, while **data issues were still addressed**.

![understanding data ](images/image_zeros.png)


---

## 3. Outliers & Bad Data

### Numerical Features

####  Outlier Clipping for Skewed Distributions
I observed extreme values in `ProppantPerFoot` and `FluidPerFoot`, which could bias the analysis. To address this:
- I **clipped** the values to the [0.04%, 99.8%] quantile range using `pandas.clip()`.
- This kept the data range realistic without removing too many samples.
- Boxplots before and after clipping showed much cleaner distributions.

![understanding data ](images/proppant.png)

####  Handling Invalid BVHH Values
- The `BVHH` feature had **two negative values**, which are **physically invalid**.
- Upon inspection, both rows also had **missing `LeftDistance`**, which made them unreliable.
- I **dropped** those rows instead of imputing, to avoid injecting noise.

####  EUR Features Inspection
- Boxplots for `NormalizedOilEUR` and `NormalizedGasEUR` revealed a few extreme values.
- I manually inspected these points (Oil EUR > 95) but left them untouched for now as they could represent **valid high-performing wells**.

####  Duplicate Detection
- I checked for **duplicate wells** using `WellID`.


###  Categorical Features

I explored the three key categorical features in the dataset:

####  `FormationAlias`
- The two main categories are:
  - `Niobrara`: **dominates the dataset** with more than **double** the number of wells compared to `Codell`.
- This imbalance is important as it may **bias the model** toward Niobrara-related trends.

![understanding data ](images/niobrara.png)


####  `LeftNeighbourType`
- Distribution:
  - `Codeveloped`: 6046 wells
  - `NoNeighbour`: 2448 wells
  - `Parent`: 712 wells
- There is a clear skew toward the `Codeveloped` category.

####  `RightNeighbourType`
- Nearly identical distribution as `LeftNeighbourType`, indicating symmetrical development patterns.

> I noted the **imbalance** in categories as it can influence statistical comparisons and model predictions. I’ll keep this in mind during modeling and visualization to avoid misleading interpretations.

---

## 4. Missing Data

- Created new columns with `_imputed` suffix for features after imputation.
- For spatial-related features (e.g., distances), incorporated neighbor data if available.

---

## 5. Exploratory Data Analysis (EDA)

### General Feature Analysis

- Used **LOESS regression** to visualize non-linear relationships with:

  - `NormalizedOilEUR`
  - `NormalizedGasEUR`
- Each feature has custom written insight displayed dynamically.

### Categorical Feature Distributions

- Created boxplots for:

  - `FormationAlias`
  - `LeftNeighbourType`
  - `RightNeighbourType`
- Used radio buttons to toggle between categories for clear comparison.

### Feature Interactions

- Binned selected features into `low`, `medium`, and `high`.
- Used `sns.lmplot()` to show interactions between binned and continuous variables.
- Plots are shown for both **Oil EUR** and **Gas EUR**.

---

## 6. Feature Engineering

- Added `*_imputed` versions of each numerical feature with missing values handled.
- Created `*_bin` versions for interaction analysis.
- Filtered irrelevant or non-numeric columns before visualization.

---

## 7. Streamlit App

The full analysis is integrated into a **Streamlit App** featuring:

- **Sidebar filters** for Formation and Neighbour Types
- **LOESS plots** for each selected feature
- **Feature insight descriptions** (automated)
- **Custom interaction analysis** using dynamic feature pairs
- **Categorical distribution comparison**
- **Download options**:
- Feature summary report
- Heatmap and LOESS plots

To launch the app:

```bash
streamlit run app.py

```

## Outputs

The Streamlit app provides various downloadable and interactive outputs:

###  Reports

- **`feature_insights_report.txt`**:Auto-generated text report summarizing:
  - Selected numerical feature
  - Interpretation and insights
  - Applied filters (Formation, Neighbours)
  - Correlation matrix table

###  Visuals (as `.png`)

- **`correlation_heatmap.png`**:Heatmap showing correlation between all numerical features and Oil/Gas EUR.
- **`oil_loess_plot.png`** & **`gas_loess_plot.png`**:
  LOESS-smoothed scatter plots for the selected feature vs. Oil/Gas EUR.

>  All plots are downloadable directly from the Streamlit interface.

###  Interactive Plots

Displayed directly inside the Streamlit app:

- General feature behavior with EUR values
- Dynamic interaction plots (binned × continuous features)
- Categorical feature distributions (via boxplots)
