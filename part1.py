"""
Part 1: Data Processing in Pandas

=== Instructions ===

There are 22 questions in this part.
For each part you will implement a function (q1, q2, etc.)
Each function will take as input a data frame
or a list of data frames and return the answer
to the given question.

To run your code, you can run `python3 part1.py`.
This will run all the questions that you have implemented so far.
It will also save the answers to part1-answers.txt.

=== Dataset ===

In this part, we will use a dataset of world university rankings
called the "QS University Rankings".

The ranking data was taken 2019--2021 from the following website:
https://www.topuniversities.com/university-rankings/world-university-rankings/2021

=== Grading notes ===

- Once you have completed this part, make sure that
  your code runs, that part1-answers.txt is being re-generated
  every time the code is run, and that the answers look
  correct to you.

- Be careful about output types. For example if the question asks
  for a list of DataFrames, don't return a numpy array or a single
  DataFrame. When in doubt, ask on Piazza!

- Make sure that you remove any NotImplementedError exceptions;
  you won't get credit for any part that raises this exception
  (but you will still get credit for future parts that do not raise it
  if they don't depend on the previous parts).

- Make sure that you fill in answers for the parts
  marked "ANSWER ___ BELOW" and that you don't modify
  the lines above and below the answer space.

- Q6 has a few unit tests to help you check your work.
  Make sure that you removed the `@pytest.mark.skip` decorators
  and that all tests pass (show up in green, no red text!)
  when you run `pytest part3.py`.

- For plots: There are no specific requirements on which
  plotting methods you use; if not specified, use whichever
  plot you think might be most appropriate for the data
  at hand.
  Please ensure your plots are labeled and human-readable.
  For example, call .legend() on the plot before saving it!

===== Questions 1-6: Getting Started =====

To begin, let's load the Pandas library.
"""

import pandas as pd

"""
1. Load the dataset into Pandas

Our first step is to load the data into a Pandas DataFrame.
We will also change the column names
to lowercase and reorder to get only the columns we are interested in.

Implement the rest of the function load_input()
by filling in the parts marked TODO below.

Return as your answer to q1 the number of dataframes loaded.
(This part is implemented for you.)
"""

NEW_COLUMNS = ['rank', 'university', 'region', 'academic reputation', 'employer reputation', 'faculty student', 'citations per faculty', 'overall score']

def load_input():
    """
    Input: None
    Return: a list of 3 dataframes, one for each year.
    """

    # Load the input files and return them as a list of 3 dataframes.
    df_2019 = pd.read_csv('data/2019.csv', encoding='latin-1')
    df_2020 = pd.read_csv('data/2020.csv', encoding='latin-1')
    df_2021 = pd.read_csv('data/2021.csv', encoding='latin-1')

    # Standardizing the column names
    df_2019.columns = df_2019.columns.str.lower()
    df_2020.columns = df_2019.columns.str.lower()
    df_2021.columns = df_2019.columns.str.lower()

    # Restructuring the column indexes
    # Fill out this part. You can use column access to get only the
    # columns we are interested in using the NEW_COLUMNS variable above.
    # Make sure you return the columns in the new order.
    df_2019 = df_2019[NEW_COLUMNS]
    df_2020 = df_2020[NEW_COLUMNS]
    df_2021 = df_2021[NEW_COLUMNS]

    return [df_2019, df_2020, df_2021]

def q1(dfs):
    # As the "answer" to this part, let's just return the number of dataframes.
    # Check that your answer shows up in part1-answers.txt.
    return len(dfs)

"""
2. Input validation

Let's do some basic sanity checks on the data for Q1.

Check that all three data frames have the same shape,
and the correct number of rows and columns in the correct order.

As your answer to q2, return True if all validation checks pass,
and False otherwise.
"""

