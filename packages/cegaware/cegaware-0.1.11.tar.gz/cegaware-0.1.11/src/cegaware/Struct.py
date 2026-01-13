###################################################################################
# Copyright © 2025 Matthieu Charrier. All rights reserved. ########################
# This file is the exclusive intellectual property of Matthieu Charrier. ##########
# No reproduction, modification, distribution, or use is permitted without ########
# prior written authorization. A separate licensing agreement may grant ###########
# Cegaware limited rights of use. Absent such agreement, no rights are granted. ###
###################################################################################

# std.
from os import cpu_count

# cegaware.
from cegaware.Enum import *

def ldeserialize(pClassName, pRoot):
    if(pRoot != None):
        return [pClassName().deserialize(Item) for Item in pRoot]
    else:
        return []
    
def lserialize(pObjectList):
    if(pObjectList != None):
        return [item.serialize() for item in pObjectList]
    else:
        return None
    
def oserialize(Object):
    return Object.serialize()

def odeserialize(pClassName, pRoot):
    return pClassName().deserialize(pRoot)

class DateShift:
    def __init__(self, pShift='', pCalendar=Calendar.Dummy, BusinessDayConvention=BusinessDayConvention.Following, EndOfMonthConvention=False):
        self.Shift = pShift
        self.Calendar = pCalendar
        self.BusinessDayConvention = BusinessDayConvention
        self.EndOfMonthConvention = EndOfMonthConvention
    def serialize(self):
        return {
            'Shift': self.Shift,
            'Calendar': self.Calendar.name.replace("_", " "),
            'BusinessDayConvention': self.BusinessDayConvention.name.replace("_", " "),
            'EndOfMonthConvention': self.EndOfMonthConvention
        }
    def deserialize(self, pRoot):
        self.Shift = pRoot['Shift']
        self.Calendar = pRoot['Calendar']
        self.BusinessDayConvention = pRoot['BusinessDayConvention']
        self.EndOfMonthConvention = pRoot['EndOfMonthConvention']
        return self

class SuffixedNumber:
    def __init__(self, Value=None, Unit=None):
        self.Value = Value
        self.Unit = Unit
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Value = pRoot['Value']
        self.Unit = pRoot['Unit']
        return self

class GetPortfolios_Portfolio:
    def __init__(self):
        self.PortfolioId = None
        self.Name = None
        self.LastCalculationDate = None
        self.PricingResults = None
        self.Pnl = None
        self.Performance = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.PortfolioId = pRoot['PortfolioId']
        self.Name = pRoot['Name']
        self.PricingResults = odeserialize(PricingResults, pRoot['PricingResults'])
        if 'LastCalculationDate' in pRoot: self.LastCalculationDate = pRoot['LastCalculationDate']
        if 'Pnl' in pRoot: self.Pnl = odeserialize(SuffixedNumber, pRoot['Pnl'])
        if 'Performance' in pRoot: self.Performance = odeserialize(SuffixedNumber, pRoot['Performance'])
        return self
    
class GetPortfolios_Results:
    def __init__(self):
        self.PortfolioTable = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.PortfolioTable = ldeserialize(GetPortfolios_Portfolio, pRoot['PortfolioTable']) 
        return self
    
class CreatePortfolio_Results:
    def __init__(self, Name, ExternalId, Currency):
        self.Name = Name
        self.ExternalId = ExternalId
        self.Currency = Currency
        self.PortfolioId = None
    def serialize(self):
        return {
            'Name': self.Name,
            'ExternalId': self.ExternalId,
            'Currency': self.Currency
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.ExternalId = pRoot['ExternalId']
        self.Currency = pRoot['Currency']
        self.PortfolioId = pRoot['PortfolioId']
        return self
    
class GetPortfolio_Results:
    def __init__(self, PortfolioId):
        self.PortfolioId = PortfolioId
        self.Name = None
        self.ExternalId = None
        self.Currency = None
    def serialize(self):
        return {
            'PortfolioId': self.PortfolioId
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.ExternalId = pRoot['ExternalId']
        self.Currency = pRoot['Currency']
        self.PortfolioId = pRoot['PortfolioId']
        return self
    
class DeletePortfolio_Results:
    def __init__(self, PortfolioId):
        self.PortfolioId = PortfolioId
    def serialize(self):
        return {
            'Id': self.PortfolioId
        }
    def deserialize(self, _):
        return self
    
class UpdatePortfolio_Results:
    def __init__(self, PortfolioId, Name, ExternalId, Currency):
        self.PortfolioId = PortfolioId
        self.Name = Name
        self.ExternalId = ExternalId
        self.Currency = Currency
    def serialize(self):
        return {
            'PortfolioId': self.PortfolioId,
            'Name': self.Name,
            'ExternalId': self.ExternalId,
            'Currency': self.Currency
        }
    def deserialize(self, _):
        return self
    
class GetPortfolioSummary_Allocation:
    def __init__(self):
        self.Name = None
        self.Weight = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.Weight = odeserialize(SuffixedNumber, pRoot['Weight'])
        return self
    

class GetPortfolioSummary_MaturityProfile:
    def __init__(self):
        self.Label = None
        self.Weight = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Label = pRoot['Label']
        self.Weight = odeserialize(SuffixedNumber, pRoot['Weight'])
        return self
    
class GetPortfolioSummary_UnderlyingMove:
    def __init__(self):
        self.Name = None
        self.Ticker = None
        self.Performance = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.Ticker = pRoot['Ticker']
        self.Performance = odeserialize(SuffixedNumber, pRoot['Performance'])
        return self
    
class GetPortfolioSummary_Notification:
    def __init__(self):
        self.ContractId = None
        self.Date = None
        self.Type = None
        self.Time = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.ContractId = pRoot['ContractId']
        self.Date = pRoot['Date']
        self.Type = pRoot['Type']
        self.Time = pRoot['Time']
        return self

class GetPortfolioSummary_Results:
    def __init__(self, PortfolioId):
        self.PortfolioId = PortfolioId
        self.NoDeals = None
        self.NoDealsAlive = None
        self.PortfolioCurrency = None
        self.LastCalculationDate = None
        self.Performance = None
        self.Pnl = None
        self.Price = None
        self.IndicatorTable = None
        self.HistoricalIndicatorTable = None
        self.AssetClassAllocation = None
        self.CurrencyAllocation = None
        self.ProductTypeAllocation = None
        self.UnderlyingAllocation = None
        self.MaturityProfile = None
        self.BestUnderlyingMoveTable = None
        self.WorstUnderlyingMoveTable = None
        self.Notifications = None
    def serialize(self):
        return {
            'PortfolioId': self.PortfolioId
        }
    def deserialize(self, pRoot):
        self.PortfolioId = pRoot['PortfolioId']
        self.NoDeals = pRoot['NoDeals']
        self.NoDealsAlive = pRoot['NoDealsAlive']
        self.PortfolioCurrency = pRoot['Currency']
        self.IndicatorTable = odeserialize(PricingResults, pRoot['IndicatorTable'])
        self.HistoricalIndicatorTable = ldeserialize(GetContractSummary_HistoricalIndicator, pRoot['HistoricalIndicatorTable'])
        self.AssetClassAllocation = ldeserialize(GetPortfolioSummary_Allocation, pRoot['AssetClassAllocation'])
        self.CurrencyAllocation = ldeserialize(GetPortfolioSummary_Allocation, pRoot['CurrencyAllocation'])
        self.ProductTypeAllocation = ldeserialize(GetPortfolioSummary_Allocation, pRoot['ProductTypeAllocation'])
        self.UnderlyingAllocation = ldeserialize(GetPortfolioSummary_Allocation, pRoot['UnderlyingAllocation'])
        self.MaturityProfile = ldeserialize(GetPortfolioSummary_MaturityProfile, pRoot['MaturityProfile'])
        self.BestUnderlyingMoveTable = ldeserialize(GetPortfolioSummary_UnderlyingMove, pRoot['BestUnderlyingMoveTable'])
        self.WorstUnderlyingMoveTable = ldeserialize(GetPortfolioSummary_UnderlyingMove, pRoot['WorstUnderlyingMoveTable'])
        self.Notifications = ldeserialize(GetPortfolioSummary_Notification, pRoot['Notifications'])
        if 'LastCalculationDate' in pRoot: self.LastCalculationDate = pRoot['LastCalculationDate']
        if 'Performance' in pRoot: self.Performance = odeserialize(SuffixedNumber, pRoot['Performance'])
        if 'Pnl' in pRoot: self.Pnl = odeserialize(SuffixedNumber, pRoot['Pnl'])
        if 'Price' in pRoot: self.Price = odeserialize(SuffixedNumber, pRoot['Price'])
        return self

class GetContracts_Results:
    def __init__(self, PortfolioId):
        self.PortfolioId = PortfolioId
        self.IndicatorTable = None
        self.ContractTable = None
    def serialize(self):
        return {
            'PortfolioId': self.PortfolioId
        }
    def deserialize(self, pRoot):
        self.PortfolioId = pRoot['PortfolioId']
        self.IndicatorTable = odeserialize(PricingResults, pRoot['IndicatorTable']) 
        self.ContractTable = ldeserialize(GetContracts_Contract, pRoot['ContractTable']) 
        return self
    
class GetContracts_Contract:
    def __init__(self):
        self.ContractId = None
        self.Name = None
        self.Type = None
        self.LastCalculationDate = None
        self.TradeDate = None
        self.MaturityDate = None
        self.Currency = None
        self.Underlyings = None
        self.Quantity = None
        self.Progression = None
        self.PricingResults = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.ContractId = pRoot['ContractId']
        self.Name = pRoot['Name']
        self.Type = pRoot['Type']
        self.LastCalculationDate = pRoot['LastCalculationDate']
        self.TradeDate = pRoot['TradeDate']
        self.MaturityDate = pRoot['MaturityDate']
        self.Currency = pRoot['Currency']
        self.Underlyings = pRoot['Underlyings']
        self.Quantity = pRoot['Quantity']
        self.Progression = pRoot['Progression']
        self.PricingResults = odeserialize(PricingResults, pRoot['PricingResults'])
        return self

class CreateContract_Results:
    def __init__(self, ContractName, ContractCurrency, TradeDate, Quantity, PortfolioId, ModelParameters, PricingOptions, ContractDefinition):
        self.ContractName = ContractName
        self.ContractCurrency = ContractCurrency
        self.TradeDate = TradeDate
        self.Quantity = Quantity
        self.PortfolioId = PortfolioId
        self.ModelParameters = ModelParameters
        self.PricingOptions = PricingOptions
        self.ContractDefinition = ContractDefinition
        self.ContractId = None
    def serialize(self):
        return {
            'ContractName': self.ContractName,
            'ContractCurrency': self.ContractCurrency,
            'TradeDate': self.TradeDate,
            'Quantity': self.Quantity,
            'PortfolioId': self.PortfolioId,
            'ModelParameters': oserialize(self.ModelParameters),
            'PricingOptions': oserialize(self.PricingOptions),
            'ContractDefinition': oserialize(self.ContractDefinition)
        }
    def deserialize(self, pRoot):
        self.ContractName = pRoot['ContractName']
        self.ContractCurrency = pRoot['ContractCurrency']
        self.TradeDate = pRoot['TradeDate']
        self.Quantity = pRoot['Quantity']
        self.PortfolioId = pRoot['PortfolioId']
        self.ContractId = pRoot['ContractId']
        self.ModelParameters = odeserialize(Model, pRoot['ModelParameters']) 
        self.PricingOptions = odeserialize(Pricer, pRoot['PricingOptions']) 
        self.ContractDefinition = odeserialize(ContractDefinition, pRoot['ContractDefinition']) 
        return self

class GetContract_Results:
    def __init__(self, ContractId):
        self.ContractId = ContractId
        self.ContractName = None
        self.ContractCurrency = None
        self.TradeDate = None
        self.Quantity = None
        self.PortfolioId = None
        self.ModelParameters = None
        self.PricingOptions = None
        self.ContractDefinition = None
    def serialize(self):
        return {
            'ContractId': self.ContractId
        }
    def deserialize(self, pRoot):
        self.ContractId = pRoot['ContractId']
        self.ContractName = pRoot['ContractName']
        self.ContractCurrency = pRoot['ContractCurrency']
        self.TradeDate = pRoot['TradeDate']
        self.Quantity = pRoot['Quantity']
        self.PortfolioId = pRoot['PortfolioId']
        self.ModelParameters = odeserialize(Model, pRoot['ModelParameters']) 
        self.PricingOptions = odeserialize(Pricer, pRoot['PricingOptions']) 
        self.ContractDefinition = odeserialize(ContractDefinition, pRoot['ContractDefinition']) 
        return self
    
class DeleteContract_Results:
    def __init__(self, ContractId):
        self.ContractId = ContractId
    def serialize(self):
        return {
            'ContractId': self.ContractId
        }
    def deserialize(self, pRoot):
        self.ContractId = pRoot['ContractId']
        return self
    
class UpdateContract_Results:
    def __init__(self, ContractId, ContractName, ContractCurrency, TradeDate, Quantity, ModelParameters, PricingOptions, ContractDefinition):
        self.ContractId = ContractId
        self.ContractName = ContractName
        self.ContractCurrency = ContractCurrency
        self.TradeDate = TradeDate
        self.Quantity = Quantity
        self.ModelParameters = ModelParameters
        self.PricingOptions = PricingOptions
        self.ContractDefinition = ContractDefinition
    def serialize(self):
        return {
            'ContractId': self.ContractId,
            'ContractName': self.ContractName,
            'ContractCurrency': self.ContractCurrency,
            'TradeDate': self.TradeDate,
            'Quantity': self.Quantity,
            'ModelParameters': oserialize(self.ModelParameters),
            'PricingOptions': oserialize(self.PricingOptions),
            'ContractDefinition': oserialize(self.ContractDefinition) 
        }
    def deserialize(self, _):
        return self
    
class GetContractSummary_Results:
    def __init__(self, ContractId):
        self.ContractId = ContractId
        self.DaysToMaturity = None
        self.ContractType = None
        self.ContractCurrency = None
        self.TradeDate = None
        self.MaturityDate = None
        self.InitialFixingDate = None
        self.LastFixingDate = None
        self.LastCalculationDate = None
        self.Script = None
        self.PastEvents = None
        self.UpcomingEvents = None
        self.Performance = None
        self.Pnl = None
        self.Price = None
        self.CorrelationMatrix = None
        self.IndicatorTable = None
        self.HistoricalIndicatorTable = None
        self.UnderlyingDevelopementTable = None
        self.Underlyings = None
        self.Fixings = None
        self.Payments = None
        self.Settings = None
    def serialize(self):
        return {
            'ContractId': self.ContractId
        }
    def deserialize(self, pRoot):
        self.ContractId = pRoot['ContractId']
        self.DaysToMaturity = pRoot['DaysToMaturity']
        self.ContractType = pRoot['ContractType']
        self.ContractCurrency = pRoot['ContractCurrency']
        self.TradeDate = pRoot['TradeDate']
        self.MaturityDate = pRoot['MaturityDate']
        self.InitialFixingDate = pRoot['InitialFixingDate']
        self.LastFixingDate = pRoot['LastFixingDate']
        self.Script = pRoot['Script']
        self.PastEvents = odeserialize(Notifications, pRoot['PastEvents'])
        self.UpcomingEvents = odeserialize(Notifications, pRoot['UpcomingEvents'])
        self.CorrelationMatrix = odeserialize(GetContractSummary_CorrelationMatrix, pRoot['CorrelationMatrix'])
        self.IndicatorTable = odeserialize(PricingResults, pRoot['IndicatorTable'])
        self.HistoricalIndicatorTable = ldeserialize(GetContractSummary_HistoricalIndicator, pRoot['HistoricalIndicatorTable'])
        self.UnderlyingDevelopementTable = ldeserialize(GetContractSummary_UnderlyingDevelopment, pRoot['UnderlyingDevelopementTable'])
        self.Underlyings = ldeserialize(GetContractSummary_Underlying, pRoot['Underlyings'])
        self.Fixings = ldeserialize(GetContractSummary_Fixing, pRoot['Fixings'])
        self.Payments = ldeserialize(GetContractSummary_Payment, pRoot['Payments'])
        self.Settings = ldeserialize(GetContractSummary_Setting, pRoot['Settings'])
        if 'LastCalculationDate' in pRoot: self.LastCalculationDate = pRoot['LastCalculationDate']
        if 'Performance' in pRoot: self.Performance = odeserialize(SuffixedNumber, pRoot['Performance'])
        if 'Pnl' in pRoot: self.Pnl = odeserialize(SuffixedNumber, pRoot['Pnl'])
        if 'Price' in pRoot: self.Price = odeserialize(SuffixedNumber, pRoot['Price'])
        return self
    
class GetContractSummary_UnderlyingDevelopment:
    def __init__(self):
        self.UnderlyingName = None
        self.UnderlyingTicker = None
        self.LastClosePrice = None
        self.UnderlyingObservationTable = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.UnderlyingName = pRoot['UnderlyingName']
        self.UnderlyingTicker = pRoot['UnderlyingTicker']
        self.LastClosePrice = odeserialize(SuffixedNumber, pRoot['LastClosePrice'])
        self.UnderlyingObservationTable = odeserialize(GetContractSummary_UnderlyingObservation, pRoot['UnderlyingObservationTable'])
        return self
    
class GetContractSummary_Underlying:
    def __init__(self):
        self.Ticker = None
        self.CompleteName = None
        self.QuoteCurrency = None
        self.AssetClass = None
        self.AssetKind = None
        self.IsQuanto = None
        self.IsInBasket = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.CompleteName = pRoot['CompleteName']
        self.QuoteCurrency = pRoot['QuoteCurrency']
        self.AssetClass = pRoot['AssetClass']
        self.AssetKind = pRoot['AssetKind']
        self.IsQuanto = pRoot['IsQuanto']
        self.IsInBasket = pRoot['IsInBasket']
        return self

class GetContractSummary_Fixing:
    def __init__(self):
        self.Date = None
        self.QuoteCurrency = None
        self.Name = None
        self.Ticker = None
        self.Quote = None
        self.IsPast = None
        self.Edit = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.QuoteCurrency = pRoot['QuoteCurrency']
        self.Name = pRoot['Name']
        self.Ticker = pRoot['Ticker']
        self.Quote = odeserialize(SuffixedNumber, pRoot['Quote'])
        self.IsPast = pRoot['IsPast']
        self.Edit = pRoot['Edit']
        return self
    
class GetContractSummary_Payment:
    def __init__(self):
        self.Date = None
        self.Kind = None
        self.Value = None
        self.Currency = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.Kind = pRoot['Kind']
        self.Value = odeserialize(SuffixedNumber, pRoot['Value'])
        self.Currency = pRoot['Currency']
        return self
    
class GetContractSummary_Setting:
    def __init__(self):
        self.Date = None
        self.Name = None
        self.Value = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.Name = pRoot['Name']
        self.Value = pRoot['Value']
        return self
    
class GetContractSummary_Correlation:
    def __init__(self):
        self.Value = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Value = odeserialize(SuffixedNumber, pRoot['Value'])
        return self
    
class GetContractSummary_CorrelationMatrix:
    def __init__(self):
        self.Rows = None
        self.Cols = None
        self.Data = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Rows = pRoot['Rows']
        self.Cols = pRoot['Cols']
        self.Data = [[odeserialize(GetContractSummary_Correlation, item) for item in jtem] for jtem in pRoot['Data']]
        return self
    
class Notifications:
    def __init__(self):
        self.Notifications = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):    
        # self.Notifications = ldeserialize(IEvent, pRoot)
        return self

class GetContractSummary_Indicator:
    def __init__(self):
        self.Name = None
        self.Value = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):    
        self.Name = pRoot['Name']
        self.Value = odeserialize(SuffixedNumber, pRoot['Value'])
        return self
    
