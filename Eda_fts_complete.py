#EDA financial time series complete
# Import libraries
import numpy as np
import pandas as pd
import scipy.stats as stats
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from arch import arch_model
import matplotlib.pyplot as plt
import warnings
import sys

# Clean warnings and set format
warnings.filterwarnings('ignore')
pd.options.display.float_format='{:.4f}'.format

# Choose commodity or financial instrument
column=1

if column==1:
    print('\n---SPOT BRASS ANALYSIS---\n')
elif column==2:
    print('\n---FUTURES COPPER ANALYSIS---\n')
elif column==3:
    print('\n---FUTURES ZINC ANALYSIS---\n')

# Import dataset
df=pd.read_excel(
    r'C:\Users\tarikB\Desktop\Thesis X.xlsx',
    sheet_name='resolve',
    skiprows=3,header=None)

data=pd.DataFrame({
    'Date': pd.to_datetime(df.iloc[:,0]),
    'Price': pd.to_numeric(df.iloc[:,column])
})

# Use date as index
data= data.set_index('Date')

# Price extraction and convertion 
Pt= data['Price']

logPt= np.log(Pt) # log prices

logRt= (logPt.diff().dropna())*100 # log returns

# Data description
print(f"{'Number of observations:':<30} {len(logRt)}")
print(f"{'First observation:':<30} {logRt.index.min()}")
print(f"{'Last observation:':<30} {logRt.index.max()}")

print(f"{'Mean of log returns:':<30} {np.mean(logRt):.4f}")
print(f"{'Standard deviation:':<30} {np.std(logRt):.4f}")
print(f"{'25% quantile:':<30} {np.quantile(logRt,0.25):.4f}")
print(f"{'50% quantile:':<30} {np.quantile(logRt,0.50):.4f}")
print(f"{'75% quantile:':<30} {np.quantile(logRt,0.75):.4f}")

# Augmented dickey fuller test
# Testing stationarity of each series
print('\n---ADF TEST ON RAW PRICES---\n')
print(adfuller(Pt))

print('\n---ADF TEST ON LOG PRICES---\n')
print(adfuller(logPt))

print('\n---ADF TEST ON LOG RETURNS---\n')
print(adfuller(logRt))

def stationarity(name):
    if name== 'Pt':
        series=Pt
    elif name=='logPt':
        series=logPt
    elif name=='logRt':
        series= logRt

    adf= adfuller(series)
    if adf[1]>0.05 :
        print(f'\n*{name} is not stationary\n')
    else:
        print(f'\n*{name} is stationary\n')
stationarity('Pt')
stationarity('logPt')
stationarity('logRt')

# Jarque bera test
# Testing normality of log returns
print('\n---JARQUE-BERA TEST ON LOG RETURNS---\n')
print(stats.jarque_bera(logRt))

jb_p= stats.jarque_bera(logRt)[1]
if jb_p<0.05:
    print(f'\n*jb_pvalue is {jb_p:.4f}:logRt are not gaussian\n')
else:
    print(f'\n*jb_pvalue is {jb_p:.4f}:logRt are gaussian\n')



# Ljung box test on log returns
# Testing linear autocorrelation
print('\n---LJUNG-BOX TEST ON LOG RETURNS---\n')
lb_test_l= acorr_ljungbox(
    logRt, lags=[10,20],
    model_df=0,
    return_df=True)

print(lb_test_l)

p_linear=lb_test_l.loc[10,'lb_pvalue']
if p_linear<0.05:
    print(f'\n*since p_value at lag 10 is {p_linear:.4f} ,then there is autocorrelation in linear returns\n')
else:
    print('\n*no autocorrelation on linear returns(so costant mean fitting for garch)\n')



# Ljung box test on squared log returns
# Testing quadratic autocorrelation
print('\n---LJUNG-BOX TEST ON LOG RETURNS---\n')
lb_test_a= acorr_ljungbox(
    logRt**2, lags=[10,20],
    model_df=0,
    return_df=True)

print(lb_test_a)

p_lag10=lb_test_a.loc[10,'lb_pvalue']
if p_lag10<0.05:
    print(f'\n*p_value at lag 10 = {p_lag10:.4f} so arch effect is present\n')
else:
    print('\n*no arch effect\n')

# Skewness and kurtosis 
print('\n---SKEWNESS AND KURTOSIS OF LOG RETURNS---\n')
print(f'Skewness: {logRt.skew():.4f}')
print(f'Kurtosis: {logRt.kurtosis()+3:.4f}')


# Mean equation choice
# order selection 
print('\n---TYPE AND ORDER CHOICE FOR MEAN EQUATION---\n')

p_max=2
q_max=2

results=[]

for p in range(p_max+1):
    for q in range(q_max+1):
        try:
            model= ARIMA(
                logRt,
                order=(p,0,q),
                trend='c').fit()

            results.append({
                'Model': f'ARMA({p},{q})',
                'p': p,
                'q': q,
                'BIC': model.bic})
        except Exception as e:
            print(f'error detected: {e}')    

# Data frame of results
model_results= pd.DataFrame(results)
model_results= model_results.sort_values(by='BIC',ascending=True)
print(model_results.to_string(index=False))
best_model=model_results.iloc[0]

print('\n*Best model for mean equation according to bic:')
print(best_model['Model'])

# Stop the code if arch effect is not present
if p_lag10>0.05:
    print(f'\n*volatility is constant\n')
    sys.exit()

# Modeling volatility clusters
# Garch variant and order selection

best_p= int(best_model['p'])
best_q= int(best_model['q'])

if best_p==0 and best_q==0:
    meanU='constant'
elif best_p==1 and best_q==0:
    meanU='AR'

