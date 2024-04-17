# read in the log file
f = File.open("price_log.txt", "r")

# create a hash to store the prices
prices = []

# read in the file line by line
f.each_line do |line|
    if line.include?("lambdaLog")
        second_part = line.split("sum_of_basket_products:")[1]
        sum_of_basket_products, third_part = second_part.split(", gift_basket_mid_price: ")
        gift_basket_mid_price = third_part.split(", basket_ratio: ")[0].to_i
        sum_of_basket_products = sum_of_basket_products.to_i
        # puts "sum_of_basket_products: #{sum_of_basket_products}, gift_basket_mid_price: #{gift_basket_mid_price}"
        prices << [sum_of_basket_products, gift_basket_mid_price]
    end
end

prices.each_with_index do |p, index|
    next if index < 10
    sum, price = p
    lookback = 2
    average = prices[index-lookback..index].compact.map { |p| p[0] }.inject(:+) / (lookback + 1).to_f
    puts "sum: #{sum}, price: #{price}, average: #{average}, ratio: #{price / average.to_f}"
end