class GetContractSummary_HistoricalIndicator:
    def __init__(self):
        self.CalculationDate = None
        self.CalculationEpoch = None
        self.PricingResults = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):    
        self.CalculationDate = pRoot['CalculationDate']
        self.CalculationEpoch = pRoot['CalculationEpoch']
        self.PricingResults = odeserialize(PricingResults, pRoot['PricingResults'])
        return self
    
class GetContractSummary_UnderlyingObservation:
    def __init__(self):
        self.ObservationDate = None
        self.ObservationEpoch = None
        self.ClosePrice = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):    
        self.ObservationDate = pRoot['ObservationDate']
        self.ObservationEpoch = pRoot['ObservationEpoch']
        self.ClosePrice = odeserialize(SuffixedNumber, pRoot['ClosePrice'])
        return self

class ContractDefinition:
    def __init__(self, ContractType='', CashFlow=None, Currency=None):
        self.CashFlow = CashFlow
        self.ContractType = ContractType
        self.Currency = Currency
    def serialize(self):
        Results = oserialize(self.CashFlow)
        Results['ContractType'] = self.ContractType.name.replace("_", " ")
        Results['Currency'] = self.Currency
        return Results
    def deserialize(self, pRoot):
        self.ContractType = pRoot['ContractType']
        if 'Currency' in pRoot: self.Currency = pRoot['Currency']
        return self
    
class ICashFlow:
    def serialize(self):
        raise NotImplementedError
    def deserialize(self, _):
        raise NotImplementedError

class Console(ICashFlow):
    def __init__(self, Script = ''):
        self.Script = Script
    def serialize(self):
        return {
            'Script': self.Script
        }
    def deserialize(self, pRoot):
        self.Script = pRoot['Script']
        return self
    
class Records:
    def __init__(self, Dict={}):
        self.Dict = Dict
    def serialize(self):
        return self.Dict
    def deserialize(self, pRoot):
        self.Dict = pRoot
        return self

class DataSource:
    def __init__(self, Provider=DataSourceKind.Cegaware_Database, IsActivated=False, Records=Records()):
        self.Provider = Provider
        self.Records = Records
        self.IsActivated = IsActivated
    def serialize(self):
        return {
            'Provider': self.Provider.name.replace("_", " "),
            'Records': oserialize(self.Records),
            'IsActivated': self.IsActivated
        }
    def deserialize(self, pRoot):
        self.Provider = pRoot['Provider']
        self.Records = odeserialize(Records, pRoot['Records'])
        self.IsActivated = pRoot['IsActivated']
        return self

class Data:
    def __init__(self,
        Date,
        Sources
    ):
        self.Date = Date
        self.Sources = Sources
    def serialize(self):
        return {
            'Date': self.Date,
            'Sources': lserialize(self.Sources)
        }
    def deserialize(self, _):
        return self

class DayCounter:
    def __init__(self, Basis=Basis.Act_365, Calendar=Calendar.Dummy):
        self.Basis = Basis
        self.Calendar = Calendar
    def serialize(self):
        return {
            'Basis': self.Basis.name.replace("_", " "),
            'Calendar': self.Calendar.name.replace("_", " ")
        }
    def deserialize(self, pRoot):
        self.Basis = pRoot['Basis']
        self.Calendar = pRoot['Calendar']
        return self

class Pricer:
    def __init__(self,
        DayCounter = DayCounter(),
        BarrierSmoothingType = BarrierSmoothingType.None_,
        BarrierSmoothingParameter = 1.0,
        Method = PricingMethod.Monte_Carlo,
        MonteCarloLSMBasis = LSMBasis.Laguerre,
        MonteCarloTrials = 100000,
        MonteCarloLSMTrials = 10,
        MonteCarloLSMNbPolynomes = 5,
        MonteCarloLSMOnlyITM = False,
        MonteCarloTimeStep = 2,
        MonteCarloSeed = 19940523,
        MonteCarloNbThreads = cpu_count(),
        MonteCarloConfidenceLevel = 99.99,
        MonteCarloAntitheticFactor = 50.00,
        MonteCarloAddIntradayDates = False,
        FiniteDifferenceBoundaryCondition = BoundaryCondition.Dirichlet,
        FiniteDifferenceTimeStep = 2,
        FiniteDifferenceExplicitRate = 0.0,
        FiniteDifferenceUseRichardsonRombergExtrapolation = False,
        ClosedFormMoneynessGridSize = 100,
        ClosedFormMoneynessGridLowerBound = 0.01,
        ClosedFormMoneynessGridUpperBound = 199.99,
        WithGreeks = False,
        ComputeTheta = False,
        ComputeDelta = False,
        ComputeDV01 = False,
        DV01Direction = GreekDirection.Center, 
        DV01RateBump = 1.0,
        ComputeRepoSensibility = False,
        RepoSensibilityDirection = GreekDirection.Center, 
        RepoSensibilityRateBump = 1.0,
        DeltaSpotBump = 1.0,
        ThetaTimeBump = 0.50,
        DeltaDirection = GreekDirection.Center,
        ComputeGamma = False,
        GammaSpotBump = 1.0,
        ComputeXGamma = False,
        XGammaSpotBump = 1.0,
        ComputeVega = False,
        VegaVolatilityBump = 1.0,
        VegaDirection = GreekDirection.Center,
        ComputeVolga = False,
        VolgaVolatilityBump = 1.0,
        ComputeXVolga = False,
        XVolgaVolatilityBump = 1.0,
        ComputeVanna = False,
        VannaVolatilityBump = 1.0,
        VannaSpotBump = 1.0,
        ComputeCharm = False,
        CharmTimeBump = 0.50,
        CharmSpotBump = 1.0,
        ComputeXVanna = False,
        XVannaVolatilityBump = 1.0,
        XVannaSpotBump = 1.0,
        ComputeCega = False,
        CegaCorrelationBump = 1.0,
        CegaDirection = GreekDirection.Center
    ):
        self.DayCounter = DayCounter
        self.BarrierSmoothingType = BarrierSmoothingType
        self.BarrierSmoothingParameter = BarrierSmoothingParameter
        self.MonteCarloAddIntradayDates = MonteCarloAddIntradayDates
        self.Method = Method
        self.MonteCarloLSMBasis = MonteCarloLSMBasis
        self.MonteCarloTrials = MonteCarloTrials
        self.MonteCarloLSMTrials = MonteCarloLSMTrials
        self.MonteCarloLSMNbPolynomes = MonteCarloLSMNbPolynomes
        self.MonteCarloLSMOnlyITM = MonteCarloLSMOnlyITM
        self.MonteCarloTimeStep = MonteCarloTimeStep
        self.MonteCarloSeed = MonteCarloSeed
        self.MonteCarloNbThreads = MonteCarloNbThreads
        self.MonteCarloConfidenceLevel = MonteCarloConfidenceLevel
        self.MonteCarloAntitheticFactor = MonteCarloAntitheticFactor
        self.FiniteDifferenceBoundaryCondition = FiniteDifferenceBoundaryCondition
        self.FiniteDifferenceTimeStep = FiniteDifferenceTimeStep
        self.FiniteDifferenceExplicitRate = FiniteDifferenceExplicitRate
        self.FiniteDifferenceUseRichardsonRombergExtrapolation = FiniteDifferenceUseRichardsonRombergExtrapolation
        self.ClosedFormMoneynessGridSize = ClosedFormMoneynessGridSize
        self.ClosedFormMoneynessGridLowerBound = ClosedFormMoneynessGridLowerBound
        self.ClosedFormMoneynessGridUpperBound = ClosedFormMoneynessGridUpperBound
        self.WithGreeks = WithGreeks
        self.ComputeTheta = ComputeTheta
        self.ComputeDelta = ComputeDelta
        self.DeltaSpotBump = DeltaSpotBump
        self.ThetaTimeBump = ThetaTimeBump
        self.DeltaDirection = DeltaDirection
        self.ComputeGamma = ComputeGamma
        self.GammaSpotBump = GammaSpotBump
        self.ComputeXGamma = ComputeXGamma
        self.XGammaSpotBump = XGammaSpotBump
        self.ComputeVega = ComputeVega
        self.VegaVolatilityBump = VegaVolatilityBump
        self.VegaDirection = VegaDirection
        self.ComputeVolga = ComputeVolga
        self.VolgaVolatilityBump = VolgaVolatilityBump
        self.ComputeXVolga = ComputeXVolga
        self.XVolgaVolatilityBump = XVolgaVolatilityBump
        self.ComputeVanna = ComputeVanna
        self.VannaVolatilityBump = VannaVolatilityBump
        self.VannaSpotBump = VannaSpotBump
        self.ComputeCharm = ComputeCharm
        self.CharmTimeBump = CharmTimeBump
        self.CharmSpotBump = CharmSpotBump
        self.ComputeXVanna = ComputeXVanna
        self.XVannaVolatilityBump = XVannaVolatilityBump
        self.XVannaSpotBump = XVannaSpotBump
        self.ComputeCega = ComputeCega
        self.CegaCorrelationBump = CegaCorrelationBump
        self.CegaDirection = CegaDirection
        self.ComputeDV01 = ComputeDV01
        self.DV01Direction = DV01Direction
        self.DV01RateBump = DV01RateBump
        self.ComputeRepoSensibility = ComputeRepoSensibility
        self.RepoSensibilityDirection = RepoSensibilityDirection
        self.RepoSensibilityRateBump = RepoSensibilityRateBump
    def serialize(self):
        return {
            'DayCounter': oserialize(self.DayCounter),
            'BarrierSmoothingType': self.BarrierSmoothingType.name.replace("_", " "),
            'BarrierSmoothingParameter': self.BarrierSmoothingParameter,
            'MonteCarloAddIntradayDates': self.MonteCarloAddIntradayDates,
            'Method': self.Method.name.replace("_", " "),
            'MonteCarloLSMBasis': self.MonteCarloLSMBasis.name.replace("_", " "),
            'MonteCarloTrials': self.MonteCarloTrials,
            'MonteCarloLSMTrials': self.MonteCarloLSMTrials,
            'MonteCarloLSMNbPolynomes': self.MonteCarloLSMNbPolynomes,
            'MonteCarloLSMOnlyITM': self.MonteCarloLSMOnlyITM,
            'MonteCarloTimeStep': self.MonteCarloTimeStep,
            'MonteCarloSeed': self.MonteCarloSeed,
            'MonteCarloNbThreads': self.MonteCarloNbThreads,
            'MonteCarloConfidenceLevel': self.MonteCarloConfidenceLevel,
            'MonteCarloAntitheticFactor': self.MonteCarloAntitheticFactor,
            'FiniteDifferenceBoundaryCondition': self.FiniteDifferenceBoundaryCondition.name.replace("_", " "),
            'FiniteDifferenceTimeStep': self.FiniteDifferenceTimeStep,
            'FiniteDifferenceExplicitRate': self.FiniteDifferenceExplicitRate,
            'FiniteDifferenceUseRichardsonRombergExtrapolation': self.FiniteDifferenceUseRichardsonRombergExtrapolation,
            'ClosedFormMoneynessGridSize': self.ClosedFormMoneynessGridSize,
            'ClosedFormMoneynessGridLowerBound': self.ClosedFormMoneynessGridLowerBound,
            'ClosedFormMoneynessGridUpperBound': self.ClosedFormMoneynessGridUpperBound,
            'WithGreeks': self.WithGreeks,
            'ComputeTheta': self.ComputeTheta,
            'ComputeDelta': self.ComputeDelta,
            'DeltaSpotBump': self.DeltaSpotBump,
            'ThetaTimeBump': self.ThetaTimeBump,
            'DeltaDirection': self.DeltaDirection,
            'ComputeGamma': self.ComputeGamma,
            'GammaSpotBump': self.GammaSpotBump,
            'ComputeXGamma': self.ComputeXGamma,
            'XGammaSpotBump': self.XGammaSpotBump,
            'ComputeVega': self.ComputeVega,
            'VegaVolatilityBump': self.VegaVolatilityBump,
            'VegaDirection': self.VegaDirection,
            'ComputeVolga': self.ComputeVolga,
            'VolgaVolatilityBump': self.VolgaVolatilityBump,
            'ComputeXVolga': self.ComputeXVolga,
            'XVolgaVolatilityBump': self.XVolgaVolatilityBump,
            'ComputeVanna': self.ComputeVanna,
            'VannaVolatilityBump': self.VannaVolatilityBump,
            'VannaSpotBump': self.VannaSpotBump,
            'ComputeCharm': self.ComputeCharm,
            'CharmTimeBump': self.CharmTimeBump,
            'CharmSpotBump': self.CharmSpotBump,
            'ComputeXVanna': self.ComputeXVanna,
            'XVannaVolatilityBump': self.XVannaVolatilityBump,
            'XVannaSpotBump': self.XVannaSpotBump,
            'ComputeCega': self.ComputeCega,
            'CegaCorrelationBump': self.CegaCorrelationBump,
            'CegaDirection': self.CegaDirection,
            'ComputeDV01': self.ComputeDV01,
            'DV01Direction': self.DV01Direction,
            'DV01RateBump': self.DV01RateBump,
            'ComputeRepoSensibility': self.ComputeRepoSensibility,
            'RepoSensibilityDirection': self.RepoSensibilityDirection,
            'RepoSensibilityRateBump': self.RepoSensibilityRateBump
        }
    def deserialize(self, pRoot):
        self.BarrierSmoothingParameter = pRoot['BarrierSmoothingParameter']
        self.MonteCarloAddIntradayDates = pRoot['MonteCarloAddIntradayDates']
        self.DV01Direction = pRoot['DV01Direction']
        self.DV01RateBump = pRoot['DV01RateBump']
        self.ComputeRepoSensibility = pRoot['ComputeRepoSensibility']
        self.RepoSensibilityDirection = pRoot['RepoSensibilityDirection']
        self.RepoSensibilityRateBump = pRoot['RepoSensibilityRateBump']
        self.DayCounter = odeserialize(DayCounter, pRoot['DayCounter'])
        self.MonteCarloLSMBasis = pRoot['MonteCarloLSMBasis']
        self.Method = pRoot['Method']
        self.MonteCarloTrials = pRoot['MonteCarloTrials']
        self.MonteCarloLSMTrials = pRoot['MonteCarloLSMTrials']
        self.MonteCarloLSMNbPolynomes = pRoot['MonteCarloLSMNbPolynomes']
        self.MonteCarloLSMOnlyITM = pRoot['MonteCarloLSMOnlyITM']
        self.MonteCarloTimeStep = pRoot['MonteCarloTimeStep']
        self.MonteCarloSeed = pRoot['MonteCarloSeed']
        self.MonteCarloNbThreads = pRoot['MonteCarloNbThreads']
        self.MonteCarloConfidenceLevel = pRoot['MonteCarloConfidenceLevel']
        self.MonteCarloAntitheticFactor = pRoot['MonteCarloAntitheticFactor']
        self.FiniteDifferenceBoundaryCondition = pRoot['FiniteDifferenceBoundaryCondition']
        self.FiniteDifferenceTimeStep = pRoot['FiniteDifferenceTimeStep']
        self.FiniteDifferenceExplicitRate = pRoot['FiniteDifferenceExplicitRate']
        self.FiniteDifferenceUseRichardsonRombergExtrapolation = pRoot['FiniteDifferenceUseRichardsonRombergExtrapolation']
        self.ClosedFormMoneynessGridSize = pRoot['ClosedFormMoneynessGridSize']
        self.ClosedFormMoneynessGridLowerBound = pRoot['ClosedFormMoneynessGridLowerBound']
        self.ClosedFormMoneynessGridUpperBound = pRoot['ClosedFormMoneynessGridUpperBound']
        self.WithGreeks = pRoot['WithGreeks']
        self.ComputeTheta = pRoot['ComputeTheta']
        self.ComputeDelta = pRoot['ComputeDelta']
        self.DeltaSpotBump = pRoot['DeltaSpotBump']
        self.ThetaTimeBump = pRoot['ThetaTimeBump']
        self.DeltaDirection = pRoot['DeltaDirection']
        self.ComputeGamma = pRoot['ComputeGamma']
        self.GammaSpotBump = pRoot['GammaSpotBump']
        self.ComputeXGamma = pRoot['ComputeXGamma']
        self.XGammaSpotBump = pRoot['XGammaSpotBump']
        self.ComputeVega = pRoot['ComputeVega']
        self.VegaVolatilityBump = pRoot['VegaVolatilityBump']
        self.VegaDirection = pRoot['VegaDirection']
        self.ComputeVolga = pRoot['ComputeVolga']
        self.VolgaVolatilityBump = pRoot['VolgaVolatilityBump']
        self.ComputeXVolga = pRoot['ComputeXVolga']
        self.XVolgaVolatilityBump = pRoot['XVolgaVolatilityBump']
        self.ComputeVanna = pRoot['ComputeVanna']
        self.VannaVolatilityBump = pRoot['VannaVolatilityBump']
        self.VannaSpotBump = pRoot['VannaSpotBump']
        self.ComputeCharm = pRoot['ComputeCharm']
        self.CharmTimeBump = pRoot['CharmTimeBump']
        self.CharmSpotBump = pRoot['CharmSpotBump']
        self.ComputeXVanna = pRoot['ComputeXVanna']
        self.XVannaVolatilityBump = pRoot['XVannaVolatilityBump']
        self.XVannaSpotBump = pRoot['XVannaSpotBump']
        self.ComputeCega = pRoot['ComputeCega']
        self.CegaCorrelationBump = pRoot['CegaCorrelationBump']
        self.CegaDirection = pRoot['CegaDirection']
        return self

