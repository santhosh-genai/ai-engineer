import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

# ---------------------------------------------------
# Page config (matches your reference app)
# ---------------------------------------------------
st.set_page_config(page_title="Sales Prediction Demo", layout="wide")

st.markdown(
    "<h1 style='font-size:30px;color:#0f4c81;margin:0;'>📈 Advertising Spend vs Sales Prediction</h1>",
    unsafe_allow_html=True
)

# ---------------------------------------------------
# Sidebar – Data source
# ---------------------------------------------------
st.sidebar.header("Data Source")
uploaded_file = st.sidebar.file_uploader("Upload sales CSV", type=["csv"])

# ---------------------------------------------------
# Main layout (3 columns – same as reference)
# ---------------------------------------------------
left, middle, right = st.columns([1.2, 1, 1.2])

# ---------------------------------------------------
# LEFT: Data preview & scatter plot
# ---------------------------------------------------
with left:
    st.markdown(
        "<h3 style='font-size:20px;color:#0f4c81;'>Data Preview</h3>",
        unsafe_allow_html=True
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(10))

        X = df[['Advertising_Spend']]
        y = df['Total Amount']

        st.markdown("**Scatter Plot**")
        fig, ax = plt.subplots()
        ax.scatter(X, y)
        ax.set_xlabel("Advertising Spend")
        ax.set_ylabel("Total Amount (Sales)")
        ax.set_title("Advertising Spend vs Total Amount")
        st.pyplot(fig)
    else:
        st.info("Upload a CSV file to begin.")

# ---------------------------------------------------
# MIDDLE: Model configuration & training
# ---------------------------------------------------
with middle:
    st.markdown(
        "<h3 style='font-size:20px;color:#0f4c81;'>Model Configuration</h3>",
        unsafe_allow_html=True
    )

    if uploaded_file:
        model_type = st.radio(
            "Regression Type",
            ["Linear Regression", "Polynomial Regression"]
        )

        degree = 1
        if model_type == "Polynomial Regression":
            degree = st.slider("Polynomial Degree", 2, 3, 2)

        test_size = st.slider("Test Size", 0.1, 0.5, 0.2, step=0.05)

        train_btn = st.button("Train Model")

        if train_btn:
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )

            if model_type == "Linear Regression":
                model = LinearRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                X_plot = X_test

            else:
                poly = PolynomialFeatures(degree=degree)
                X_train_poly = poly.fit_transform(X_train)
                X_test_poly = poly.transform(X_test)

                model = LinearRegression()
                model.fit(X_train_poly, y_train)
                y_pred = model.predict(X_test_poly)

                # Smooth curve
                X_plot = np.linspace(
                    X.min()[0], X.max()[0], 200
                ).reshape(-1, 1)
                X_plot = poly.transform(X_plot)

            # Metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)

            st.session_state["results"] = {
                "model": model,
                "y_test": y_test,
                "y_pred": y_pred,
                "X_test": X_test,
                "X_plot": X_plot,
                "degree": degree,
                "type": model_type,
                "metrics": (mse, rmse, r2)
            }

            st.success("Model trained successfully!")

# ---------------------------------------------------
# RIGHT: Evaluation & plots
# ---------------------------------------------------
with right:
    st.markdown(
        "<h3 style='font-size:20px;color:#0f4c81;'>Evaluation</h3>",
        unsafe_allow_html=True
    )

    results = st.session_state.get("results")

    if results:
        mse, rmse, r2 = results["metrics"]

        st.metric("MSE", f"{mse:.2f}")
        st.metric("RMSE", f"{rmse:.2f}")
        st.metric("R² Score", f"{r2:.4f}")

        st.markdown("**Actual vs Predicted**")
        
        fig, ax = plt.subplots()
        ax.scatter(results["y_test"], results["y_pred"], label="Predicted")
        ax.plot(results["y_test"], results["y_test"], linestyle="--", label="Ideal")
        ax.set_xlabel("Actual Sales")
        ax.set_ylabel("Predicted Sales")
        ax.legend()
        st.pyplot(fig)

        st.markdown("**Regression Curve**")

        fig2, ax2 = plt.subplots()
        ax2.scatter(X, y, label="Actual Data")

        if results["type"] == "Linear Regression":
            y_curve = results["model"].predict(X)
            ax2.plot(X, y_curve, color="green", label="Regression Line")
        else:
            y_curve = results["model"].predict(results["X_plot"])
            ax2.plot(
                np.linspace(X.min()[0], X.max()[0], 200),
                y_curve,
                color="green",
                label=f"Polynomial Degree {results['degree']}"
            )

        ax2.set_xlabel("Advertising Spend")
        ax2.set_ylabel("Total Amount (Sales)")
        ax2.legend()
        st.pyplot(fig2)

    else:
        st.info("Train a model to view evaluation results.")
