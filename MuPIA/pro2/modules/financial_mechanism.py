#numpy, pandas
import numpy as np
import pandas as pd


class Subsidy():
    """Class of Subsidy Mechanism.
    """
    def __init__(self, measure, subsidy_rate):
        """
        Args:
            measure (dictionary): contains measure attributes.
            subsidy_rate (float): rate of subsidy of cost.
        """
        self.measure = measure
        self.subsidy_rate = subsidy_rate
        #: float: state cost based on subsidy rate
        self.state_cost = 0

        self.state_cost = self.measure['cost']*self.subsidy_rate*1.24
        cost = round(self.state_cost, 2)
        self.state_cost = cost


class Tax_depreciation():
    """Class of Tax Depreciation Mechanism.
    """
    def __init__(self, tax_rate, tax_depreciation_rate, tax_lifetime):
        """
        Args:
            tax_rate (float): annual tax rate.
            tax_depreciation_rate (float): rate of tax depreciation.
            tax_lifetime (int): how long this mechanism lasts in analysis.
        """
        self.tax_rate = tax_rate
        self.tax_depreciation_rate= tax_depreciation_rate
        self.tax_lifetime = tax_lifetime


class Loan(): 
    """Class of Loan Mechanism.
    """
    def __init__(self, logistic_cost, loan_rate, annual_interest, subsidized_interest, loan_period, grace_period):
        """
        Args:
            logistic_cost (float): initial cost that will be divided in loan amount and own funds amount.
            loan (float): how much of the logistic cost will be in loan amount.
            annual_interest (float): annual interest rate of loan.
            subsidizes_interest (float): annual subsidized interest rate of loan.
            loan_period (int): period that loan lasts. 
            grace_period (int): grace period of the repayment process. 
        """       
        self.logistic_cost = logistic_cost #with taxes
        self.loan_rate = loan_rate
        self.annual_interest = annual_interest
        self.subsidized_interest = subsidized_interest
        self.loan_period = loan_period
        self.grace_period = grace_period

        self.own_funds_rate = 1 - self.loan_rate
        self.own_fund = self.logistic_cost*self.own_funds_rate
        self.loan_fund = self.loan_rate*self.logistic_cost

        if self.loan_period == 0:
            self.calculate_loan_period()

        self.grace_period_tokos = self.annual_interest*self.grace_period*self.loan_fund
        self.repayment_amount = self.loan_fund + self.grace_period_tokos

        #: float: tok/ki dosi ana etos danismou
        self.interest_rate_instalment = []
        self.interest_rate_instalment.append(0)

        #: float: xreolisio ana etos danismou
        self.interest_rate = []
        self.interest_rate.append(0)

        #: float: tokos
        self.interest = []
        self.interest.append(0)

        #: float: epidotisi tokou 
        self.interest_subsidy = []
        self.interest_subsidy.append(0)

        #: float: tokos pliroteos 
        self.interest_paid = []
        self.interest_paid.append(0)

        #: float: aneksoflito ipolipo
        self.unpaid = []
        self.unpaid.append(self.repayment_amount)

        self.calculate_return_specs()

    def calculate_return_specs(self):
        """
            Calculate the necessary attributes for the loan repayment process.
            Each element is represented by a list of floats and contains the relevant annual values.
        """

        sum_xreolisio = 0
        for year in range(1, self.loan_period+1):
            self.interest_rate_instalment.append(-np.pmt(self.annual_interest, self.loan_period, self.repayment_amount, 0))
            self.interest_rate.append(-np.ppmt(self.annual_interest, year, self.loan_period, self.repayment_amount))
            self.interest.append(self.interest_rate_instalment[year] - self.interest_rate[year])
            if year == 1:
                self.interest_subsidy.append(self.repayment_amount*self.subsidized_interest)
            else:
                sum_xreolisio = sum_xreolisio + self.interest_rate[year-1]
                endiameso = self.repayment_amount - sum_xreolisio
                self.interest_subsidy.append(endiameso*self.subsidized_interest)
            
            self.interest_paid.append(self.interest[year] - self.interest_subsidy[year])
            self.unpaid.append(self.unpaid[year-1] - self.interest_rate[year])

    def calculate_loan_period(self):
        """
            If user does not enter a specific loan period, 
            it is calculated based on the condition statement below. 
        """
        if self.loan_fund < 15000: 
            self.loan_period = 3
        else: 
            self.loan_period = 10
    