class GetContractPrice_InterestRateIndicator:
    def __init__(self):
        self.InstrumentName = None
        self.DV01 = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.InstrumentName = pRoot['InstrumentName']
        self.DV01 = odeserialize(SuffixedNumber, pRoot['DV01'])
        return self
    
class GetContractPrice_PairUnderlyingIndicator:
    def __init__(self):
        self.FirstTicker = None
        self.SecondTicker = None
        self.Cega = None
        self.XGamma = None
        self.XVolga = None
        self.XVanna = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.FirstTicker = pRoot['FirstTicker']
        self.SecondTicker = pRoot['SecondTicker']
        self.Cega = odeserialize(SuffixedNumber, pRoot['Cega'])
        self.XGamma = odeserialize(SuffixedNumber, pRoot['XGamma'])
        self.XVolga = odeserialize(SuffixedNumber, pRoot['XVolga'])
        self.XVanna = odeserialize(SuffixedNumber, pRoot['XVanna'])
        return self

class GetContractPrice_SingleUnderlyingIndicator:
    def __init__(self):
        self.Ticker = None
        self.Delta = None
        self.Vega = None
        self.Gamma = None
        self.Volga = None
        self.Vanna = None
        self.Charm = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Delta = odeserialize(SuffixedNumber, pRoot['Delta'])
        self.Vega = odeserialize(SuffixedNumber, pRoot['Vega'])
        self.Gamma = odeserialize(SuffixedNumber, pRoot['Gamma'])
        self.Volga = odeserialize(SuffixedNumber, pRoot['Volga'])
        self.Vanna = odeserialize(SuffixedNumber, pRoot['Vanna'])
        self.Charm = odeserialize(SuffixedNumber, pRoot['Charm'])
        return self

class GetContractPrice_Results:
    def __init__(self):
        self.SingleUnderlyingIndicatorTable = None
        self.PairUnderlyingIndicatorTable = None
        self.InterestRateIndicatorTable = None
        self.Price = None
        self.Theta = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        if pRoot['SingleUnderlyingIndicatorTable'] != None: self.SingleUnderlyingIndicatorTable = odeserialize(GetContractPrice_SingleUnderlyingIndicator, pRoot['SingleUnderlyingIndicatorTable'])
        if pRoot['PairUnderlyingIndicatorTable'] != None: self.PairUnderlyingIndicatorTable = odeserialize(GetContractPrice_PairUnderlyingIndicator, pRoot['PairUnderlyingIndicatorTable'])
        if pRoot['InterestRateIndicatorTable'] != None: self.InterestRateIndicatorTable = odeserialize(GetContractPrice_InterestRateIndicator, pRoot['InterestRateIndicatorTable'])
        if 'Price' in pRoot: self.Price = odeserialize(SuffixedNumber, pRoot['Price'])
        if 'Theta' in pRoot: self.Theta = odeserialize(SuffixedNumber, pRoot['Theta'])
        return self

class GetContractFeatures_FeatureToSolve:
    def __init__(self, Name=None, Min=None, Max=None, Precision=100):
        self.Name = Name
        self.Min = Min
        self.Max = Max
        self.Precision = Precision
        self.Lower = None
        self.Upper = None
        self.Root = None
        self.HasLower = None
        self.HasUpper = None
        self.HasRoot = None
    def serialize(self):
        return {
            'Name': self.Name,
            'Min': self.Min,
            'Max': self.Max,
            'Precision': self.Precision
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.Min = pRoot['Min']
        self.Max = pRoot['Max']
        self.Precision = pRoot['Precision']
        self.Lower = pRoot['Lower']
        self.Upper = pRoot['Upper']
        self.Root = pRoot['Root']
        self.HasLower = pRoot['HasLower']
        self.HasUpper = pRoot['HasUpper']
        self.HasRoot = pRoot['HasRoot']
        return self

class GetContractFeatures_Target:
    def __init__(self, Price=None):
        self.Price = Price
        self.Lower = None
        self.Upper = None
        self.HasLower = None
        self.HasUpper = None
    def serialize(self):
        return {
            'Price': self.Price
        }
    def deserialize(self, pRoot):
        self.Price = pRoot['Price']
        self.Lower = pRoot['Lower']
        self.Upper = pRoot['Upper']
        self.HasLower = pRoot['HasLower']
        self.HasUpper = pRoot['HasUpper']
        return self

class GetContractFeatures_Results:
    def __init__(self, Target, FeaturesToSolve):
        self.FeaturesToSolve = FeaturesToSolve
        self.Target = Target
    def serialize(self):
        Results = oserialize(self.Target)
        Results['FeaturesToSolve'] = lserialize(self.FeaturesToSolve)
        return Results
    def deserialize(self, pRoot):
        self.FeaturesToSolve = ldeserialize(GetContractFeatures_FeatureToSolve, pRoot['FeaturesToSolve'])
        self.Target = odeserialize(GetContractFeatures_Target, pRoot)
        return self

class GetRiskNeutralStatistics_Results:
    def __init__(self, ConvergenceSize=1000):
        self.ConvergenceSize = ConvergenceSize
        self.Result = None
        self.Mediane = None
        self.Quartile1 = None
        self.Quartile3 = None
        self.Decile1 = None
        self.Decile2 = None
        self.Decile3 = None
        self.Decile4 = None
        self.Decile5 = None
        self.Decile6 = None 
        self.Decile7 = None
        self.Decile8 = None
        self.Decile9 = None
        self.Duration = None
        self.Decomposition = None
        self.ForwardFixings = None
        self.Barriers = None
        self.Convergence = None
        self.Choices = None
    def serialize(self):
        return {
            'ConvergenceSize': self.ConvergenceSize
        }
    def deserialize(self, pRoot):
        self.ConvergenceSize = pRoot['ConvergenceSize']
        self.Result = odeserialize(PricingResult, pRoot['Result'])
        self.Mediane = odeserialize(SuffixedNumber, pRoot['Mediane'])
        self.Quartile1 = odeserialize(SuffixedNumber, pRoot['Quartile1'])
        self.Quartile3 = odeserialize(SuffixedNumber, pRoot['Quartile2'])
        self.Decile1 = odeserialize(SuffixedNumber, pRoot['Decile1'])
        self.Decile2 = odeserialize(SuffixedNumber, pRoot['Decile2'])
        self.Decile3 = odeserialize(SuffixedNumber, pRoot['Decile3'])
        self.Decile4 = odeserialize(SuffixedNumber, pRoot['Decile4'])
        self.Decile5 = odeserialize(SuffixedNumber, pRoot['Decile5'])
        self.Decile6 = odeserialize(SuffixedNumber, pRoot['Decile6'])
        self.Decile7 = odeserialize(SuffixedNumber, pRoot['Decile7'])
        self.Decile8 = odeserialize(SuffixedNumber, pRoot['Decile8'])
        self.Decile9 = odeserialize(SuffixedNumber, pRoot['Decile9'])
        self.Duration = odeserialize(PricingResult, pRoot['Duration'])
        self.Decomposition = ldeserialize(GetMCPriceWithDetails_Decomposition, pRoot['Decomposition'])
        self.ForwardFixings = ldeserialize(GetMCPriceWithDetails_ForwardFixing, pRoot['ForwardFixings'])
        self.Barriers = ldeserialize(GetMCPriceWithDetails_Barrier, pRoot['Barriers'])
        self.Convergence = ldeserialize(GetMCPriceWithDetails_Convergence, pRoot['Convergence'])
        self.Choices = ldeserialize(GetMCPriceWithDetails_Choice, pRoot['Choices'])
        return self

class GetMCPriceWithDetails_ChoiceDetail:
    def __init__(self):
        self.Script = None
        self.Probability = None
        self.ContinuationValue = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):    
        self.Script = pRoot['Script']
        self.Probability = odeserialize(PricingResult, pRoot['Probability'])
        self.ContinuationValue = pRoot['ContinuationValue']
        return self

class GetMCPriceWithDetails_Choice:
    def __init__(self):
        self.ChoiceDate = None
        self.ChoiceOwnership = None
        self.RegressorScript = None
        self.Details = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):    
        self.ChoiceDate = pRoot['ChoiceDate']
        self.ChoiceOwnership = pRoot['ChoiceOwnership']
        self.RegressorScript = pRoot['RegressorScript']
        self.Details = ldeserialize(GetMCPriceWithDetails_ChoiceDetail, pRoot['Details'])
        return self

class GetMCPriceWithDetails_Convergence:
    def __init__(self):
        self.Trials = None
        self.Result = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Trials = pRoot['Trials']
        self.Result = odeserialize(PricingResult, pRoot['Result'])
        return self

class GetMCPriceWithDetails_Barrier:
    def __init__(self):
        self.EventDate = None
        self.EventScript = None
        self.ProbaIn = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.EventDate = pRoot['EventDate']
        self.EventScript = pRoot['EventScript']
        self.ProbaIn = odeserialize(PricingResult, pRoot['ProbaIn'])
        return self

class GetMCPriceWithDetails_ForwardFixing:
    def __init__(self):
        self.FixingDate = None
        self.Ticker = None
        self.Value = None
        self.Currency = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.FixingDate = pRoot['FixingDate']
        self.Ticker = pRoot['Ticker']
        self.Value = pRoot['Value']
        self.Currency = pRoot['Currency']
        return self

