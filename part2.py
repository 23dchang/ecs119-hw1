"""
Part 2: Performance Comparisons

In this part, we will explore comparing the performance
of different pipelines.
First, we will set up some helper classes.
Then we will do a few comparisons
between two or more versions of a pipeline
to report which one is faster.
"""

import part1

import timeit
import math
import matplotlib.pyplot as plt
import pandas as pd
import pytest

def make_bar_plot(names, values, ylabel, title, filename, log_scale=False):
    """Save a bar chart with one labeled (legend) bar per pipeline."""
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.tab10.colors
    for i, (name, value) in enumerate(zip(names, values)):
        ax.bar(name, value, label=name, color=colors[i % len(colors)])
    if log_scale:
        ax.set_yscale("log")
    ax.set_title(title)
    ax.set_xlabel("Pipeline")
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=30)
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)

"""
=== Questions 1-5: Throughput and Latency Helpers ===

We will design and fill out two helper classes.

The first is a helper class for throughput (Q1).
The class is created by adding a series of pipelines
(via .add_pipeline(name, size, func))
where name is a title describing the pipeline,
size is the number of elements in the input dataset for the pipeline,
and func is a function that can be run on zero arguments
which runs the pipeline (like def f()).

The second is a similar helper class for latency (Q3).

1. Throughput helper class

Fill in the add_pipeline, eval_throughput, and generate_plot functions below.
"""

# Number of times to run each pipeline in the following results.
# You may modify this as you go through the file if you like, but make sure
# you set it back to 10 at the end before you submit.
NUM_RUNS = 10

class ThroughputHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline input sizes
        self.sizes = []

        # Pipeline throughputs
        # This is set to None, but will be set to a list after throughputs
        # are calculated.
        self.throughputs = None

    def add_pipeline(self, name, size, func):
        self.pipelines.append(func)
        self.names.append(name)
        self.sizes.append(size)

    def compare_throughput(self):
        # Measure the throughput of all pipelines
        # and store it in a list in self.throughputs.
        # Make sure to use the NUM_RUNS variable.
        # Also, return the resulting list of throughputs,
        # in **number of items per second.**
        self.throughputs = []
        for func, size in zip(self.pipelines, self.sizes):
            total_seconds = timeit.timeit(func, number=NUM_RUNS)
            self.throughputs.append(size * NUM_RUNS / total_seconds)
        return self.throughputs

    def generate_plot(self, filename):
        # Generate a plot for throughput using matplotlib.
        # You can use any plot you like, but a bar chart probably makes
        # the most sense.
        # Make sure you include a legend.
        # Save the result in the filename provided.
        # Log scale, since throughputs can differ by orders of magnitude.
        make_bar_plot(self.names, self.throughputs, "Throughput (items/second, log scale)",
                      "Throughput comparison", filename, log_scale=True)

"""
As your answer to this part,
return the name of the method you decided to use in
matplotlib.

(Example: "boxplot" or "scatter")
"""

def q1():
    # Return plot method (as a string) from matplotlib
    return "bar"

"""
2. A simple test case

To make sure your monitor is working, test it on a very simple
pipeline that adds up the total of all elements in a list.

We will compare three versions of the pipeline depending on the
input size.
"""

LIST_SMALL = [10] * 100
LIST_MEDIUM = [10] * 100_000
LIST_LARGE = [10] * 100_000_000

def add_list(l):
    total = 0
    for item in l:
        total += item
    return total

def q2a():
    # Create a ThroughputHelper object
    h = ThroughputHelper()
    # Add the 3 pipelines.
    h.add_pipeline("small", len(LIST_SMALL), lambda: add_list(LIST_SMALL))
    h.add_pipeline("medium", len(LIST_MEDIUM), lambda: add_list(LIST_MEDIUM))
    h.add_pipeline("large", len(LIST_LARGE), lambda: add_list(LIST_LARGE))
    throughputs = h.compare_throughput()
    h.generate_plot('output/part2-q2a.png')
    return throughputs

