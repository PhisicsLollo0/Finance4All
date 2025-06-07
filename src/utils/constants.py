PORTFOLIOS = [
    '100_2factors',
    '100_1factor',
    '80_20_2factors',
    '80_20_1factor',
    '80_20_ACWI',
    '80_20_World'
]

PORTOFOLIO_NAMES = {
    '100_2factors'  : '100% Stocks + SmallCap Value + Momentum',
    '100_1factor'   : '100% Stocks + SmallCap Value',
    '80_20_2factors': '80% Stocks + 20% Bonds + SmallCap Value + Momentum',
    '80_20_1factor' : '80% Stocks + 20% Bonds + SmallCap Value',
    '80_20_ACWI'    : '80% Stocks(ACWI) + 20% Bonds',
    '80_20_World'   : '80% Stocks(World) + 20% Bonds',
}

PORTFOLIO_DESCRIPTIONS = {
    '100_2factors'  : 'This portfolio invests 100% in stocks, focusing on small-cap value and momentum strategies.',
    '100_1factor'   : 'This portfolio invests 100% in stocks, focusing on small-cap value.',
    '80_20_2factors': 'This portfolio allocates 80% to stocks and 20% to bonds, incorporating small-cap value and momentum factors.',
    '80_20_1factor' : 'This portfolio invests 80% in stocks and 20% in bonds, focusing on small-cap value.',
    '80_20_ACWI'    : 'This portfolio invests 80% in global stocks (ACWI) and 20% in bonds.',
    '80_20_World'   : 'This portfolio invests 80% in world stocks and 20% in bonds.'
}

# Add another group of portfolios in col2
SIMPLE_PORTFOLIOS = [
    'lifestrategy100',
    'lifestrategy80',
    'lifestrategy60',
    'lifestrategy40',
    'lifestrategy20',
    'lifestrategy0'
]

SIMPLE_PORTFOLIO_NAMES = {
    'lifestrategy100': '100% Stocks',
    'lifestrategy80' : '80% Stocks + 20% Bonds',
    'lifestrategy60' : '60% Stocks + 40% Bonds',
    'lifestrategy40' : '40% Stocks + 60% Bonds',
    'lifestrategy20' : '20% Stocks + 80% Bonds',
    'lifestrategy0'  : '100% Bonds'
}

SIMPLE_PORTFOLIO_DESCRIPTIONS = {
    'lifestrategy100': 'This portfolio invests 100% in stocks, suitable for aggressive strategies seeking high growth. Note that stocks are MSCI World',
    'lifestrategy80' : 'This portfolio allocates 80% to stocks and 20% to bonds, balancing growth and stability. Stocks are MSCI World',
    'lifestrategy60' : 'This portfolio invests 60% in stocks and 40% in bonds, providing moderate growth with some stability. Stocks are MSCI World',
    'lifestrategy40' : 'This portfolio invests 40% in stocks and 60% in bonds, focusing on stability with some growth potential. Stocks are MSCI World',
    'lifestrategy20' : 'This portfolio invests 20% in stocks and 80% in bonds, prioritizing stability with minimal growth. Stocks are MSCI World',
    'lifestrategy0'  : 'This portfolio invests 100% in bonds, suitable for conservative strategies seeking capital preservation.'
}

ALL_PORTFOLIOS = PORTFOLIOS + SIMPLE_PORTFOLIOS
ALL_PORTFOLIOS_NAMES = {**PORTOFOLIO_NAMES, **SIMPLE_PORTFOLIO_NAMES}
ALL_PORTFOLIOS_DESCRIPTIONS = {**PORTFOLIO_DESCRIPTIONS, **SIMPLE_PORTFOLIO_DESCRIPTIONS}