class GetMCPriceWithDetails_Decomposition:
    def __init__(self):
        self.Date = None
        self.Price = None
        self.ProbaExists = None
        self.ProbaPositive = None
        self.ProbaIsKilled = None
        self.ProbaHasBeenKilled = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.Price = odeserialize(PricingResult, pRoot['Price'])
        self.ProbaExists = odeserialize(PricingResult, pRoot['ProbaExists'])
        self.ProbaPositive = odeserialize(PricingResult, pRoot['ProbaPositive'])
        self.ProbaIsKilled = odeserialize(PricingResult, pRoot['ProbaIsKilled'])
        self.ProbaHasBeenKilled = odeserialize(PricingResult, pRoot['ProbaHasBeenKilled'])
        return self

class Get1DScenarioPricing_Results:
    def __init__(self, Name, ResultKind, BumpKind, LadderKind, BumpUnit, Plots):
        self.Name = Name
        self.ResultKind = ResultKind
        self.BumpKind = BumpKind
        self.LadderKind = LadderKind
        self.BumpUnit = BumpUnit
        self.Plots = Plots
        self.CentralResult = None
    def serialize(self):
        return {
            'Name': self.Name,
            'ResultKind': self.ResultKind.name.replace("_", " "),
            'LadderKind': self.LadderKind.name.replace("_", " "),
            'BumpKind': self.BumpKind.name.replace("_", " "),
            'BumpUnit': self.BumpUnit.name.replace("_", " "),
            'Plots': lserialize(self.Plots)
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.ResultKind = pRoot['ResultKind']
        self.LadderKind = pRoot['LadderKind']
        self.BumpKind = pRoot['BumpKind']
        self.BumpUnit = pRoot['BumpUnit']
        self.CentralResult = odeserialize(PricingResults, pRoot['CentralResult'])
        self.Plots = ldeserialize(Get1DScenarioPricing_Plot, pRoot['Plots'])
        return self

class Get1DScenarioPricing_Plot:
    def __init__(self, BumpValue=0.0):
        self.BumpValue = BumpValue
        self.Results = None
    def serialize(self):
        return {
            'BumpValue': self.BumpValue
        }
    def deserialize(self, pRoot):
        self.BumpValue = pRoot['BumpValue']
        self.Results = odeserialize(PricingResults, pRoot['Results'])
        return self

class Get2DScenarioPricing_Plot:
    def __init__(self):
        self.Results = PricingResults()
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Results = odeserialize(PricingResults, pRoot['Results'])
        return self

class Get2DScenarioPricing_Results:
    def __init__(self, 
        LadderKind, ResultKind,
        FirstName, FirstBumpKind, FirstBumpUnit,FirstBumpValues,
        SecondName, SecondBumpKind, SecondBumpUnit, SecondBumpValues
    ):
        self.LadderKind = LadderKind
        self.ResultKind = ResultKind
        self.FirstName = FirstName
        self.SecondName = SecondName
        self.FirstBumpKind = FirstBumpKind
        self.SecondBumpKind = SecondBumpKind
        self.FirstBumpUnit = FirstBumpUnit
        self.SecondBumpUnit = SecondBumpUnit
        self.FirstBumpValues = FirstBumpValues
        self.SecondBumpValues = SecondBumpValues
        self.Plots = None
        self.CentralResult = None
    def serialize(self):
        return {
            'LadderKind': self.LadderKind.name.replace("_", " "),
            'ResultKind': self.ResultKind.name.replace("_", " "),
            'FirstName': self.FirstName,
            'SecondName': self.SecondName,
            'FirstBumpKind': self.FirstBumpKind.name.replace("_", " "),
            'SecondBumpKind': self.SecondBumpKind.name.replace("_", " "),
            'FirstBumpUnit': self.FirstBumpUnit.name.replace("_", " "),
            'SecondBumpUnit': self.SecondBumpUnit.name.replace("_", " "),
            'FirstBumpValues': self.FirstBumpValues,
            'SecondBumpValues': self.SecondBumpValues
        }
    def deserialize(self, pRoot):
        self.LadderKind = pRoot['LadderKind']
        self.ResultKind = pRoot['ResultKind']
        self.FirstName = pRoot['FirstName']
        self.SecondName = pRoot['SecondName']
        self.FirstBumpKind = pRoot['FirstBumpKind']
        self.SecondBumpKind = pRoot['SecondBumpKind']
        self.FirstBumpUnit = pRoot['FirstBumpUnit']
        self.SecondBumpUnit = pRoot['SecondBumpUnit']
        self.FirstBumpValues = pRoot['FirstBumpValues']
        self.SecondBumpValues = pRoot['SecondBumpValues']
        self.Plots = odeserialize(Get2DScenarioPricing_PlotMatrix, pRoot['Plots'])
        self.CentralResult = odeserialize(PricingResults, pRoot['CentralResult'])
        return self

class Get2DScenarioPricing_PlotMatrix:
    def __init__(self):
        self.Rows = []
        self.Cols = []
        self.Data = [[]]
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Rows = pRoot['Rows']
        self.Cols = pRoot['Cols']
        self.Data = [[odeserialize(Get2DScenarioPricing_Plot, item) for item in jtem] for jtem in pRoot['Data']]
        return self

class GetNDScenarioPricing_Results:
    def __init__(self, ResultKind, LadderKind, Plots):
        self.Plots = Plots
        self.LadderKind = LadderKind
        self.ResultKind = ResultKind
        self.CentralResult = None
    def serialize(self):
        return {
            'ResultKind': self.ResultKind.name.replace("_", " "),
            'LadderKind': self.LadderKind.name.replace("_", " "),
            'Plots': lserialize(self.Plots)
        }
    def deserialize(self, pRoot):
        self.ResultKind = pRoot['ResultKind']
        self.LadderKind = pRoot['LadderKind']
        self.Plots = ldeserialize(GetNDScenarioPricing_Plot, pRoot['Plots'])
        self.CentralResult = odeserialize(PricingResults, pRoot['CentralResult'])
        return self
    
class GetNDScenarioPricing_Plot:
    def __init__(self, Scenarios=[]):
        self.Scenarios = Scenarios
        self.Results = None
    def serialize(self):
        return {
            'Scenarios': lserialize(self.Scenarios)
        }
    def deserialize(self, pRoot):
        self.Scenarios = ldeserialize(GetNDScenarioPricing_Scenario, pRoot['Scenarios'])
        self.Results = odeserialize(PricingResults, pRoot['Results'])
        return self

class GetNDScenarioPricing_Scenario:
    def __init__(self, Name='', BumpValue=0.0, BumpKind=BumpKind.Hybrid, BumpUnit=BumpUnit.None_):
        self.Name = Name
        self.BumpKind = BumpKind
        self.BumpUnit = BumpUnit
        self.BumpValue = BumpValue
    def serialize(self):
        return {
            'Name': self.Name,
            'BumpKind': self.BumpKind.name.replace("_", " "),
            'BumpUnit': self.BumpUnit,
            'BumpValue': self.BumpValue
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.BumpKind = pRoot['BumpKind']
        self.BumpUnit = pRoot['BumpUnit']
        self.BumpValue = pRoot['BumpValue']
        return self

class GetPortfolioPrice_Results:
    def __init__(self, PortfolioId):
        self.PortfolioId = PortfolioId
    def serialize(self):
        return {
            'PortfolioId': self.PortfolioId
        }
    def deserialize(self, _):
        return self

class GetBlackScholesCalibration_Results:
    def __init__(self, Maturity, UnderlyingTicker):
        self.Maturity = Maturity
        self.UnderlyingTicker = UnderlyingTicker
        self.Volatility = None
    def serialize(self):
        return {
            'Maturity': self.Maturity,
            'UnderlyingTicker': self.UnderlyingTicker
        }
    def deserialize(self, pRoot):
        self.Maturity = pRoot['Maturity']
        self.Volatility = odeserialize(SuffixedNumber, pRoot['Volatility'])
        self.UnderlyingTicker = pRoot['UnderlyingTicker']
        return self

class GetBlackScholesTermStructureCalibration_VolatilityCurveTable:
    def __init__(self, Maturity=None):
        self.Maturity = Maturity
        self.MaturityEpoch = None
        self.Volatility = None
    def serialize(self):
        return {
            'Maturity': self.Maturity
        }
    def deserialize(self, pRoot):
        self.Maturity = pRoot['Maturity']
        self.MaturityEpoch = pRoot['MaturityEpoch']
        self.Volatility = odeserialize(SuffixedNumber, pRoot['Volatility'])
        return self
    
class GetBlackScholesTermStructureCalibration_Results:
    def __init__(self, UnderlyingTicker, VolatilityCurveTable):
        self.UnderlyingTicker = UnderlyingTicker
        self.VolatilityCurveTable = VolatilityCurveTable
    def serialize(self):
        return {
            'UnderlyingTicker': self.UnderlyingTicker,
            'VolatilityCurveTable': lserialize(self.VolatilityCurveTable)
        }
    def deserialize(self, pRoot):
        self.UnderlyingTicker = pRoot['UnderlyingTicker']
        self.Volatility = ldeserialize(GetBlackScholesTermStructureCalibration_VolatilityCurveTable, pRoot['VolatilityCurveTable'])
        return self

class GetHestonCalibration_Results:
    def __init__(self,
        UnderlyingTicker,
        SpaceKind=SpaceKind.Strike,
        ValueKind=PriceKind.Volatility,
        InitialVolatility=SuffixedNumber(0.0, '%'),
        VarianceVolatilityFactor=SuffixedNumber(0.0, ''),
        LongTermVolatility=SuffixedNumber(0.0, '%'),
        MeanReversionFactor=SuffixedNumber(0.0, ''),
        SpotVarianceCorrelation=SuffixedNumber(0.0, '%'),
        RootMeanSquareError=SuffixedNumber(0.0, '')
    ):
        self.UnderlyingTicker = UnderlyingTicker
        self.SpaceKind = SpaceKind
        self.ValueKind = ValueKind
        self.InitialVolatility = InitialVolatility
        self.VarianceVolatilityFactor = VarianceVolatilityFactor
        self.LongTermVolatility = LongTermVolatility
        self.MeanReversionFactor = MeanReversionFactor
        self.SpotVarianceCorrelation = SpotVarianceCorrelation
        self.RootMeanSquareError = RootMeanSquareError
        self.ErrorByExpiryTable = None
    def serialize(self):
        return {
            'UnderlyingTicker': self.UnderlyingTicker,
            'SpaceKind': self.SpaceKind.name.replace("_", " "),
            'ValueKind': self.ValueKind.name.replace("_", " "),
            'InitialVolatility': oserialize(self.InitialVolatility),
            'VarianceVolatilityFactor': oserialize(self.VarianceVolatilityFactor),
            'LongTermVolatility': oserialize(self.LongTermVolatility),
            'MeanReversionFactor': oserialize(self.MeanReversionFactor),
            'SpotVarianceCorrelation': oserialize(self.SpotVarianceCorrelation),
            'RootMeanSquareError': oserialize(self.RootMeanSquareError)
        }
    def deserialize(self, pRoot):
        self.UnderlyingTicker = pRoot['UnderlyingTicker']
        self.SpaceKind = pRoot['SpaceKind']
        self.ValueKind = pRoot['ValueKind']
        self.InitialVolatility = odeserialize(SuffixedNumber, pRoot['InitialVolatility'])
        self.VarianceVolatilityFactor = odeserialize(SuffixedNumber, pRoot['VarianceVolatilityFactor'])
        self.LongTermVolatility = odeserialize(SuffixedNumber, pRoot['LongTermVolatility'])
        self.MeanReversionFactor = odeserialize(SuffixedNumber, pRoot['MeanReversionFactor'])
        self.SpotVarianceCorrelation = odeserialize(SuffixedNumber, pRoot['SpotVarianceCorrelation'])
        self.RootMeanSquareError = odeserialize(SuffixedNumber, pRoot['RootMeanSquareError'])
        self.ErrorByExpiryTable = ldeserialize(GetEquityFXImpliedVolatilityInterpolation_ErrorByExpiry, pRoot['ErrorByExpiryTable'])
        return self

class GetDupireLocalVolatilityCalibration_Results:
    def __init__(self,
        UnderlyingTicker,
        MaturityTable,
        ForwardMoneynessTable
    ):
        self.UnderlyingTicker = UnderlyingTicker
        self.MaturityTable = MaturityTable
        self.ForwardMoneynessTable = ForwardMoneynessTable
        self.LocalVolatilityMatrix = None
    def serialize(self):
        return {
            'UnderlyingTicker': self.UnderlyingTicker,
            'MaturityTable': [item for item in self.MaturityTable],
            'ForwardMoneynessTable': [item for item in self.ForwardMoneynessTable]
        }
    def deserialize(self, pRoot):
        self.UnderlyingTicker = pRoot['UnderlyingTicker']
        self.MaturityTable = [item for item in pRoot['MaturityTable']]
        self.ForwardMoneynessTable = [item for item in pRoot['ForwardMoneynessTable']]
        self.LocalVolatilityMatrix = odeserialize(GetEquityFXImpliedVolatilityArbitrage_ArbitrageMatrix, pRoot['LocalVolatilityMatrix'])
        return self

class GetGenOTCCalibration_Results:
    def __init__(self, ComputationTable):
        self.ComputationTable = ComputationTable
    def serialize(self):
        return {
            'ComputationTable': lserialize(self.ComputationTable)
        }
    def deserialize(self, pRoot):
        self.ComputationTable = ldeserialize(GetGenOTCCalibration_ComputationItem, pRoot['ComputationTable'])
        return self

class GetGenOTCCalibration_ComputationItem:
    def __init__(self, Ticker=None):
        self.Ticker = Ticker
        self.Uuid = None
        self.Status = None
    def serialize(self):
        return {
            'Ticker': self.Ticker
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Uuid = pRoot['Uuid']
        self.Status = pRoot['Status']
        return self

class GetContractScenarios_Results:
    def __init__(self, Underlyings):
        self.Underlyings = Underlyings
        self.Events = None
    def serialize(self):
        return {
            'Underlyings': lserialize(self.Underlyings)
        }
    def deserialize(self, pRoot):    
        self.Underlyings = ldeserialize(GetContractScenarios_UnderlyingFixing, pRoot['Underlyings'])
        self.Events = odeserialize(Notifications, pRoot['Events'])
        return self

class GetContractScenarios_UnderlyingFixing:
    def __init__(self, Ticker=None, Fixings=None):
        self.Ticker = Ticker
        self.Fixings = Fixings
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'Fixings': lserialize(self.Fixings)
        }
    def deserialize(self, pRoot):    
        self.Ticker = pRoot['Ticker']
        self.Fixings = ldeserialize(GetContractScenarios_Fixing, pRoot['Fixings'])
        return self

class GetContractScenarios_Fixing:
    def __init__(self, Date=None, Value=None):
        self.Date = Date
        self.Value = Value
        self.Time = None
        self.Currency = None
    def serialize(self):
        return {
            'Date': self.Date,
            'Value': self.Value,
            'Time': self.Time,
            'Currency': self.Currency
        }
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.Value = pRoot['Value']
        self.Time = pRoot['Time']
        self.Currency = pRoot['Currency']
        return self

class GetModelEquityFXForward_Results:
    def __init__(self, Ticker, TermStructure):
        self.Ticker = Ticker
        self.TermStructure = TermStructure
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'TermStructure': lserialize(self.TermStructure)
        }
    def deserialize(self, pRoot):    
        self.Ticker = pRoot['Ticker']
        self.TermStructure = ldeserialize(GetModelEquityFXForward_TermStructure, pRoot['TermStructure'])
        return self

class GetModelEquityFXForward_TermStructure:
    def __init__(self, Maturity=None):
        self.Maturity = Maturity
        self.MaturityEpoch = None
        self.ModelLowerBound = None
        self.ModelUpperBound = None
        self.Market = None
        self.Error = None
    def serialize(self):
        return {
            'Maturity': self.Maturity
        }
    def deserialize(self, pRoot):
        self.Maturity = pRoot["Maturity"]
        self.MaturityEpoch = pRoot["MaturityEpoch"]
        self.ModelLowerBound = odeserialize(SuffixedNumber, pRoot["ModelLowerBound"])
        self.ModelUpperBound = odeserialize(SuffixedNumber, pRoot["ModelUpperBound"])
        self.Market = odeserialize(SuffixedNumber, pRoot["Market"])
        self.Error = odeserialize(SuffixedNumber, pRoot["Error"])
        return self

class GetModelImpliedVolatility_Results:
    def __init__(self, 
        UnderlyingTicker, 
        StrikeKind, 
        PriceKind
    ):
        self.UnderlyingTicker = UnderlyingTicker
        self.StrikeKind = StrikeKind
        self.PriceKind = PriceKind
        self.Score = None
        self.ScoreByExpiryTable = None
    def serialize(self):
        return {
            'UnderlyingTicker': self.UnderlyingTicker,
            'StrikeKind': self.StrikeKind.name.replace("_", " "),
            'PriceKind': self.PriceKind.name.replace("_", " ")
        }
    def deserialize(self, pRoot):
        self.UnderlyingTicker = pRoot['UnderlyingTicker']
        self.StrikeKind = pRoot['StrikeKind']
        self.PriceKind = pRoot['PriceKind']
        self.Score = odeserialize(SuffixedNumber, pRoot['Score']) 
        self.ScoreByExpiryTable = ldeserialize(GetModelImpliedVolatility_ScoreByExpiry, pRoot['ScoreByExpiryTable'])
        return self

class GetModelImpliedVolatility_ScoreByExpiry:
    def __init__(self):
        self.MaturityDate = None
        self.Score = None
        self.ErrorByStrikeTable = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.MaturityDate = pRoot['MaturityDate']
        self.Score = odeserialize(SuffixedNumber, pRoot['Score'])
        self.ErrorByStrikeTable = ldeserialize(GetModelImpliedVolatility_ScoreByStrike, pRoot['ErrorByStrikeTable'])
        return self
    
class GetModelImpliedVolatility_ScoreByStrike:
    def __init__(self):
        self.Strike = None
        self.Bid = None
        self.Ask = None
        self.Model = None
        self.ModelLower = None
        self.ModelUpper = None
        self.Error = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Strike = odeserialize(SuffixedNumber, pRoot['Strike'])
        self.Bid = odeserialize(SuffixedNumber, pRoot['Bid'])
        self.Ask = odeserialize(SuffixedNumber, pRoot['Ask'])
        self.Model = odeserialize(SuffixedNumber, pRoot['Model'])
        self.ModelLower = odeserialize(SuffixedNumber, pRoot['ModelLower'])
        self.ModelUpper = odeserialize(SuffixedNumber, pRoot['ModelUpper'])
        self.Error = odeserialize(SuffixedNumber, pRoot['Error'])
        return self
    
class GetVanillaCurveCalibration_Results:
    def __init__(self, 
        Ticker, 
        Maturity, 
        StrikeKind,
        PriceKind,
        Table
    ):
        self.Ticker = Ticker
        self.Maturity = Maturity
        self.PriceKind = PriceKind
        self.StrikeKind = StrikeKind
        self.Table = Table
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'MaturityDate': self.Maturity,
            'StrikeKind': self.StrikeKind.name.replace("_", " "),
            'PriceKind': self.PriceKind.name.replace("_", " "),
            'Table': lserialize(self.Table)
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Maturity = pRoot['Maturity']
        self.StrikeKind = pRoot['StrikeKind']
        self.PriceKind = pRoot['PriceKind']
        self.Table = ldeserialize(GetVanillaCurveCalibration_Table, pRoot['Table'])
        return self    

class GetVanillaCurveCalibration_Table:
    def __init__(self, Strike=None):
        self.Strike = Strike
        self.Error = None
        self.Market = None
        self.ModelLowerBound = None
        self.ModelUpperBound = None
    def serialize(self):
        return {
            'Strike': self.Strike
        }
    def deserialize(self, pRoot):
        self.Strike = pRoot['Strike']
        self.Market = odeserialize(SuffixedNumber, pRoot['Market'])
        self.ModelLowerBound = odeserialize(SuffixedNumber, pRoot['ModelLowerBound'])
        self.ModelUpperBound = odeserialize(SuffixedNumber, pRoot['ModelUpperBound'])
        self.Error = odeserialize(SuffixedNumber, pRoot['Error'])
        return self

class GetEquityFXImpliedVolatilityInterpolation_Results:
    def __init__(self, Ticker, SpaceKind, ValueKind):
        self.Ticker = Ticker
        self.SpaceKind = SpaceKind
        self.ValueKind = ValueKind
        self.Error = None
        self.ErrorByExpiry = None
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'SpaceKind': self.SpaceKind.name.replace("_", " "),
            'ValueKind': self.ValueKind.name.replace("_", " ")
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.SpaceKind = pRoot['SpaceKind']
        self.ValueKind = pRoot['ValueKind']
        self.Error = odeserialize(SuffixedNumber, pRoot['Error'])
        self.ErrorByExpiry = ldeserialize(GetEquityFXImpliedVolatilityInterpolation_ErrorByExpiry, pRoot['ErrorByExpiry'])
        return self

class GetEquityFXImpliedVolatilityInterpolation_ErrorByExpiry:
    def __init__(self):
        self.MaturityDate = None
        self.Error = None
        self.ErrorBySpace = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):    
        self.MaturityDate = pRoot['MaturityDate']
        self.Error = odeserialize(SuffixedNumber, pRoot['Error'])
        self.ErrorBySpace = ldeserialize(GetEquityFXImpliedVolatilityInterpolation_ErrorBySpace, pRoot['ErrorBySpace'])
        return self