"""
2b.
Which pipeline has the highest throughput?
Is this what you expected?

=== ANSWER Q2b BELOW ===
Medium and large are basically tied for the highest throughput (about 17
million items/second each). Small is always the lowest, though how much
lower changed between runs (anywhere from about 11 to 16 million/second).
That's mostly what I expected. Adding up a list is linear, so per-item
cost should be the same no matter the size, which is why medium and large
match. Small is lower because every run has a fixed cost (calling the
function, setting up the loop, timer overhead). With only 100 items, that
fixed cost is a big part of the total time, but with 100,000+ items it
disappears into the noise.
=== END OF Q2b ANSWER ===
"""

"""
3. Latency helper class.

Now we will create a similar helper class for latency.

The helper should assume a pipeline that only has *one* element
in the input dataset.

It should use the NUM_RUNS variable as with throughput.
"""

LIST_ONE_ITEM = [10]

class LatencyHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline latencies
        # This is set to None, but will be set to a list after latencies
        # are calculated.
        self.latencies = None

    def add_pipeline(self, name, func):
        self.pipelines.append(func)
        self.names.append(name)

    def compare_latency(self):
        # Measure the latency of all pipelines
        # and store it in a list in self.latencies.
        # Also, return the resulting list of latencies,
        # in **milliseconds.**
        # Latency = average time for one run on a single input item.
        self.latencies = []
        for func in self.pipelines:
            total_seconds = timeit.timeit(func, number=NUM_RUNS)
            self.latencies.append(total_seconds / NUM_RUNS * 1000)
        return self.latencies

    def generate_plot(self, filename):
        # Generate a plot for latency using matplotlib.
        # You can use any plot you like, but a bar chart probably makes
        # the most sense.
        # Make sure you include a legend.
        # Save the result in the filename provided.
        make_bar_plot(self.names, self.latencies, "Latency (milliseconds)",
                      "Latency comparison", filename)

"""
As your answer to this part,
return the number of input items that each pipeline should
process if the class is used correctly.
"""

def q3():
    # Return the number of input items in each dataset,
    # for the latency helper to run correctly.
    return 1

"""
4. To make sure your monitor is working, test it on
the simple pipeline from Q2.

For latency, all three pipelines would only process
one item. Therefore instead of using
LIST_SMALL, LIST_MEDIUM, and LIST_LARGE,
for this question run the same pipeline three times
on a single list item.
"""

LIST_SINGLE_ITEM = [10] # Note: a list with only 1 item

def q4a():
    # Create a LatencyHelper object
    h = LatencyHelper()
    # Add the single pipeline three times.
    for copy_num in range(1, 4):
        h.add_pipeline(f"copy {copy_num}", lambda: add_list(LIST_SINGLE_ITEM))
    latencies = h.compare_latency()
    h.generate_plot('output/part2-q4a.png')
    return latencies

"""
4b.
How much did the latency vary between the three copies of the pipeline?
Is this more or less than what you expected?

=== ANSWER Q4b BELOW ===
All three are tiny, around 0.0003-0.0008 ms (less than a microsecond).
In relative terms they varied a lot: sometimes one copy was 2x another,
and the first copy was the slowest every time I ran it, probably because
it warms up the caches and the code path the other two then reuse.
In absolute terms the differences are a fraction of a microsecond, which
is close to what the timer can even measure. So it was more variation than
I expected percentage-wise, but none of it really matters. At this scale
you're mostly measuring noise, and for small timings like this you need
lots of runs to get a stable number.
=== END OF Q4b ANSWER ===
"""

"""
Now that we have our helpers, let's do a simple comparison.

NOTE: you may add other helper functions that you may find useful
as you go through this file.

5. Comparison on Part 1

Finally, use the helpers above to calculate the throughput and latency
of the pipeline in part 1.

Remember that for latency you should use a version of the pipeline with only one input row!
You may need to write a new version of the pipeline for this to work.
"""

# You will need these:
# part1.load_input
# part1.PART_1_PIPELINE

def part1_single_row_pipeline():
    """
    Part 1's data processing steps (Q7-Q11), run on only the first row of
    each year's data. Most of Part 1 (validation, sampling, plots) only makes
    sense on the full dataset, so those steps are left out here.
    """
    dfs = [df.head(1).copy() for df in part1.load_input()]
    part1.q7(dfs)
    part1.q8a(dfs)
    part1.q9(dfs)
    avg_2021 = part1.q10_helper(dfs)
    part1.q11(avg_2021)

