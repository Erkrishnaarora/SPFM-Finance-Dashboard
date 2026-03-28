# Project: SPFM Finance Dashboard
# Developed by: Krishna Arora
# Year: 2025
# Description: Personal Finance Management and Analytics Dashboard for tracking income, expenses, and financial insights
# GitHub: https://github.com/ErKrishnaarora
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

file_name = "finance_data.csv"
search_file = "search_history.csv"

# Create finance file if not exists
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=["Type", "Category", "Amount"])
    df.to_csv(file_name, index=False)

# Create search history file
if not os.path.exists(search_file):
    df = pd.DataFrame(columns=["Category", "Amount"])
    df.to_csv(search_file, index=False)

st.title(" Smart Personal Finance Manager (SPFM)")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Income",
        "Add Expense",
        "View Data",
        "Search Expense",
        "Expense Pie Chart",
        "Income vs Expense",
        "Category Spending",
        "Delete Specific Record",
        "Clear All Data"
    ]
)

# ================= ADD INCOME =================
if menu == "Add Income":

    st.header("Add Income")

    category = st.text_input("Income Source")

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=0.01,
        format="%.2f"
    )

    if st.button("Add Income"):

        df = pd.read_csv(file_name)

        new_row = pd.DataFrame(
            [["Income", category, amount]],
            columns=["Type", "Category", "Amount"]
        )

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(file_name, index=False)

        st.success("Income Added Successfully")


# ================= ADD EXPENSE =================
elif menu == "Add Expense":

    st.header("Add Expense")

    category = st.text_input("Expense Category")

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=0.01,
        format="%.2f"
    )

    if st.button("Add Expense"):

        df = pd.read_csv(file_name)

        new_row = pd.DataFrame(
            [["Expense", category, amount]],
            columns=["Type", "Category", "Amount"]
        )

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(file_name, index=False)

        st.success("Expense Added Successfully")


# ================= VIEW DATA =================
elif menu == "View Data":

    st.header("Finance Records")

    df = pd.read_csv(file_name)

    st.dataframe(df)

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()

    balance = income - expense

    st.write("Total Income:", income)
    st.write("Total Expense:", expense)
    st.write("Balance:", balance)

    if expense > income:
        st.error(" Warning: Your expenses exceeded your income!")
    else:
        st.success(" Your finances are under control.")


# ================= SEARCH EXPENSE =================
elif menu == "Search Expense":

    st.header("Search Expense by Category")

    search_category = st.text_input("Enter Category")

    if st.button("Search"):

        df = pd.read_csv(file_name)

        result = df[
            (df["Type"] == "Expense") &
            (df["Category"].str.lower() == search_category.lower())
        ]

        if not result.empty:

            st.success("Expense Found")
            st.dataframe(result)

            total = result["Amount"].sum()

            st.write("Total Spending on", search_category, ":", total)

            history = pd.read_csv(search_file)

            new_row = pd.DataFrame(
                [[search_category, total]],
                columns=["Category", "Amount"]
            )

            history = pd.concat([history, new_row], ignore_index=True)
            history.to_csv(search_file, index=False)

        else:
            st.warning("No expense found")


# ================= PIE CHART =================
elif menu == "Expense Pie Chart":

    st.header("Expense Distribution")

    df = pd.read_csv(file_name)

    expense_data = df[df["Type"] == "Expense"]

    if not expense_data.empty:

        category_sum = expense_data.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots()

        colors = ["red", "blue", "green", "orange", "purple"]

        ax.pie(
            category_sum,
            labels=category_sum.index,
            autopct='%1.1f%%',
            colors=colors
        )

        ax.set_title("Expense Distribution")

        st.pyplot(fig)

    else:
        st.warning("No expense data available")


# ================= INCOME VS EXPENSE =================
elif menu == "Income vs Expense":

    st.header("Income vs Expense Comparison")

    df = pd.read_csv(file_name)

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()

    labels = ["Income", "Expense"]
    values = [income, expense]

    fig, ax = plt.subplots()

    ax.bar(labels, values, color=["green", "red"])

    ax.set_title("Income vs Expense")
    ax.set_ylabel("Amount")

    st.pyplot(fig)


# ================= CATEGORY SPENDING =================
elif menu == "Category Spending":

    st.header("Spending by Category")

    df = pd.read_csv(file_name)

    expense_data = df[df["Type"] == "Expense"]

    if not expense_data.empty:

        category_sum = expense_data.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots()

        category_sum.plot(kind="bar", ax=ax, color="orange")

        ax.set_title("Category Spending")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount")

        st.pyplot(fig)

    else:
        st.warning("No expense data available")


# ================= DELETE SPECIFIC RECORD =================
elif menu == "Delete Specific Record":

    st.header("Delete Specific Record")

    df = pd.read_csv(file_name)

    st.dataframe(df)

    if not df.empty:

        row_number = st.number_input(
            "Enter Row Number to Delete",
            min_value=0,
            max_value=len(df)-1,
            step=1
        )

        if st.button("Delete Row"):

            df = df.drop(row_number)
            df = df.reset_index(drop=True)

            df.to_csv(file_name, index=False)

            st.success("Record Deleted Successfully")

    else:
        st.warning("No records available")


# ================= CLEAR ALL DATA =================
elif menu == "Clear All Data":

    st.header("Delete All Records")

    if st.button("Clear Finance Data"):

        if os.path.exists(file_name):
            os.remove(file_name)

        df = pd.DataFrame(columns=["Type", "Category", "Amount"])
        df.to_csv(file_name, index=False)

        st.success("All finance data cleared successfully")