class GetEquityFXImpliedVolatilityInterpolation_ErrorBySpace:
    def __init__(self):
        self.MarketBid = None
        self.MarketAsk = None
        self.Model = None
        self.Error = None
        self.Space = None
    def serialize(self):
        return {
            'MarketBid': oserialize(self.MarketBid),
            'MarketAsk': oserialize(self.MarketAsk),
            'Model': oserialize(self.Model),
            'Error': oserialize(self.Error),
            'Space': oserialize(self.Space)
        }
    def deserialize(self, pRoot):    
        self.MarketBid = odeserialize(SuffixedNumber, pRoot['MarketBid'])
        self.MarketAsk = odeserialize(SuffixedNumber, pRoot['MarketAsk'])
        self.Model = odeserialize(SuffixedNumber, pRoot['Model'])
        self.Error = odeserialize(SuffixedNumber, pRoot['Error'])
        self.Space = odeserialize(SuffixedNumber, pRoot['Space'])
        return self

class GetEquityFXImpliedVolatilityArbitrage_Results:
    def __init__(self, Ticker, SpaceKind, ValueKind, MaturityRequested, Space):
        self.Ticker = Ticker
        self.SpaceKind = SpaceKind
        self.ValueKind = ValueKind
        self.MaturityRequested = MaturityRequested
        self.Space = Space
        self.ArbitrageScore = None
        self.CalendarSpreadArbitrageScore = None
        self.ButterflySpreadArbitrageScore = None
        self.CallSpreadArbitrageScore = None
        self.ImpliedVolatilityValueMatrix = None
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'SpaceKind': self.SpaceKind.name.replace("_", " "),
            'ValueKind': self.ValueKind.name.replace("_", " "),
            'MaturityRequested': self.MaturityRequested,
            'Space': self.Space
        }
    def deserialize(self, pRoot):    
        self.Ticker = pRoot['Ticker']
        self.SpaceKind = pRoot['SpaceKind']
        self.ValueKind = pRoot['ValueKind']
        self.MaturityRequested = pRoot['MaturityRequested'] 
        self.Space = pRoot['Space']
        self.ArbitrageScore = odeserialize(SuffixedNumber, pRoot['ArbitrageScore']) 
        self.CalendarSpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['CalendarSpreadArbitrageScore']) 
        self.ButterflySpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['ButterflySpreadArbitrageScore']) 
        self.CallSpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['CallSpreadArbitrageScore']) 
        self.ImpliedVolatilityValueMatrix = odeserialize(GetEquityFXImpliedVolatilityArbitrage_ArbitrageMatrix, pRoot['Map']) 
        return self

class GetEquityFXImpliedVolatilityArbitrage_ArbitrageMatrix:
    def __init__(self):
        self.Rows = None
        self.Cols = None
        self.Data = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Rows = ldeserialize(GetEquityFXImpliedVolatilityArbitrage_Space, pRoot['Rows']) 
        self.Cols = ldeserialize(GetEquityFXImpliedVolatilityArbitrage_Time, pRoot['Cols'])
        self.Data = [[odeserialize(GetEquityFXImpliedVolatilityArbitrage_ArbitrageResult, item) for item in jtem] for jtem in pRoot['Data']]
        return self

class GetEquityFXImpliedVolatilityArbitrage_ArbitrageResult:
    def __init__(self):
        self.Value = None
        self.ArbitrageScore = None
        self.CalendarSpreadArbitrageScore = None
        self.ButterflySpreadArbitrageScore = None
        self.CallSpreadArbitrageScore = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Value = odeserialize(SuffixedNumber, pRoot['Value']) 
        self.ArbitrageScore = odeserialize(SuffixedNumber, pRoot['ArbitrageScore']) 
        self.CalendarSpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['CalendarSpreadArbitrageScore']) 
        self.ButterflySpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['ButterflySpreadArbitrageScore']) 
        self.CallSpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['CallSpreadArbitrageScore']) 
        return self

class GetEquityFXImpliedVolatilityArbitrage_Time:
    def __init__(self):
        self.Maturity = None
        self.ArbitrageScore = None
        self.CalendarSpreadArbitrageScore = None
        self.CallSpreadArbitrageScore = None
        self.ButterflySpreadArbitrageScore = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Maturity = pRoot['Maturity']
        self.ArbitrageScore = odeserialize(SuffixedNumber, pRoot['ArbitrageScore']) 
        self.CalendarSpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['CalendarSpreadArbitrageScore']) 
        self.ButterflySpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['ButterflySpreadArbitrageScore']) 
        self.CallSpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['CallSpreadArbitrageScore']) 
        return self

class GetEquityFXImpliedVolatilityArbitrage_Space:
    def __init__(self):
        self.Value = None
        self.ArbitrageScore = None
        self.ButterflySpreadArbitrageScore = None
        self.CalendarSpreadArbitrageScore = None
        self.CallSpreadArbitrageScore = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Value = odeserialize(SuffixedNumber, pRoot['Value']) 
        self.ArbitrageScore = odeserialize(SuffixedNumber, pRoot['ArbitrageScore']) 
        self.CalendarSpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['CalendarSpreadArbitrageScore']) 
        self.ButterflySpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['ButterflySpreadArbitrageScore']) 
        self.CallSpreadArbitrageScore = odeserialize(SuffixedNumber, pRoot['CallSpreadArbitrageScore']) 
        return self

class PricingResult:
    def __init__(self):
        self.Mean = None
        self.Lower = None
        self.Upper = None
        self.Stddev = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Mean = odeserialize(SuffixedNumber, pRoot['Mean'])
        self.Lower = odeserialize(SuffixedNumber, pRoot['Lower'])
        self.Upper = odeserialize(SuffixedNumber, pRoot['Upper'])
        self.Stddev = pRoot['Stddev']
        return self

class NameValueResult:
    def __init__(self):
        self.Name = None
        self.Value = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.Value = odeserialize(SuffixedNumber, pRoot['Value'])
        return self

class TickerValueResult:
    def __init__(self):
        self.Ticker = None
        self.Value = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Value = odeserialize(SuffixedNumber, pRoot['Value'])
        return self

class XGreek:
    def __init__(self):
        self.FirstTicker = None
        self.SecondTicker = None
        self.Value = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.FirstTicker = pRoot['FirstTicker']
        self.SecondTicker = pRoot['SecondTicker']
        self.Value = odeserialize(SuffixedNumber, pRoot['Value'])
        return self

class PricingResults:
    def __init__(self):
        self.All = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.All = ldeserialize(NameValueResult, pRoot)
        return self

class GetAPIToken_Results:
    def __init__(self, Username, Password):
        self.Username = Username
        self.Password = Password
        self.Company = None
        self.ExpirationDate = None
        self.APIToken = None
    def serialize(self):
        return {
            'Username': self.Username,
            'Password': self.Password
        }
    def deserialize(self, pRoot):
        self.Username = pRoot['Username']
        self.Company = pRoot['Company']
        self.ExpirationDate = pRoot['ExpirationDate']
        self.APIToken = pRoot['APIToken']
        return self

class GetSequence_Results:
    def __init__(self, Kind, LowerValue, UpperValue, Size=None, Step=None):
        self.Kind = Kind
        self.LowerValue = LowerValue
        self.UpperValue = UpperValue
        self.Size = Size
        self.Step = Step
        self.Values = None
    def serialize(self):
        return {
            'Kind': self.Kind.name.replace("_", " "),
            'LowerValue': self.LowerValue,
            'UpperValue': self.UpperValue,
            'Size': self.Size,
            'Step': self.Step
        }
    def deserialize(self, pRoot):
        self.Kind = pRoot['Kind']
        self.LowerValue = pRoot['LowerValue']
        self.UpperValue = pRoot['UpperValue']
        self.Size = pRoot['Size']
        self.Values = pRoot['Values']
        return self

class GetSchedule_Results:
    def __init__(self, StartDate, EndDate, DateShift, Calendar):
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.DateShift = DateShift
        self.Calendar = Calendar
        self.Dates = None
    def serialize(self):
        return {
            'StartDate': self.StartDate,
            'EndDate': self.EndDate,
            'DateShift': self.DateShift,
            'Calendar': self.Calendar.name.replace("_", " ")
        }
    def deserialize(self, pRoot):
        self.StartDate = pRoot['StartDate']
        self.EndDate = pRoot['EndDate']
        self.DateShift = pRoot['Shift']
        self.Calendar = pRoot['Calendar']
        self.Dates = pRoot['Dates']
        return self
    
class UpdatePassword_Results:
    def __init__(self, NewPassword, NewPasswordConfirmation):
        self.NewPassword = NewPassword
        self.NewPasswordConfirmation = NewPasswordConfirmation
    def serialize(self):
        return {
            'NewPassword': self.NewPassword,
            'NewPasswordConfirmation': self.NewPasswordConfirmation
        }
    def deserialize(self, pRoot):
        self.NewPassword = pRoot['NewPassword']
        self.NewPasswordConfirmation = pRoot['NewPasswordConfirmation']
        return self

class GetChangelog_Results:
    def __init__(self):
        self.Changelog = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Changelog = pRoot['Changelog']
        return self
    
class Log:
    def __init__(self):
        self.Time = None
        self.Level = None
        self.Message = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Time = pRoot['Time']
        self.Level = pRoot['Level']
        self.Message = pRoot['Message']
        return self

class Logger:
    def __init__(self):
        self.Logs = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Logs = ldeserialize(Log, pRoot)
        return self

