"""
Part 3: Short Exercises on the Shell

For the third and last part of this homework,
we will complete a few tasks related to shell programming
and shell commands, particularly, with relevance to how
the shell is used in data science.

Please note:
The "project proposal" portion will be postponed to part of Homework 2.

===== Questions 1-5: Setup Scripting =====

1. For this first part, let's write a setup script
that downloads a dataset from the web,
clones a GitHub repository, and runs the Python script
contained in `script.py` on the dataset in question.

For the download portion, we have written a helper
download_file(url, filename) which downloads the file
at `url` and saves it in `filename`.

You should use Python subprocess to run all of these operations.

To test out your script, and as your answer to this part,
run the following:
    setup(
        "https://github.com/DavisPL-Teaching/119-hw1",
        "https://raw.githubusercontent.com/DavisPL-Teaching/119-hw1/refs/heads/main/data/test-input.txt",
        "test-script.py"
    )

Then read the output of `output/test-output.txt`,
convert it to an integer and return it. You should get "12345".

Note:
Running this question will leave an extra repo 119-hw1 lying around in your repository.
We recommend adding this to your .gitignore file so it does not
get uploaded when you submit.
"""

# You may need to conda install requests or pip3 install requests
import requests

def download_file(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)

import os
import subprocess
import sys

def clone_repo(repo_url):
    # Skip the clone if the repo is already here (e.g. from a previous run),
    # since git refuses to clone into an existing folder.
    repo_dir = repo_url.rstrip("/").split("/")[-1].removesuffix(".git")
    if not os.path.isdir(repo_dir):
        subprocess.run(["git", "clone", repo_url], check=True)

def run_script(script_path, data_path):
    # sys.executable = the same Python running this file, so this works
    # whether Python is called "python3", "python", or something else.
    subprocess.run([sys.executable, script_path, data_path], check=True)

def setup(repo_url, data_url, script_path):
    data_path = "data/" + data_url.split("/")[-1]
    clone_repo(repo_url)
    download_file(data_url, data_path)
    run_script(script_path, data_path)

def q1():
    # Call setup as described in the prompt
    setup(
        "https://github.com/DavisPL-Teaching/119-hw1",
        "https://raw.githubusercontent.com/DavisPL-Teaching/119-hw1/refs/heads/main/data/test-input.txt",
        "test-script.py"
    )
    with open("output/test-output.txt") as f:
        output = f.read()
    return int(output)

"""
2.
Suppose you are on a team of 5 data scientists working on
a project; every 2 weeks you need to re-run your scripts to
fetch the latest data and produce the latest analysis.

a. When might you need to use a script like setup() above in
this scenario?

=== ANSWER Q2a BELOW ===
Every two weeks when we need to refresh the analysis. Instead of each of
the 5 of us manually pulling the latest code, downloading the newest data
by hand, and running the scripts (and maybe getting different versions of
things), one setup() script does it the same way every time. It's also
useful when someone new joins the team or gets a new laptop, when we need
to re-run an old analysis from scratch to check a result, or if we want to
run it automatically on a server instead of on someone's machine.
=== END OF Q2a ANSWER ===

Do you see an alternative to using a script like setup()?

=== ANSWER Q2b BELOW ===
A few options:
- Schedule it: have a cron job or a GitHub Actions workflow run the
  pipeline every two weeks automatically, so no one has to remember.
- Use a container (a Docker image) with the code and dependencies already
  installed, so everyone runs the exact same environment.
- Use a workflow/pipeline tool (like Make, Airflow, or DVC) that knows the
  steps and their dependencies and only re-runs what changed.
- Keep the data in a shared database or cloud storage bucket instead of
  having everyone download their own copy.
- Or just do it manually with a written checklist. That works for a small
  team, but it's easy to make mistakes.
=== END OF Q2b ANSWER ===

3.
Now imagine we have to re-think our script to
work on a brand-new machine, without any software installed.
(For example, this would be the case if you need to run
your pipeline inside an Amazon cloud instance or inside a
Docker instance -- to be more specific you would need
to write something like a Dockerfile, see here:
https://docs.docker.com/reference/dockerfile/
which is basically a list of shell commands.)

Don't worry, we won't test your code for this part!
I just want to see that you are thinking about how
shell commands can be used for setup and configuration
necessary for data processing pipelines to work.

Think back to HW0. What sequence of commands did you
need to run?
Write a function setup_for_new_machine() that would
be able to run on a brand-new machine and set up
everything that you need.

Assume that you need your script to work on all of the packages
that we have used in HW1 (that is, any `import` statements
and any other software dependencies).

Assume that the new server machine is identical
in operating system and architecture to your own,
but it doesn't have any software installed.
It has Python 3.12
and conda or pip3 installed to get needed packages.

Hint: use subprocess again!

Hint: search for "import" in parts 1-3. Did you miss installing
any packages?
"""

