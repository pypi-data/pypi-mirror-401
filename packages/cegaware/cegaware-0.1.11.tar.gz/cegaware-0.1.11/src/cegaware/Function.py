###################################################################################
# Copyright © 2025 Matthieu Charrier. All rights reserved. ########################
# This file is the exclusive intellectual property of Matthieu Charrier. ##########
# No reproduction, modification, distribution, or use is permitted without ########
# prior written authorization. A separate licensing agreement may grant ###########
# Cegaware limited rights of use. Absent such agreement, no rights are granted. ###
###################################################################################

# cegaware.
from cegaware.Request import *
from cegaware.Enum import *

def GetAPIToken(Results, Logger, Verbose=False):
    return Request(
        '/GetAPIToken',
        [([], Results)],
        Logger, '', Verbose
    )

def CreatePortfolio(Results, Logger, APIToken, Verbose=False):
    return Request(
        '/CreatePortfolio',
        [([], Results)],
        Logger, APIToken, Verbose
    )

def GetPortfolio(Results, Logger, APIToken, Verbose=False):
    return Request(
        '/GetPortfolio',
        [([], Results)],
        Logger, APIToken, Verbose
    )

def GetPortfolios(Results, Logger, APIToken, Verbose=False):
    return Request(
        '/GetPortfolios',
        [([], Results)],
        Logger, APIToken, Verbose
    )

def UpdatePortfolio(Results, Logger, APIToken, Verbose=False):
    return Request(
        '/UpdatePortfolio',
        [([], Results)],
        Logger, APIToken, Verbose
    )

def CreateContract(Results, Data, Logger, APIToken, Verbose=False):
    return Request(
        '/CreateContract',
        [([], Results), (['Data'], Data)],
        Logger, APIToken, Verbose
    )

def GetContract(Results, Logger, APIToken, Verbose=False):
    return Request(
        '/GetContract',
        [([], Results)],
        Logger, APIToken, Verbose
    )

def GetContractSummary(Results, Data, Logger, APIToken, Verbose=False):
    return Request(
        '/GetContractSummary',
        [([], Results), (['Data'], Data)],
        Logger, APIToken, Verbose
    )

def GetContracts(Results, Data, Logger, APIToken, Verbose=False):
    return Request(
        '/GetContracts',
        [([], Results), (['Data'], Data)],
        Logger, APIToken, Verbose
    )

def UpdateContract(Results, Data, Logger, APIToken, Verbose=False):
    return Request(
        '/UpdateContract',
        [([], Results), (['Data'], Data)],
        Logger, APIToken, Verbose
    )

def GetPortfolioSummary(Results, Data, Logger, APIToken, Verbose=False):
    return Request(
        '/GetPortfolioSummary',
        [([], Results), (['Data'], Data)],
        Logger, APIToken, Verbose
    )

def DeleteContract(Results, Logger, APIToken, Verbose=False):
    return Request(
        '/DeleteContract',
        [([], Results)],
        Logger, APIToken, Verbose
    )

def DeletePortfolio(Results, Logger, APIToken, Verbose=False):
    return Request(
        '/DeletePortfolio',
        [([], Results)],
        Logger, APIToken, Verbose
    )

def GetContractPrice(Results, Data, Contract, Model, Pricer, Logger, APIToken, Verbose=False):
    return Request(
        '/GetContractPrice',
        [([], Results), (['Data'], Data), (['ContractDefinition'], Contract), (['ModelParameters'], Model), (['PricingOptions'], Pricer)],
        Logger, APIToken, Verbose
    )

def Get1DScenarioPricing(Results, Data, Contract, Model, Pricer, Logger, APIToken, Verbose=False):
    return Request(
        '/Get1DScenarioPricing',
        [([], Results), (['Data'], Data), (['ContractDefinition'], Contract), (['ModelParameters'], Model), (['PricingOptions'], Pricer)],
        Logger, APIToken, Verbose
    )

def GetSequence(Results, Logger, APIToken, Verbose=False):
    return Request(
        '/GetSequence',
        [([], Results)],
        Logger, APIToken, Verbose
    )

def GetSchedule(Results, Logger, APIToken, Verbose=False):
    return Request(
        '/GetSchedule',
        [([], Results)],
        Logger, APIToken, Verbose
    )

