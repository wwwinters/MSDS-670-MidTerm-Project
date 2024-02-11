#!/usr/bin/env python
###############################################################################
#
# Title: World Population Matplotlib Analysis
#
# Author: Wiley Winters (wwinters@regis.edu)
#
# Propose: To study if birth and death rates have a major affect on population
#          growth.
#
# Class: MSDS 670 -- Data Visualization
#
# Date: Febrary 11, 2024
#
###############################################################################

#
# Import reqired packages and functions
#
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

#
# Pandas has not been playing nice with this project
# Adding options to display numbers in float format
# and supress warnings on copy on write functions,
# 
pd.options.display.float_format = '{:.0f}'.format
pd.options.mode.copy_on_write = True
#
# Make plots pretty
#
plt.style.use('ggplot')

#
# Define path names
#
homeDir = '/home/wiley/regis/dataScience/msds670'
data = homeDir+'/MidTermProject/MSDS-670-MidTerm-Project/data/worldPopulationData.csv'
images = homeDir+'/MidTermProject/MSDS-670-MidTerm-Project/images/'

#
# Load dataset into a DataFrame and rename columns
#
# Do not like the column names supplied by Data Bank.  Using shorter column names
# to avoid confusion
columns = ['country','cntry_code','series','series_code','1960','1965','1970',
           '1975','1980','1985','1990','1995','2000','2005','2010','2015','2020',
           '2022','2023','2024']
world_df = pd.read_csv(data, skiprows=1, names=columns,
                       na_values='..')

#
# Do some basic data cleaning to remove unused columns
#
world_df.drop(['cntry_code','series','series_code'], inplace=True, axis=1)

###############################################################################
#
# The format of this dataset is different from what I am used to working with.
# First four columns are the country name, country code, series name, and series code.
# Rest of the columns contain the population data from 1960 to 2024.
# Series will have to be extracted from the DataFrame line-by-line
#

#
# Create a list of countries contained in the DataFrame that will be part of this
# analysis.  The list is in order of the largest GDP to the smallest.
#
countries = ['United States','China','Germany','Japan','India','United Kingdom',
             'France','Italy','Brazil','Canada']

###############################################################################
#
# Define Functions
#

#
# Function to extract a series from the DataFrame based
# on country name.
#
def formatSeries(country):
    """
    formatSeries accepts a country name and returns a series of values
    Accepts: country name
    Returns: series of values
    """
    cntry = world_df[world_df['country'] == country]
    cntry.drop('country', inplace=True, axis=1)
    return cntry

#
# Function to scale population by millions.
#
def scalePopulation(population):
    """
    scalePopulation accepts a population number and returns its
    value in millions
    Accepts: population
    Returns: scaled population
	"""
    scaled = population.apply(lambda x: x/1000000)
    return scaled

#
# Function to plot birth and death rates for each country
#
def plotBirthDeath(country):
    """
    plotBirthDeath creates a plot of the country's birth and
    death rates.  The plot is saved in an image file.
    Accepts: country name
    Returns: nothing
    """
    cntry = formatSeries(country)
    birth = cntry.iloc[0]
    death = cntry.iloc[1]
    plt.figure(figsize=(10,6))
    title = 'Birth and Death Rates per 1000 ('+country+')'
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Rate/1000')
    plt.plot(birth, color='darkorange', label='Births', marker='o')
    plt.plot(death, color='blue', label='Deaths', marker='o')
    plt.legend()
    plt.plot()
    if country == 'United States':
        fileName = images+'usBirthDeathRate.png'
    elif country == 'United Kingdom':
        fileName = images+'ukBirthDeathRate.png'
    else:
        fileName = images+country+'BirthDeathRate.png'
    plt.savefig(fileName, format='png')

#
# Function to plot the over 65 and population totals
#
def plotOver65(country):
    """
    plotOver65 plots the over 65 and total population totals.
    The plot is saved in an image file
    Accepts: country name
    Returns: nothing
    """
    cntry = formatSeries(country)
    over65 = cntry.iloc[2]
    total = cntry.iloc[4]
    # Scale populations to make graph easier to read
    over65_scaled = scalePopulation(over65)
    total_scaled = scalePopulation(total)
    plt.figure(figsize=(10,6))
    title = 'Total Population and Over 65 ('+country+')'
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Population in Millions')
    plt.plot(over65_scaled, color='black', label='Over 65', marker='o')
    plt.plot(total_scaled, color='blue', label='Total', marker='o')
    plt.legend()
    plt.plot()
    if country == 'United States':
        fileName = images+'usTotalandOver65.png'
    elif country == 'United Kingdom':
        fileName = images+'ukTotalandOver65.png'
    else:
        fileName = images+country+'TotalandOver65.png'
    plt.savefig(fileName, format='png')