def q2(dfs):
    """
    Input: Assume the input is provided by load_input()

    Return: True if all validation checks pass, False otherwise.

    Make sure you return a Boolean!
    From this part onward, we will not provide the return
    statement for you.
    You can check that the "answers" to each part look
    correct by inspecting the file part1-answers.txt.
    """
    # Check:
    # - that all three dataframes have the same shape
    # - the number of rows
    # - the number of columns
    # - the columns are listed in the correct order
    expected_shape = (100, len(NEW_COLUMNS))
    same_shape = all(df.shape == dfs[0].shape for df in dfs)
    correct_rows = all(df.shape[0] == expected_shape[0] for df in dfs)
    correct_cols = all(df.shape[1] == expected_shape[1] for df in dfs)
    correct_order = all(list(df.columns) == NEW_COLUMNS for df in dfs)
    return len(dfs) == 3 and same_shape and correct_rows and correct_cols and correct_order

"""
===== Interlude: Checking your output so far =====

Run your code with `python3 part1.py` and open up the file
output/part1-answers.txt to see if the output looks correct so far!

You should check your answers in this file after each part.

You are welcome to also print out stuff to the console
in each question if you find it helpful.
"""

ANSWER_FILE = "output/part1-answers.txt"

def interlude():
    print("Answers so far:")
    with open(f"{ANSWER_FILE}") as fh:
        print(fh.read())

"""
===== End of interlude =====

3a. Input validation, continued

Now write a validate another property: that the set of university names
in each year is the same.
As in part 2, return a Boolean value.
(True if they are the same, and False otherwise)

Once you implement and run your code,
remember to check the output in part1-answers.txt.
(True if the checks pass, and False otherwise)
"""

def q3(dfs):
    # Check:
    # - that the set of university names in each year is the same
    # Return:
    # - True if they are the same, and False otherwise.
    name_sets = [set(df["university"]) for df in dfs]
    return all(names == name_sets[0] for names in name_sets)

"""
3b (commentary).
Did the checks pass or fail?
Comment below and explain why.

=== ANSWER Q3b BELOW ===
The check fails. Each file is a top 100 list, and the top 100 changes a bit
from year to year: schools near the cutoff drop out and new ones move in.
Comparing 2019 and 2021, six names only show up in one of the two years:
Purdue, Ohio State, KTH, Eindhoven, Hong Kong PolyU, and Sungkyunkwan.
So the data isn't broken, my assumption that the set stays fixed was just wrong.
(Some of the mismatch could also be from the same school being spelled
differently in different years, which is worth watching for when joining.)

=== END OF Q3b ANSWER ===
"""

"""
4. Random sampling

Now that we have the input data validated, let's get a feel for
the dataset we are working with by taking a random sample of 5 rows
at a time.

Implement q4() below to sample 5 points from each year's data.

As your answer to this part, return the *university name*
of the 5 samples *for 2021 only* as a list.
(That is: ["University 1", "University 2", "University 3", "University 4", "University 5"])

Code design: You can use a for for loop to iterate over the dataframes.
If df is a DataFrame, df.sample(5) returns a random sample of 5 rows.

Hint:
    to get the university name:
    try .iloc on the sample, then ["university"].
"""

def q4(dfs):
    # Sample 5 rows from each dataframe and print them out
    samples = []
    for df in dfs:
        sample = df.sample(5)
        print(sample)
        samples.append(sample)

    # Answer as a list of 5 university names (2021 only)
    sample_2021 = samples[2]
    return [sample_2021.iloc[i]["university"] for i in range(len(sample_2021))]

