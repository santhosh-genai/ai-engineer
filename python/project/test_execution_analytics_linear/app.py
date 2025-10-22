# app.py
import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import pickle
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
# --- Helper classes (adapted from your code) ---
class DatasetLoader:
    def __init__(self, file_path=None, dataframe=None):
        self.data = None
        if dataframe is not None:
            self.data = dataframe.copy()
        elif file_path:
            try:
                self.data = pd.read_csv(file_path)
            except Exception as e:
                st.error(f"Error loading dataset: {e}")

    def get_data(self):
        return self.data

    def set_data(self, data, file_path=None):
        self.data = data.copy()
        if file_path:
            self.data.to_csv(file_path, index=False)

class CleanedData(DatasetLoader):
    def __init__(self, file_path=None, dataframe=None):
        super().__init__(file_path=file_path, dataframe=dataframe)

    def fill_missing_values(self, numeric_only=True):
        try:
            data_cleaned = self.get_data().copy()
            if numeric_only:
                numeric_columns = data_cleaned.select_dtypes(include=[np.number]).columns
            else:
                numeric_columns = data_cleaned.columns
            for col in numeric_columns:
                mean = data_cleaned[col].mean()
                data_cleaned[col] = data_cleaned[col].fillna(mean)
            return data_cleaned
        except Exception as e:
            st.error(f"Error filling missing values: {e}")
            return self.get_data()

    def remove_outliers(self, data_cleaned, columns):
        try:
            df = data_cleaned.copy()
            for column in columns:
                if column not in df.columns:
                    continue
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
            return df
        except Exception as e:
            st.error(f"Error removing outliers: {e}")
            return data_cleaned

class DataScaler(CleanedData):
    def __init__(self, file_path=None, dataframe=None):
        super().__init__(file_path=file_path, dataframe=dataframe)
        self.scaler = StandardScaler()

    def scale_data(self, data, columns=None):
        try:
            data_scaled = data.copy()
            if columns is None:
                columns = data_scaled.select_dtypes(include=['float64', 'int64']).columns
            data_scaled[columns] = self.scaler.fit_transform(data_scaled[columns])
            return data_scaled
        except Exception as e:
            st.error(f"Error scaling data: {e}")
            return data

# --- Streamlit UI ---
st.set_page_config(page_title="Linear Regression Model", layout="wide")
# Main title with icon and themed color
st.markdown("<h1 style='font-size:30px;color:#0f4c81;margin:0;'>📊 Test Execution and Defect Count Prediction</h1>", unsafe_allow_html=True)

# Sidebar: data source
st.sidebar.header("Data source")
upload = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if upload is not None:
    # Read uploaded file into dataframe
    try:
        df_initial = pd.read_csv(upload)
    except Exception as e:
        st.sidebar.error(f"Upload error: {e}")
        df_initial = None
else:
    df_initial = None
    st.sidebar.info("Upload a CSV file to begin.")

# Main layout: 3 columns
left, middle, right = st.columns([1.2, 1, 1.2])

# Left: Data preview and cleaning options
with left:
    # header: 20px and themed color
    st.markdown("<h3 style='font-size:20px;color:#0f4c81;margin:0;'>Data preview & cleaning</h3>", unsafe_allow_html=True)
    if df_initial is not None:
        loader = DatasetLoader(dataframe=df_initial)
        df = loader.get_data()
    else:
        df = None

    if df is not None:
        # smaller subheader for raw/input sample
        st.markdown("<h4 style='font-size:14px;margin:4px 0 6px 0;'>Raw / Input sample (first 10 rows)</h4>", unsafe_allow_html=True)
        st.dataframe(df.head(10))

        # Missing value options
        st.markdown("**Missing values**")
        fill_mean = st.checkbox("Fill missing numeric values with mean", value=True)
        numeric_only = st.checkbox("Only apply mean to numeric columns", value=True)

        # Outlier removal options
        st.markdown("**Outlier removal (IQR)**")
        numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
        outlier_columns = st.multiselect("Choose numeric columns to remove outliers from", numeric_cols, default=numeric_cols[:3])
        run_clean = st.button("Run cleaning")

        if run_clean:
            cd = CleanedData(dataframe=df)
            if fill_mean:
                cleaned = cd.fill_missing_values(numeric_only=numeric_only)
            else:
                cleaned = cd.get_data().copy()
            if outlier_columns:
                cleaned = cd.remove_outliers(cleaned, outlier_columns)

            st.success("Cleaning completed.")
            # smaller subheader for cleaned data preview
            st.markdown("<h4 style='font-size:14px;margin:4px 0 6px 0;'>Cleaned data preview (first 10 rows)</h4>", unsafe_allow_html=True)
            st.dataframe(cleaned.head(10))

            # Allow saving cleaned CSV to session state
            st.session_state["cleaned_df"] = cleaned

            # Download cleaned CSV
            towrite = io.StringIO()
            cleaned.to_csv(towrite, index=False)
            st.download_button("Download cleaned CSV", data=towrite.getvalue(), file_name="cleaned_data.csv", mime="text/csv")

    else:
        st.info("No data loaded yet. Upload a CSV in the sidebar or set env path.")

