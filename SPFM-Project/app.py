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

# Create file if not exists
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=["Type", "Category", "Amount"])
    df.to_csv(file_name, index=False)

st.title("Smart Personal Finance Manager (SPFM)")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Income",
        "Add Expense",
        "View Data",
        "Expense Pie Chart",
        "Income vs Expense",
        "Category Spending"
    ]
)

# ADD INCOME
if menu == "Add Income":

    st.header("Add Income")

    category = st.text_input("Income Source")
    amount = st.number_input("Amount", min_value=0)

    if st.button("Add Income"):

        df = pd.read_csv(file_name)

        new_row = pd.DataFrame(
            [["Income", category, amount]],
            columns=["Type", "Category", "Amount"]
        )

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(file_name, index=False)

        st.success("Income Added Successfully")


# ADD EXPENSE
elif menu == "Add Expense":

    st.header("Add Expense")

    category = st.text_input("Expense Category")
    amount = st.number_input("Amount", min_value=0)

    if st.button("Add Expense"):

        df = pd.read_csv(file_name)

        new_row = pd.DataFrame(
            [["Expense", category, amount]],
            columns=["Type", "Category", "Amount"]
        )

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(file_name, index=False)

        st.success("Expense Added Successfully")


# VIEW DATA
elif menu == "View Data":

    st.header("Finance Records")

    df = pd.read_csv(file_name)

    st.dataframe(df)

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()

    st.write("Total Income:", income)
    st.write("Total Expense:", expense)
    st.write("Balance:", income - expense)


# PIE CHART
elif menu == "Expense Pie Chart":

    st.header("Expense Distribution")

    df = pd.read_csv(file_name)

    expense_data = df[df["Type"] == "Expense"]

    if not expense_data.empty:

        category_sum = expense_data.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots()

        ax.pie(
            category_sum,
            labels=category_sum.index,
            autopct='%1.1f%%'
        )

        ax.set_title("Expense Distribution")

        st.pyplot(fig)

    else:
        st.warning("No expense data available")


# INCOME VS EXPENSE
elif menu == "Income vs Expense":

    st.header("Income vs Expense Comparison")

    df = pd.read_csv(file_name)

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()

    labels = ["Income", "Expense"]
    values = [income, expense]

    fig, ax = plt.subplots()

    ax.bar(labels, values)

    ax.set_title("Income vs Expense")
    ax.set_ylabel("Amount")

    st.pyplot(fig)


# CATEGORY SPENDING
elif menu == "Category Spending":

    st.header("Spending by Category")

    df = pd.read_csv(file_name)

    expense_data = df[df["Type"] == "Expense"]

    if not expense_data.empty:

        category_sum = expense_data.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots()

        category_sum.plot(kind="bar", ax=ax)

        ax.set_title("Category Spending")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount")

        st.pyplot(fig)

    else:
        st.warning("No expense data available")