class Model:
    def __init__(self,
        Name = ModelName.Black_Scholes_Model,
        Smiler = Smiler.Robust_SSVI,
        EnableVegaWeighted = True,
        EnableBidAskSpreadWeighted = True,
        CorrelationSampleSize = 20,
        CurvatureSampleSize = 20,
        CorrelationLaps = 3,
        CurveInterpolationSmoothingParameter = 50.0,
        YieldCurveCalibrationPrecision = 0.01,
        CorrelationCalibrationMethod = CorrelationCalibrationMethod.Historical,
        HistoricalCalibrationLookbackDays = 365,
        HistoricalCalibrationCenterReturns = True,
        HistoricalCalibrationUseEWMAEstimator = False,
        HistoricalCalibrationEWMADecayFactor = 94.0,
        BlackScholesFiniteDifferenceGridSize = 500,
        BlackScholesFiniteDifferenceConfidenceLevel = 99.99,
        BlackScholesCalibrationKind = BlackScholesCalibrationKind.Implied_Volatility,
        BlackScholesHistoricalVolatilityFrequency = DateShift(pShift='1d',pCalendar=Calendar.Dummy),
        BlackScholesHistoricalVolatilityDepth = 180,
        DupireLocalVolatilityGridScale = 10.0,
        DupireLocalVolatilityGridSize = 1000,
        DupireLocalVolatilityFloor = 0.0,
        DupireLocalVolatilityCap = 300.0,
        BlackScholesImpliedVolatilityPointForwardMoneyness = 100.0,
        BlackScholesImpliedVolatilityPointMaturity = DateShift(pShift='1y',pCalendar=Calendar.Dummy),
        HestonGridSizeExponent=12,
        HestonFitNearTheMoneyOptions=True,
        HestonMinimumIntegralDiscretizationStep=0.25,
        HestonObjectiveFunctionToleranceExponent=1,
        HestonParametersToleranceExponent=1,
        HestonGradientNormToleranceExponent=1,
        HestonMaximumFunctionEvaluation=100,
        HestonInitialVolatilitysGuess=20.0,
        HestonVarianceVolatilityFactorsGuess=1.00,
        HestonLongTermVolatilitysGuess=20.0,
        HestonMeanReversionFactorsGuess=10.0,
        HestonSpotVarianceCorrelationsGuess=-50.0,
        HestonDiscretizationScheme=HestonDiscretizationScheme.Quadratic_Exponential,
        GenOTCLocalVolatilityGridSize = 1000,
        GenOTCLocalVolatilityFloor = 0.0,
        GenOTCLocalVolatilityCap = 300.0
    ):
        self.Name = Name
        self.Smiler = Smiler
        self.EnableVegaWeighted = EnableVegaWeighted
        self.EnableBidAskSpreadWeighted = EnableBidAskSpreadWeighted
        self.CorrelationSampleSize = CorrelationSampleSize
        self.CurvatureSampleSize = CurvatureSampleSize
        self.CorrelationLaps = CorrelationLaps
        self.CurveInterpolationSmoothingParameter = CurveInterpolationSmoothingParameter
        self.YieldCurveCalibrationPrecision = YieldCurveCalibrationPrecision
        self.CorrelationCalibrationMethod = CorrelationCalibrationMethod
        self.HistoricalCalibrationLookbackDays = HistoricalCalibrationLookbackDays
        self.HistoricalCalibrationCenterReturns = HistoricalCalibrationCenterReturns
        self.HistoricalCalibrationUseEWMAEstimator = HistoricalCalibrationUseEWMAEstimator
        self.HistoricalCalibrationEWMADecayFactor = HistoricalCalibrationEWMADecayFactor
        self.DupireLocalVolatilityGridScale = DupireLocalVolatilityGridScale
        self.DupireLocalVolatilityGridSize = DupireLocalVolatilityGridSize
        self.DupireLocalVolatilityFloor = DupireLocalVolatilityFloor
        self.DupireLocalVolatilityCap = DupireLocalVolatilityCap
        self.BlackScholesFiniteDifferenceGridSize = BlackScholesFiniteDifferenceGridSize
        self.BlackScholesFiniteDifferenceConfidenceLevel = BlackScholesFiniteDifferenceConfidenceLevel
        self.BlackScholesCalibrationKind = BlackScholesCalibrationKind
        self.BlackScholesHistoricalVolatilityFrequency = BlackScholesHistoricalVolatilityFrequency
        self.BlackScholesHistoricalVolatilityDepth = BlackScholesHistoricalVolatilityDepth
        self.BlackScholesImpliedVolatilityPointForwardMoneyness = BlackScholesImpliedVolatilityPointForwardMoneyness
        self.BlackScholesImpliedVolatilityPointMaturity = BlackScholesImpliedVolatilityPointMaturity
        self.HestonGridSizeExponent = HestonGridSizeExponent
        self.HestonFitNearTheMoneyOptions = HestonFitNearTheMoneyOptions
        self.HestonMinimumIntegralDiscretizationStep = HestonMinimumIntegralDiscretizationStep
        self.HestonObjectiveFunctionToleranceExponent = HestonObjectiveFunctionToleranceExponent
        self.HestonParametersToleranceExponent = HestonParametersToleranceExponent
        self.HestonGradientNormToleranceExponent = HestonGradientNormToleranceExponent
        self.HestonMaximumFunctionEvaluation = HestonMaximumFunctionEvaluation
        self.HestonInitialVolatilitysGuess = HestonInitialVolatilitysGuess
        self.HestonVarianceVolatilityFactorsGuess = HestonVarianceVolatilityFactorsGuess
        self.HestonLongTermVolatilitysGuess = HestonLongTermVolatilitysGuess
        self.HestonMeanReversionFactorsGuess = HestonMeanReversionFactorsGuess
        self.HestonSpotVarianceCorrelationsGuess = HestonSpotVarianceCorrelationsGuess
        self.HestonDiscretizationScheme = HestonDiscretizationScheme
        self.GenOTCLocalVolatilityGridSize = GenOTCLocalVolatilityGridSize
        self.GenOTCLocalVolatilityFloor = GenOTCLocalVolatilityFloor
        self.GenOTCLocalVolatilityCap = GenOTCLocalVolatilityCap
    def serialize(self):
        return {
            'Name': self.Name.name.replace("_", " "),
            'Smiler': self.Smiler.name.replace("_", " "),
            'EnableVegaWeighted': self.EnableVegaWeighted,
            'EnableBidAskSpreadWeighted': self.EnableBidAskSpreadWeighted,
            'CorrelationSampleSize': self.CorrelationSampleSize,
            'CurvatureSampleSize': self.CurvatureSampleSize,
            'CorrelationLaps': self.CorrelationLaps,
            'CurveInterpolationSmoothingParameter': self.CurveInterpolationSmoothingParameter,
            'YieldCurveCalibrationPrecision': self.YieldCurveCalibrationPrecision,
            'DupireLocalVolatilityGridScale': self.DupireLocalVolatilityGridScale,
            'DupireLocalVolatilityGridSize': self.DupireLocalVolatilityGridSize,
            'DupireLocalVolatilityFloor': self.DupireLocalVolatilityFloor,
            'DupireLocalVolatilityCap': self.DupireLocalVolatilityCap,
            'BlackScholesFiniteDifferenceGridSize': self.BlackScholesFiniteDifferenceGridSize,
            'BlackScholesFiniteDifferenceConfidenceLevel': self.BlackScholesFiniteDifferenceConfidenceLevel,
            'BlackScholesCalibrationKind': self.BlackScholesCalibrationKind.name.replace("_", " "),
            'BlackScholesHistoricalVolatilityFrequency': oserialize(self.BlackScholesHistoricalVolatilityFrequency),
            'BlackScholesHistoricalVolatilityDepth': self.BlackScholesHistoricalVolatilityDepth,
            'BlackScholesImpliedVolatilityPointForwardMoneyness': self.BlackScholesImpliedVolatilityPointForwardMoneyness,
            'BlackScholesImpliedVolatilityPointMaturity': oserialize(self.BlackScholesImpliedVolatilityPointMaturity),
            'HestonGridSizeExponent': self.HestonGridSizeExponent,
            'HestonFitNearTheMoneyOptions': self.HestonFitNearTheMoneyOptions,
            'HestonMinimumIntegralDiscretizationStep': self.HestonMinimumIntegralDiscretizationStep,
            'HestonObjectiveFunctionToleranceExponent': self.HestonObjectiveFunctionToleranceExponent,
            'HestonParametersToleranceExponent': self.HestonParametersToleranceExponent,
            'HestonGradientNormToleranceExponent': self.HestonGradientNormToleranceExponent,
            'HestonMaximumFunctionEvaluation': self.HestonMaximumFunctionEvaluation,
            'HestonInitialVolatilitysGuess': self.HestonInitialVolatilitysGuess,
            'HestonVarianceVolatilityFactorsGuess': self.HestonVarianceVolatilityFactorsGuess,
            'HestonLongTermVolatilitysGuess': self.HestonLongTermVolatilitysGuess,
            'HestonMeanReversionFactorsGuess': self.HestonMeanReversionFactorsGuess,
            'HestonSpotVarianceCorrelationsGuess': self.HestonSpotVarianceCorrelationsGuess,
            'HestonDiscretizationScheme': self.HestonDiscretizationScheme.name.replace("_", " "),
            'GenOTCLocalVolatilityGridSize': self.GenOTCLocalVolatilityGridSize,
            'GenOTCLocalVolatilityFloor': self.GenOTCLocalVolatilityFloor,
            'GenOTCLocalVolatilityCap': self.GenOTCLocalVolatilityCap,
            'CorrelationCalibrationMethod': self.CorrelationCalibrationMethod.name.replace("_", " "),
            'HistoricalCalibrationLookbackDays': self.HistoricalCalibrationLookbackDays,
            'HistoricalCalibrationCenterReturns': self.HistoricalCalibrationCenterReturns,
            'HistoricalCalibrationUseEWMAEstimator': self.HistoricalCalibrationUseEWMAEstimator,
            'HistoricalCalibrationEWMADecayFactor': self.HistoricalCalibrationEWMADecayFactor
        }
    def deserialize(self, pRoot):
        if 'Name' in pRoot: self.Name = pRoot['Name']
        if 'EnableVegaWeighted' in pRoot: self.EnableVegaWeighted = pRoot['EnableVegaWeighted']
        if 'EnableBidAskSpreadWeighted' in pRoot: self.EnableBidAskSpreadWeighted = pRoot['EnableBidAskSpreadWeighted']
        if 'CorrelationSampleSize' in pRoot: self.CorrelationSampleSize = pRoot['CorrelationSampleSize']
        if 'CurvatureSampleSize' in pRoot: self.CurvatureSampleSize = pRoot['CurvatureSampleSize']
        if 'CorrelationLaps' in pRoot: self.CorrelationLaps = pRoot['CorrelationLaps']
        if 'CurveInterpolationSmoothingParameter' in pRoot: self.CurveInterpolationSmoothingParameter = pRoot['CurveInterpolationSmoothingParameter']
        if 'YieldCurveCalibrationPrecision' in pRoot: self.YieldCurveCalibrationPrecision = pRoot['YieldCurveCalibrationPrecision']
        if 'CorrelationCalibrationMethod' in pRoot: self.CorrelationCalibrationMethod = pRoot['CorrelationCalibrationMethod']
        if 'HistoricalCalibrationLookbackDays' in pRoot: self.HistoricalCalibrationLookbackDays = pRoot['HistoricalCalibrationLookbackDays']
        if 'HistoricalCalibrationCenterReturns' in pRoot: self.HistoricalCalibrationCenterReturns = pRoot['HistoricalCalibrationCenterReturns']
        if 'HistoricalCalibrationUseEWMAEstimator' in pRoot: self.HistoricalCalibrationUseEWMAEstimator = pRoot['HistoricalCalibrationUseEWMAEstimator']
        if 'HistoricalCalibrationEWMADecayFactor' in pRoot: self.HistoricalCalibrationEWMADecayFactor = pRoot['HistoricalCalibrationEWMADecayFactor']
        if 'DupireLocalVolatilityGridScale' in pRoot: self.DupireLocalVolatilityGridScale = pRoot['DupireLocalVolatilityGridScale']
        if 'BlackScholesFiniteDifferenceGridSize' in pRoot: self.BlackScholesFiniteDifferenceGridSize = pRoot['BlackScholesFiniteDifferenceGridSize']
        if 'BlackScholesFiniteDifferenceConfidenceLevel' in pRoot: self.BlackScholesFiniteDifferenceConfidenceLevel = pRoot['BlackScholesFiniteDifferenceConfidenceLevel']
        if 'BlackScholesCalibrationKind' in pRoot: self.BlackScholesCalibrationKind = pRoot['BlackScholesCalibrationKind']
        if 'BlackScholesHistoricalVolatilityFrequency' in pRoot: self.BlackScholesHistoricalVolatilityFrequency = odeserialize(DateShift, pRoot['BlackScholesHistoricalVolatilityFrequency']) 
        if 'BlackScholesHistoricalVolatilityDepth' in pRoot: self.BlackScholesHistoricalVolatilityDepth = pRoot['BlackScholesHistoricalVolatilityDepth']
        if 'BlackScholesImpliedVolatilityPointForwardMoneyness' in pRoot: self.BlackScholesImpliedVolatilityPointForwardMoneyness = pRoot['BlackScholesImpliedVolatilityPointForwardMoneyness']
        if 'BlackScholesImpliedVolatilityPointMaturity' in pRoot: self.BlackScholesImpliedVolatilityPointMaturity = odeserialize(DateShift, pRoot['BlackScholesImpliedVolatilityPointMaturity'])
        if 'HestonGridSizeExponent' in pRoot: self.HestonGridSizeExponent = pRoot['HestonGridSizeExponent']
        if 'HestonFitNearTheMoneyOptions' in pRoot: self.HestonFitNearTheMoneyOptions = pRoot['HestonFitNearTheMoneyOptions']
        if 'HestonMinimumIntegralDiscretizationStep' in pRoot: self.HestonMinimumIntegralDiscretizationStep = pRoot['HestonMinimumIntegralDiscretizationStep']
        if 'HestonObjectiveFunctionToleranceExponent' in pRoot: self.HestonObjectiveFunctionToleranceExponent = pRoot['HestonObjectiveFunctionToleranceExponent']
        if 'HestonParametersToleranceExponent' in pRoot: self.HestonParametersToleranceExponent = pRoot['HestonParametersToleranceExponent']
        if 'HestonGradientNormToleranceExponent' in pRoot: self.HestonGradientNormToleranceExponent = pRoot['HestonGradientNormToleranceExponent']
        if 'HestonMaximumFunctionEvaluation' in pRoot: self.HestonMaximumFunctionEvaluation = pRoot['HestonMaximumFunctionEvaluation']
        if 'HestonInitialVolatilitysGuess' in pRoot: self.HestonInitialVolatilitysGuess = pRoot['HestonInitialVolatilitysGuess']
        if 'HestonVarianceVolatilityFactorsGuess' in pRoot: self.HestonVarianceVolatilityFactorsGuess = pRoot['HestonVarianceVolatilityFactorsGuess']
        if 'HestonLongTermVolatilitysGuess' in pRoot: self.HestonLongTermVolatilitysGuess = pRoot['HestonLongTermVolatilitysGuess']
        if 'HestonMeanReversionFactorsGuess' in pRoot: self.HestonMeanReversionFactorsGuess = pRoot['HestonMeanReversionFactorsGuess']
        if 'HestonSpotVarianceCorrelationsGuess' in pRoot: self.HestonSpotVarianceCorrelationsGuess = pRoot['HestonSpotVarianceCorrelationsGuess']
        if 'HestonDiscretizationScheme' in pRoot: self.HestonDiscretizationScheme = pRoot['HestonDiscretizationScheme']
        if 'GenOTCLocalVolatilityGridSize' in pRoot: self.GenOTCLocalVolatilityGridSize = pRoot['GenOTCLocalVolatilityGridSize']
        if 'GenOTCLocalVolatilityFloor' in pRoot: self.GenOTCLocalVolatilityFloor = pRoot['GenOTCLocalVolatilityFloor']
        if 'GenOTCLocalVolatilityCap' in pRoot: self.GenOTCLocalVolatilityCap = pRoot['GenOTCLocalVolatilityCap']
        return self

