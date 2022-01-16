#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 16:49:59 2020

@author: sunilguglani
"""

import pandas as pd
import yfinance as yf

region='in'
if region=='in':
    multi_script="ACC.NS 	ADANIPORTS.NS 	ADANITRANS.NS 	AMBUJACEM.NS  	ASHOKLEY.NS 	ASIANPAINT.NS 	AUROPHARMA.NS 	DMART.NS 	 AXISBANK.NS 	BAJAJ-AUTO.NS 	BAJFINANCE.NS 	BAJAJFINSV.NS 	BAJAJHLDNG.NS 	BANDHANBNK.NS 	BANKBARODA.NS 	BERGEPAINT.NS 	BPCL.NS 	BHARTIARTL.NS 	BIOCON.NS 	BOSCHLTD.NS 	BRITANNIA.NS 	CADILAHC.NS 	CIPLA.NS 	COALINDIA.NS 	COLPAL.NS 	CONCOR.NS 	DLF.NS 	DABUR.NS 	DIVISLAB.NS 	DRREDDY.NS 	EICHERMOT.NS 	GAIL.NS 	GICRE.NS 	GODREJCP.NS 	GRASIM.NS 	HCLTECH.NS 	HDFCAMC.NS 	HDFCBANK.NS 	HDFCLIFE.NS 	HAVELLS.NS 	HEROMOTOCO.NS 	HINDALCO.NS 	HINDPETRO.NS 	HINDUNILVR.NS 	HINDZINC.NS 	HDFC.NS 	ICICIBANK.NS 	ICICIGI.NS 	ICICIPRULI.NS 	ITC.NS 	IBULHSGFIN.NS 	IOC.NS 	INDUSINDBK.NS 	INFY.NS 	INDIGO.NS 	JSWSTEEL.NS 	KOTAKBANK.NS 	L&TFH.NS 	LT.NS 	LUPIN.NS 	M&M.NS 	MARICO.NS 	MARUTI.NS 	MOTHERSUMI.NS 	NHPC.NS 	NMDC.NS 	NTPC.NS 	NESTLEIND.NS 	ONGC.NS 	OFSS.NS 	PAGEIND.NS 	PETRONET.NS 	PIDILITIND.NS 	PEL.NS 	PFC.NS 	POWERGRID.NS 	PGHH.NS 	PNB.NS 	RELIANCE.NS 	SBILIFE.NS 	SHREECEM.NS 	SRTRANSFIN.NS 	SIEMENS.NS 	SBIN.NS 	SUNPHARMA.NS 	TCS.NS 	TATAMTRDVR.NS 	TATAMOTORS.NS 	TATASTEEL.NS 	TECHM.NS 	NIACL.NS 	TITAN.NS 	UPL.NS 	ULTRACEMCO.NS 	UBL.NS 	MCDOWELL-N.NS 	VEDL.NS 	IDEA.NS 	WIPRO.NS  ZEEL.NS "
    
    freq=15
    lookback_period,freq_yf='15y','1d'
    #lookback_period,freq_yf='1000m','1m'
    #lookback_period,freq_yf='4000m','2m'
    lookback_period,freq_yf='4000m','5m'

    lookback_period,freq_yf='8000m','15m'
    #lookback_period,freq_yf='8000m','30m'

    #lookback_period,freq_yf='6000m','60m'
    lookback_period,freq_yf='2y','1h'

elif (region=='us'):
    multi_script= "AAPL	ABBV	ABT	ACN	ADBE	AIG	ALL	AMGN	AMT	AMZN	AXP	BA	BAC	BIIB	BK	BKNG	BLK	BMY	BRK.B	C	CAT	CHTR	CL	CMCSA	COF	COP	COST	CRM	CSCO	CVS	CVX	DD	DHR	DIS	DOW	DUK	EMR	EXC	F	FB	FDX	GD	GE	GILD	GM	GOOG	GOOGL	GS	HD	HON	IBM	INTC	JNJ	JPM	KHC	KMI	KO	LLY	LMT	LOW	MA	MCD	MDLZ	MDT	MET	MMM	MO	MRK	MS	MSFT	NEE	NFLX	NKE	NVDA	ORCL	OXY	PEP	PFE	PG	PM	PYPL	QCOM	RTX	SBUX	SLB	SO	SPG	T	TGT	TMO	TXN	UNH	UNP	UPS	USB	V	VZ	WBA	WFC	WMT	XOM"
    freq=15
    lookback_period,freq_yf='1d','1m'
    lookback_period,freq_yf='60m','1m'

def fetch_yf_data_multi(script,lookback_period,interval):

    df = yf.download((script),period=lookback_period, interval=interval)

    df2=df.copy()
    df3=df2.stack().reset_index()
    
    try:
        t=pd.to_datetime(df3['Datetime'])
    except :
        df3['Datetime']=df3['Date'].copy()
        t=pd.to_datetime(df3['Datetime'])

    df3.index=t

    t=pd.to_datetime(df3.index)
    df3.index=t.tz_localize(None)
    
    df3.rename(columns={'level_1':'script'},inplace=True)
    
    
    try:
        t=pd.to_datetime(df3['Date'])
    except :
        df3['Date']=df3['Datetime'].copy()
        
    return df3

mode='yahoo'
five_min_flag=0
import time
a=time.time()
#df_van_all=fetch_yf_data_multi(multi_script,lookback_period,interval=freq_yf)

df = yf.download((multi_script),period=lookback_period, interval=freq_yf)

import numpy as np

def bb(df_temp,price_field):
    bb_width_entry=1.6
    bb_width_exit=1.7
    
    df_temp['ema_short'],df_temp['ema_long']=df_temp['Close'].ewm(span=3,adjust=False).mean(),df_temp['Close'].ewm(span=7,adjust=False).mean()
    df_temp['ema_short'],df_temp['ema_long']=df_temp['Close'].rolling(5).mean(),df_temp['Close'].rolling(11).mean()
    df_temp['ratio']=(df_temp['ema_short']/df_temp['ema_long'])
    df_temp['ema_signal']=np.where(df_temp['ema_short']>df_temp['ema_long'],1,-1)

    sma_lookback=25
    df_temp['sma']=df_temp[price_field].rolling(sma_lookback).mean()
    df_temp['std']=df_temp[price_field].rolling(sma_lookback).std()
    df_temp['std_min']=df_temp['std'].rolling(500).min()
    
    
    boll_entry=((df_temp['std']/df_temp['std_min'])<1.3)
        
    return df_temp,boll_entry[-1],((df_temp['std']/df_temp['std_min']))[-1]

df=df[['Close']]
df.columns = df.columns.droplevel()
df_temp=pd.DataFrame()
for col in df.columns:
    
    df_temp['Close']=df[col]
    df_temp,signal,ratio= bb(df_temp,'Close')
    '''
    if ratio<1.5:
        print(col,ratio)
    '''
    if signal:
        print(freq_yf,col,ratio,signal)
    