# Middle: scaling & model training
with middle:
    # header: 20px and themed color
    st.markdown("<h3 style='font-size:20px;color:#0f4c81;margin:0;'>Scaling & Model Training</h3>", unsafe_allow_html=True)
    cleaned_df = st.session_state.get("cleaned_df", None)

    if cleaned_df is not None:
        # smaller subheader for scaling section
        st.markdown("<h4 style='font-size:14px;margin:4px 0 6px 0;'>Scaling</h4>", unsafe_allow_html=True)
        numeric_cols = list(cleaned_df.select_dtypes(include=[np.number]).columns)
        chosen_cols = st.multiselect("Columns to scale (numeric)", numeric_cols, default=numeric_cols)
        scale_button = st.button("Scale selected columns")
        if scale_button:
            scaler = DataScaler(dataframe=cleaned_df)
            scaled_df = scaler.scale_data(cleaned_df, columns=chosen_cols)
            st.success("Scaling completed.")
            st.session_state["scaled_df"] = scaled_df
            st.dataframe(scaled_df.head(8))
            # Download scaled
            s = io.StringIO()
            scaled_df.to_csv(s, index=False)
            st.download_button("Download scaled CSV", data=s.getvalue(), file_name="scaled_data.csv", mime="text/csv")
    else:
        st.info("Please run cleaning first.")

    st.markdown("---")
    # training section header: 20px and themed color
    st.markdown("<h3 style='font-size:20px;color:#0f4c81;margin:4px 0 8px 0;'>Train Linear Models</h3>", unsafe_allow_html=True)

    # Model feature/target selection
    st.markdown("**Select features & targets**")
    
    # Get the appropriate DataFrames for feature and target selection
    if "scaled_df" in st.session_state:
        df_features = st.session_state.scaled_df
    else:
        df_features = pd.DataFrame()
        st.warning("Please clean and scale your data first")
    
    # Use cleaned data for target selection
    if "cleaned_df" in st.session_state:
        df_targets = st.session_state.cleaned_df
    else:
        df_targets = pd.DataFrame()
        st.warning("Please clean your data first")
    
    feature_cols = list(df_features.columns) if not df_features.empty else []
    target_cols = list(df_targets.columns) if not df_targets.empty else []
    default_features = [c for c in feature_cols if c in [
        'Module_Complexity_Score', 'Test_Case_Count', 'Automation_Coverage',
        'Code_Churn', 'Defects_Previous_Cycle', 'Execution_Time_Previous'
    ]]
    selected_features = st.multiselect("Feature columns (scaled)", feature_cols, default=default_features) 
    if "cleaned_df" not in st.session_state:
        st.error("Please clean your data first before selecting target columns")
        target_time = None
        target_defects = None
    else:
        cleaned_cols = list(st.session_state.cleaned_df.columns)
        target_time = st.selectbox("Target: Execution Time column (from cleaned data)", 
                                options=cleaned_cols + [None], 
                                index=cleaned_cols.index('Estimated_Execution_Time') if 'Estimated_Execution_Time' in cleaned_cols else 0)
        target_defects = st.selectbox("Target: Defect Count column (from cleaned data)", 
                                   options=cleaned_cols + [None], 
                                   index=cleaned_cols.index('Expected_Defect_Count') if 'Expected_Defect_Count' in cleaned_cols else 0)

    test_size = st.slider("Test set fraction", min_value=0.05, max_value=0.5, value=0.2, step=0.05)
    random_state = st.number_input("Random state (int)", value=42, step=1)

    train_button = st.button("Train models")
    if train_button:
        # load appropriate dataframes: scaled features (X) and targets (y) from cleaned data
        scaled_df = st.session_state.get("scaled_df", None)
        cleaned_df = st.session_state.get("cleaned_df", None)

        if scaled_df is None:
            st.error("No scaled dataframe found. Scale data before training.")
        elif cleaned_df is None:
            st.error("No cleaned dataframe found. Clean data before training.")
        elif selected_features == []:
            st.error("Pick at least one feature column.")
        elif target_time is None or target_defects is None:
            st.error("Select both targets.")
        else:
            try:
                # Ensure we use exactly the same feature columns as linear_regression_model.py
                default_features = [
                    'Module_Complexity_Score',
                    'Test_Case_Count',
                    'Automation_Coverage',
                    'Code_Churn',
                    'Defects_Previous_Cycle',
                    'Execution_Time_Previous'
                ]
                
                # Features from scaled data, targets from cleaned data (to match linear_regression_model.py)
                X = scaled_df[default_features].values  # Use exact same features
                # Use cleaned data for targets
                y_time = cleaned_df['Estimated_Execution_Time'].values
                y_defects = cleaned_df['Expected_Defect_Count'].values

                # Use exact same split parameters
                X_train, X_test, y_train_time, y_test_time = train_test_split(X, y_time, test_size=0.2, random_state=42)
                _, _, y_train_defects, y_test_defects = train_test_split(X, y_defects, test_size=0.2, random_state=42)

                time_model = LinearRegression()
                time_model.fit(X_train, y_train_time)

                defect_model = LinearRegression()
                defect_model.fit(X_train, y_train_defects)

                y_pred_time = time_model.predict(X_test)
                y_pred_defects = defect_model.predict(X_test)

                # Metrics
                mse_time = mean_squared_error(y_test_time, y_pred_time)
                r2_time = r2_score(y_test_time, y_pred_time)

                mse_def = mean_squared_error(y_test_defects, y_pred_defects)
                r2_def = r2_score(y_test_defects, y_pred_defects)

                st.session_state["models"] = {"time_model": time_model, "defect_model": defect_model}
                st.session_state["last_eval"] = {
                    "y_test_time": y_test_time, "y_pred_time": y_pred_time,
                    "y_test_defects": y_test_defects, "y_pred_defects": y_pred_defects,
                    "mse_time": mse_time, "r2_time": r2_time,
                    "mse_def": mse_def, "r2_def": r2_def
                }

                st.success("Models trained and stored in session.")
                st.metric("Execution Time R²", f"{r2_time:.4f}")
                st.metric("Defect Count R²", f"{r2_def:.4f}")

            except Exception as e:
                st.error(f"Training error: {e}")