"""
Once you have implemented this part,
you can run a few times to see different samples.

4b (commentary).
Based on the data, write down at least 2 strengths
and 3 weaknesses of this dataset.
This is subjective - you may interpret this however you like!
If you were to use this dataset for a project, what would *you* consider to be
some advantages and drawbacks?

=== ANSWER Q4b BELOW ===
Strengths:
1. It's clean and easy to work with: same columns every year, scores on a
   0-100 scale, and no missing values, so there's almost no cleaning to do.
2. It breaks the overall score into its parts (academic reputation, employer
   reputation, citations, etc.), so you can see why a school ranks where it
   does, not just its final rank.

Weaknesses:
1. It's only the top 100, so it says nothing about most universities and
   the set of schools changes from year to year (see Q3).
2. The reputation columns come from surveys, so they're subjective and
   probably favor schools that are already famous. Rankings like this can
   reinforce themselves.
3. There are quality problems: the 2021 file is almost a copy of 2020, ties
   share a rank (two schools are both "11"), and the 2019 region column
   has typos/inconsistencies ("Switzerand", and "Scotland" listed apart
   from "UK"). The overall score is also rescaled so the top school always
   gets 100, which makes year to year comparisons of raw scores unreliable.
=== END OF Q4b ANSWER ===
"""

"""
5. Data cleaning

Let's see where we stand in terms of null values.
We can do this in two different ways.

a. Use .info() to see the number of non-null values in each column
displayed in the console.

b. Write a version using .count() to calculate the number of
non-null values in each column.

In both 5a and 5b: return as your answer
*for the 2021 data only*
as a list of the number of non-null values in each column.

Example: if there are 5 non-null values in the first column, 3 in the second, 4 in the third, and so on, you would return
    [5, 3, 4, ...]
"""

def q5a(dfs):
    dfs[2].info()
    # .info() only prints, so this list is copied from its output
    # (the "Non-Null Count" column).
    return [100, 100, 100, 100, 100, 100, 100, 100]

def q5b(dfs):
    return dfs[2].count().tolist()

"""
5c.
One other thing:
Also fill this in with how many non-null values are expected (for the 2021 data).
This should be a list for each column as before.
We will use this in the unit tests below.
"""

def q5c():
    # Every column should be fully populated: 100 universities in each year.
    num_non_null = [100] * len(NEW_COLUMNS)
    return num_non_null

"""
===== Interlude again: Unit tests =====

Unit tests

Now that we have completed a few parts,
let's talk about unit tests.
We won't be using them for the entire assignment
(in fact we won't be using them after this),
but they can be a good way to ensure your work is correct
without having to manually inspect the output.

We need to import pytest first.
"""

import pytest

"""
The following are a few unit tests for Q1-5.

To run the unit tests,
first, remove (or comment out) the `@pytest.mark.skip` decorator
from each unit test (function beginning with `test_`).
Then, run `pytest part1.py` in the terminal.
"""

def test_q1():
    dfs = load_input()
    assert len(dfs) == 3
    assert all([isinstance(df, pd.DataFrame) for df in dfs])

def test_q2():
    dfs = load_input()
    assert q2(dfs)

@pytest.mark.xfail
def test_q3():
    dfs = load_input()
    assert q3(dfs)

def test_q4():
    dfs = load_input()
    samples = q4(dfs)
    assert len(samples) == 5

def test_q5():
    dfs = load_input()
    num_non_null = q5c()
    assert len(num_non_null) > 0
    assert q5a(dfs) == num_non_null
    assert q5b(dfs) == num_non_null

"""
6a. Are there any tests which fail?

=== ANSWER Q6a BELOW ===
Yes, test_q3 fails. The other four pass.
=== END OF Q6a ANSWER ===

6b. For each test that fails, is it because your code
is wrong or because the test is wrong?

=== ANSWER Q6b BELOW ===
The test is wrong, not the code. q3 correctly reports that the university
names differ between years. The test assumes they should always be the same,
and for a top 100 list that isn't true. So I marked it with xfail.
=== END OF Q6b ANSWER ===

IMPORTANT: for any failing tests, if you think you have
not made any mistakes, mark it with
@pytest.mark.xfail
above the test to indicate that the test is expected to fail.
Run pytest part1.py again to see the new output.

6c. Return the number of tests that failed, even after your
code was fixed as the answer to this part.
(As an integer)
Please include expected failures (@pytest.mark.xfail).
(If you have no failing or xfail tests, return 0.)
"""

