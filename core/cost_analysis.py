from database.database import FixedRates, OSCharges


def calculateProfit(
    basic_rate: float = 0.0,
    os_charges: OSCharges = None,
    material_cost: float = 0.0,
    fixed_rates=None,
) -> tuple:
    """
    Returns Cost of Production, Total Cost, NET MARGIN of a article.

    """

    EXPENSES_OVERHEADS = 0
    SELL_DISTR_ROYALTY = 0
    SALES_RETURN = 0

    for rate in fixed_rates:
        if rate.rate_type.upper() == "OH":
            EXPENSES_OVERHEADS += rate.value
        elif rate.rate_type.upper() == "OC":
            SELL_DISTR_ROYALTY += rate.value / 100
        elif rate.rate_type.upper() == "SR":
            SALES_RETURN += rate.value / 100

    # Cost of Production including overheads and other expenses
    cost_of_upper_prod = round(
        os_charges.stitch_rate + os_charges.print_rate + material_cost, 2
    )
    cost_of_prod = cost_of_upper_prod + EXPENSES_OVERHEADS

    # Total Cost: Selling & Distribution, Royalty, Sales Return added
    total_cost = ((basic_rate * SELL_DISTR_ROYALTY) + cost_of_prod) * (1 + SALES_RETURN)

    # Net margin
    if basic_rate != 0:
        net_margin = (basic_rate - total_cost) / basic_rate
        net_margin_percent = round(net_margin * 100, 2)
    else:
        net_margin = 0
        net_margin_percent = 0

    return (cost_of_prod, total_cost, net_margin_percent)