class GetContractSummary_Underlying:
    def __init__(self):
        self.Ticker = None
        self.CompleteName = None
        self.QuoteCurrency = None
        self.AssetClass = None
        self.AssetKind = None
        self.IsQuanto = None
        self.IsInBasket = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.CompleteName = pRoot['CompleteName']
        self.AssetClass = pRoot['AssetClass']
        self.AssetKind = pRoot['AssetKind']
        self.IsQuanto = pRoot['IsQuanto']
        self.IsInBasket = pRoot['IsInBasket']
        return self

class GetContractSummary_Fixing:
    def __init__(self):
        self.Date = None
        self.QuoteCurrency = None
        self.Ticker = None
        self.Quote = None
        self.HasQuote = None
        self.IsPast = None
        self.Edit = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.QuoteCurrency = pRoot['QuoteCurrency']
        self.Ticker = pRoot['Ticker']
        self.Quote = odeserialize(SuffixedNumber, pRoot['Quote'])
        self.HasQuote = pRoot['HasQuote']
        self.IsPast = pRoot['IsPast']
        self.Edit = pRoot['Edit']
        return self

class GetContractSummary_Correlation:
    def __init__(self):
        self.Value = SuffixedNumber(0.0, '%')
        self.HasValue = False
    def serialize(self):
        return {
            'Value': oserialize(self.Value),
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Value = odeserialize(SuffixedNumber, pRoot['Value'])
        self.HasValue = pRoot['HasValue']
        return self

class GetContractSummary_CorrelationMatrix:
    def __init__(self):
        self.Rows = []
        self.Cols = []
        self.Data = [[]]
    def serialize(self):
        return {
            'Rows': self.Rows,
            'Cols': self.Cols,
            'Data': [[item.serialize() for item in jtem] for jtem in self.Data]
        }
    def deserialize(self, pRoot):
        self.Rows = pRoot['Rows']
        self.Cols = pRoot['Cols']
        self.Data = [[odeserialize(GetContractSummary_Correlation, item) for item in jtem] for jtem in pRoot['Data']]
        return self

class IEvent:
    def serialize(self):
        raise NotImplementedError
    def deserialize(self, _):
        raise NotImplementedError
    
class GetContractSummary_Payment:
    def __init__(self):
        self.Date = None
        self.Currency = None
        self.Value = None
        self.Kind = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Currency = pRoot['Currency']
        self.Date = pRoot['Date']
        self.Value = odeserialize(SuffixedNumber, pRoot['Value'])
        self.Kind = pRoot['Kind']
        return self
    
class GetContractSummary_Setting:
    def __init__(self):
        self.Date = None
        self.Name = None
        self.Value = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.Name = pRoot['Name']
        self.Value = pRoot['Value']
        return self
    
class PaymentEvent(IEvent):
    def __init__(self):
        self.Currency = ''
        self.Script = ''
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Currency': self.Currency,
            'Script': self.Script,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Currency = pRoot['Currency']
        self.Script = pRoot['Script']
        self.HasValue = pRoot['HasValue']
        return self
    
class PurchaseEvent(IEvent):
    def __init__(self):
        self.Quantity = 0
        self.Start = 0
        self.End = 0
    def serialize(self):
        return {
            'Quantity': self.Quantity,
            'Start': self.Start,
            'End': self.End
        }
    def deserialize(self, pRoot):
        self.Quantity = pRoot['Quantity']
        self.Start = pRoot['Start']
        self.End = pRoot['End']
        return self
    
class FixingEvent(IEvent):
    def __init__(self):
        self.Ticker = ''
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self
    
class SettingEvent(IEvent):
    def __init__(self):
        self.Name = ''
        self.Script = ''
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Name': self.Name,
            'Script': self.Script,
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.Script = pRoot['Script']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self
    
class ChoiceEvent(IEvent):
    def __init__(self):
        self.ChoiceOwnership = ''
        self.Starts = []
        self.Ends = []
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'ChoiceOwnership': self.ChoiceOwnership,
            'Starts': self.Starts,
            'Ends': self.Ends,
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.ChoiceOwnership = pRoot['ChoiceOwnership']
        self.Starts = pRoot['Starts']
        self.Ends = pRoot['Ends']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self
    
class BarrierEvent(IEvent):
    def __init__(self):
        self.Script = ''
        self.StartLeft = 0
        self.StartRight = 0
        self.EndLeft = 0
        self.EndRight = 0
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Script': self.Script,
            'StartLeft': self.StartLeft,
            'StartRight': self.StartRight,
            'EndLeft': self.EndLeft,
            'EndRight': self.EndRight,
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Script = pRoot['Script']
        self.StartLeft = pRoot['StartLeft']
        self.StartRight = pRoot['StartRight']
        self.EndLeft = pRoot['EndLeft']
        self.EndRight = pRoot['EndRight']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self

class EndEvent(IEvent):
    def serialize(self):
        return None
    def deserialize(self, _):
        return self
    
class Event:
    def __init__(self):
        self.EventKind = EventKind.Barrier
        self.Date = ''
        self.HasDate = False
        self.Attributes = None
    def serialize(self):
        return {
            'EventKind': self.EventKind.name.replace("_", " "),
            'Date': self.Date,
            'HasDate': self.HasDate,
            'Attributes': oserialize(self.Attributes)
        }
    def deserialize(self, pRoot):
        self.EventKind = pRoot['EventKind']
        self.Date = pRoot['Date']
        self.HasDate = pRoot['HasDate']
        self.Attributes.deserialize(pRoot['Attributes'])
        return self

class GetPortfolioSummary_Allocation:
    def __init__(self):
        self.Name = None
        self.Weight = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.Weight = odeserialize(SuffixedNumber, pRoot['Weight'])
        return self

class GetPortfolioSummary_MaturityDistribution:
    def __init__(self):
        self.Label = None
        self.Weight = None
    def serialize(self):
        return {
            'Label': self.Label,
            'Weight': oserialize(self.Weight)
        }
    def deserialize(self, pRoot):
        self.Label = pRoot['Label']
        self.Weight = odeserialize(SuffixedNumber, pRoot['Weight'])
        return self

class GetPortfolioSummary_Notification:
    def __init__(self):
        self.ContractId = None
        self.Date = None
        self.Type = None
        self.Time = None
    def serialize(self):
        return {}
    def deserialize(self, pRoot):
        self.ContractId = pRoot['ContractId']
        self.Date = pRoot['Date']
        self.Type = pRoot['Type']
        self.Time = pRoot['Time']
        return self

# Payoff.

class VanillaOption:
    def __init__(self, 
        PayoffType,
        UnderlyingTicker,
        Ratio,
        StrikePrice,
        MaturityDate,
        SettlementDate,
        PaymentCurrency
    ):
        self.PayoffType = PayoffType
        self.UnderlyingTicker = UnderlyingTicker
        self.Ratio = Ratio
        self.StrikePrice = StrikePrice
        self.MaturityDate = MaturityDate
        self.SettlementDate = SettlementDate
        self.PaymentCurrency = PaymentCurrency
    def serialize(self):
        return {
            'PayoffType': self.PayoffType.name.replace("_", " "),
            'UnderlyingTicker': self.UnderlyingTicker,
            'Ratio': self.Ratio,
            'StrikePrice': self.StrikePrice,
            'MaturityDate': self.MaturityDate,
            'SettlementDate': self.SettlementDate,
            'PaymentCurrency': self.PaymentCurrency
        }
    def deserialize(self, pRoot):    
        self.PayoffType = pRoot['PayoffType']
        self.UnderlyingTicker = pRoot['UnderlyingTicker']
        self.Ratio = pRoot['Ratio']
        self.StrikePrice = pRoot['StrikePrice']
        self.MaturityDate = pRoot['MaturityDate']
        self.SettlementDate = pRoot['SettlementDate']
        self.PaymentCurrency = pRoot['PaymentCurrency']
        return self
        
class Basket:
    def __init__(self, 
        BasketKind = BasketKind.Basket,
        BasketValueKind = BasketValueKind.Performance,
        PerformanceKind = PerformanceKind.Absolute,
        StrikeKind = StrikeKind.Asian,
        AsianOutKind = StrikeKind.Asian,
        Weight = [],
        ForwardStartDate='',
        AsianIn = []
    ):
        self.AsianOutKind = AsianOutKind
        self.BasketKind = BasketKind
        self.BasketValueKind = BasketValueKind
        self.ForwardStartDate = ForwardStartDate
        self.PerformanceKind = PerformanceKind
        self.StrikeKind = StrikeKind
        self.Weight = Weight
        self.AsianIn = AsianIn
    def serialize(self):
        return {
            'AsianOutKind': self.AsianOutKind.name.replace("_", " "),
            'BasketKind': self.BasketKind.name.replace("_", " "),
            'BasketValueKind': self.BasketValueKind.name.replace("_", " "),
            'ForwardStartDate': self.ForwardStartDate,
            'PerformanceKind': self.PerformanceKind.name.replace("_", " "),
            'StrikeKind': self.StrikeKind.name.replace("_", " "),
            'Weight': [item.serialize() for item in self.Weight],
            'AsianIn': self.AsianIn
        }
    def deserialize(self, pRoot):    
        self.AsianOutKind = pRoot['AsianOutKind']
        self.BasketKind = pRoot['BasketKind']
        self.BasketValueKind = pRoot['BasketValueKind']
        self.ForwardStartDate = pRoot['ForwardStartDate']
        self.PerformanceKind = pRoot['PerformanceKind']
        self.StrikeKind = pRoot['StrikeKind']
        self.Weight = ldeserialize(BasketItem, pRoot['Weight'])
        self.AsianIn = pRoot['AsianIn']
        return self
    
class VanillaOptional:
    def __init__(self,
        Notional=0.0,
        Quantity=0.0,
        PayReceiveKind=PayReceiveKind.Pay,
        Kind=VanillaPayoffKind.Call_Put,
        AsianOutDates = [],
        PaymentDate='',
        ObservationDate='',
        PaymentCurrency='',
        Payoff=None
    ):
        self.AsianOutDates = AsianOutDates
        self.Notional = Notional
        self.Quantity = Quantity
        self.PaymentDate = PaymentDate
        self.ObservationDate = ObservationDate
        self.PaymentCurrency = PaymentCurrency
        self.PayReceiveKind = PayReceiveKind
        self.Kind = Kind
        self.Payoff = Payoff
    def serialize(self):
        root = oserialize(self.Payoff)
        root['AsianOutDates'] = self.AsianOutDates
        root['Notional'] = self.Notional
        root['Quantity'] = self.Quantity
        root['Kind'] = self.Kind
        root['PaymentDate'] = self.PaymentDate
        root['ObservationDate'] = self.ObservationDate
        root['PaymentCurrency'] = self.PaymentCurrency
        root['PayReceiveKind'] = self.PayReceiveKind
        return root
    def deserialize(self, pRoot):
        # self.Payoff.deserialize(pRoot)
        self.AsianOutDates = pRoot['AsianOutDates']
        self.Notional = pRoot['Notional']
        self.Notional = pRoot['Notional']
        self.Quantity = pRoot['Quantity']
        self.Kind = pRoot['Kind']
        self.PaymentDate = pRoot['PaymentDate']
        self.ObservationDate = pRoot['ObservationDate']
        self.PaymentCurrency = pRoot['PaymentCurrency']
        self.Kind = pRoot['Kind']
        return self

class Vanilla(ICashFlow):
    def __init__(self, Basket=Basket(), Option=VanillaOptional()):
        self.Option = Option
        self.Basket = Basket
    def serialize(self):
        return {
            'Basket': oserialize(self.Basket),
            'Option': lserialize(self.Option)
        }
    def deserialize(self, pRoot):
        self.Basket = odeserialize(Basket, pRoot['Basket'])
        return self
    
class TargetAccrualRedemptionForward(ICashFlow):
    def __init__(self):
        pass
    def serialize(self):
        return {
            
        }
    def deserialize(self, pRoot):
        return self

class TargetRedemption(ICashFlow):
    def __init__(self, Vanilla=Vanilla(), Target=0.0):
        self.Vanilla = Vanilla
        self.Target = Target
    def serialize(self):
        return {
            'Vanilla': oserialize(self.Vanilla),
            'Target': self.Target
        }
    def deserialize(self, pRoot):
        self.Vanilla = odeserialize(Vanilla, pRoot['Vanilla'])
        self.Target = pRoot['Target']
        return self
        
class BasketItem:
    def __init__(self, Ticker = '', Weight = 0.0):
        self.Ticker = Ticker
        self.Weight = Weight
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'Weight': self.Weight
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Weight = pRoot['Weight']
        return self
        
class Point:
    def __init__(self, X = 0.0, Y = 0.0):
        self.X = X
        self.Y = Y
    def serialize(self):
        return {
            'X': self.X,
            'Y': self.Y
        }
    def deserialize(self, pRoot):
        self.X = pRoot['X']
        self.Y = pRoot['Y']
        return self

class Spot(ICashFlow):
    def __init__(self,
        Underlying = ''
    ):
        self.Underlying = Underlying
    def serialize(self):
        return {
            'Underlying': self.Underlying
        }
    def deserialize(self, pRoot):
        self.Underlying = pRoot['Underlying']
        return self

class Autocall(ICashFlow):
    def __init__(self,
        Basket = Basket(),
        Schedule = [],
        FinalObservationDate = '',
        FinalPaymentDate = '',
        FinalPaymentCurrency = '',
        FinalPaymentNotional = 0.0,
        CapitalProtectionBarrier = 0.0,
        BonusCouponWithMemory = False,
        BasketKind = BasketKind.Basket,
        PerformanceKind = PerformanceKind.Absolute,
        StrikeKind = StrikeKind.Asian,
        ForwardStartDate = ''
    ):
        self.Basket = Basket
        self.Schedule = Schedule
        self.FinalObservationDate = FinalObservationDate
        self.FinalPaymentDate = FinalPaymentDate
        self.FinalPaymentCurrency = FinalPaymentCurrency
        self.FinalPaymentNotional = FinalPaymentNotional
        self.CapitalProtectionBarrier = CapitalProtectionBarrier
        self.BonusCouponWithMemory = BonusCouponWithMemory
        self.BasketKind = BasketKind
        self.PerformanceKind = PerformanceKind
        self.StrikeKind = StrikeKind
        self.ForwardStartDate = ForwardStartDate
    def serialize(self):
        return {
            'BonusCouponWithMemory': self.BonusCouponWithMemory,
            'BasketKind': self.BasketKind.name.replace("_", " "),
            'PerformanceKind': self.PerformanceKind.name.replace("_", " "),
            'StrikeKind': self.StrikeKind.name.replace("_", " "),
            'ForwardStartDate': self.ForwardStartDate,
            'Basket': oserialize(self.Basket),
            'Schedule': lserialize(self.Schedule),
            'FinalObservationDate': self.FinalObservationDate,
            'FinalPaymentDate': self.FinalPaymentDate,
            'FinalPaymentCurrency': self.FinalPaymentCurrency,
            'FinalPaymentNotional': self.FinalPaymentNotional,
            'CapitalProtectionBarrier': self.CapitalProtectionBarrier
        }
    def deserialize(self, pRoot):
        self.BonusCouponWithMemory = pRoot['BonusCouponWithMemory']
        self.BasketKind = pRoot['BasketKind']
        self.PerformanceKind = pRoot['PerformanceKind']
        self.StrikeKind = pRoot['StrikeKind']
        self.ForwardStartDate = pRoot['ForwardStartDate'] 
        self.Basket = odeserialize(Basket, pRoot['Basket'])
        self.Schedule = ldeserialize(AutocallScheduleStatement, pRoot['Schedule'])
        self.FinalObservationDate = pRoot['FinalObservationDate']
        self.FinalPaymentDate = pRoot['FinalPaymentDate']
        self.FinalPaymentCurrency = pRoot['FinalPaymentCurrency']
        self.FinalPaymentNotional = pRoot['FinalPaymentNotional']
        self.CapitalProtectionBarrier = pRoot['CapitalProtectionBarrier']
        return self
    
class VarianceSwap(ICashFlow):
    def __init__(self,
        Basket = Basket(),
        Schedule = []
    ):
        self.Basket = Basket
        self.Schedule = Schedule
    def serialize(self):
        return {
            'Basket': oserialize(self.Basket),
            'Schedule': lserialize(self.Schedule)
        }
    def deserialize(self, pRoot):
        self.Basket = odeserialize(Basket, pRoot['Basket'])
        self.Schedule = ldeserialize(Schedule, pRoot['Schedule'])
        return self
    
class VanillaCustomPoint:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
    def serialize(self):
        return {
            'X': self.X,
            'Y': self.Y
        }
    def deserialize(self, pRoot):
        self.X = pRoot['X']
        self.Y = pRoot['Y']
        return self
    
class Schedule:
    def __init__(self, StartDate='', DateShift='', Calendar=Calendar.Dummy):
        self.StartDate = StartDate
        self.DateShift = DateShift
        self.Calendar = Calendar
        self.Dates = []
    def serialize(self):
        return {
            'StartDate': self.StartDate,
            'DateShift': self.DateShift,
            'Calendar': self.Calendar.name.replace("_", " "),
            'Dates': self.Dates
        }
    def deserialize(self, pRoot):
        self.StartDate = pRoot['StartDate']
        self.DateShift = pRoot['DateShift']
        self.Calendar = pRoot['Calendar']
        self.Dates = pRoot['Dates']
        return self
        
class AutocallScheduleStatement:
    def __init__(self,
        AsianOutDates = [],
        ObservationDate='',
        PaymentDate='',
        PaymentCurrency='',
        Notional=0.0,
        AutocallBarrier=0.0,
        PhoenixCoupon=0.0,
        CouponBarrier=0.0,
        BonusCoupon=0.0
    ):
        self.AsianOutDates = AsianOutDates
        self.ObservationDate = ObservationDate
        self.PaymentDate = PaymentDate
        self.PaymentCurrency = PaymentCurrency
        self.Notional = Notional
        self.AutocallBarrier = AutocallBarrier
        self.PhoenixCoupon = PhoenixCoupon
        self.CouponBarrier = CouponBarrier
        self.BonusCoupon = BonusCoupon
    def serialize(self):
        return {
            'AsianOutDates': self.AsianOutDates,
            'ObservationDate': self.ObservationDate,
            'PaymentDate': self.PaymentDate,
            'PaymentCurrency': self.PaymentCurrency,
            'Notional': self.Notional,
            'AutocallBarrier': self.AutocallBarrier,
            'PhoenixCoupon': self.PhoenixCoupon,
            'CouponBarrier': self.CouponBarrier,
            'BonusCoupon': self.BonusCoupon
        }
    def deserialize(self, pRoot):    
        self.AsianOutDates = pRoot['AsianOutDates']
        self.ObservationDate = pRoot['ObservationDate']
        self.PaymentDate = pRoot['PaymentDate']
        self.PaymentCurrency = pRoot['PaymentCurrency']
        self.Notional = pRoot['Notional']
        self.AutocallBarrier = pRoot['AutocallBarrier']
        self.PhoenixCoupon = pRoot['PhoenixCoupon']
        self.CouponBarrier = pRoot['CouponBarrier']
        self.BonusCoupon = pRoot['BonusCoupon']
        return self
    
class SwapScheduleStatement:
    def __init__(self,
        EndDate='',
        AsianOutDates=[],
        FixedRate=0.0,
        FloatingRate=0.0,
        Notional=0.0,
        PaymentCurrency='',
        PaymentDate='',
        StartDate='',
        WeightBasket=0.0,
        WeightFixedRate=0.0,
        WeightFloatingRate=0.0
    ):
        self.AsianOutDates = AsianOutDates
        self.EndDate = EndDate
        self.FixedRate = FixedRate
        self.FloatingRate = FloatingRate
        self.Notional = Notional
        self.PaymentCurrency = PaymentCurrency
        self.PaymentDate = PaymentDate
        self.StartDate = StartDate
        self.WeightBasket = WeightBasket
        self.WeightFixedRate = WeightFixedRate
        self.WeightFloatingRate = WeightFloatingRate
    def serialize(self):
        return {
            'AsianOutDates': self.AsianOutDates,
            'EndDate': self.EndDate,
            'FixedRate': self.FixedRate,
            'FloatingRate': self.FloatingRate,
            'Notional': self.Notional,
            'PaymentCurrency': self.PaymentCurrency,
            'PaymentDate': self.PaymentDate,
            'StartDate': self.StartDate,
            'WeightBasket': self.WeightBasket,
            'WeightFixedRate': self.WeightFixedRate,
            'WeightFloatingRate': self.WeightFloatingRate,
        }
    def deserialize(self, pRoot):    
        self.AsianOutDates = pRoot['AsianOutDates']
        self.EndDate = pRoot['EndDate']
        self.FixedRate = pRoot['FixedRate']
        self.FloatingRate = pRoot['FloatingRate']
        self.Notional = pRoot['Notional']
        self.PaymentCurrency = pRoot['PaymentCurrency']
        self.PaymentDate = pRoot['PaymentDate']
        self.StartDate = pRoot['StartDate']
        self.WeightBasket = pRoot['WeightBasket']
        self.WeightFixedRate = pRoot['WeightFixedRate']
        self.WeightFloatingRate = pRoot['WeightFloatingRate']
        return self
    
class CallVsCall(ICashFlow):
    def __init__(self,
        Basket=Basket(),
        ObservationDate='',
        PaymentCurrency='',
        PaymentDate='',
        PayoffKind=PayoffKind.Call_Type,
        Strike=0.0
    ):
        self.Basket = Basket
        self.ObservationDate = ObservationDate
        self.PaymentCurrency = PaymentCurrency
        self.PaymentDate = PaymentDate
        self.PayoffKind = PayoffKind
        self.Strike = Strike
    def serialize(self):
        return {
            'Basket': oserialize(self.Basket),
            'ObservationDate': self.ObservationDate,
            'PaymentCurrency': self.PaymentCurrency,
            'PaymentDate': self.PaymentDate,
            'PayoffKind': self.PayoffKind.name.replace("_", " "),
            'Strike': self.Strike
        }
    def deserialize(self, pRoot):    
        self.Basket = Basket().deserialize(pRoot['Basket'])
        self.ObservationDate = pRoot['ObservationDate']
        self.PaymentCurrency = pRoot['PaymentCurrency']
        self.PaymentDate = pRoot['PaymentDate']
        self.PayoffKind = pRoot['PayoffKind']
        self.Strike = pRoot['Strike']
        return self
    
class FXForward(ICashFlow):
    def __init__(self,
        DomesticCurrency='',
        ForeignCurrency='',
        ForwardExchangeRate=0.0,
        SettlementDate='',
        Notional=0.0
    ):
        self.DomesticCurrency = DomesticCurrency
        self.ForeignCurrency = ForeignCurrency
        self.ForwardExchangeRate = ForwardExchangeRate
        self.SettlementDate = SettlementDate
        self.Notional = Notional
    def serialize(self):
        return {
            'DomesticCurrency': self.DomesticCurrency,
            'ForeignCurrency': self.ForeignCurrency,
            'ForwardExchangeRate': self.ForwardExchangeRate,
            'SettlementDate': self.SettlementDate,
            'ForwardExchangeRate': self.ForwardExchangeRate,
            'Notional': self.Notional,
        }
    def deserialize(self, pRoot):    
        self.DomesticCurrency = pRoot['DomesticCurrency']
        self.ForeignCurrency = pRoot['ForeignCurrency']
        self.ForwardExchangeRate = pRoot['ForwardExchangeRate']
        self.SettlementDate = pRoot['SettlementDate']
        self.ForwardExchangeRate = pRoot['ForwardExchangeRate']
        self.Notional = pRoot['Notional']
        return self
    
class FXOption(ICashFlow):
    def __init__(self,
        Ratio = 0.0,
        ObservationDate = '',
        PaymentDate = '',
        Underlying = '',
        Strike = 0.0,
        PaymentCurrency = ''
    ):
        self.Ratio = Ratio
        self.ObservationDate = ObservationDate
        self.PaymentDate = PaymentDate
        self.Underlying = Underlying
        self.Strike = Strike
        self.PaymentCurrency = PaymentCurrency
    def serialize(self):
        return {
            'Ratio': self.Ratio,
            'ObservationDate': self.ObservationDate,
            'PaymentDate': self.PaymentDate,
            'Underlying': self.Underlying,
            'Strike': self.Strike,
            'PaymentCurrency': self.PaymentCurrency,
        }
    def deserialize(self, pRoot):    
        self.Ratio = pRoot['Ratio']
        self.ObservationDate = pRoot['ObservationDate']
        self.PaymentDate = pRoot['PaymentDate']
        self.Underlying = pRoot['Underlying']
        self.Strike = pRoot['Strike']
        self.PaymentCurrency = pRoot['PaymentCurrency']
        return self
    
class FXSwap(ICashFlow):
    def __init__(self,
        DomesticCurrency='',
        ForeignCurrency='',
        ForwardExchangeRate=0.0,
        SpotExchangeRate=0.0,
        SettlementDate='',
        SpotDate='',
        Notional=0.0
    ):
        self.DomesticCurrency = DomesticCurrency
        self.ForeignCurrency = ForeignCurrency
        self.ForwardExchangeRate = ForwardExchangeRate
        self.SpotExchangeRate = SpotExchangeRate
        self.SettlementDate = SettlementDate
        self.SpotDate = SpotDate
        self.Notional = Notional
    def serialize(self):
        return {
            'DomesticCurrency': self.DomesticCurrency,
            'ForeignCurrency': self.ForeignCurrency,
            'ForwardExchangeRate': self.ForwardExchangeRate,
            'SpotExchangeRate': self.SpotExchangeRate,
            'SettlementDate': self.SettlementDate,
            'SpotDate': self.SpotDate,
            'Notional': self.Notional
        }
    def deserialize(self, pRoot):    
        self.DomesticCurrency = pRoot['DomesticCurrency']
        self.ForeignCurrency = pRoot['ForeignCurrency']
        self.ForwardExchangeRate = pRoot['ForwardExchangeRate']
        self.SpotExchangeRate = pRoot['SpotExchangeRate']
        self.SettlementDate = pRoot['SettlementDate']
        self.SpotDate = pRoot['SpotDate']
        self.Notional = pRoot['Notional']
        return self
    
class Swap(ICashFlow):
    def __init__(self,
        BasketPayer=Basket(),
        BasketReceiver=Basket(),
        SchedulePayer=[],
        ScheduleReceiver=[]
    ):
        self.BasketPayer = BasketPayer
        self.BasketReceiver = BasketReceiver
        self.SchedulePayer = SchedulePayer
        self.ScheduleReceiver = ScheduleReceiver
    def serialize(self):
        return {
            'BasketPayer': self.BasketPayer.serialize(),
            'BasketReceiver': self.BasketReceiver.serialize(),
            'SchedulePayer': [item.serialize() for item in self.SchedulePayer],
            'ScheduleReceiver': [item.serialize() for item in self.ScheduleReceiver]
        }
    def deserialize(self, pRoot):    
        self.BasketPayer = Basket().deserialize(pRoot['BasketPayer'])
        self.BasketReceiver = Basket().deserialize(pRoot['BasketReceiver']) 
        self.SchedulePayer = ldeserialize(SwapScheduleStatement, pRoot['SchedulePayer'])
        self.ScheduleReceiver = ldeserialize(SwapScheduleStatement, pRoot['ScheduleReceiver'])
        return self
    
class IPayoff:
    def serialize(self):
        raise NotImplementedError
    def deserialize(self, _):
        raise NotImplementedError
    
class CallPut(IPayoff):
    def __init__(self, PayoffKind=PayoffKind.Call_Type, Strike=0.0):
        self.Strike = Strike
        self.PayoffKind = PayoffKind
    def serialize(self):
        return {
            'Strike': self.Strike,
            'PayoffKind': self.PayoffKind.name.replace("_", " ")
        }
    def deserialize(self, pRoot):    
        self.Strike = pRoot['Strike']
        self.PayoffKind = pRoot['PayoffKind']
        return self
    
class CallPutSpread(IPayoff):
    def __init__(self,
        PayoffKind=PayoffKind.Call_Type,
        Cap=0.0,
        Floor=0.0,
        Constant=0.0,
        Scale=0.0,
        Strike=0.0
    ):
        self.PayoffKind = PayoffKind
        self.Cap = Cap
        self.Floor = Floor
        self.Constant = Constant
        self.Scale = Scale
        self.Strike = Strike
    def serialize(self):
        return {
            'PayoffKind': self.PayoffKind.name.replace("_", " "),
            'Cap': self.Cap,
            'Floor': self.Floor,
            'Constant': self.Constant,
            'Scale': self.Scale,
            'Strike': self.Strike
        }
    def deserialize(self, pRoot):    
        self.PayoffKind = pRoot['PayoffKind']
        self.Cap = pRoot['Cap']
        self.Floor = pRoot['Floor']
        self.Constant = pRoot['Constant']
        self.Scale = pRoot['Scale']
        self.Strike = pRoot['Strike']
        return self
    
class CapitalProtection(IPayoff):
    def __init__(self,
        CapitalProtection=0.0
    ):
        self.CapitalProtection = CapitalProtection
    def serialize(self):
        return {
            'CapitalProtection': self.CapitalProtection
        }
    def deserialize(self, pRoot):    
        self.CapitalProtection = pRoot['CapitalProtection']
        return self
    
class VanillaCustom(IPayoff):
    def __init__(self, Payoff=[]):
        self.Payoff = Payoff
    def serialize(self):
        return {
            'Payoff': [item.serialize() for item in self.Payoff]
        }
    def deserialize(self, pRoot):    
        self.Payoff = ldeserialize(VanillaCustomPoint, pRoot['Payoff'])
        return self
    
class Forward(IPayoff):
    def __init__(self, PayoffKind=PayoffKind.Call_Type, Strike=0.0):
        self.PayoffKind = PayoffKind
        self.Strike = Strike
    def serialize(self):
        return {
            'Strike': self.Strike,
            'PayoffKind': self.PayoffKind.name.replace("_", " ")
        }
    def deserialize(self, pRoot):    
        self.Strike = pRoot['Strike']
        self.PayoffKind = pRoot['PayoffKind']
        return self