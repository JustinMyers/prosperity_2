exchange_rates = {
    'pizza' => {
        'pizza' => 1,
        'wasabi' => 0.48,
        'snowball' => 1.52,
        'shells' => 0.71
    },
    'wasabi' => {
        'pizza' => 2.05,
        'wasabi' => 1,
        'snowball' => 3.26,
        'shells' => 1.56
    },
    'snowball' => {
        'pizza' => 0.64,
        'wasabi' => 0.3,
        'snowball' => 1,
        'shells' => 0.46
    },
    'shells' => {
        'pizza' => 1.41,
        'wasabi' => 0.61,
        'snowball' => 2.08,
        'shells' => 1
    }
}

shells = 2000000.0

products = ['pizza', 'wasabi', 'snowball', 'shells']

results = {}

[1,2,3, 4].map { |size|
    products.combination(size).to_a
}.flatten(1).each do |products|
    products.repeated_permutation(products.length).to_a.each do |permutation|
        permutation = permutation.unshift('shells').push('shells')
        exchange_rate = permutation.each_cons(2).map { |a, b|
            exchange_rates[a][b]
        }.inject(:*)
        results[permutation] = shells * exchange_rate
    end
end

pp results.count

pp results.keys.sort_by { |k| results[k] }.reverse.first