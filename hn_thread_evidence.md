# HN Thread 46120611 – Python Data Science Handbook

Title: Python Data Science Handbook
URL: https://jakevdp.github.io/PythonDataScienceHandbook/
Score: 312

Total comments fetched: 61
Relevant comments retained: 52

## 46121830 by ellisv

These types of books are always interesting to me because they tackle so many different things. They cover a range of topics at a high level (data manipulation, visualization, machine learning) and each could have its own book. They balance teaching programming while introducing concepts (and sometimes theory).

In short I think it's hard to strike an appropriate balance between these but this seems to be a good intro level book.

## 46122067 by sschnei8

Interesting choice of Pandas in this day and age. Maybe he’s after imparting general concepts that you could apply to any tabular data manipulator rather than selecting for the latest shiny tool.

## 46122151 by xenophonf

What's wrong with Pandas?

## 46122158 by wiz21c

I wouldn't say it's a handbook because it's more like an introduction. But it's pretty well written.

## 46122249 by clickety_clack

I probably wouldn’t rewrite an entire data science stack that used pandas, but most people would use polars if starting a new project today.

## 46122294 by dahcryn

why? It's the industry standard as far as my reach goes.

What other framework would you replace it with?

No, polars or spark is not a good answer, those are optimized for data engineering performance, not a holistic approach to data science.

## 46122373 by farhanhubble

I loved his Statistics for Hackers talk: https:&#x2F;&#x2F;speakerdeck.com&#x2F;pycon2016&#x2F;jake-vanderplas-statistics...

## 46122464 by porker

> No, polars or spark is not a good answer, those are optimized for data engineering performance, not a holistic approach to data science.

Can you expand on why Polars isn't optimised for a holistic approach to data science?

## 46122588 by __rito__

This is one of the few books that I read cover-to-cover when I was starting out learning Data Science in 2020&#x2F;21. Will recommend.

## 46122829 by ayhanfuat