def q5a():
    # Return the throughput of the pipeline in part 1.
    # Items = total rows across the three years of data.
    num_rows = sum(len(df) for df in part1.load_input())
    h = ThroughputHelper()
    h.add_pipeline("part 1", num_rows, part1.PART_1_PIPELINE)
    return h.compare_throughput()[0]

def q5b():
    # Return the latency of the pipeline in part 1.
    h = LatencyHelper()
    h.add_pipeline("part 1 (single row)", part1_single_row_pipeline)
    return h.compare_latency()[0]

"""
===== Questions 6-10: Performance Comparison 1 =====

For our first performance comparison,
let's look at the cost of getting input from a file, vs. in an existing DataFrame.

6. We will use the same population dataset
that we used in lecture 3.

Load the data using load_input() given the file name.

- Make sure that you clean the data by removing
  continents and world data!
  (World data is listed under OWID_WRL)

Then, set up a simple pipeline that computes summary statistics
for the following:

- *Year over year increase* in population, per country

    (min, median, max, mean, and standard deviation)

How you should compute this:

- For each country, we need the maximum year and the minimum year
in the data. We should divide the population difference
over this time by the length of the time period.

- Make sure you throw out the cases where there is only one year
(if any).

- We should at this point have one data point per country.

- Finally, as your answer, return a list of the:
    min, median, max, mean, and standard deviation
  of the data.

Hints:
You can use the describe() function in Pandas to get these statistics.
You should be able to do something like
df.describe().loc["min"]["colum_name"]

to get a specific value from the describe() function.

You shouldn't use any for loops.
See if you can compute this using Pandas functions only.
"""

POPULATION_COLUMN = "Population (historical)"

def load_input(filename):
    # Return a dataframe containing the population data
    # Continents, income groups, etc. have no country code,
    # and the world total is listed under OWID_WRL.
    df = pd.read_csv(filename)
    is_country = df["Code"].notna() & (df["Code"] != "OWID_WRL")
    return df[is_country]

def population_pipeline(df):
    # Input: the dataframe from load_input()
    # Return a list of min, median, max, mean, and standard deviation
    by_country = df.groupby("Entity")
    first = df.loc[by_country["Year"].idxmin()].set_index("Entity")
    last = df.loc[by_country["Year"].idxmax()].set_index("Entity")

    # Average yearly increase per country, skipping countries with only one year
    num_years = last["Year"] - first["Year"]
    has_range = num_years > 0
    yearly_increase = (last[POPULATION_COLUMN] - first[POPULATION_COLUMN])[has_range] / num_years[has_range]

    stats = yearly_increase.describe()
    return [float(stats[stat]) for stat in ["min", "50%", "max", "mean", "std"]]

def q6():
    # As your answer to this part,
    # call load_input() and then population_pipeline()
    # Return a list of min, median, max, mean, and standard deviation
    df = load_input("data/population.csv")
    return population_pipeline(df)

"""
7. Varying the input size

Next we want to set up three different datasets of different sizes.

Create three new files,
    - data/population-small.csv
      with the first 600 rows
    - data/population-medium.csv
      with the first 6000 rows
    - data/population-single-row.csv
      with only the first row
      (for calculating latency)

You can edit the csv file directly to extract the first rows
(remember to also include the header row)
and save a new file.

Make four versions of load input that load your datasets.
(The _large one should use the full population dataset.)
Each should return a dataframe.

The input CSV file will have 600 rows, but the DataFrame (after your cleaning) may have less than that.
"""

def load_input_small():
    return load_input("data/population-small.csv")

def load_input_medium():
    return load_input("data/population-medium.csv")

def load_input_large():
    return load_input("data/population.csv")

def load_input_single_row():
    # This is the pipeline we will use for latency.
    return load_input("data/population-single-row.csv")

def q7():
    # Don't modify this part
    s = load_input_small()
    m = load_input_medium()
    l = load_input_large()
    x = load_input_single_row()
    return [len(s), len(m), len(l), len(x)]

"""
8.
Create baseline pipelines

First let's create our baseline pipelines.
Create four pipelines,
    baseline_small
    baseline_medium
    baseline_large
    baseline_latency

based on the three datasets above.
Each should call your population_pipeline from Q6.

Your baseline_latency function will not be very interesting
as the pipeline does not produce any meaningful output on a single row!
You may choose to instead run an example with two rows,
or you may fill in this function in any other way that you choose
that you think is meaningful.
"""

