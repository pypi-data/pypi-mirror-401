###################################################################################
# Copyright © 2025 Matthieu Charrier. All rights reserved. ########################
# This file is the exclusive intellectual property of Matthieu Charrier. ##########
# No reproduction, modification, distribution, or use is permitted without ########
# prior written authorization. A separate licensing agreement may grant ###########
# Cegaware limited rights of use. Absent such agreement, no rights are granted. ###
###################################################################################

# std.
from enum import auto
from strenum import StrEnum

class BumpKind(StrEnum):
    Multiplicative = auto()
    Additive = auto()
    Assignment = auto()
    Hybrid = auto()

class LadderKind(StrEnum):
    Contract = auto()
    Market = auto()

class BumpUnit(StrEnum):
    Percentage = auto()
    Basis_Point = auto()
    None_ = auto()

class ResultKind(StrEnum):
    Absolute = auto()
    Absolute_Difference = auto()
    Ratio = auto()
    Return = auto()

class ObservableKind(StrEnum):
    Basket_Strategy = auto()
    Current_Realized_Volatility = auto()
    Dollar_Cost_Average_Strategy = auto()
    Running_Realized_Volatility = auto()

class YieldCurveKind(StrEnum):
    Discount_Factor = auto()
    Forward_Rate = auto()
    FRA_Rate = auto()
    Zero_Rate = auto()

class SequenceKind(StrEnum):
    Arange = auto()
    Constant = auto()
    Linspace = auto()

class BoundaryCondition(StrEnum):
    Dirichlet = auto()
    Neumann = auto()

class GreekDirection(StrEnum):
    Left = auto()
    Center = auto()
    Right = auto()

class PricingMethod(StrEnum):
    Auto = auto()
    Automatic_Adjoint_Differentiation = auto()
    Finite_Difference = auto()
    Monte_Carlo = auto()
    Static_Replication = auto()

class LSMBasis(StrEnum):
    Canonical_Basis = auto()
    First_Kind_Tchebychev = auto()
    Hermite = auto()
    Laguerre = auto()
    Legendre = auto()
    Second_Kind_Tchebychev = auto()

class BarrierSmoothingType(StrEnum):
    None_ = auto()
    Lower_Call_Spread = auto()
    Symmetric_Call_Spread = auto()
    Upper_Call_Spread = auto()
    Sigmoid = auto()
    Hyperbolic_Tangent = auto()
    Smooth_Step = auto()
    Normal_Cumulative_Distribution = auto()

class Basis(StrEnum):
    Act_365 = auto()

class HestonDiscretizationScheme(StrEnum):
    Quadratic_Exponential = auto()
    Implicit_Variance_Integrated = auto()

class BlackScholesCalibrationKind(StrEnum):
    Implied_Volatility = auto()
    Historical_Volatility = auto()
    Specific_Volatility = auto()

class ModelName(StrEnum):
    Black_Scholes_Model = auto()
    Black_Scholes_Term_Structure_Model = auto()
    Heston_Stochastic_Volatility_Model = auto()
    Dupire_Local_Volatility_Model = auto()
    GenOTC_Local_Volatility_Model = auto()

class BusinessDayConvention(StrEnum):
    Following = auto()
    Modified_Following = auto()
    Modified_Preceding = auto()
    Preceding = auto()

class Smiler(StrEnum):
    Robust_SSVI = auto()
    SVI_Free_Wings = auto()
    SVI = auto()
    Vanna_Volga = auto()
    Convex_Monotone_Cubic_Spline = auto()
    Dummy = auto()

class ContractKind(StrEnum):
    Autocall = auto()
    Bonus_Certificate = auto()
    Capital_Protected_Note = auto()
    Console = auto()
    Custom_Payoff = auto()
    Discount_Certificate = auto()
    Outperformance_Certificate = auto()
    Participation_Note = auto()
    Reverse_Convertible = auto()
    Twin_Win_Certificate = auto()
    Vanilla_Option = auto()
    Vanilla_Strategy = auto()

class QuotationTerm(StrEnum):
    Close = auto()
    Live = auto()

class DataSourceKind(StrEnum):
    Cegaware_File = auto()
    Cegaware_Database = auto()
    Yahoo_Finance = auto()

class CorrelationCalibrationMethod(StrEnum):
    Historical = auto()
    User_Data = auto()

class AssetClass(StrEnum):
    Share = auto()
    Fund = auto()
    Index = auto()
    Exchange_Rate = auto()
    Zero_Coupon_Bond = auto()
    Deposit_Rate = auto()
    Swap_Rate = auto()

class AssetKind(StrEnum):
    Equity = auto()
    Foreign_Exchange = auto()
    Interest_Rate = auto()

class LogLevel(StrEnum):
    Info = auto()
    Warning = auto()
    Err = auto()
    Exception = auto()
    Success = auto()
    Failure = auto()

class EventKind(StrEnum):
    Barrier = auto()
    Choice = auto()
    Fixing = auto()
    Nothing = auto()
    Payment = auto()
    Purchase = auto()
    Receipt = auto()
    Sale = auto()
    Setting = auto()

class StrikeKind(StrEnum):
    Asian = auto()
    Lookback_Min = auto()
    Lookback_Max = auto()

class BarrierKind(StrEnum):
    Knock_Out = auto()
    Knock_In = auto()

class Calendar(StrEnum):
    Dummy = auto()
    Euronext_Paris_Stock_Exchange = auto()
    London_Stock_Exchange = auto()
    TARGET = auto()

class ObservationKind(StrEnum):
    File = auto()
    Spot = auto()

class InitialGuessMethod(StrEnum):
    Legacy = auto()
    Stefanica_Radoicic = auto()

class BasketKind(StrEnum):
    Basket = auto()
    Best_Of = auto()
    Rainbow = auto()
    Worst_Of = auto()

class PerformanceKind(StrEnum):
    Absolute = auto()
    Difference = auto()
    Log_Return = auto()
    Ratio = auto()
    Return = auto()

class BarrierType(StrEnum):
    Down = auto()
    Up = auto()

class PayoffKind(StrEnum):
    Call_Type = auto()
    Put_Type = auto()

class BasketValueKind(StrEnum):
    Performance = auto()
    Dispersion = auto()

class SpaceKind(StrEnum):
    Forward_Moneyness = auto()
    Moneyness = auto()
    Strike = auto()

class PriceKind(StrEnum):
    Call_Price = auto()
    Put_Price = auto()
    Volatility = auto()

class VanillaPayoffKind(StrEnum):
    Call_Put = auto()
    Call_Put_Spread = auto()
    Capital_Protection = auto()
    Custom = auto()
    Forward = auto()

class PayReceiveKind(StrEnum):
    Pay = auto()
    Receive = auto()