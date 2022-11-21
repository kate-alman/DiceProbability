import pandas as pd


class DiceProbability:
    def __init__(self):
        self._data = []
        self._min_face = 1
        self._max_face = 6

    def __call__(self, quantity, *args, **kwargs):
        verified_quantity = self.check_integer(quantity)
        min_sum = self._min_face * verified_quantity
        max_sum = self._max_face * verified_quantity
        return self.get_frequency(quantity, min_sum, max_sum)

    def get_frequency(self, quantity, min_sum, max_sum):
        throws = [1] * 6
        for dice in range(2, quantity + 1):
            next_throws = [0] * (len(throws) + 5)
            for shift in range(self._max_face):
                for i in range(len(throws)):
                    next_throws[i + shift] += throws[i]
            throws = next_throws
        return self.get_probability(dict(zip([*range(min_sum, max_sum + 1)], throws)), min_sum)

    def get_probability(self, data_frame, start):
        probability_table = pd.DataFrame(data_frame, index=[0])
        probability_table = probability_table.T
        probability_table = probability_table.rename(columns={0: 'Frequency'})
        probability_table.insert(0, 'Sum of dice', range(start, start + len(probability_table)))
        sum_rate = probability_table['Frequency'].sum()
        drop_chance = []
        for i in probability_table['Frequency']:
            drop_chance.append(round(i / sum_rate * 100, 2))
        probability_table['Drop Chance %'] = drop_chance
        return probability_table

    def check_integer(self, num):
        if not isinstance(num, int) or num < 1:
            num = self.check_integer(int(input('The number you enter must be a positive integer, please try again: ')))
        return num


dp = DiceProbability()
print(dp(int(input('Enter the number of cubes here: '))))

