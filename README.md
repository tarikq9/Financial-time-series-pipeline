The following work, is an automated tool used to analize financial time series,
By transforming raw prices in logPt then logRt and  studying it's statistical properties the script chooses (according to bic) the optimal stochastic processes to represent both

The mean equation: choosing from AR, MA , ARMA, ARIMA (order from 0 to 2) 
and the volatility equation: GARCH, EGARCH, APARCH, FIGARCH (order from 0 to 2)

Distributions tested are: normal, studentst and ged
Finally a 3x3 Plot is created, showing visually the statistical properties of the time series

(This work example, has been tested on commodities futures, such as copper) 
<img width="1706" height="852" alt="Copper comdty analysis" src="https://github.com/user-attachments/assets/02e9cc43-9f7f-4173-989a-e598cfdfb156" />

<details>
<summary>Click here to see python terminal output</summary>

```text
---FUTURES COPPER ANALYSIS---

Number of observations:        4665
First observation:             2008-01-03 00:00:00
Last observation:              2026-09-25 00:00:00
Mean of log returns:           0.0221
Standard deviation:            1.4521
25% quantile:                  -0.7243
50% quantile:                  0.0247
75% quantile:                  0.7780

---ADF TEST ON RAW PRICES---

(0.45718045216938724, 0.9835118514410697, 1, 4664, {'1%': -3.4317528522101646, '5%': -2.8621598991520445, '10%': -2.5670999747583036}, 54345.49939932645)

---ADF TEST ON LOG PRICES---

(-0.6525809789984433, 0.8586529062351113, 1, 4664, {'1%': -3.4317528522101646, '5%': -2.8621598991520445, '10%': -2.5670999747583036}, -26110.175918765828)

---ADF TEST ON LOG RETURNS---

(-73.42532717229686, 0.0, 0, 4664, {'1%': -3.4317528522101646, '5%': -2.8621598991520445, '10%': -2.5670999747583036}, 16552.09019718317)

*Pt is not stationary


*logPt is not stationary


*logRt is stationary


---JARQUE-BERA TEST ON LOG RETURNS---

SignificanceResult(statistic=4016.502002082425, pvalue=0.0)

*jb_pvalue is 0.0000:logRt are not gaussian


---LJUNG-BOX TEST ON LOG RETURNS---

    lb_stat  lb_pvalue
10  30.5777     0.0007
20  53.3742     0.0001

*since p_value at lag 10 is 0.0007 ,then there is autocorrelation in linear returns


---LJUNG-BOX TEST ON LOG RETURNS---

     lb_stat  lb_pvalue
10 2686.6588     0.0000
20 4736.5046     0.0000

*p_value at lag 10 = 0.0000 so arch effect is present


---SKEWNESS AND KURTOSIS OF LOG RETURNS---

Skewness: -0.0629
Kurtosis: 7.5502

---TYPE AND ORDER CHOICE FOR MEAN EQUATION---

    Model  p  q        BIC
ARMA(1,0)  1  0 16719.6893
ARMA(0,1)  0  1 16719.8172
ARMA(2,0)  2  0 16728.1371
ARMA(1,1)  1  1 16728.1372
ARMA(0,2)  0  2 16728.1408
ARMA(0,0)  0  0 16735.5535
ARMA(1,2)  1  2 16736.5179
ARMA(2,1)  2  1 16736.5850
ARMA(2,2)  2  2 16744.8973

*Best model for mean equation according to bic:
ARMA(1,0)

---TYPE AND ORDER CHOICE FOR VOLATILITY EQUATION---

         Model Distribution        BIC  LB_pvalue_lag10  ARCH_pvalue_lag10  Convergence
  GARCH(1,0,1)            t 15492.3331           0.4889             0.5365            0
FIGARCH(1,0,1)            t 15494.2468           0.4183             0.9583            0
  GARCH(1,0,2)            t 15499.6435           0.4838             0.7271            0
  GARCH(2,0,1)            t 15500.7810           0.4889             0.5363            0
 EGARCH(1,1,1)            t 15502.2403           0.4372             0.1628            0
 APARCH(1,1,1)            t 15502.3154           0.4680             0.4300            0
  GARCH(2,0,2)            t 15505.0929           0.5083             0.3819            0
  GARCH(1,0,1)          ged 15505.1041           0.4840             0.6163            0
FIGARCH(1,0,1)          ged 15505.5030           0.4071             0.9667            0
 EGARCH(2,1,1)            t 15508.1545           0.4197             0.6825            0
 EGARCH(1,1,2)            t 15509.1093           0.4271             0.3999            0
 APARCH(1,1,2)            t 15509.7075           0.4633             0.6498            0
 APARCH(2,1,1)            t 15510.7632           0.4680             0.4299            0
  GARCH(1,0,2)          ged 15512.6970           0.4798             0.7685            0
 APARCH(2,1,2)            t 15512.9465           0.4751             0.3162            0
 APARCH(1,1,1)          ged 15513.4652           0.4594             0.5004            0
  GARCH(2,0,1)          ged 15513.5519           0.4840             0.6164            0
 EGARCH(1,1,1)          ged 15514.6742           0.4327             0.2228            0
 EGARCH(2,1,2)            t 15516.6024           0.4197             0.6824            0
  GARCH(2,0,2)          ged 15518.4482           0.4996             0.5024            0
 APARCH(1,1,2)          ged 15521.0786           0.4555             0.6824            0
 EGARCH(2,1,1)          ged 15521.2328           0.4181             0.6563            0
 EGARCH(1,1,2)          ged 15521.7904           0.4234             0.4455            0
 APARCH(2,1,1)          ged 15521.9130           0.4594             0.5003            0
 APARCH(2,1,2)          ged 15525.7358           0.4690             0.4548            0
 EGARCH(2,1,2)          ged 15529.6806           0.4181             0.6562            0
FIGARCH(1,0,1)       normal 15651.4959           0.3941             0.9623            0
 APARCH(1,1,1)       normal 15655.9069           0.4442             0.5250            0
  GARCH(1,0,1)       normal 15655.9116           0.4753             0.6693            0
 EGARCH(1,1,1)       normal 15661.4893           0.4241             0.2608            0
  GARCH(1,0,2)       normal 15663.4792           0.4719             0.7889            0
 APARCH(1,1,2)       normal 15663.4889           0.4415             0.6751            0
 APARCH(2,1,1)       normal 15664.3547           0.4442             0.5250            0
  GARCH(2,0,1)       normal 15664.3594           0.4753             0.6694            0
 EGARCH(2,1,1)       normal 15668.2498           0.4134             0.5867            0
 EGARCH(1,1,2)       normal 15668.5467           0.4167             0.4471            0
 APARCH(2,1,2)       normal 15669.4710           0.4569             0.5553            0
  GARCH(2,0,2)       normal 15671.9270           0.4719             0.7890            0
 EGARCH(2,1,2)       normal 15676.6977           0.4135             0.5869            0

*Best model for volatility equation according to bic:
GARCH(1,0,1) t
```

</details>