class Esco():
    def __init__(self, measure, energy_savings, avg_ratios, criterion, criterion_value, criterion_satisfaction, discount_rate, cost_share_rate, benefit_share_rate, contract_period, loan):
        self.measure = measure
        self.energy_savings = energy_savings
        self.avg_ratios = avg_ratios
        self.criterion = criterion
        self.criterion_value = criterion_value
        self.criterion_satisfaction = criterion_satisfaction
        self.discount_rate = discount_rate
        self.cost_share_rate = cost_share_rate
        self.benefit_share_rate = benefit_share_rate 
        self.contract_period = contract_period
        self.loan = loan

        self.costs = pd.DataFrame([])
        self.benefits = pd.DataFrame([])
        self.pure_discounted_cash_flow = []

        self.sum_costs = 0
        self.sum_benefits = 0

        """

        Investment sustainability criteria:
            PV κόστους
            PV οφέλους
            NPV
            B/C ratio
            IRR
            Simple Payback period (years)
            Discounted Payback period (years)

        """
        self.cost_pv = 0.0 
        self.benefit_pv = 0.0
        self.npv = 0.0
        self.b_to_c = 0.0
        self.irr = 0.0
        self.profit = 0.0
        self.pbp = 0.0
        self.dpbp = 0.0

        if self.benefit_share_rate > 0:
            self.initialize_criterion_params()
            self.construct_benefits_df()
            self.construct_cost_df()
            self.esco_criterion_satisfy()
            self.measure_judgement()

    def initialize_criterion_params(self):
        if self.criterion_satisfaction == 'benefit_share':
            self.benefit_share_rate = 1
        elif self.criterion_satisfaction == 'contract_period':
            self.contract_period = 1

    def construct_benefits_df(self):
        esco_savings = []
        for year in range(len(self.energy_savings)):
            if year < self.contract_period:
                esco_savings.append(self.benefit_share_rate*self.energy_savings[year])
            else:
                esco_savings.append(0)
        rounded_savings = [ round(elem, 2) for elem in esco_savings ]
        self.benefits['Energy savings'] = rounded_savings
        flow = []
        self.pure_discounted_cash_flow = esco_savings
        for year in range(len(self.energy_savings)):
            if year < self.contract_period:
                flow.append(esco_savings[year]/(1.0 + self.discount_rate)**year)
            else:
                self.pure_discounted_cash_flow.append(0)
                flow.append(0)
        rounded_flow = [ round(elem, 2) for elem in flow ]
        self.benefits['Discounted Cash Flow'] = rounded_flow

    def construct_cost_df(self):
        initial_cost = []
        if self.loan.loan_fund > 0:
            esco_loan = Loan(self.measure['cost']*self.cost_share_rate, self.loan.loan_rate, self.loan.annual_interest, self.loan.subsidized_interest,self.loan.loan_period, self.loan.grace_period)
        
        for year in range(len(self.energy_savings)):
            if self.loan.loan_fund == 0:
                if year == 0:            
                    initial_cost.append(self.measure['cost']*self.cost_share_rate)
                else:
                    initial_cost.append(0)
            else:
                if year == 0:
                    initial_cost.append(esco_loan.own_fund)
                else:
                    if year <= esco_loan.loan_period:
                        initial_cost.append(esco_loan.interest_rate[year]/1.24 + esco_loan.interest_paid[year])
                    else:
                        initial_cost.append(0)
        rounded_cost = [ round(elem, 2) for elem in initial_cost ]
        self.costs['Equipment Cost'] = rounded_cost
        flow = []
        sum_costs = self.costs.sum(axis=1)
        for year in range(len(self.energy_savings)):
            self.pure_discounted_cash_flow[year] = self.pure_discounted_cash_flow[year] - sum_costs[year]
            flow.append(sum_costs[year]/(1.0 + self.discount_rate)**year)
        rounded_flow = [ round(elem, 2) for elem in flow ]
        self.costs['Discounted Cash Flow'] = rounded_flow

    def calculate_simplePBP(self):
        pbp = 1 
        diff = self.pure_discounted_cash_flow[0]
        while diff < 0 and pbp < len(self.pure_discounted_cash_flow)-1:
            diff = diff + self.pure_discounted_cash_flow[pbp]
            pbp = pbp +1 
        return pbp

    def calculate_discountedPBP(self):
        dpbp = float(np.log((self.pbp*(1+self.discount_rate))*(float((1 + self.avg_ratios))/(1+self.discount_rate)-1)+1))/np.log(float(1 + self.avg_ratios)/(1+self.discount_rate))
        rounded_dpbp = round(dpbp, 2)
        dpbp = rounded_dpbp
        return dpbp
    
    def get_benefit_share(self):
        self.benefit_share_rate = self.sum_benefits/self.benefits['Energy savings'].sum()
        rounded_rate = round(self.benefit_share_rate, 2)
        self.benefit_share_rate = rounded_rate
        print(self.benefit_share_rate)


    def calc_cp(self):
        sum = 0
        self.contract_period = 0
        while sum < self.sum_benefits and self.contract_period < len(self.energy_savings):
            self.contract_period = self.contract_period + 1
            sum = sum + self.energy_savings[self.contract_period-1]*self.benefit_share_rate
        print(self.contract_period)
    
    def calc_cp_disc(self):
        sum = 0
        self.contract_period = 0
        while sum < self.sum_benefits and self.contract_period < len(self.energy_savings):
            self.contract_period = self.contract_period + 1
            sum = sum + self.energy_savings[self.contract_period-1]*self.benefit_share_rate/(1+self.discount_rate)**(self.contract_period-1)
        print(self.contract_period)

    def esco_criterion_satisfy(self):
        if self.criterion == "npv":          
            if self.criterion_satisfaction == 'benefit_share':
                self.sum_benefits = self.costs['Discounted Cash Flow'].sum() + self.criterion_value
                self.benefit_share_rate = self.sum_benefits/self.benefits['Discounted Cash Flow'].sum()
                rounded_rate = round(self.benefit_share_rate, 2)
                self.benefit_share_rate = rounded_rate
                self.benefits = pd.DataFrame([])
                self.construct_benefits_df()
                print(self.benefit_share_rate)
            if self.criterion_satisfaction == 'contract_period':
                self.sum_benefits = self.costs['Discounted Cash Flow'].sum() + self.criterion_value
                self.calc_cp_disc()
                self.benefits = pd.DataFrame([])
                self.construct_benefits_df()

        if self.criterion == "b_to_c":
            if self.criterion_satisfaction == 'benefit_share':
                self.sum_benefits = self.costs['Equipment Cost'].sum()*self.criterion_value
                self.get_benefit_share()
                self.benefits = pd.DataFrame([])
                self.construct_benefits_df()
            if self.criterion_satisfaction == 'contract_period':
                self.sum_benefits = self.costs['Equipment Cost'].sum()*self.criterion_value
                self.calc_cp()
                self.benefits = pd.DataFrame([])
                self.construct_benefits_df()

        if self.criterion == "profit":
            if self.criterion_satisfaction == 'benefit_share':
                self.sum_benefits = self.costs['Equipment Cost'].sum()*(1+self.criterion_value)
                self.get_benefit_share()
                self.benefits = pd.DataFrame([])
                self.construct_benefits_df()
            if self.criterion_satisfaction == 'contract_period':
                self.sum_benefits = self.costs['Equipment Cost'].sum()*(1+self.criterion_value)
                self.calc_cp()
                self.benefits = pd.DataFrame([])
                self.construct_benefits_df()
    
    def measure_judgement(self):
        self.cost_pv = round(self.costs['Discounted Cash Flow'].sum(), 2)
        self.benefit_pv = round(self.benefits['Discounted Cash Flow'].sum(),2)
        self.npv = round(self.benefit_pv - self.cost_pv, 2)
        self.b_to_c = round(self.benefit_pv/self.cost_pv, 2)
        self.irr = round(np.irr(self.pure_discounted_cash_flow), 2)
        self.pbp = round(self.calculate_simplePBP(), 2)
        self.dpbp = round(self.calculate_discountedPBP(), 2)
        sum1 = self.costs['Equipment Cost'].sum()
        if sum1 !=0 :
            self.profit = round((self.benefits['Energy savings'].sum() - self.costs['Equipment Cost'].sum())/sum1, 2)