He is also the creator of the Altair visualization library (Vega-Lite in Python https:&#x2F;&#x2F;altair-viz.github.io&#x2F;). I really like using it.

## 46123029 by biofox

R and Matlab workflows have been fairly stable for the past decade. Why is the Python ecosystem so... unstable? It puts me off investing any time in it.

## 46123160 by crystal_revenge

You can assert whatever you want, but Polars is a great answer. The performance improvements are secondary to me compared to the dramatic improvement in interface.

Today all serious DS work will ultimately become data engineering work anyway. The time when DS can just fiddle around in notebooks all day has passed.

## 46123231 by trio8453

This book was absolute fire for getting started with data science in 2017-2018, Jake is a great teacher.

## 46123340 by phone_book

The linked Github seems to have the 2nd edition in the form of notebooks, https:&#x2F;&#x2F;github.com&#x2F;jakevdp&#x2F;PythonDataScienceHandbook&#x2F;blob&#x2F;ma..., under the Using Code Examples section, "attribution usually includes the title, author, publisher, and ISBN. For example: "Python Data Science Handbook, 2nd edition, by Jake VanderPlas (O’Reilly). Copyright 2023..." compared to the OP's link which has "The Python Data Science Handbook by Jake VanderPlas (O’Reilly). Copyright 2016..."

## 46123456 by amelius

Pandas turns 10x developers with a lust for life into 0.1x developers with grey hairs.

## 46123497 by fifilura

I have not work with Polars, but I would imagine any incompatibility with existing libraries (e.g. plotting libraries like plotnine, bokeh) would quickly put me off.

It is a curse I know. I would also choose a better interface. Performance is meh to me, I use SQL if i want to do something at scale that involves row&#x2F;column data.

## 46123523 by clickety_clack

The R ecosystem has had a similar evolution with the tidyverse, it was just a little further ago. As for Matlab, I initially learned statistical programming with it a long time ago, but I’m not sure I’ve ever seen it in the wild. I don’t know what’s going on there.

I’m actually quite partial to R myself, and I used to use it extensively back when quick analysis was more valuable to my career. Things have probably progressed, but I dropped it in favor of python because python can integrate into production systems whereas R was (and maybe still is) geared towards writing reports. One of the best things to happen recently in data science is the plotnine library, bringing the grammar of graphics to python imho.

The fact is that today, if you want career opportunities as a data scientist, you need to be fluent in python.

## 46123590 by rbartelme

This is a non-issue with Polars dataframes to_pandas() method. You get all the performance of Polars for cleaning large datasets, and to_pandas() gives you backwards compatibility with other libraries. However, plotnine is completely compatible with Polars dataframe objects.

## 46123593 by maleldil

You can always convert from Polars to Pandas. Plotnine will do it automatically for you, even.

## 46123633 by rbartelme

Outside bioconductor or the tidyverse in R can be just as unstable due to CRAN's package requirements.

## 46123864 by minimaxir

What can you do in more easily in pandas than polars?

## 46124108 by linhns

Thanks for the fact, I used Altair sometimes and really admire the simplicity, not knowing it was written by Jake.

## 46124552 by this_user

Pandas is widely adopted and deeply integrated into the Python ecosystem. Meanwhile, Polars remains a small niche, and it's one of those hype technologies that will likely be dead in 3 years once most of its users realise that it offers them no actual practical advantages over Pandas.

If you are dealing with huge data sets, you are probably using Spark or something like Dask already where jobs can run in the cloud. If you need speed and efficiency on your local machine, you use NumPy outright. And if you really, really need speed, you rewrite it in C&#x2F;C++.

Polars is trying to solve an issue that just doesn't exist for the vast majority of users.

## 46124881 by stdbrouw

Arguably Spark solves a problem that does not exist anymore: single node performance with tools like DuckDB and Polars is so good that there’s no need for more complex orchestration anymore, and these tools are sufficiently user-friendly that there is little point to switching to Pandas for smaller datasets.

## 46125420 by yboris

Amazing Thank you for sharing.

Reminds me of how thinking using frequencies rather than computing probabilities is easier and can avoid errors (e.g. a 99% accurate test being positive does not mean 99% likelihood of having disease for a disease with a 1&#x2F;10,000 prevalence in population).

## 46125445 by pantsforbirds

I used the Kernel Density Estimation (KDE) page&#x2F;blog at my very first job. It was immensely useful and I've loved his work ever since.

## 46126188 by minimaxir

> once most of its users realise that it offers them no actual practical advantages over Pandas

What? Speed and better nested data support (arrays&#x2F;JSON) alone are extremely useful to every data scientist.

My produtivity skyrocketed after switching from pandas to polars.

## 46126783 by crystal_revenge

> Pandas is widely adopted and deeply integrated into the Python ecosystem.

This is pretty laughable.  Yes there are very DS specific tools that make good use of Pandas, but `to_pandas` in Polars trivially solves this. The fact that Pandas always feels like injecting some weird DSL into existing Python code bases is one of the major reasons why I really don't like it.

> If you are dealing with huge data sets, you are probably using Spark or something like Dask already where jobs can run in the cloud. If you need speed and efficiency on your local machine, you use NumPy outright. And if you really, really need speed, you rewrite it in C&#x2F;C++.

Have you used Polars at all? Or for that matter written significant Pandas outside of a notebook? The number one benefit of Polars, imho, is that Polars works using Expressions that allow you to trivially compose and reuse fundamental logic when working with data in a way the works well with other Python code. This solves the biggest problem with Pandas is that it does not abstract well.

Not to mention that Pandas is really poor dataframe experience outside of it's original use case which was financial time series. The entire multi-inde

## 46127093 by crystal_revenge

"Data Science" has never been related to academic research, it has always emerged in a business context. I wouldn't say that researchers at Deep Mind are "data scientists", they are academic researchers who focus on shipping papers. If you're in a pure research environment, nobody cares if you write everything in Matlab.

But the last startup I was at tried to take a similar approach to research was unable to ship a functioning product and will likely disappear in a year from now. FAIR has been largely disbanded in favor of the way more shipping-centric MSL, and the people I know at Deep Mind are increasingly finding themselves under pressure to actually produce things.

Since you've been hanging out in an ivory tower then you might be unaware that during the peek DS frenzy (2016-2019) there were companies where data scientists were allowed to live entirely in notebooks and it was someone else's problem to ship their notebooks. Today if you have that expectation you won't last long at most companies, if you can even find a job in the first place.

On top of that, I know quite a few people at the major LLM teams and, based on my conversations, all of them are doing pretty serious da

## 46127323 by crystal_revenge

Pandas is generally awful unless you're just living in a notebook (and even then it's probably least favorite implementation of the 'data frame' concept).

Since Pandas lacks Polars' concept of an Expression, it's actually quite challenging to programmatically interact with non-trivial Pandas queries. In Polars the query logic can be entirely independent of the data frame while still referencing specific columns of the data frame. This makes Polars data frames work much more naturally with typical programming abstractions.

Pandas multi-index is a bad idea in nearly all contexts other than it's original use case: financial time series (and I'll admit, if you're working with purely financial time series, then Pandas feels much better). Sufficiently large Pandas code bases are littered with seemingly arbitrary uses of 'reset_index', there are many times where multi-index will create bugs, and, most important, I've never seen any non-financial scenario where anyone has ever used Multi-index to their advantage.

Finally Pandas is slow, which is honestly the least priority for me personally, but using Polars is so refreshing.

What other data frames have you used? Having used R's native

## 46127390 by crystal_revenge

I love R, but how can you make that claim when R uses three distinct object-oriented systems all at the same time? R might seem stable only because it carries along with it 50 years of history of programming languages (part of it's charm, where else can you see the generic function approach to OOP in a language that's still evolving?)

Finally, as someone who wrote a lot of R pre-tidyverse, I've seen the entire ecosystem radically change over my career.

## 46129287 by pid-1

Pandas is cancer. Please stop teaching it to people.

Everything it does can be done reasonable well with list comprehensions and objects that support type annotations and runtime type checking (if needed).

Pandas code is untestable, unreadable, hard to refactor and impossible to reuse.

Trillions of dollars are wasted every year by people having to rewrite pandas code.

## 46129504 by refactor_master

I honestly don't get why you'd hate pandas more than anything else in the Python ecosystem. It's probably not the best tool in the world, and sure, like everybody else I'd rewrite the universe in Rust if I could start over, and had infinite time to catch up.

But the code base I work on has thousands and THOUSANDS of lines of Pandas churning through big data, and I can't remember the last time it lead to a bug or error in production.

We use pandas + static schema wrapper + type checker, so you'll have to get exotic to break things.

## 46129720 by mttpgn

> Pandas code is untestable

The thousand-plus data integrity tests I've written in pandas tell a different story...

## 46130685 by physicsguy

I found Pandera quite good for wrapping input&#x2F;output expectations over Pandas. At the end of the day the vectorisation of operations in it and other table based formats mean they’re not easy to replace performantly.

## 46130828 by isolatedsystem

I've recently had to migrate over to Python from Matlab. Pandas has been doing my head in. The syntax is so unintuitive. In Matlab, everything begins with a `for` loop. Inelegant and slow, yes, but easy to reason about. Easy to see the scope and domain of the problem, to visualise the data wrangling.

Pandas insist you never use a for loop. So, I feel guilty if I ever need a throwaway variable on the way to creating a new column. Sometimes methods are attached to objects, other times they aren't. And if you need to use a function that isn't vectorised, you've got to do df.apply anyway. You have to remember to change the 'axis' too. Plotting is another thing that I can't get my head around. Am I supposed to use Pandas' helpers like df.plot() all the time? Or ditch it and use the low level matplotlib directly? What is idiomatic? I cannot find answers to much of it, even with ChatGPT. Worse, I can't seem to create a mental model of what Pandas expects me to do in a given situation.

Pandas has disabused me of the notion that Python syntax is self-explanatory and executable-pseudocode. I find it terrible to look at. Matlab was infinitely more enjoyable.

## 46131023 by runningmike

https:&#x2F;&#x2F;learningds.org&#x2F;intro.html  
Cc-by-nc-nd

## 46131030 by radus

Polars has a much more consistent API, give it a shot.

Regarding your plotting question: use seaborn when you can, but you’ll still need to know matplotlib.

## 46131428 by wesleywt

Maybe you are just bad at pandas.

## 46131431 by globular-toast

Can you write more about this? A lot of people use pandas where I work, whereas I'm completely fluent in list comprehensions and dataclasses etc. I had the impression it was doing something "more" like using numpy arrays&#x2F;matrices for columns.

## 46131445 by wesleywt

Nothing, it gets the job done for most people. If you don't like it, make a better tool. Polars is not it.

## 46131481 by mkl

Looks like it.  From https:&#x2F;&#x2F;jakevdp.github.io&#x2F;PythonDataScienceHandbook&#x2F;00.00-pr...:

> Copyright 2016

## 46131615 by jononor

Code using pandas is testable and reusable in much the same way as any other code, make functions that take and return data.

That said, the polars&#x2F;narwals style API is better than pandas  API for sure. More readable and composable, simpler (no index) and a bit less weird overall.

## 46131678 by jononor

The pandas workflows have also been stable for the last decade. That there is a new kid on the block (polars) does not make the existing stuff any less stable. And one can just continue writing pandas for the next decade too.

## 46131976 by jmpeax

Polars made the mistake of not maintaining row order for all operations, via the False-by-default argument of maintain_order. This is basically the billion-dollar null mistake for data frames.

## 46133305 by kelipso

Yeah, pandas is truly awful. After working with things like R, ggplot, data.table, you soon realize pandas is the worst dataframe analysis and plotting library out there.

I pretty much consider anyone who likes it to have Stockholm syndrome.

## 46133791 by fluidcruft

Mostly what's going on with Matlab in the wild is that it costs at least $10k a seat as soon as you are no longer at an academic institution.

Yes, there is Octave but often the toolboxes aren't available or compatible so you're rewriting everything anyway. And when you start rewriting things for Octave you learn&#x2F;remember what trash Matlab actually is as a language or how big a pain doing anything that isn't what Mathworks expects actually is.

To be fair: Octave has extended Matlab's syntax with amazing improvements (many inspired by numpy and R). It really makes me angry that Mathworks hasn't stolen Octave's innovations and I hate every minute of not being able to broadcast and having to manually create temp variables because you can't chain indexing whenever I have to touch actual Matlab. So to be clear Octave is somewhat pleasant and for pure numerical syntax superior to numpy.

But the siren call of Python is significant. Python is not the perfect language (for anything really) but it is a better-than-good language for almost everything and it's old enough and used by so many people that someone has usually scratched what's itching already. Matlab's toolboxes can't compet

## 46133993 by fifilura

A lot of people appreciate the declarative approach.

A for loop is a lot about the "how" but apply, join etc are much closer to the "what".

## 46134432 by jononor

Yeah that really should have been default. Very big footgun, especially when preserving ordering is default in pandas, numpy, etc. And especially when there is no ingrained index concept in polars, people might very well forget that one needs to have some natural keys and not rely on ordering. One needs to bring more of an SQL mindset.

## 46135422 by xenophonf

I initially considered using Pandas to work with community collections of Elite: Dangerous game data, specifically those published first by EDDB (RIP) and now by Spansh.  However, I quickly hit the maximum process memory limits because my naïve attempts at manipulating even the smallest of those collections resulted in Pandas loading GB-scale JSON data files into RAM.  I'm intrigued by Polars stated support for data streaming.  More professionally, I support the work of bioinformaticians, statisticians, and data scientists, so I like to stay informed.

I like how in Pandas (and in R), I can quickly load data sets up in a manner that lets me do relational queries using familiar syntax.  For my Elite: Dangerous project, because I couldn't get Pandas to work for me (which the reader should chalk up to my ignorance and not any deficiency of Pandas itself), I ended up using the SQLAlchemy ORM with Marshmallow to load the data into SQLite or PostgreSQL.  Looking back at the work, I probably ought to have thrown it into a JSON-aware data warehouse somehow, which I think is how the guy behind Spansh does it, but I'm not a big data guy (yet) and have a lot to learn about what's possible.

## 46155935 by refactor_master

Originally I used Pandera, but it had several issues last

* Mypy dependency and really bad PEP compliance
* Sub-optimal runtime check decorators
* Subclasses pd.DataFrame, so using e.g. .assign(...) makes the type checker think it's still the same type, but now you just violated your own schema

So I wrote my own library that solves all these issues, but it's currently company-internal. I've been meaning to push for open-sourcing it, but just haven't had the time.

## 46159156 by mayankkaizen

This was the solid book to get into data science and ML scene. Covers everything. Jake is a fantastic teacher. I really wish he comes up with updated second edition.

