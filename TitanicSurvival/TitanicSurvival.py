#import libraries
import pandas as pd
import matplotlib.pyplot as plt


titanic_df = pd.read_csv(r"C:\Users\Suvralipi\workspace\Titanic\Titanic\Input\Titanic.csv")
print(len(titanic_df))
print(titanic_df.head())


# Select passengers' id and port, and drop the records that are nan.Then compute passengers' amount from different ports.
Port_count = titanic_df[['PassengerId','Embarked']].dropna(axis=0).groupby('Embarked')['PassengerId'].count()

#Draw a pie to show the proportions of passengers from three ports
plt.clf()
plt.pie(Port_count ,
        colors=('y', 'g', 'c'),
        labels =tuple(Port_count.index), autopct='%1.1f%%')
plt.title('Proportions of Passengers From Three Ports')
plt.savefig("./Output Log/" + "Passenger_Embarked" + ".png")

# Select passengers' id and sex, drop the records that are nan.Then compute passengers' amount by sex.
Sex_count = titanic_df[['PassengerId','Sex']].dropna(axis=0).groupby('Sex')['PassengerId'].count()

#Draw a pie to show the sex ratios of passengers 
plt.clf()
plt.pie(Sex_count ,
        colors=('y', 'g'),
        labels =tuple(Sex_count.index), autopct='%1.1f%%')
plt.title('Sex Ratios')
plt.savefig("./Output Log/" + "Passenger_Sex" + ".png")


# Select passengers' id and pclass, drop the records with nan.Then compute passengers' amount by pclass.
Pclass_count = titanic_df[['PassengerId','Pclass']].dropna(axis=0).groupby('Pclass')['PassengerId'].count()

#Draw a pie to show the sex ratios of passengers 
plt.clf()
plt.pie(Pclass_count ,
        colors=('y', 'g','c'),
        labels =tuple(Pclass_count.index), autopct='%1.1f%%')
plt.title('Proportions of Different Pclasses')
plt.savefig("./Output Log/" + "Passenger_Pclasses" + ".png")

print('max age: {}, min age: {}, average age: {}'.format(titanic_df['Age'].max(),titanic_df['Age'].min(),titanic_df['Age'].mean()))

plt.clf()
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Histogram of Age')
plt.hist(titanic_df['Age'], bins=8, range=(0,80))  # 
plt.savefig("./Output Log/" + "Age vs Freq" + ".png")


# Write a function: mapping age to the corresponding age group
def age_segment(age):
    if age >= 70 :
        return '70-80'
    elif age >=60 :
        return '60-69'
    elif age >=50 :
        return '50-59'
    elif age >=40 :
        return '40-49'
    elif age >=30 :
        return '30-39'
    elif age >=20 :
        return '20-29'
    elif age >=10 :
        return '10-19'
    elif age >=0 :
        return '0-9'  
    else:
        return None
# Combine age,segment of age, survived or not into a dataframe. Then drop records with nan. 
age_seg_tmp = pd.Series(titanic_df['Age'].dropna(axis=0).apply(age_segment),name ='Seg')  
age_seg_df = pd.concat([titanic_df[['Age', 'Survived']].dropna(axis=0),age_seg_tmp],axis=1)

# Write a function to gennerate a contingency table
def Contingency_table(df,inde_var,de_var):    
    de_var_group = df.groupby(inde_var)[de_var].sum()   
    inde_var_group = df.groupby(inde_var)[de_var].count().rename('Sum') 
    op_de_var_group = ( inde_var_group -df.groupby(inde_var)[de_var].sum()).rename('Un'+de_var)
    tmp = pd.concat([de_var_group,op_de_var_group,inde_var_group],axis=1)    
    contingency = pd.concat([tmp,pd.DataFrame([tmp.sum()],index=['Sum'])],axis=0)  
    return contingency

# Use the function to gennerate the contingency table of age segment and survived or not 
age_survived_contingency = Contingency_table(age_seg_df,'Seg','Survived')
print("age_survived_contingency table:")
print(age_survived_contingency)


# Write a function to compute Chi-squared value
def Compute_Chi2(contingency,n,m):
    Chi = 0
    for i in range(n):
        for j in range(m):
            E = 1.0*contingency.iloc[i,m] * contingency.iloc[n,j] / contingency.iloc[n,m]  # Compute expected value in row i , column j
            Chi += (contingency.iloc[i,j] - E)**2 / E
    return Chi