print('\n---TYPE AND ORDER CHOICE FOR VOLATILITY EQUATION---\n')

pg_max = 2
qg_max = 2

ddist = ['normal', 't', 'ged']
vvol = ['GARCH', 'EGARCH', 'APARCH','FIGARCH']

gresults = []

for pg in range(1,pg_max+1):
    for qg in range(1,qg_max+1):
        for dis in ddist:
            for vl in vvol:
                # Correcting leverage parameter
                if vl in ['EGARCH', 'APARCH']:
                    o_param= 1
                elif vl in ['GARCH','FIGARCH']:
                    o_param= 0
                # Correcting number of parameters for figarch
                if vl == 'FIGARCH' and (pg !=1 or qg!=1):
                    continue
                # Fit the models 
                try:
                    gmodel= arch_model(
                        logRt,
                        p=pg,
                        o=o_param,
                        q=qg,
                        mean=meanU,
                        dist=dis,
                        vol=vl,
                        rescale=False).fit(disp='off',
                                           cov_type='robust')
                    # Ljung-box on standardized residuals 
                    an= acorr_ljungbox(gmodel.std_resid,lags=[10],return_df=True)
                    # Arch lm test on standardized squared residuals
                    arch_test= gmodel.arch_lm_test(lags=10,standardized=True)

                    # Append data
                    gresults.append({
                        'Model': f'{vl}({pg},{o_param},{qg})', 
                        'Distribution': dis,
                        'BIC': gmodel.bic,
                        'LB_pvalue_lag10': an['lb_pvalue'].iloc[0],
                        'ARCH_pvalue_lag10': arch_test.pval,
                        'Convergence': gmodel.convergence_flag})
                except Exception as e:
                    print(f'error detected: {e}')

# Data frame of results
gmodel_results= pd.DataFrame(gresults)
gmodel_results= gmodel_results.sort_values(by='BIC',ascending=True)
print(gmodel_results.to_string(index=False))
best_gmodel=gmodel_results.iloc[0]

print('\n*Best model for volatility equation according to bic:')
print(best_gmodel['Model'], best_gmodel['Distribution'])

#Plot diagnostics time series
fig, ax=plt.subplots(3,3,figsize=(17,15),layout='constrained')

if column==1:
    ax[0,0].set_title('Prices in € per metric tonne spot brass',fontsize=10,fontweight='bold')
    colorU= '#C3A25D' 

elif column==2:
    ax[0,0].set_title('Prices in € per metric tonne future copper',fontsize=10,fontweight='bold')
    colorU= '#B87333'

elif column==3:
    ax[0,0].set_title('Prices in € per metric tonne future zinc',fontsize=10,fontweight='bold')
    colorU="#5D6D7A"


ax[0,0].plot(Pt.iloc[1:],color=colorU)  ####
ax[0,0].grid(True,linestyle='--',alpha=0.5)

#Plot logRt
ax[1,0].plot(logRt,color=colorU)  #####
ax[1,0].grid(True,linestyle='--',alpha=0.5)
ax[1,0].set_title('Log returns plot',fontsize=10,fontweight='bold')

#Plot acf logRt
plot_acf(logRt,lags=30, ax=ax[1,1], color=colorU,vlines_kwargs={'colors':colorU})
ax[1,1].grid(True,linestyle='--',alpha=0.5)
ax[1,1].set_title('ACF log returns',fontsize=10,fontweight='bold')


#Plot pacf logRt
plot_pacf(logRt,lags=30, ax=ax[1,2], color=colorU,vlines_kwargs={'colors':colorU})
ax[1,2].grid(True,linestyle='--',alpha=0.5)
ax[1,2].set_title('PACF log returns',fontsize=10,fontweight='bold')



#Plot histogram & theoretical N of logRt
ax[0,1].hist(logRt, bins=80, density=True, color=colorU,edgecolor=colorU,alpha=0.9)
x= np.linspace(logRt.min(), logRt.max(),500)
normpdf= stats.norm.pdf(x, logRt.mean() , logRt.std())
ax[0,1].plot(x,normpdf,color='black',linewidth=2)
ax[0,1].grid(True,linestyle='--',alpha=0.5)
ax[0,1].set_title('Log returns distribution',fontsize=10,fontweight='bold')


#Q-Q plot of log Rt
stats.probplot(logRt, dist='norm', plot=ax[0,2])
ax[0,2].lines[0].set_markerfacecolor(colorU)
ax[0,2].lines[0].set_markeredgecolor(colorU)
ax[0,2].lines[1].set_color('black')
ax[0,2].set_xlabel('')
ax[0,2].set_ylabel('')
ax[0,2].grid(True,linestyle='--',alpha=0.5)
ax[0,2].set_box_aspect(1)
ax[0,2].set_title('Q-Q Plot log returns',fontsize=10,fontweight='bold')

#Plot squared logRt
ax[2,0].plot(logRt**2, color=colorU) #####
ax[2,0].grid(True,linestyle='--',alpha=0.5)
ax[2,0].set_title('Squared log returns plot',fontsize=10,fontweight='bold')

#Plot acf squared logRt
plot_acf(logRt**2,lags=30, ax=ax[2,1], color=colorU,vlines_kwargs={'colors':colorU})
ax[2,1].grid(True,linestyle='--',alpha=0.5)
ax[2,1].set_title('ACF squared log returns',fontsize=10,fontweight='bold')

#Plot pacf squared logRt
plot_pacf(logRt**2,lags=30, ax=ax[2,2],color=colorU,vlines_kwargs={'colors':colorU})
ax[2,2].grid(True,linestyle='--',alpha=0.5)
ax[2,2].set_title('PACF squared log returns',fontsize=10,fontweight='bold')

plt.show()