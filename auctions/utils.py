def get_listing_price(listing):
    #current price by default is equal to the starting_bid
    price = listing.starting_bid

    #if there are any bids on the listing, current price is equal to the higher bid
    bids = listing.bids.order_by('-amount')
    if bids:
        price = listing.bids.order_by('-amount')[0].amount

    return price