def q6c():
    # Only test_q3 fails (marked xfail).
    return 1

"""
===== End of interlude =====

===== Questions 7-10: Data Processing =====

7. Adding columns

Notice that there is no 'year' column in any of the dataframe. As your first task, append an appropriate 'year' column in each dataframe.

Append a column 'year' in each dataframe. It must correspond to the year for which the data is represented.

As your answer to this part, return the number of columns in each dataframe after the addition.
"""

YEARS = [2019, 2020, 2021]

def q7(dfs):
    for df, year in zip(dfs, YEARS):
        df["year"] = year
    return [len(df.columns) for df in dfs]

"""
8a.
Next, find the count of universities in each region that made it to the Top 100 each year. Print all of them.

As your answer, return the count for "USA" in 2021.
"""

def q8a(dfs):
    region_counts = [df["region"].value_counts() for df in dfs]
    for year, counts in zip(YEARS, region_counts):
        print(f"Universities in the top 100 by region, {year}:")
        print(counts)
    return region_counts[2].get("USA", 0)

"""
8b.
Do you notice some trend? Comment on what you observe and why might that be consistent throughout the years.

=== ANSWER Q8b BELOW ===
The USA has by far the most schools every year (30 in 2019, 29 in 2020 and
2021), then the UK (18-19), then China (11 every year), then Australia
(6-7). The order barely changes from year to year, and most countries only
gain or lose one school.
That makes sense because the things being measured change slowly. Reputation
is built over decades, and research output depends on funding and faculty,
which don't change much in a year. Richer English-speaking countries also
have an edge on reputation surveys and international citations, so the same
countries stay on top.

=== END OF Q8b ANSWER ===
"""

"""
9.
From the data of 2021, find the average score of all attributes for all universities.

As your answer, return the list of averages (for all attributes)
in the order they appear in the dataframe:
academic reputation, employer reputation, faculty student, citations per faculty, overall score.

The list should contain 5 elements.
"""

ATTRIBUTES = ['academic reputation', 'employer reputation', 'faculty student', 'citations per faculty', 'overall score']

def q9(dfs):
    return dfs[2][ATTRIBUTES].mean().tolist()

"""
10.
From the same data of 2021, now find the average of *each* region for **all** attributes **excluding** 'rank' and 'year'.

In the function q10_helper, store the results in a variable named **avg_2021**
and return it.

Then in q10, print the first 5 rows of the avg_2021 dataframe.
"""

def region_averages(df):
    """Average of every score attribute (no rank/year) per region."""
    return df.groupby("region")[ATTRIBUTES].mean()

def q10_helper(dfs):
    avg_2021 = region_averages(dfs[2])
    return avg_2021

def q10(avg_2021):
    """
    Input: the avg_2021 dataframe
    Print: the first 5 rows of the dataframe

    As your answer, simply return the number of rows printed.
    (That is, return the integer 5)
    """
    print(avg_2021.head(5))
    return len(avg_2021.head(5))

"""
===== Questions 11-14: Exploring the avg_2021 dataframe =====

11.
Sort the avg_2021 dataframe from the previous question based on overall score in a descending fashion (top to bottom).

As your answer to this part, return the first row of the sorted dataframe.
"""

def q11(avg_2021):
    sorted_avg = avg_2021.sort_values("overall score", ascending=False)
    print(sorted_avg)
    return sorted_avg.iloc[0]

"""
12a.
What do you observe from the table above? Which country tops the ranking?

What is one country that went down in the rankings
between 2019 and 2021?

You will need to load the data from 2019 to get the answer to this part.
You may choose to do this
by writing another function like q10_helper and running q11,
or you may just do it separately
(e.g., in a Python shell) and return the name of the country/region
that you found went down in the rankings.

Errata: please note that the 2021 dataset we provided is flawed
(it is almost identical to the 2020 data).
This is why the question now asks for the difference between 2019 and 2021.

For the answer to this part return the name of the country/region that tops the ranking
and the name of one country/region that went down in the rankings.
"""