#
# Function to plot growth
#
def plotGrowth(country):
    """
    plotGrowth plots the change in growth in percent and saves it
    as an image file.
    Accepts: country name
    Returns: nothing
    """
    cntry = formatSeries(country)
    growth = cntry.iloc[3]
    plt.figure(figsize=(10,6))
    title = 'Growth in Percent ('+country+')'
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Percent of Growth')
    plt.plot(growth, color='black', label='Over 65', marker='o')
    plt.legend()
    plt.plot()
    if country == 'United States':
        fileName = images+'usGrowthPercent.png'
    elif country == 'United Kingdom':
        fileName = images+'ukGrowthPercent.png'
    else:
        fileName = images+country+'GrowthPercent.png'
    plt.savefig(fileName, format='png')

#
# Function to extract the different series from the
# DataFrame
#
def getIndividual(country):
    """
    getIndividual extracts the different series from the DataFrame
    Accepts: country DataFrame
    Returns the series: birth, death, over65, and total
    """
    cntry = formatSeries(country)
    birth = cntry.iloc[0]
    death = cntry.iloc[1]
    over65 = cntry.iloc[2]
    growth = cntry.iloc[3]
    total = cntry.iloc[4]
    return birth, death, over65, growth, total

###############################################################################
#
# Crate individual plots
#

#
# Plot birth and death rates
#
for country in countries:
    plotBirthDeath(country)

#
# Plot over 65 and total population
#
for country in countries:
    plotOver65(country)
    
#
# Plot population growth
#
for country in countries:
    plotGrowth(country)

###############################################################################
#
# Create summary plots
#

#
# Extract and create series to plot
#
us_birth, us_death, us_over65, us_growth, us_total = getIndividual('United States')
us_over65_scaled = scalePopulation(us_over65)
us_total_scaled = scalePopulation(us_total)
cn_birth, cn_death, cn_over65, cn_growth, cn_total = getIndividual('China')
cn_over65_scaled = scalePopulation(cn_over65)
cn_total_scaled = scalePopulation(cn_total)
de_birth, de_death, de_over65, de_growth, de_total = getIndividual('Germany')
de_over65_scaled = scalePopulation(de_over65)
de_total_scaled = scalePopulation(de_total)
jp_birth, jp_death, jp_over65, jp_growth, jp_total = getIndividual('Japan')
jp_over65_scaled = scalePopulation(jp_over65)
jp_total_scaled = scalePopulation(jp_total)
in_birth, in_death, in_over65, in_growth, in_total = getIndividual('India')
in_over65_scaled = scalePopulation(in_over65)
in_total_scaled = scalePopulation(in_total)
uk_birth, uk_death, uk_over65, uk_growth, uk_total = getIndividual('United Kingdom')
uk_over65_scaled = scalePopulation(uk_over65)
uk_total_scaled = scalePopulation(uk_total)
fr_birth, fr_death, fr_over65, fr_growth, fr_total = getIndividual('France')
fr_over65_scaled = scalePopulation(fr_over65)
fr_total_scaled = scalePopulation(fr_total)
it_birth, it_death, it_over65, it_growth, it_total = getIndividual('Italy')
it_over65_scaled = scalePopulation(it_over65)
it_total_scaled = scalePopulation(it_total)
br_birth, br_death, br_over65, br_growth, br_total = getIndividual('Brazil')
br_over65_scaled = scalePopulation(br_over65)
br_total_scaled = scalePopulation(br_total)
ca_birth, ca_death, ca_over65, ca_growth, ca_total = getIndividual('Canada')
ca_over65_scaled = scalePopulation(ca_over65)
ca_total_scaled = scalePopulation(ca_total)

#
# Plot birth rates for all countries
#
plt.figure(figsize=(10,6))
plt.title('Birth Rates per 1000 (Top Ten Economies)')
plt.xlabel('Year')
plt.ylabel('Rate/1000')
plt.plot(us_birth, color='blue', label='United States', marker='o')
plt.plot(cn_birth, color='red', label='China', marker='o')
plt.plot(de_birth, color='gold', label='Germany', marker='o')
plt.plot(jp_birth, color='purple', label='Japan', marker='o')
plt.plot(in_birth, color='yellow', label='India', marker='o')
plt.plot(uk_birth, color='black', label='United Kingdom', marker='o')
plt.plot(fr_birth, color='orange', label='France', marker='o')
plt.plot(it_birth, color='chartreuse', label='Italy', marker='o')
plt.plot(br_birth, color='olive', label='Brazil', marker='o')
plt.plot(ca_birth, color='salmon', label='Canada', marker='o')
plt.legend()
plt.plot()
fileName = images+'sumBirthRates.png'
plt.savefig(fileName, format='png')

