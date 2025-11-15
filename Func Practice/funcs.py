import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st 

# --- FUNCTION TO ADD TWO NUMBERS --- #
def add_me(x, y):
    z = x + y
    return z
z = add_me(5, 5)

print(z)

# --- FUNCTION TO ADD n NUMBERS --- #
def add_all(*args):
    total = 0
    for i in args:
        total += i
    return total
total = add_all(1, 2, 3, 4, 5)

print(total)

# --- FUNCTION TO ADD NUMBERS FROM USER INPUT --- #
def add_inputs(in1, in2):
    tot = in1 + in2
    return tot

in1 = int(input('Please enter a number: '))
in2 = int(input('Please enter a number: '))

tot = add_inputs(in1, in2)
print(tot)

# --- FUNCTION TO ADD NUMBERS THEN SEND THAT NUMBER TO ANOTHER FUNCTION --- #
def mult_me(a, b):
    c = a * b
    return c

c = mult_me(5, 10)
print(c)

def div_me(c, d):
    e = c / d
    return e

e = div_me(c, 2)
print(e)

# --- FUNCTION TO READ IN AN EXCEL OR CSV FILE --- #

# --- FUNCTION TO GET DATA FROM AN API --- #