def q12a(avg_2021):
    # Rank regions by average overall score (1 = best) in 2019 and 2021.
    avg_2019 = region_averages(load_input()[0])
    rank_2019 = avg_2019["overall score"].rank(ascending=False)
    rank_2021 = avg_2021["overall score"].rank(ascending=False)

    top_region = rank_2021.idxmin()
    # Positive change = moved to a worse (higher-numbered) position.
    rank_change = (rank_2021 - rank_2019).dropna()
    dropped_region = rank_change.idxmax()
    return (top_region, dropped_region)

"""
12b.
Comment on why the country above is at the top of the list.
(Note: This is an open-ended question.)

=== ANSWER Q12b BELOW ===
Singapore is at the top because it only has two schools in the top 100,
NUS and NTU, and both are ranked around #11. Since this is an average per
region, a small country with two elite schools beats a country like the USA,
whose average gets pulled down by the many schools it has ranked in the
60-100 range. So it's partly a real result (Singapore has invested heavily
in those two universities and they do well on reputation and international
measures), but it's also a side effect of averaging over very different
sample sizes.

=== END OF Q12b ANSWER ===
"""

"""
13a.
Represent all the attributes in the avg_2021 dataframe using a box and whisker plot.

Store your plot in output/part1-13a.png.

As the answer to this part, return the name of the plot you saved.

**Hint:** You can do this using subplots (and also otherwise)
"""

import matplotlib.pyplot as plt

def q13a(avg_2021):
    filename = "output/part1-13a.png"
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(avg_2021.values)
    ax.set_xticklabels(avg_2021.columns)
    ax.set_title("Distribution of regional averages by attribute (2021)")
    ax.set_xlabel("Attribute")
    ax.set_ylabel("Average score across universities in region")
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    return filename

"""
b. Do you observe any anomalies in the box and whisker
plot?

=== ANSWER Q13b BELOW ===
Yes, a few things stand out.
- Overall score has one outlier dot above the box. That's Singapore (91.8),
  much higher than every other region (most are between 61 and 81).
- Academic reputation has a really long lower whisker that goes down to 2.4
  (Argentina), and Russia is around 7. Universidad de Buenos Aires and
  Moscow State are famous schools, so near-zero reputation scores look
  wrong. Combined with Q19, I think the 2020/2021 columns might be
  mislabeled or shifted.
- The overall score box is much narrower than the individual attributes.
  That's expected because it's a weighted average, so the extremes cancel
  out. It also means regions differ a lot more on individual attributes
  than on the final score.
=== END OF Q13b ANSWER ===
"""

"""
14a.
Pick two attributes in the avg_2021 dataframe
and represent them using a scatter plot.

Store your plot in output/part1-14a.png.

As the answer to this part, return the name of the plot you saved.
"""

def q14a(avg_2021):
    filename = "output/part1-14a.png"
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(avg_2021["academic reputation"], avg_2021["overall score"], label="Region")
    for region, row in avg_2021.iterrows():
        ax.annotate(region, (row["academic reputation"], row["overall score"]), fontsize=7)
    ax.set_title("Academic reputation vs. overall score by region (2021)")
    ax.set_xlabel("Average academic reputation")
    ax.set_ylabel("Average overall score")
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    return filename

"""
Do you observe any general trend?

=== ANSWER Q14b BELOW ===
There's a weak positive trend: regions with higher average academic
reputation usually have a higher average overall score (Singapore, USA, and
Switzerland are top right, Russia and Argentina are bottom left). But
there's a lot of scatter. Belgium and the Netherlands have very high
academic reputation but below-average overall scores, and Canada scores
high overall with only average reputation. So academic reputation alone
doesn't predict the overall score well, at least in this (2021) data. The
correlation is only about 0.39 at the university level (see Q18).
=== END OF Q14b ANSWER ===

===== Questions 15-20: Exploring the data further =====

We're more than halfway through!

Let's come to the Top 10 Universities and observe how they performed over the years.

15. Create a smaller dataframe which has the top ten universities from each year, and only their overall scores across the three years.

Hint:

*   There will be four columns in the dataframe you make
*   The top ten universities are same across the three years. Only their rankings differ.
*   Use the merge function. You can read more about how to use it in the documentation: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html
*   Shape of the resultant dataframe should be (10, 4)

As your answer, return the shape of the new dataframe.
"""