def baseline_small():
    return population_pipeline(load_input_small())

def baseline_medium():
    return population_pipeline(load_input_medium())

def baseline_large():
    return population_pipeline(load_input_large())

def baseline_latency():
    # One row = one country with one year, so the statistics come out as NaN.
    # That's fine: we only care how long it takes one item to go through.
    return population_pipeline(load_input_single_row())

def q8():
    # Don't modify this part
    _ = baseline_medium()
    return ["baseline_small", "baseline_medium", "baseline_large", "baseline_latency"]

"""
9.
Finally, let's compare whether loading an input from file is faster or slower
than getting it from an existing Pandas dataframe variable.

Create four new dataframes (constant global variables)
directly in the script.
Then use these to write 3 new pipelines:
    fromvar_small
    fromvar_medium
    fromvar_large
    fromvar_latency

These pipelines should produce the same answers as in Q8.

As your answer to this part;
a. Generate a plot in output/part2-q9a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, fromvar_small, fromvar_medium, fromvar_large
b. Generate a plot in output/part2-q9b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, fromvar_latency
"""

POPULATION_SMALL = load_input_small()
POPULATION_MEDIUM = load_input_medium()
POPULATION_LARGE = load_input_large()
POPULATION_SINGLE_ROW = load_input_single_row()

def fromvar_small():
    return population_pipeline(POPULATION_SMALL)

def fromvar_medium():
    return population_pipeline(POPULATION_MEDIUM)

def fromvar_large():
    return population_pipeline(POPULATION_LARGE)

def fromvar_latency():
    return population_pipeline(POPULATION_SINGLE_ROW)

def compare_throughputs(pipelines, filename):
    """
    pipelines: list of (name, dataset, func) where dataset is used for the size.
    Saves a plot to filename and returns the list of throughputs.
    """
    h = ThroughputHelper()
    for name, dataset, func in pipelines:
        h.add_pipeline(name, len(dataset), func)
    throughputs = h.compare_throughput()
    h.generate_plot(filename)
    return throughputs

def compare_latencies(pipelines, filename):
    """
    pipelines: list of (name, func).
    Saves a plot to filename and returns the list of latencies.
    """
    h = LatencyHelper()
    for name, func in pipelines:
        h.add_pipeline(name, func)
    latencies = h.compare_latency()
    h.generate_plot(filename)
    return latencies

BASELINE_THROUGHPUT_PIPELINES = [
    ("baseline_small", POPULATION_SMALL, baseline_small),
    ("baseline_medium", POPULATION_MEDIUM, baseline_medium),
    ("baseline_large", POPULATION_LARGE, baseline_large),
]

def q9a():
    # Add all 6 pipelines for a throughput comparison
    # Generate plot in output/part2-q9a.png
    # Return list of 6 throughputs
    return compare_throughputs(BASELINE_THROUGHPUT_PIPELINES + [
        ("fromvar_small", POPULATION_SMALL, fromvar_small),
        ("fromvar_medium", POPULATION_MEDIUM, fromvar_medium),
        ("fromvar_large", POPULATION_LARGE, fromvar_large),
    ], 'output/part2-q9a.png')

def q9b():
    # Add 2 pipelines for a latency comparison
    # Generate plot in output/part2-q9b.png
    # Return list of 2 latencies
    return compare_latencies([
        ("baseline_latency", baseline_latency),
        ("fromvar_latency", fromvar_latency),
    ], 'output/part2-q9b.png')

"""
10.
Comment on the plots above!
How dramatic is the difference between the two pipelines?
Which differs more, throughput or latency?
What does this experiment show?

===== ANSWER Q10 BELOW =====
Getting the data from a variable is faster every time, and the gap grows
with the input size. In my runs, fromvar was about 1.8x faster on the
small data, 2.5-3x on medium, and about 5x on large (around 4.5 million
vs. 0.9 million rows/second).
For latency, fromvar was about 1.5-1.9x faster (around 4-5 ms vs 6-9 ms).
So throughput differs more, at least for the large dataset.
This shows that reading and parsing the CSV is the most expensive part of
the baseline pipeline. On the full dataset, about 80% of each run is just
loading the file, and the actual computation is the smaller part. For
latency, both pipelines have the same fixed Pandas overhead (groupby,
describe, etc.), so the file reading matters less there.
In practice: load data once and reuse it, rather than re-reading the file
each time you need it.
===== END OF Q10 ANSWER =====
"""