# Right: evaluation + plots + downloads
with right:
    # header: 20px and themed color
    st.markdown("<h3 style='font-size:20px;color:#0f4c81;margin:0;'>Evaluation & Downloads</h3>", unsafe_allow_html=True)
    eval_info = st.session_state.get("last_eval", None)
    if eval_info:
        # Metrics header: match Scaling style (h3)
        st.markdown("<h3 style='font-size:18px;margin:0;'>Metrics</h3>", unsafe_allow_html=True)
        st.write(f"Execution Time — MSE: {eval_info['mse_time']:.4f}, R²: {eval_info['r2_time']:.4f}")
        st.write(f"Defect Count — MSE: {eval_info['mse_def']:.4f}, R²: {eval_info['r2_def']:.4f}")

        # Prediction plots header: match Train Linear Models style
        st.markdown("<h3 style='font-size:20px;color:#0f4c81;margin:0;'>Prediction plots</h3>", unsafe_allow_html=True)
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        axes[0].scatter(eval_info["y_test_time"], eval_info["y_pred_time"])
        axes[0].plot(eval_info["y_test_time"], eval_info["y_test_time"], linestyle="--")
        axes[0].set_title("Execution Time: actual vs predicted")
        axes[0].set_xlabel("Actual")
        axes[0].set_ylabel("Predicted")

        axes[1].scatter(eval_info["y_test_defects"], eval_info["y_pred_defects"])
        axes[1].plot(eval_info["y_test_defects"], eval_info["y_test_defects"], linestyle="--")
        axes[1].set_title("Defects: actual vs predicted")
        axes[1].set_xlabel("Actual")
        axes[1].set_ylabel("Predicted")

        st.pyplot(fig)

        # Download models header: match Train Linear Models style
        st.markdown("<h3 style='font-size:20px;color:#0f4c81;margin:0;'>Download Models</h3>", unsafe_allow_html=True)
        models = st.session_state.get("models")
        if models:
            # time model
            time_bytes = io.BytesIO()
            pickle.dump(models["time_model"], time_bytes)
            time_bytes.seek(0)
            st.download_button("Download time model (.pkl)", data=time_bytes, file_name="time_model.pkl", mime="application/octet-stream")

            def_bytes = io.BytesIO()
            pickle.dump(models["defect_model"], def_bytes)
            def_bytes.seek(0)
            st.download_button("Download defect model (.pkl)", data=def_bytes, file_name="defect_model.pkl", mime="application/octet-stream")
    else:
        st.info("Train models to see evaluation and download options.")