def q15_helper(dfs):
    # Top 10 by overall score per year, keeping only name and score
    top_by_year = [
        df.nlargest(10, "overall score")[["university", "overall score"]]
        for df in dfs
    ]
    top_10 = top_by_year[0]
    for top in top_by_year[1:]:
        top_10 = top_10.merge(top, on="university")
    return top_10

def q15(top_10):
    print(top_10)
    return top_10.shape

"""
16.
You should have noticed that when you merged,
Pandas auto-assigned the column names. Let's change them.

For the columns representing scores, rename them such that they describe the data that the column holds.

You should be able to modify the column names directly in the dataframe.
As your answer, return the new column names as a list.
"""

SCORE_COLUMNS = [f"overall score {year}" for year in YEARS]

def q16(top_10):
    top_10.columns = ["university"] + SCORE_COLUMNS
    return list(top_10.columns)

"""
17a.
Draw a suitable plot to show how the overall scores of the Top 10 universities varied over the three years. Clearly label your graph and attach a legend. Explain why you chose the particular plot.

Save your plot in output/part1-17a.png.

As the answer to this part, return the name of the plot you saved.

Note:
*   All universities must be in the same plot.
*   Your graph should be clear and legend should be placed suitably
"""

def q17a(top_10):
    # A line plot shows each university's trend across the three years,
    # and lets all 10 universities share one set of axes.
    filename = "output/part1-17a.png"
    fig, ax = plt.subplots(figsize=(10, 6))
    for _, row in top_10.iterrows():
        ax.plot(YEARS, row[SCORE_COLUMNS].values, marker="o", label=row["university"])
    ax.set_xticks(YEARS)
    ax.set_title("Overall scores of the top 10 universities, 2019-2021")
    ax.set_xlabel("Year")
    ax.set_ylabel("Overall score")
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    return filename

"""
17b.
What do you observe from the plot above? Which university has remained consistent in their scores? Which have increased/decreased over the years?

=== ANSWER Q17b BELOW ===
(I used a line plot because the x-axis is time, and a line per university
makes it easy to see the direction each one moved.)

MIT is the most consistent: it scores exactly 100 every year, because the
scores are scaled so #1 gets 100. Stanford and Caltech are also very stable
(they drop by 0.2-0.3).
Increased: UCL had the biggest jump (92.9 -> 94.8), followed by Imperial
(93.3 -> 94.1), ETH Zurich (95.3 -> 95.9), and Oxford (96.8 -> 97.2), which
moved past Caltech.
Decreased: Chicago (93.2 -> 92.0) and Harvard (98.5 -> 97.4) dropped the
most, and Cambridge dipped a little (95.6 -> 95.0).
Every line is flat from 2020 to 2021, which matches the errata: the 2021
file is basically a copy of 2020, so the only real change is 2019 -> 2020.
Also, all of these changes are within about 2 points, so the top 10 is
mostly just reshuffling among the same schools.
=== END OF Q17b ANSWER ===
"""

"""
===== Questions 18-19: Correlation matrices =====

We're almost done!

Let's look at another useful tool to get an idea about how different variables are corelated to each other. We call it a **correlation matrix**

A correlation matrix provides a correlation coefficient (a number between -1 and 1) that tells how strongly two variables are correlated. Values closer to -1 mean strong negative correlation whereas values closer to 1 mean strong positve correlation. Values closer to 0 show variables having no or little correlation.

You can learn more about correlation matrices from here: https://www.statology.org/how-to-read-a-correlation-matrix/

18.
Plot a correlation matrix to see how each variable is correlated to another. You can use the data from 2021.

Print your correlation matrix and save it in output/part1-18.png.

As the answer to this part, return the name of the plot you saved.

**Helpful link:** https://datatofish.com/correlation-matrix-pandas/
"""