"""
===== Questions 11-14: Performance Comparison 2 =====

Our second performance comparison will explore vectorization.

Operations in Pandas use Numpy arrays and vectorization to enable
fast operations.
In particular, they are often much faster than using for loops.

Let's explore whether this is true!

11.
First, we need to set up our pipelines for comparison as before.

We already have the baseline pipelines from Q8,
so let's just set up a comparison pipeline
which uses a for loop to calculate the same statistics.

Your pipeline should produce the same answers as in Q6 and Q8.

Create a new pipeline:
- Iterate through the dataframe entries. You can assume they are sorted.
- Manually compute the minimum and maximum year for each country.
- Compute the same answers as in Q6.
- Manually compute the summary statistics for the resulting list (min, median, max, mean, and standard deviation).
"""

def summary_stats(values):
    """Min, median, max, mean, and sample standard deviation, computed by hand."""
    n = len(values)
    if n == 0:
        return [math.nan] * 5
    values = sorted(values)
    middle = n // 2
    median = values[middle] if n % 2 == 1 else (values[middle - 1] + values[middle]) / 2
    mean = sum(values) / n
    # Sample standard deviation (n - 1), to match Pandas' describe()
    std = math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1)) if n > 1 else math.nan
    return [float(values[0]), float(median), float(values[-1]), float(mean), float(std)]

def for_loop_pipeline(df):
    # Input: the dataframe from load_input()
    # Return a list of min, median, max, mean, and standard deviation
    # country -> [min year, population at min year, max year, population at max year]
    year_ranges = {}
    for country, year, population in zip(df["Entity"], df["Year"], df[POPULATION_COLUMN]):
        if country not in year_ranges:
            year_ranges[country] = [year, population, year, population]
            continue
        country_range = year_ranges[country]
        if year < country_range[0]:
            country_range[0], country_range[1] = year, population
        if year > country_range[2]:
            country_range[2], country_range[3] = year, population

    yearly_increases = []
    for min_year, min_population, max_year, max_population in year_ranges.values():
        if max_year > min_year:
            yearly_increases.append((max_population - min_population) / (max_year - min_year))

    return summary_stats(yearly_increases)

def q11():
    # As your answer to this part, call load_input() and then
    # for_loop_pipeline() to return the 5 numbers.
    # (these should match the numbers you got in Q6.)
    # ** Please return these as Python floats, not Numpy **
    df = load_input("data/population.csv")
    return for_loop_pipeline(df)

"""
12.
Now, let's create our pipelines for comparison.

As before, write 4 pipelines based on the datasets from Q7.
"""

def for_loop_small():
    return for_loop_pipeline(load_input_small())

def for_loop_medium():
    return for_loop_pipeline(load_input_medium())

def for_loop_large():
    return for_loop_pipeline(load_input_large())

def for_loop_latency():
    return for_loop_pipeline(load_input_single_row())

def q12():
    # Don't modify this part
    _ = for_loop_medium()
    return ["for_loop_small", "for_loop_medium", "for_loop_large", "for_loop_latency"]

"""
13.
Finally, let's compare our two pipelines,
as we did in Q9.

a. Generate a plot in output/part2-q13a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, for_loop_small, for_loop_medium, for_loop_large

b. Generate a plot in output/part2-q13b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, for_loop_latency
"""

def q13a():
    # Add all 6 pipelines for a throughput comparison
    # Generate plot in output/part2-q13a.png
    # Return list of 6 throughputs
    return compare_throughputs(BASELINE_THROUGHPUT_PIPELINES + [
        ("for_loop_small", POPULATION_SMALL, for_loop_small),
        ("for_loop_medium", POPULATION_MEDIUM, for_loop_medium),
        ("for_loop_large", POPULATION_LARGE, for_loop_large),
    ], 'output/part2-q13a.png')

def q13b():
    # Add 2 pipelines for a latency comparison
    # Generate plot in output/part2-q13b.png
    # Return list of 2 latencies
    return compare_latencies([
        ("baseline_latency", baseline_latency),
        ("for_loop_latency", for_loop_latency),
    ], 'output/part2-q13b.png')

