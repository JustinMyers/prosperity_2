ratio = 1.0 / 5000.0

minimum_bid = 900
maximum_bid = 1000

max_gain = 0
max_gain_bids = []

(minimum_bid..maximum_bid).each do |bid_one|
    (bid_one..maximum_bid).each do |bid_two|
        x_one = bid_one - minimum_bid
        profit_one = maximum_bid - bid_one
        height_one = x_one * ratio
        percent_of_trades_one = height_one * x_one * 0.5
        gain_one = profit_one * percent_of_trades_one

        x_two = bid_two - minimum_bid
        profit_two = maximum_bid - bid_two
        height_two = x_two * ratio
        percent_of_trades_two = height_two * x_two * 0.5
        gain_two = profit_two * percent_of_trades_two
        gain_two -= percent_of_trades_one * profit_two

        if (gain_one + gain_two) > max_gain
            max_gain = gain_one + gain_two
            max_gain_bids = [bid_one, bid_two]
        end
    end
end

pp max_gain
pp max_gain_bids