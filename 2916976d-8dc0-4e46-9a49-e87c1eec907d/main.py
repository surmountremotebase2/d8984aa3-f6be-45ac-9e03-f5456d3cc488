from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, InstitutionalOwnership, SocialSentiment

class TradingStrategy(Strategy):
    def __init__(self):
        # Hypothetically selected companies known for strong female leadership or gender diversity
        self.tickers = ["TICKER1", "TICKER2", "TICKER3"]
        self.data_list = [SocialSentiment(i) for i in self.tickers]

    @property
    def interval(self):
        # Daily data to assess longer-term trends
        return "1day"

    @property
    def assets(self):
        # List of assets to trade
        return self.tickers

    @property
    def data(self):
        # Data requirements for the strategy
        return self.data_list

    def run(self, data):
        # Initialize an empty allocation dictionary
        allocation_dict = {}
        
        # Scenario: Allocating more to companies with positive social sentiment as a proxy to popularity and possibly good governance
        # Note: In a real scenario, more specific data towards gender diversity metrics would be preferable
        for ticker in self.tickers:
            sentiment_data = data.get(("social_sentiment", ticker), [])
            if sentiment_data:
                latest_sentiment_score = sentiment_data[-1].get("twitterSentiment", 0)
                # Hypothetical criterion: Higher allocation for sentiment score > 0.5
                allocation = 0.33 if latest_sentiment_score > 0.5 else 0.1
            else:
                # In case no sentiment data is available, go with a minimal investment
                allocation = 0.1
            
            allocation_dict[ticker] = allocation
            
        # Make sure the total allocation doesn't exceed 1
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            allocation_dict = {k: v / total_allocation for k, v in allocation_dict.items()}
            
        return TargetAllocation(allocation_dict)