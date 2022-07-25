# -*- coding: utf-8 -*-
"""
Finds eligible loans
"""
from qualifier.utils.fileio import (
    load_csv,
    save_csv
)
from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)
from qualifier.functions.max_loan_size import filter_max_loan_size
from qualifier.functions.credit_score import filter_credit_score
from qualifier.functions.debt_to_income import filter_debt_to_income
from qualifier.functions.loan_to_value import filter_loan_to_value
from pathlib import Path
import os

path = Path(os.path.dirname(__file__))
PROJECT_DIR = path.parent.parent.absolute()

import pandas as pd

def get_data():
    return pd.read_csv(str(PROJECT_DIR) + r'\data\data.csv')

def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)

    # Run qualification filters
    bank_data_filtered = bank_data[(loan_to_value_ratio<bank_data['Max LTV']) & (monthly_debt_ratio<bank_data['Max DTI']) & \
                                    (bank_data['Min Credit Score']<int(credit_score)) & (int(loan)<bank_data['Max Loan Amount'])]
    '''
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)
    '''
    return list(bank_data_filtered['Lender'].unique())

def get_stats(bank_data,value,feature):

    if feature == 'Max LTV':
        count = len(bank_data[value<bank_data['Max LTV']])
        where_you_stand = f'There are {count} banks which grant loans for this feature. You have to decrease your loan value to increase your chances'
    elif feature == 'Max DTI':
        count = len(bank_data[value<bank_data['Max DTI']])
        where_you_stand = f'There are {count} banks which grant loans for this feature. You have to increase your income to increase your chances'
    elif feature == 'Min Credit Score':
        count = len(bank_data[bank_data['Min Credit Score']<value*1000])
        where_you_stand = f'There are {count} banks which grant loans for this feature. You have to increase your credit score to increase your chances'
    elif feature == 'Max Loan Amount':
        count = len(bank_data[value<bank_data['Max Loan Amount']])
        where_you_stand = f'There are {count} banks which grant loans for this feature. You have to decrease your loan amount to increase your chances'
        
    return where_you_stand