def setup_for_new_machine():
    """
    Set up a brand-new Windows machine that only has Python 3.12 and pip.
    Not run as part of the pipeline (it installs software).
    """
    # Git is needed to clone the repo. Git for Windows also comes with the
    # Unix shell tools (cat, tail, wc) used by pipeline_shell() below.
    subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"], check=True)

    # Python packages imported in parts 1-3 (everything else is built in)
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install",
                    "pandas", "numpy", "matplotlib", "pytest", "requests"], check=True)

    # Get the homework code and data
    subprocess.run(["git", "clone", "https://github.com/DavisPL-Teaching/119-hw1"], check=True)

def q3():
    # As your answer, return a string containing
    # the operating system name that you assumed the
    # new machine to have.
    os_name = "Windows"
    return os_name

"""
4. This question is open ended :)
It won't be graded for correctness.

What percentage of the time do you think real data scientists
working in larger-scale projects in industry have to write
scripts like setup() and setup_for_new_machine()
in their day-to-day jobs?

=== ANSWER Q4 BELOW ===
My guess is around 10-20% of their time. Most of the job is probably
analysis, cleaning data, and meetings, but setup and environment problems
come up all the time: new projects, new team members, broken dependencies,
moving work onto cloud machines. At bigger companies there are often
platform/DevOps teams that handle a lot of this, so a data scientist might
spend less time writing these scripts themselves, but they still have to
use and fix them.
=== END OF Q4 ANSWER ===

5.
Copy your setup_for_new_machine() function from Q3
(remove the other code in this file)
to a new script and run it on a friend's machine who
is not in this class. Did it work? What problems did you run into?

Only answer this if you actually did the above.
Paste the output you got when running the script on the
new machine:

If you don't have a friend's machine, please speculate about
what might happen if you tried. You can guess.

=== ANSWER Q5 BELOW ===
I didn't run it on a friend's machine, so this is a guess.
Things that would probably go wrong:
- winget might not be there or might need admin approval, so Git
  wouldn't install. Even if it did, the current terminal wouldn't see
  the new `git` command until it's restarted (PATH isn't updated), so the
  git clone step would fail on the first run.
- If my friend has a Mac or Linux, the winget line fails right away.
  The script assumes Windows.
- pip might install into a different Python than the one they actually
  use, or fail with a permissions error if it's a system-wide Python
  (a virtual environment would avoid that).
- I don't pin package versions, so they might get newer versions of
  pandas/matplotlib where something I use is deprecated or changed. (I
  actually hit a deprecation warning for boxplot's `labels` argument
  while doing part 1.)
- The shell pipeline in Q6 needs cat/tail/wc. On Windows those only exist
  if Git Bash's tools are on the PATH, so plain PowerShell/cmd wouldn't
  find them.
=== END OF Q5 ANSWER ===

===== Questions 6-9: A comparison of shell vs. Python =====

The shell can also be used to process data.

This series of questions will be in the same style as part 2.
Let's import the part2 module:
"""

import part2
import pandas as pd

"""
Write two versions of a script that takes in the population.csv
file and produces as output the number of rows in the file.
The first version should use shell commands and the second
should use Pandas.

For technical reasons, you will need to use
os.popen instead of subprocess.run for the shell version.
Example:
    os.popen("echo hello").read()

Runs the command `echo hello` and returns the output as a string.

Hints:
    1. Given a file, you can print it out using
        cat filename

    2. Given a shell command, you can use the `tail` command
        to skip the first line of the output. Like this:

    (shell command that spits output) | tail -n +2

    Note: if you are curious why +2 is required here instead
        of +1, that is an odd quirk of the tail command.
        See here: https://stackoverflow.com/a/604871/2038713

    3. Given a shell command, you can use the `wc` command
        to count the number of lines in the output

   (shell command that spits output) | wc -l

NOTE:
The shell commands above require that population.csv
has a newline at the end of the file.
Otherwise, it will give an off-by-one error
FYI, if this were not the case you can replace
    cat filename
with:
    (cat filename ; echo)
.
"""