"""
14.
Comment on the results you got!

14a. Which pipelines is faster in terms of throughput?

===== ANSWER Q14a BELOW =====
It depends on the input size. The for loop pipeline was faster on small
data (about 2.5x) and medium data (about 1.2x), but the vectorized baseline
was faster on large data (about 890k vs 650k rows/second). This was
consistent across all my runs.
===== END OF Q14a ANSWER =====

14b. Which pipeline is faster in terms of latency?

===== ANSWER Q14b BELOW =====
The for loop pipeline, by about 3x (around 2.5 ms vs 7.5-9 ms).
===== END OF Q14b ANSWER =====

14c. Do you notice any other interesting observations?
What does this experiment show?

===== ANSWER Q14c BELOW =====
The interesting part is the crossover. Pandas has a fixed setup cost every
time you call groupby/idxmin/describe (around 4-5 ms here, even on one row),
but after that each row is very cheap. The for loop has almost no setup,
but each row costs more because it's plain Python. So on small inputs the
setup cost dominates and the loop wins. On large inputs the per-row cost
dominates and Pandas wins.
Also, the difference on large data is smaller than I expected, because
both pipelines first read the CSV, and that takes most of the time (see
Q10). Comparing just the computation (fromvar_large at ~4.5M rows/s vs
for_loop_large at ~650k), vectorization is a lot faster.
What this shows: "vectorized is faster" is true when there's a lot of
data, but it's not free. For tiny inputs or latency-sensitive work, the
overhead can make it slower than a simple loop.
===== END OF Q14c ANSWER =====
"""

"""
===== Questions 15-17: Reflection Questions =====
15.

Take a look at all your pipelines above.
Which factor that we tested (file vs. variable, vectorized vs. for loop)
had the biggest impact on performance?

===== ANSWER Q15 BELOW =====
File vs. variable had the biggest impact. Skipping the file read made the
large pipeline about 5x faster, and it helped at every size. For loop vs.
vectorized was at most about 2.5x either way, and the direction depended
on input size. In other words, I/O (reading and parsing the CSV) cost more
than the choice of how to do the computation.
===== END OF Q15 ANSWER =====

16.
Based on all of your plots, form a hypothesis as to how throughput
varies with the size of the input dataset.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q16 BELOW =====
Hypothesis: throughput goes up as the input gets bigger, then levels off.
Each run takes roughly (fixed overhead) + (number of rows) x (cost per row).
With small inputs the fixed overhead dominates, so throughput is low. As the
input grows, that overhead is spread over more rows, so throughput rises
toward a maximum of 1 / (cost per row).
Evidence: every population pipeline gets faster per row from small to
medium to large (baseline goes from ~30k to ~350k to ~890k rows/s). And
in Q2, where the per-run overhead is tiny, it has already leveled off:
medium and large are both ~17M items/s, and only small is lower.
===== END OF Q16 ANSWER =====

17.
Based on all of your plots, form a hypothesis as to how
throughput is related to latency.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q17 BELOW =====
Hypothesis: throughput is NOT just 1 / latency. Latency mostly measures the
fixed overhead of a pipeline, and throughput on big inputs mostly measures
the per-item cost. So they only line up when the input is small.
Evidence:
- If throughput were 1 / latency, the baseline (latency ~8 ms) would only
  handle ~125 rows/s. Its actual throughput on the large data is ~890k
  rows/s, thousands of times more, because the fixed cost is shared across
  all the rows.
- On the small data they do line up: baseline_small takes about
  261 rows / 30k rows/s = ~9 ms per run, almost exactly its latency. So for
  small inputs, throughput is about (input size) / latency.
- The pipeline with the best latency isn't always the one with the best
  throughput: the for loop had the lowest latency (~2.5 ms) but lower
  throughput than Pandas on large data.
So a low-latency pipeline and a high-throughput pipeline can be different
pipelines, and which one you want depends on whether you care about quick
answers for single items or processing lots of data.
===== END OF Q17 ANSWER =====
"""