def q18(dfs):
    filename = "output/part1-18.png"
    # 'year' is constant within one year's data, so leave it out.
    corr = dfs[2][["rank"] + ATTRIBUTES].corr()
    print(corr)

    fig, ax = plt.subplots(figsize=(8, 7))
    image = ax.matshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    fig.colorbar(image, label="Correlation coefficient")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="left")
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    ax.set_title("Correlation matrix (2021)")
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)
    return filename

"""
19. Comment on at least one entry in the matrix you obtained in the previous
part that you found surprising or interesting.

=== ANSWER Q19 BELOW ===
The surprising part is that in 2021, citations per faculty has the
strongest correlation with overall score (0.77), and academic reputation
is only 0.39. QS weights academic reputation the most (40%) and citations
only 20%, so I expected the opposite.
When I ran the same correlation on the 2019 data, it looked like I
expected: academic reputation was 0.79 with overall score, and citations
was only 0.37. A change that big in one or two years doesn't make sense,
so I think the 2020/2021 columns were scraped in a different order and
the column labels don't match the data anymore. This also explains the
strange 2.4 reputation for Argentina in Q13.
Another interesting one: employer reputation and faculty student are
correlated at 0.69 in 2021, but only 0.09 in 2019. That's another sign the
labels got mixed up. Rank vs. overall score is -0.99, which is just a
sanity check (higher score = better = smaller rank number).
=== END OF Q19 ANSWER ===
"""

"""
===== Questions 20-23: Data manipulation and falsification =====

This is the last section.

20. Exploring data manipulation and falsification

For fun, this part will ask you to come up with a way to alter the
rankings such that your university of choice comes out in 1st place.

The data does not contain UC Davis, so let's pick a different university.
UC Berkeley is a public university nearby and in the same university system,
so let's pick that one.

We will write two functions.
a.
First, write a function that calculates a new column
(that is you should define and insert a new column to the dataframe whose value
depends on the other columns)
and calculates
it in such a way that Berkeley will come out on top in the 2021 rankings.

Note: you can "cheat"; it's OK if your scoring function is picked in some way
that obviously makes Berkeley come on top.
As an extra challenge to make it more interesting, you can try to come up with
a scoring function that is subtle!

b.
Use your new column to sort the data by the new values and return the top 10 university names as a list.

"""

BERKELEY = "University of California, Berkeley (UCB)"

def add_research_focus(df):
    """
    Add a 'research focus' score: the average of the three academic metrics,
    minus a penalty for leaning on industry (employer) reputation.
    Sounds reasonable, but it happens to reward Berkeley's exact profile.
    """
    academic = df[["academic reputation", "faculty student", "citations per faculty"]].mean(axis=1)
    df["research focus"] = academic - 0.5 * df["employer reputation"]
    return df

def q20a(dfs):
    df_2021 = add_research_focus(dfs[2])
    return df_2021.loc[df_2021["university"] == BERKELEY, "research focus"].iloc[0]

def q20b(dfs):
    df_2021 = add_research_focus(dfs[2])
    return df_2021.sort_values("research focus", ascending=False)["university"].head(10).tolist()

"""
21. Exploring data manipulation and falsification, continued

This time, let's manipulate the data by changing the source files
instead.
Create a copy of data/2021.csv and name it
data/2021_falsified.csv.
Modify the data in such a way that UC Berkeley comes out on top.

For this part, you will also need to load in the new data
as part of the function.
The function does not take an input; you should get it from the file.

Return the top 10 university names as a list from the falsified data.
"""

