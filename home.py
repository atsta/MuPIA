import energy_measure
import social_investment_analysis
import financial_investment_analysis
import investment_analysis_perspective
import loan

import decimal 

def main():
    #select actors 
    #select measures 
    #check social 
    #check financial 
    #check esco 
    #check every other perspective
    #check for subsidy
    #return cost and whatever for each actor

    """
    analysis = input('Select analysis: ')
    input_measure = input('Select a measure: ')
    measure = energy_measure.Measure(input_measure)
    if analysis.strip() == 'Social':
        print("Social analysis for measure %s" % (input_measure))
        #print(measure.get_cost())
        scba = social_investment_analysis.Social(measure.get_cost(), measure.get_lifetime(), measure.get_externalities(), measure.get_energy_conservation())

    elif analysis.strip() == 'Financial': 
        print("Financial analysis for measure %s" % (input_measure))
        fcba = financial_investment_analysis.Financial(measure.get_cost(), measure.get_lifetime(), measure.get_externalities(), measure.get_energy_conservation())
        
    else: 
        analysis = input('Select analysis: ')
    
    #analysis from business perspective
    persp = investment_analysis_perspective.Perspective(measure.get_cost(), measure.get_lifetime(), measure.get_externalities(), measure.get_energy_conservation(), decimal.Decimal(0.1), decimal.Decimal(0.4))

    """

    #check loan 
    oroi_daneiou = loan.Terms(decimal.Decimal(0.5), 41912, decimal.Decimal(0.4))
    epistrofi_daneiou = loan.Return()

    

if __name__ == "__main__":
    main()