"""
===== Extra Credit =====

This part is optional.

Use your pipeline to compare something else!

Here are some ideas for what to try:
- the cost of random sampling vs. the cost of getting rows from the
  DataFrame manually
- the cost of cloning a DataFrame
- the cost of sorting a DataFrame prior to doing a computation
- the cost of using different encodings (like one-hot encoding)
  and encodings for null values
- the cost of querying via Pandas methods vs querying via SQL
  For this part: you would want to use something like
  pandasql that can run SQL queries on Pandas data frames. See:
  https://stackoverflow.com/a/45866311/2038713

As your answer to this part,
as before, return
a. the list of 6 throughputs
and
b. the list of 2 latencies.

and generate plots for each of these in the following files:
    output/part2-ec-a.png
    output/part2-ec-b.png
"""

# Extra credit (optional)
# Comparison: the cost of sorting the DataFrame (by country, then year)
# before running the same pipeline, vs. running it on the data as-is.

def sort_by_country_year(df):
    return df.sort_values(["Entity", "Year"])

def sorted_small():
    return population_pipeline(sort_by_country_year(POPULATION_SMALL))

def sorted_medium():
    return population_pipeline(sort_by_country_year(POPULATION_MEDIUM))

def sorted_large():
    return population_pipeline(sort_by_country_year(POPULATION_LARGE))

def sorted_latency():
    return population_pipeline(sort_by_country_year(POPULATION_SINGLE_ROW))

def extra_credit_a():
    return compare_throughputs([
        ("fromvar_small", POPULATION_SMALL, fromvar_small),
        ("fromvar_medium", POPULATION_MEDIUM, fromvar_medium),
        ("fromvar_large", POPULATION_LARGE, fromvar_large),
        ("sorted_small", POPULATION_SMALL, sorted_small),
        ("sorted_medium", POPULATION_MEDIUM, sorted_medium),
        ("sorted_large", POPULATION_LARGE, sorted_large),
    ], 'output/part2-ec-a.png')

def extra_credit_b():
    return compare_latencies([
        ("fromvar_latency", fromvar_latency),
        ("sorted_latency", sorted_latency),
    ], 'output/part2-ec-b.png')

"""
Extra credit results:
Sorting first only made a clear difference on the large dataset, where it
was slower in every run by about 30-45% (roughly 4.3M -> 2.5-3.0M rows/s).
On small and medium the two were within noise of each other (sorted was
sometimes even a bit faster), and latency bounced between ~4-8 ms for both
with no consistent winner, since sorting one row costs almost nothing.
That fits sorting being O(n log n): it's cheap on small data and only
starts to show up when n is large. Since the pipeline uses
idxmin/idxmax and doesn't depend on row order, sorting was pure overhead
here.
"""

"""
Unit tests: sanity checks for the helpers and pipelines above.
Run with `pytest part2.py`.
"""

def test_add_list():
    assert add_list(LIST_SMALL) == 1000
    assert add_list([]) == 0

def test_load_input_removes_aggregates():
    assert POPULATION_LARGE["Code"].notna().all()
    assert not (POPULATION_LARGE["Code"] == "OWID_WRL").any()

def test_for_loop_matches_pandas():
    assert for_loop_pipeline(POPULATION_MEDIUM) == pytest.approx(population_pipeline(POPULATION_MEDIUM))

def test_q7():
    assert q7() == [261, 5122, 55240, 1]

"""
===== Wrapping things up =====

**Don't modify this part.**

To wrap things up, we have collected
your answers and saved them to a file below.
This will be run when you run the code.
"""

ANSWER_FILE = "output/part2-answers.txt"
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

def PART_2_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    # Q1-5
    log_answer("q1", q1)
    log_answer("q2a", q2a)
    # 2b: commentary
    log_answer("q3", q3)
    log_answer("q4a", q4a)
    # 4b: commentary
    log_answer("q5a", q5a)
    log_answer("q5b", q5b)

    # Q6-10
    log_answer("q6", q6)
    log_answer("q7", q7)
    log_answer("q8", q8)
    log_answer("q9a", q9a)
    log_answer("q9b", q9b)
    # 10: commentary

    # Q11-14
    log_answer("q11", q11)
    log_answer("q12", q12)
    log_answer("q13a", q13a)
    log_answer("q13b", q13b)
    # 14: commentary

    # 15-17: reflection
    # 15: commentary
    # 16: commentary
    # 17: commentary

    # Extra credit
    log_answer("extra credit (a)", extra_credit_a)
    log_answer("extra credit (b)", extra_credit_b)

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
=== END OF PART 2 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 2", PART_2_PIPELINE)