def q21():
    df = pd.read_csv('data/2021_falsified.csv', encoding='latin-1')
    df.columns = df.columns.str.lower()
    return df.sort_values("overall score", ascending=False)["university"].head(10).tolist()

"""
22. Exploring data manipulation and falsification, continued

Which of the methods above do you think would be the most effective
if you were a "bad actor" trying to manipulate the rankings?

Which do you think would be the most difficult to detect?

=== ANSWER Q22 BELOW ===
Most effective: changing the scoring formula (Q20). It doesn't touch any of
the raw data, so every number can be checked and is "true", but you still
get the result you want. If you can make the formula sound reasonable (mine
is a "research focus" score that rewards academic strength and penalizes
relying on industry reputation), people will probably accept it. You can
also keep adjusting the weights until your school comes out on top, and no
single number looks off.

Hardest to detect: I'd also say the scoring formula. Editing the CSV (Q21)
works, but it's fragile. If anyone compares against the original source or
an older copy, the diff will show it right away. In my case Berkeley went
from 82.6 to 100, which is a huge jump compared to last year's ranking.
A biased formula is a judgement call, not a lie that can be proven by
checking the data, so it's much harder to call out. The only way to catch
it is to ask why those specific weights were chosen.
(A smaller version of the CSV edit, like nudging a few sub-scores by
1-2 points, would also be hard to detect, but it wouldn't move Berkeley
from #28 to #1.)
=== END OF Q22 ANSWER ===
"""

"""
===== Wrapping things up =====

To wrap things up, we have collected
everything together in a pipeline for you
below.

**Don't modify this part.**
It will put everything together,
run your pipeline and save all of your answers.

This is run in the main function
and will be used in the first part of Part 2.
"""

UNFINISHED = 0

def log_answer(name, func, *args):
    try:
        answer = func(*args)
        print(f"{name} answer: {answer}")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},{answer}\n')
            print(f"Answer saved to {ANSWER_FILE}")
    except NotImplementedError:
        print(f"Warning: {name} not implemented.")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},Not Implemented\n')
        global UNFINISHED
        UNFINISHED += 1

def PART_1_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    try:
        dfs = load_input()
    except NotImplementedError:
        print("Welcome to Part 1! Implement load_input() to get started.")
        dfs = []

    # Questions 1-6
    log_answer("q1", q1, dfs)
    log_answer("q2", q2, dfs)
    log_answer("q3a", q3, dfs)
    # 3b: commentary
    log_answer("q4", q4, dfs)
    # 4b: commentary
    log_answer("q5a", q5a, dfs)
    log_answer("q5b", q5b, dfs)
    log_answer("q5c", q5c)
    # 6a: commentary
    # 6b: commentary
    log_answer("q6c", q6c)

    # Questions 7-10
    log_answer("q7", q7, dfs)
    log_answer("q8a", q8a, dfs)
    # 8b: commentary
    log_answer("q9", q9, dfs)
    # 10: avg_2021
    avg_2021 = q10_helper(dfs)
    log_answer("q10", q10, avg_2021)

    # Questions 11-15
    log_answer("q11", q11, avg_2021)
    log_answer("q12", q12a, avg_2021)
    # 12b: commentary
    log_answer("q13", q13a, avg_2021)
    # 13b: commentary
    log_answer("q14a", q14a, avg_2021)
    # 14b: commentary

    # Questions 15-17
    top_10 = q15_helper(dfs)
    log_answer("q15", q15, top_10)
    log_answer("q16", q16, top_10)
    log_answer("q17", q17a, top_10)
    # 17b: commentary

    # Questions 18-20
    log_answer("q18", q18, dfs)
    # 19: commentary

    # Questions 20-22
    log_answer("q20a", q20a, dfs)
    log_answer("q20b", q20b, dfs)
    log_answer("q21", q21)
    # 22: commentary

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
That's it for Part 1!

=== END OF PART 1 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 1", PART_1_PIPELINE)
