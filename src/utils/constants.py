PORTFOLIOS = [
    '100_2factors_EUR',
    '100_2factors',
    '80_20_2factors',
    '80_20_1factor',
    '80_20_ACWI',
    '80_20_World'
]

PORTFOLIO_NAMES = {
    '100_2factors_EUR': '100% Stocks + SmallCap Value + Momentum + Currency Bias',
    '100_2factors'  : '100% Stocks + SmallCap Value + Momentum',
    '80_20_2factors': '80% Stocks + 20% Bonds + SmallCap Value + Momentum',
    '80_20_1factor' : '80% Stocks + 20% Bonds + SmallCap Value',
    '80_20_ACWI'    : '80% Stocks (ACWI) + 20% Bonds',
    '80_20_World'   : '80% Stocks (World) + 20% Bonds',
}

PORTFOLIO_DESCRIPTIONS = {
    '100_2factors_EUR': 'This portfolio invests 100% in stocks, focusing on small-cap value and momentum strategies, with a currency bias towards EUR currency.',
    '100_2factors'    : 'This portfolio invests 100% in stocks, focusing on small-cap value and momentum strategies.',
    '80_20_2factors'  : 'This portfolio allocates 80% to stocks and 20% to bonds, incorporating small-cap value and momentum factors.',
    '80_20_1factor'   : 'This portfolio invests 80% in stocks and 20% in bonds, focusing on small-cap value.',
    '80_20_ACWI'      : 'This portfolio invests 80% in global stocks (ACWI) and 20% in bonds.',
    '80_20_World'     : 'This portfolio invests 80% in world stocks and 20% in bonds.'
}

# Simple portfolios renamed from lifestrategy to simple
SIMPLE_PORTFOLIOS = [
    'simple100',
    'simple80',
    'simple60',
    'simple40',
    'simple20',
    'simple0'
]

SIMPLE_PORTFOLIO_NAMES = {
    'simple100': '100% Stocks',
    'simple80' : '80% Stocks + 20% Bonds',
    'simple60' : '60% Stocks + 40% Bonds',
    'simple40' : '40% Stocks + 60% Bonds',
    'simple20' : '20% Stocks + 80% Bonds',
    'simple0'  : '100% Bonds'
}

SIMPLE_PORTFOLIO_DESCRIPTIONS = {
    'simple100': 'This portfolio invests 100% in stocks, suitable for aggressive strategies seeking high growth. Stocks are MSCI World.',
    'simple80' : 'This portfolio allocates 80% to stocks and 20% to bonds, balancing growth and stability. Stocks are MSCI World.',
    'simple60' : 'This portfolio invests 60% in stocks and 40% in bonds, providing moderate growth with some stability. Stocks are MSCI World.',
    'simple40' : 'This portfolio invests 40% in stocks and 60% in bonds, focusing on stability with some growth potential. Stocks are MSCI World.',
    'simple20' : 'This portfolio invests 20% in stocks and 80% in bonds, prioritizing stability with minimal growth. Stocks are MSCI World.',
    'simple0'  : 'This portfolio invests 100% in bonds, suitable for conservative strategies seeking capital preservation.'
}


ALL_PORTFOLIOS = PORTFOLIOS + SIMPLE_PORTFOLIOS
ALL_PORTFOLIOS_NAMES = {**PORTFOLIO_NAMES, **SIMPLE_PORTFOLIO_NAMES}
ALL_PORTFOLIOS_DESCRIPTIONS = {**PORTFOLIO_DESCRIPTIONS, **SIMPLE_PORTFOLIO_DESCRIPTIONS}