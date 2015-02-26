#//need dataframe for input manifestation and sign
import numpy as num
import pandas as pd

# hard coded disease numbers and prevalences for testing
disease = [362,351,114,187,352,441,188,192,189,616]
prev = [.1,.01,.001,.001,.001,.0001,.0001,.0001,.0001,.00001]

# creating the results dataframe
data = {'Disease': disease,'Prevalence': prev}
result=pd.DataFrame(data,columns=['Disease','Prevalence'])
result=result.set_index('Disease')
result['Numerator']=result['Prevalence']
result['Denominator']=1-result['Prevalence']
result['Tracker']=0

#TEST df and values representing knowledge base
data = {'Disease': disease}
df=pd.DataFrame(data, columns=['Disease'])
df['Manifestation']=1
df['ppv']=0.6
df['sens']=0.4
df=df.set_index('Disease')
df.loc[187,'ppv']=0

# test values for manifestation and sign
mx = 1
sign = '+'

#//for mx in range(len(mx)):
for index in range(len(disease)):
#        //define sign
  # find row of knowledge base with appropriate disease and manifestation
    row = df[(df.index == disease[index])&(df.Manifestation == mx)]
    #test to see if row actually does exist. If not, then we will skip the manifestation for this disease
    if row.empty:()
    else:
        # get the ppv
        ppv=row.iloc[0]['ppv']
        # Only proceed if ppv is not 0, otherwise move on to the next disease/manifestation
        if ppv==0:()
        else: 
            # get sensitivity and prevalance, calculate fdr 
            sens = row.iloc[0]['sens']
            prev = result.loc[disease[index],'Prevalence']
            fdr = 1 - sens
            result.loc[disease[index],'Tracker'] += 1
            # Based on the finding being + or -, multiply by appropriate factors
            if sign=='+':
                result.loc[disease[index],'Numerator']*=sens
                result.loc[disease[index], 'Denominator']*=fdr
            else:
                falseOrate = 1-sens
                spec = 1-(((sens*prev)/ppv)-(sens*prev))/(1-prev)
                result.loc[disease[index],'Numerator']*=falseOrate
                result.loc[disease[index], 'Denominator']*=spec
                
#//calc conditional probabilities for each row
result = result[result.Tracker != 0] #get rid of diseases with no findings
result['Results']=result['Numerator']/(result['Numerator']+result['Denominator'])

# TO DO: output differential dx in rank order and with names instead of numbers for diseases                

print result   
    


                
