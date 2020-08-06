from app.Calculator import square
from app.Calculator.Division import division
from app.Statistics import populationmean


def variance(num):
    try:
        pop_mean = populationmean(num)
        num_values = len(num)
        x = 0
        for i in num:
            x = x + square(i-pop_mean)
        return division(x, num_values)
    except ZeroDivisionError:
        print("Error: Can't Divide by 0")
    except ValueError:
        print ("Error: Check your data inputs")