POPULATION_FILE = "data/population.csv"

def pipeline_shell():
    # Skip the header line, then count the remaining lines
    output = os.popen(f"cat {POPULATION_FILE} | tail -n +2 | wc -l").read()
    return int(output)

def pipeline_pandas():
    df = pd.read_csv(POPULATION_FILE)
    return len(df)

def q6():
    # As your answer to this part, check that both
    # integers are the same and return one of them.
    shell_rows = pipeline_shell()
    pandas_rows = pipeline_pandas()
    assert shell_rows == pandas_rows, f"shell: {shell_rows}, pandas: {pandas_rows}"
    return shell_rows

"""
Let's do a performance comparison between the two methods.

Use use your ThroughputHelper and LatencyHelper classes
from part 2 to get answers for both pipelines.

Additionally, generate a plot and save it in
    output/part3-q7.png

7. Throughput
"""

def q7():
    # Return a list of two floats
    # [throughput for shell, throughput for pandas]
    # (in rows per second)
    num_rows = pipeline_pandas()
    h = part2.ThroughputHelper()
    h.add_pipeline("shell", num_rows, pipeline_shell)
    h.add_pipeline("pandas", num_rows, pipeline_pandas)
    throughputs = h.compare_throughput()
    h.generate_plot("output/part3-q7.png")
    return throughputs

"""
8. Latency

For latency, remember that we should create a version of the
pipeline that processes only a single row! (As in Part 2).
However, for this question only, it is OK if you choose to run
latency on the entire pipeline instead.

Additionally, generate a plot and save it in
    output/part3-q8.png
"""

def q8():
    # Return a list of two floats
    # [latency for shell, latency for pandas]
    # (in milliseconds)
    # As allowed for this question, latency is measured on the full pipeline.
    h = part2.LatencyHelper()
    h.add_pipeline("shell", pipeline_shell)
    h.add_pipeline("pandas", pipeline_pandas)
    latencies = h.compare_latency()
    h.generate_plot("output/part3-q8.png")
    return latencies

"""
9. Which method is faster?
Comment on anything else you notice below.

=== ANSWER Q9 BELOW ===
On my machine (Windows), Pandas was faster: about 1.7 million rows/s vs
about 0.6 million rows/s for the shell, and about 35 ms vs 100 ms latency.
I didn't expect that, since `wc -l` just counts newlines and doesn't parse
anything, while Pandas actually parses every row into a DataFrame.

To see why, I timed a few commands. Just running `echo hi` through
os.popen takes ~34 ms, `wc -l` on the file takes ~67 ms, and the full
`cat | tail | wc` takes ~100 ms. So each extra process in the pipe adds
about 30 ms, and almost all the shell's time is spent starting processes
(cmd.exe, then Git for Windows' versions of cat/tail/wc, which are slow
to start), not reading the file. Pandas runs inside the Python process
that's already open, so it has no startup cost.

Other things I noticed:
- `cat file | tail` is redundant. `tail -n +2 file | wc -l` (or just
  `wc -l` minus 1) does the same thing with fewer processes, and that
  should be faster.
- On Linux/Mac, where starting a process is much cheaper, I'd expect the
  shell version to win, especially on bigger files, because it streams
  the file and never stores it in memory.
- The shell version also depends on the file ending with a newline and
  on cat/tail/wc being installed, so the Pandas version is more portable
  even though it does more work.
=== END OF Q9 ANSWER ===
"""

"""
Unit tests: run with `pytest part3.py`.
"""

def test_pipeline_pandas():
    assert pipeline_pandas() == 59177

def test_shell_matches_pandas():
    assert pipeline_shell() == pipeline_pandas()

"""
===== Wrapping things up =====

**Don't modify this part.**

To wrap things up, we have collected
your answers and saved them to a file below.
This will be run when you run the code.
"""

ANSWER_FILE = "output/part3-answers.txt"
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

def PART_3_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    # Q1-5
    log_answer("q1", q1)
    # 2a: commentary
    # 2b: commentary
    log_answer("q3", q3)
    # 4: commentary
    # 5: commentary
    log_answer("q6", q6)
    log_answer("q7", q7)
    log_answer("q8", q8)
    # 9: commentary

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
=== END OF PART 3 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 3", PART_3_PIPELINE)
