The following work, is an automated tool used to analize financial time series,
By transforming raw prices in logPt then logRt and  studying it's statistical properties the script chooses (according to bic) the optimal stochastic processes to represent both

The mean equation: choosing from AR, MA , ARMA, ARIMA (order from 0 to 2) 
and the volatility equation: GARCH, EGARCH, APARCH, FIGARCH (order from 0 to 2)

Distributions tested are: normal, studentst and ged
Finally a 3x3 Plot is created, showing visually the statistical properties of the time series

(This work example, has been tested on commodities futures, such as copper) 
<img width="1706" height="852" alt="Copper comdty analysis" src="https://github.com/user-attachments/assets/02e9cc43-9f7f-4173-989a-e598cfdfb156" />