#  Use the function to compute Chi-squared value of Chi2-test between age and  survived or not
Chi_value_age = Compute_Chi2(age_survived_contingency,8,2) 
print("Chi Value for age :")       
print(Chi_value_age)


# Compute survived ratios of each age segment
age_seg_ratio = age_seg_df.groupby('Seg')['Survived'].sum() / age_seg_df.groupby('Seg')['Survived'].count()

plt.clf()
plt.xlabel('Age')
plt.ylabel('Ratio')
plt.title('Survived Ratio of Different Ages')
plt.bar(range(8),age_seg_ratio,tick_label=tuple(age_seg_ratio.index),align ='center')
plt.savefig("./Output Log/" + "Age vs Survived_Ratio" + ".png")


def z_stat_ratio_diff(n1,y1,n2,y2):
    return (1.0*y1/n1-1.0*y2/n2)/pow(1.0*(y1+y2)/(n1+n2)*(n1+n2-y1-y2)/(n1+n2)*(1.0/n1+1.0/n2),0.5)


# Combine sex and survived or not into a dataframe. Then drop records with nan
sex_cleaned_df = titanic_df[['Sex', 'Survived']].dropna(axis=0)

# Use the function to gennerate the contingency table of sex and survived or not 
sex_survived_contingency = Contingency_table(sex_cleaned_df,'Sex','Survived')
print("Sex ~ Survived Contigency:")
print(sex_survived_contingency)

Chi_value_sex = Compute_Chi2(sex_survived_contingency,2,2)      
print("Chi Value for Sex:")  
print(Chi_value_sex)

# Compute survived ratios of each sex
sex_survived_ratio = sex_cleaned_df.groupby('Sex')['Survived'].sum() / sex_cleaned_df.groupby('Sex')['Survived'].count()
print("Sex survival ratio:",sex_survived_ratio)

# Use function to compute  z statistic
print("z_value for sex:",z_stat_ratio_diff(314,233,577,109))
# Combine pclass and survived or not into a dataframe. Then drop records with nan
pclass_cleaned_df = titanic_df[['Pclass', 'Survived']].dropna(axis=0)

# Use the function to gennerate the contingency table of pclass and survived or not 
pclass_survived_contingency = Contingency_table(pclass_cleaned_df,'Pclass','Survived')
print("pclass vs survived Contigency:")
print(pclass_survived_contingency)

#  Use the function to compute Chi-squared value of Chi2-test between pclass and  survived or not
Chi_value_pclass = Compute_Chi2(pclass_survived_contingency,3,2)        
print("Chi Value for Pclass:",Chi_value_pclass) 

# Compute survived ratios of each pclass
pclass_survived_ratio = pclass_cleaned_df.groupby('Pclass')['Survived'].sum() / pclass_cleaned_df.groupby('Pclass')['Survived'].count()
print("Pclass Survived Ratio:",pclass_survived_ratio)

# Use function to compute  z statistic
print("z value for pclass:",z_stat_ratio_diff(216,136,184,87))

# Combine embarked and survived or not into a dataframe. Then drop records with nan
embarked_cleaned_df = titanic_df[['Embarked', 'Survived']].dropna(axis=0)

# Use the function to gennerate the contingency table of embarked port and survived or not 
embarked_survived_contingency = Contingency_table(embarked_cleaned_df,'Embarked','Survived')
print("Embarked vs survived contingency")
print(embarked_survived_contingency)

#  Use the function to compute Chi-squared value of Chi2-test between embarked port and  survived or not
Chi_value_embarked  = Compute_Chi2(embarked_survived_contingency,3,2)        
print("Chi Value for embarked",Chi_value_embarked) 

# Compute survived ratios of each port
embarked_survived_ratio = embarked_cleaned_df.groupby('Embarked')['Survived'].sum() / embarked_cleaned_df.groupby('Embarked')['Survived'].count()
print("Embarked Survived Ratio :",embarked_survived_ratio)

# Use function to compute  z statistic
print("z value for Embarked:",z_stat_ratio_diff(168,93,77,30))

 