#
# Plot death rates for all countries
#
plt.figure(figsize=(10,6))
plt.title('Death Rates per 1000 (Top Ten Economies)')
plt.xlabel('Year')
plt.ylabel('Rate/1000')
plt.plot(us_death, color='blue', label='United States', marker='o')
plt.plot(cn_death, color='red', label='China', marker='o')
plt.plot(de_death, color='gold', label='Germany', marker='o')
plt.plot(jp_death, color='purple', label='Japan', marker='o')
plt.plot(in_death, color='yellow', label='India', marker='o')
plt.plot(uk_death, color='black', label='United Kingdom', marker='o')
plt.plot(fr_death, color='orange', label='France', marker='o')
plt.plot(it_death, color='chartreuse', label='Italy', marker='o')
plt.plot(br_death, color='olive', label='Brazil', marker='o')
plt.plot(ca_death, color='salmon', label='Canada', marker='o')
plt.legend()
plt.plot()
fileName = images+'sumDeathRate.png'
plt.savefig(fileName, format='png')

#
# Plot over 65 population for all countries
#
plt.figure(figsize=(10,6))
plt.title('Population over 65 (Top Ten Economies)')
plt.xlabel('Year')
plt.ylabel('Population in Millions')
plt.plot(us_over65, color='blue', label='United States', marker='o')
plt.plot(cn_over65, color='red', label='China', marker='o')
plt.plot(de_over65, color='gold', label='Germany', marker='o')
plt.plot(jp_over65, color='purple', label='Japan', marker='o')
plt.plot(in_over65, color='yellow', label='India', marker='o')
plt.plot(uk_over65, color='black', label='United Kingdom', marker='o')
plt.plot(fr_over65, color='orange', label='France', marker='o')
plt.plot(it_over65, color='chartreuse', label='Italy', marker='o')
plt.plot(br_over65, color='olive', label='Brazil', marker='o')
plt.plot(ca_over65, color='salmon', label='Canada', marker='o')
plt.legend()
plt.plot()
fileName = images+'sumOver65.png'
plt.savefig(fileName, format='png')

#
# Plot growth percentage for all countries
#
plt.figure(figsize=(10,6))
plt.title('Growth in Percent (Top Ten Economies)')
plt.xlabel('Year')
plt.ylabel('Percent of Growth')
plt.plot(us_growth, color='blue', label='United States', marker='o')
plt.plot(cn_growth, color='red', label='China', marker='o')
plt.plot(de_growth, color='gold', label='Germany', marker='o')
plt.plot(jp_growth, color='purple', label='Japan', marker='o')
plt.plot(in_growth, color='yellow', label='India', marker='o')
plt.plot(uk_growth, color='black', label='United Kingdom', marker='o')
plt.plot(fr_growth, color='orange', label='France', marker='o')
plt.plot(it_growth, color='chartreuse', label='Italy', marker='o')
plt.plot(br_growth, color='olive', label='Brazil', marker='o')
plt.plot(ca_growth, color='salmon', label='Canada', marker='o')
plt.legend()
plt.plot()
fileName = images+'sumGrowthPercent.png'
plt.savefig(fileName, format='png')

#
# Plot total population for all countries
#
plt.figure(figsize=(10,6))
plt.title('Total Population (Top Ten Economies)')
plt.xlabel('Year')
plt.ylabel('Population in Millions')
plt.plot(us_total_scaled, color='blue', label='United States', marker='o')
plt.plot(cn_total_scaled, color='red', label='China', marker='o')
plt.plot(de_total_scaled, color='gold', label='Germany', marker='o')
plt.plot(jp_total_scaled, color='purple', label='Japan', marker='o')
plt.plot(in_total_scaled, color='yellow', label='India', marker='o')
plt.plot(uk_total_scaled, color='black', label='United Kingdom', marker='o')
plt.plot(fr_total_scaled, color='orange', label='France', marker='o')
plt.plot(it_total_scaled, color='chartreuse', label='Italy', marker='o')
plt.plot(br_total_scaled, color='olive', label='Brazil', marker='o')
plt.plot(ca_total_scaled, color='salmon', label='Canada', marker='o')
plt.legend()
plt.plot()
fileName = images+'sumTotalPopulation.png'
plt.savefig(fileName, format='png')

#
# End
#