def Get2DScenarioPricing(Results, Data, Contract, Model, Pricer, Logger, APIToken, Verbose=False):
    return Request(
        '/Get2DScenarioPricing',
        [([], Results), (['Data'], Data), (['ContractDefinition'], Contract), (['ModelParameters'], Model), (['PricingOptions'], Pricer)],
        Logger, APIToken, Verbose
    )

def GetNDScenarioPricing(Results, Data, Contract, Model, Pricer, Logger, APIToken, Verbose=False):
    return Request(
        '/GetNDScenarioPricing',
        [([], Results), (['Data'], Data), (['ContractDefinition'], Contract), (['ModelParameters'], Model), (['PricingOptions'], Pricer)],
        Logger, APIToken, Verbose
    )

def GetContractFeatures(Results, Data, Contract, Model, Pricer, Logger, APIToken, Verbose=False):
    return Request(
        '/GetContractFeatures',
        [([], Results), (['Data'], Data), (['ContractDefinition'], Contract), (['ModelParameters'], Model), (['PricingOptions'], Pricer)],
        Logger, APIToken, Verbose
    )

def GetRiskNeutralStatistics(Results, Data, Contract, Model, Pricer, Logger, APIToken, Verbose=False):
    return Request(
        '/GetRiskNeutralStatistics',
        [([], Results), (['Data'], Data), (['ContractDefinition'], Contract), (['ModelParameters'], Model), (['PricingOptions'], Pricer)],
        Logger, APIToken, Verbose
    )

def GetContractScenarios(Results, Data, Contract, Logger, APIToken, Verbose=False):
    return Request(
        '/GetContractScenarios',
        [([], Results), (['Data'], Data), (['ContractDefinition'], Contract)],
        Logger, APIToken, Verbose
    )

def GetBlackScholesCalibration(Results, Data, Model, Logger, APIToken, Verbose=False):
    return Request(
        '/GetBlackScholesCalibration',
        [([], Results), (['Data'], Data), (['ModelParameters'], Model)],
        Logger, APIToken, Verbose
    )

def GetBlackScholesTermStructureCalibration(Results, Data, Model, Logger, APIToken, Verbose=False):
    return Request(
        '/GetBlackScholesTermStructureCalibration',
        [([], Results), (['Data'], Data), (['ModelParameters'], Model)],
        Logger, APIToken, Verbose
    )

def GetDupireLocalVolatilityCalibration(Results, Data, Model, Logger, APIToken, Verbose=False):
    return Request(
        '/GetDupireCalibration',
        [([], Results), (['Data'], Data), (['ModelParameters'], Model)],
        Logger, APIToken, Verbose
    )

def GetGenOTCCalibration(Results, Data, Model, Logger, APIToken, Verbose=False):
    return Request(
        '/GetGenOTCCalibration',
        [([], Results), (['Data'], Data), (['ModelParameters'], Model)],
        Logger, APIToken, Verbose
    )

def GetVanillaMarketComparison(Results, Data, Model, Pricer, Logger, APIToken, Verbose=False):
    return Request(
        '/GetVanillaMarketComparison',
        [([], Results), (['Data'], Data), (['ModelParameters'], Model), (['PricingOptions'], Pricer)],
        Logger, APIToken, Verbose
    )

def GetForwardMarketComparison(Results, Data, Model, Pricer, Logger, APIToken, Verbose=False):
    return Request(
        '/GetForwardMarketComparison',
        [([], Results), (['Data'], Data), (['ModelParameters'], Model), (['PricingOptions'], Pricer)],
        Logger, APIToken, Verbose
    )

def GetVanillaModelComparison(Results, Data, Model, Pricer, Logger, APIToken, Verbose=False):
    return Request(
        '/GetVanillaModelComparison',
        [([], Results), (['Data'], Data), (['ModelParameters'], Model), (['PricingOptions'], Pricer)],
        Logger, APIToken, Verbose
    )

def GetVanillaInterpolation(Results, Data, Model, Logger, APIToken, Verbose=False):
    return Request(
        '/GetVanillaInterpolation',
        [([], Results), (['Data'], Data), (['ModelParameters'], Model)],
        Logger, APIToken, Verbose
    )

def GetVanillaArbitrage(Results, Data, Model, Logger, APIToken, Verbose=False):
    return Request(
        '/GetVanillaArbitrage',
        [([], Results), (['Data'], Data), (['ModelParameters'], Model)],
        Logger, APIToken, Verbose
    )