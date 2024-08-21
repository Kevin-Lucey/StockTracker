import yfinance as yf 
import mysql.connector
import pandas as pd
from MySQLConnection import Connection

""" List of all stock ticker names from 
https://github.com/shilewenuw/get_all_tickers/blob/master/get_all_tickers/tickers.csv

Author: shilewenuw

This file writes all stock ticker symbols into a local MySQL Instance

"""



c = Connection()
conn, cur = c.ConnectToMySQL('StockTracker'), c.MakeCursor()

tickers = pd.read_csv('tickers.csv')

delisted = ['MIE', 'RZA', 'MBT', 'TGP', 'ATV', 'PLM', 'SMM', 'BDXB',
 'CLGX', 'AXO', 'TEN', 'IVC', 'DLPH', 'UBP', 'CFX', 'FFG', 'TREC', 'DMS',
   'CZZ', 'DTP', 'UFAB', 'DNI', 'IRL', 'SJIU', 'MAXR', 'NIQ',
     'EXD', 'SEAS', 'GTS', 'CCXX', 'ROYT', 'HCFT', 'RXN', 'VOLT', 
     'CHL', 'TMBR', 'INT', 'NSCO', 'CTT', 'PCGU', 'FDEU', 'WUBA', 'BFO', 'NM', 
     'MNP', 'ADSW', 'SWT', 'HHC', 'AT', 'DL', 'CXP', 'GSLD', 'TRQ', 'MDLA', 'TCRW',
       'IBA', 'ENBA', 'PRTY', 'STAR', 'BKK', 'WTRU', 'ATCO', 'CBX', 'IRR', 'ATH', 'QTS', 'PCPL', 'CEL', 'HNGR', 'NWHM', 'NCR', 'MCC', 'EXTN', 'MNK', 'IPOC', 'VCIF', 'LCI', 'DTQ', 'GDP', 'SNP', 'GRAF', 'UBA', 'MSGN', 'SOLN', 'CBB', 'TDA', 'CIR', 'RYCE', 'CLDR', 'LFC', 'CDR', 'PRSP', 'AHC', 'SRC', 'SYX', 'STOR', 'RYB', 'CLNC', 'DCP', 'CVA', 'WMC', 'NEW', 'IPOB', 'ABB', 'GTT', 'MYJ', 'SJR', 'QEP', 'LGVW', 'AZRE', 'LSI', 'GIM', 'FOE', 'STL', 'TOT', 'MFAC', 'MFT', 'THGA', 'CXO', 'GLOP', 'CRY', 'BBF', 'AVLR', 'ETM', 'MZA', 'MGP', 'ANTM', 'BZM', 'OFC', 'CINR', 'AXU', 'NJV', 'JDD', 'DYFN', 'MFO', 'GIX', 'MYOV', 'LGC', 'PROS', 'IVH', 'DNK', 'FIV', 'GFLU', 'WTT', 'OAC', 'MGU', 'NHA', 'CLNY', 'BSA', 'CNR', 'CDOR', 'SWCH', 'FBHS', 'APRN', 'IMH', 'SZC', 'PZN', 'NRGX', 'AMOV', 'HKIB', 'ENBL', 'NKG', 'SHI', 'REV', 'DRE', 'KDMN', 'AIZP', 'NES', 'CEN', 'RLGY', 'NLSN', 'EFL', 'ADS', 'SOAC', 'ARA', 'CMD', 'WEI', 'FVAC', 'NP', 'GIX~', 'BPMP', 'NBO', 'GHL', 'ENIA', 'FRC', 'HIL', 'PBFX', 'ZEN', 'VTA', 'ANH', 'GOL', 'BSMX', 'CNXM', 'GSH', 'CHU', 'TKAT', 'UZA', 'TLRD', 'Y', 'CTL', 'VEDL', 'JWS', 'SI', 'BRG', 'BFY', 'EMAN', 'BLL', 'NBW', 'BGIO', 'LEAF', 'DDF', 'NXQ', 'RENN', 'CELG~', 'TCO', 'RST', 'HPR', 'JRO', 'SJIJ', 'OSB', 'INFO', 'QUOT', 'JAX', 'PING', 'ALUS', 'KRA', 'MEN', 'PTR', 'LN', 'ARNC', 'MUS', 'GFY', 'DEX', 'VMW', 'HT', 'TGC', 'WDR', 'FLY', 'SAK', 'JMP', 'WRI', 'CCC', 'HMI', 'GRA', 'RPT', 'RMG', 'ACY', 'SNMP', 'CLI', 'BAF', 'JE', 'VER', 'JHB', 'SRLP', 'ARD', 'ONDK', 'CPLG', 'ESTE', 'PSXP', 'GSX', 'NCB', 'RLH', 'SFE', 'RPAI', 'GPM', 'SC', 'IHC', 'DCUE', 'HUD', 'LAIX', 'VCF', 'BCEI', 'ACC', 'SFUN', 'GMO', 'GOED', 'AQUA', 'FEAC', 'JT', 'EROS', 'GLOG', 'LOAK', 'ELAT', 'UZC', 'RFP', 'CTB', 'LPI', 'NUM', 'CCAC', 'UN', 'USX', 'CBO', 'INS', 'EDI', 'VCRA', 'CS', 'WRE', 'SCVX', 'PLT', 'TUFN', 'PVG', 'WBAI', 'SHLX', 'ACH', 'MMP', 'TDE', 'CLR', 'WPX', 'CKH', 'NHF', 'VVNT', 'NTP', 'DSSI', 'AVYA', 'PSB', 'WYND', 'FCAU', 'CHA', 'TDJ', 'FBC', 'SFTW', 'PIC', 'APTS', 'RRD', 'KL', 'ZNH', 'FTSI', 'CTEK', 'DS', 'JEMD', 'TTM', 'TRXC', 'BSE', 'NLS', 'MVC', 'SBE', 'ORCC', 'FSLF', 'NUO', 'UNVR', 'HTA', 'HMG', 'JPS', 'TRNE', 'NVTA', 'MN', 'PPX', 'TPRE', 'CSU', 'MCF', 'KSU', 'MFL', 'STON', 'SNR', 'BXG', 'SRT', 'HNP', 'BIF', 'PFNX', 'XAN', 'COG', 'BXS', 'IPHI', 'KMF', 'VSLR', 'CUB', 'BMRG', 'CSLT', 'ATTO', 'GER', 'NTCO', 'MHE', 'JCO', 'ISR', 'MDLY', 'IHIT', 'XEC', 'NSL', 'WBT', 'WPF', 'BKI', 'DVD', 'ECCB', 'HCHC', 'BBX', 'NEV', 'SCPE', 'GGO', 'FSB', 'PQG', 'BSD', 'JP', 'AUY', 'WWE', 'TRWH', 'PJH', 'BITA', 'MIC', 'BDR', 'VRTV', 'RCA', 'RAD', 'MTL', 'CIT', 'BQH', 'BRMK', 'VMM', 'PBC', 'LB', 'CHAQ', 'GBL', 'CAJ', 'MTCN', 'PER', 'NNA', 'EHT', 'JIH', 'SHLL', 'NXR', 'IID', 'MR', 'MYF', 'SPN', 'WPG', 'JPT', 'VRS', 'VAR', 'NMY', 'DMYT', 'PLAN', 'PE', 'GPX', 'CTAA', 'NPTN', 'HSC', 'GSB', 'GLEO', 'AFC', 'SCU', 'BTN', 'HEP', 'WORK', 'IFFT', 'TRTN', 'CCH', 'FSKR', 'ABC', 'MTT', 'ELVT', 'BMY~', 'CHAP', 'IO', 'HMLP', 'HZN', 'MFGP', 'PCI', 'HGH', 'LDL', 'NTN', 'CCR', 'SAIL', 'PACD', 'CEO', 'PSV', 'VNTR', 'UFS', 'AIC', 'KNL', 'FEO', 'JTD', 'EFF', 'AUG', 'TWTR', 'HRC', 'CHRA', 'CO', 'CMO', 'GCP', 'TAT', 'CAI', 'CHS', 'SJI', 'DFNS', 'AFGH', 'NFH', 'RVI', 'SALT', 'CELP', 'VEC', 'DSE', 'ONE', 'HFC', 'ETH', 'TLI', 'LOV', 'GIK', 'EAE', 'SOGO', 'CDAY', 'AQNA', 'MMX', 'NMFX', 'GRUB', 'MUH', 'MNRL', 'EAB', 'AIW', 'ITCB', 'JHAA', 'GWB', 'NEX', 'CSPR', 'CCX', 'CEQP', 'NID', 'ELJ', 'GPL', 'IPV', 'PEI', 'MTOR', 'BBL', 'SMTS', 'NEWR', 'IAA', 'KLR', 'JSD', 'JTA', 'HOME', 'NYV', 'LINX', 'NRZ', 'CRHM', 'ELY', 'JCAP', 'CCF', 'TIF', 'DUC', 'WLL', 'TCP', 'PKO', 'LUB', 'BBK', 'LTHM', 'PKI', 'SNE', 'SYN', 'MDP', 'MCA', 'DPW', 'ARGO', 'FTCH', 'RPLA', 'VNE', 'AFI', 'ECOM', 'AJRD', 'NPN', 'CTY', 'CTK', 'TSU', 'FIT', 'RMED', 'NAV', 'FBM', 'CFXA', 'MCV', 'HEXO', 'FPAC', 'PPR', 'WBK', 'SWM', 'RE', 'GMZ', 'JHY', 'CEA'
'ATEST', 'IBO'
'ECCY', 'AEB', 'LMHB', 'SOJA', 
'DRUA', 'MVCD', 'RESI', 'GMTA', 
'TCRZ', 'DTJ', 'WALA', 'GSS', 'MYC', 'DTY', 'TPVY', 'AYX', 'ELU', 
'CTZ', 'PYS', 'SAF', 'GSV', 'EZT', 'PBB', 'HCXZ', 'UZB', 'MDLQ', 'GYC', 'MDLX', 'DUKH', 'SOJB', 'SCA', 'HTFA', 'TGH', 'PBY', 'LMHA', 'MCX'
'STAR', 'CTT', 'CEA', 'ECOM','IBO', 'ATEST','ECCY'
]

insert_string = """
    INSERT INTO TickerSymbol (tickerName)
    VALUES (%s);
"""
print(tickers['DDD'][1] in delisted)

for i in range(len(tickers)):
    if tickers['DDD'][i] in delisted:
        print(tickers['DDD'][i])
    else:    
        cur.execute(
            insert_string, (tickers['DDD'][i],)
            )
conn.commit()
cur.close()
conn.close()