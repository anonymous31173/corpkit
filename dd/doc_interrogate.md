---
layout: page
title: "Interrogate"
category: doc
date: 2015-08-30 22:08:28
order: 4
---

> `Interrogate` will iterate over subcorpora in a corpus, searching for the same thing, and tabulating the results.

<!-- MarkdownTOC -->

- [Selecting a corpus](#selecting-a-corpus)
- [Selecting a kind of data](#selecting-a-kind-of-data)
    - [Trees](#trees)
    - [Dependencies](#dependencies)
    - [Dependency grammars](#dependency-grammars)
    - [Search types](#search-types)
    - [Dependency options](#dependency-options)
    - [Plain text](#plain-text)
    - [Tokens](#tokens)
- [Special queries](#special-queries)
    - [Preset queries](#preset-queries)
    - [Query parts](#query-parts)
- [Lemmatisation](#lemmatisation)
- [Speaker IDs](#speaker-ids)
- [Naming an interrogation](#naming-an-interrogation)
- [Running interrogations](#running-interrogations)
- [Editing spreadsheets](#editing-spreadsheets)
- [Making dictionaries](#making-dictionaries)
- [Next steps](#next-steps)

<!-- /MarkdownTOC -->


## Selecting a corpus

If you were working in the `Build` tab, `corpkit` will try to guess the corpus you want to interrogate. If a corpus hasn't been selected, or you'd like to interrogate a different corpus, you can select it now. Corpora can also be selected via the File menu.

## Selecting a kind of data

`corpkit` can presently work with three kinds of data:

1. Constituency parse trees
2. Dependency parses
3. Plain text
4. Tokenised corpora

The first two can both be found inside the parsed version of a corpus. The third is the unparsed version of the corpus. The fourth is your corpus as a list of tokens, which can be created via the `Build` tab.

When you select a kind of data, the kinds of search that are available to you change, as do the kinds of queries that can be understood. These will be explained in the next secitons.

### Trees

If you want to search for information in `trees`, you need to write a Tregex query. Tregex is a language for searching syntax trees like this one:

<p align="center">
<img src="https://raw.githubusercontent.com/interrogator/sfl_corpling/master/images/const-grammar.png"  height="400" width="400"/>
</p>

To write a Tregex query, you specify **words and/or tags** you want to match, in combination with **operators** that link them together.

To match any adjective, you can simply write:

> `JJ`

If you want to get NPs containing adjectives, you might use:

> `NP < JJ`
 
Where `<` means `with a child/immediately below`. These operators can be reversed: If we wanted to show the adjectives within these NPs only, we could use:

> `JJ > NP`

It's good to remember that the output will always be the left-most part of your query.

If you only want to match Subject NPs, you can use bracketting, and the `$` operator, which means `sister/directly to the left/right of`:

> `JJ > (NP $ VP)`

In this way, you build more complex queries. The query below finds adjectives modifying `book`:

> `JJ > (NP <<# /book/)`

Notice that here, we have a different kind of operator. The `<<` operator means that the node on the right does not need to be a child, but can be a descendent. the `#` means `head`---that is, in SFL, it matches the `Thing` in a Nominal Group.

If we wanted to also match `magazine` or `newspaper`, there are a few different approaches. One way would be to use `|` as an operator meaning `or`:

> `JJ > (NP ( <<# /book/ | <<# /magazine/ | <<# /newspaper/))`

This can be cumbersome, however. Instead, we could use a [*Regular Expression*](http://www.regular-expressions.info):

> `JJ > (NP <<# /^(book|newspaper|magazine)s*$/)`

Though it is unfortunately beyond the scope of this guide to teach Regular Expressions, it is important to note that Regular Expressions are extremely powerful ways of searching text, and are invaluable for any linguist interested in digital datasets.

Detailed documentation for Tregex usage (with more complex queries and operators) can be found [here](http://nlp.stanford.edu/~manning/courses/ling289/Tregex.html). If you want to learn Regular Expressions, there are hundreds of free resources online, including [Regular Expression Crosswords](http://regexcrossword.com/)!

If your searches aren't matching what you think they should, you might want to look at how your data has been parsed. Head to the `Build` tab and select your parsed corpus. You can then open up a file, and view its parse trees. These visualisations make it much easier to understand how Tregex queries work.

#### Tree searching options
 
When searching with trees, there are a few extra options available.

`Multiword results` informs `corpkit` that you expect your results to be more than one word long (if you are searching for VPs, for example). This causes `corpkit` to do tokenisation of results, leading to overall better processing.

When working with multiple word results, `Filter titles` will remove `Mr`, `Mrs`, `Dr`, etc. to help normalise and count references to specific people.

### Dependencies

In dependency grammar, words in sentences are connected in a series of governor--dependent relationships. The Predicator is typically the `root` of a sentence, which may have the head of the Subject as a dependent. The head of the subject may in turn have dependants, such as adjectival modifiers or determiners.

<p align="center">
<img src="https://raw.githubusercontent.com/interrogator/sfl_corpling/master/images/dep-grammar.png"  height="60" width="400"/>
</p>

The best source of information and dependency relationships is the [Stanford Dependencies manual](http://nlp.stanford.edu/software/dependencies_manual.pdf).

### Dependency grammars

Your data has actually been annotated with three slightly different dependency grammars. You can choose to work with:

1. Basic dependencies
2. Collapsed dependencies
3. Collapsed dependencies with conjunctions collapsed too

For more information on the dependency grammars, you can look at section 4 of the [Stanford Dependencies manual](http://nlp.stanford.edu/software/dependencies_manual.pdf#page=12).

### Search types

There are many potentially interesting things in dependency annotations, and, accordingly, many different kinds of search available for them. 

The different options match and print different combinations of *governors*, *dependents* and *relationships*. In each case, the kind of query you'll write is a Regular Expression or list.

Below is a basic explanation of what each kind of query matches, and what it outputs.

| Search type            | Query matches | Output                             |
|------------------------|----------|-----------------------------------------|
| Get role of match      | Token   |  Token's role                            |
| Get lemmata of match   | Token   |  Token's lemma form                      |
| Get tokens             | Token   |  Token                                   |
| Get tokens by role     | Role    |  Role's dependent                        |
| Get distance from root | Token   |  Number of steps away from root position |
| Get "role:dependent", matching governor  |  Governor  | role:dependent      |
| Get "role:governor", matching dependent  |  Dependent | role:governor       |

### Dependency options

Dependency queries can also be filtered, so that only results matching a given role or part-of-speech are returned. Both of these fields are regular expressions or lists.

For the `role:governor` and `role:dependent` search options, if you use a function filter, the `role:` portion of the output is not printed.

### Plain text

Plain text is the simplest kind of search. You can either use Regular Expressions or simple search. When writing simple queries, you can search for a list of words by entering:

> `[cat,dog,fish]`

Using regular expressions, you could do something more complex, like get both the singular and plural forms:

> `(cats?|dogs?|fish)`

This kind of search has drawbacks, though. Lemmatisation, for example, will not work very well, because `corpkit` won't know the word classes of the words you're finding.

### Tokens

As with plain text, you can use either a list of a regular expression to match tokens.

> More coming soon

## Special queries

`corpkit` also has some pre-programmed queries and query parts, based mostly around concepts from systemic-functional grammar. 

### Preset queries

`'Any'` will match any word, tag or function, depending on the search type. `Participants` and `Processes` approximate notions from systemic functional grammar. 

`Stats` will get the absolute frequencies for different moods and process types. It involves many sub-interrogations (for different process types and grammatical moods, mostly), and may take a long time.

### Query parts

There are also some things you can type into your query that `corpkit` recognises and handles differently. You can, for example, enter

> `PROCESSES:VERBAL`

to match any token corresponding to a verbal process (including all possible inflections). This can be powerful when used in conjunction with Tregex or dependency queries:

> `VP <<# /PROCESSES:MENTAL/ $ NP`
 
will get verbal groups that contain mental process types.

Currently, the special query types are:

| Special query kind -| Matches           |
|---------------------|-------------------|
| `PROCESSES:`        | Tokens            |
| `ROLES:`            | CoreNLP functions |
| `WORDLISTS:`        | Tokens            |

Each special query type has a number of possible subtypes:

* `WORDLISTS:` recognises `PRONOUNS`, `ARTICLES`, `CONJUNCTIONS`, `DETERMINERS`, `PREPOSITIONS`, `CONNECTORS`, `MODALS`, `CLOSEDCLASS` and `TITLES`.
* `ROLES:` recognises `ACTOR`, `ADJUNCT`, `AUXILIARY`, `CIRCUMSTANCE`, `CLASSIFIER`, `COMPLEMENT`, `DEICTIC`, `EPITHET`, `EVENT`, `EXISTENTIAL`, `GOAL`, `MODAL`, `NUMERATIVE`, `PARTICIPANT`, `PARTICIPANT1`, `PARTICIPANT2`, `POLARITY`, `PREDICATOR`, `PROCESS`, `QUALIFIER`, `SUBJECT`, `TEXTUAL` and `THING`.
* `PROCESSES:` recognises `MENTAL`, `VERBAL` and `RELATIONAL`.

When using dependencies, you could get *Sensers* by searching for the role and dependent of `PROCESSES:MENTAL`, and then by using a function filter for `ROLES:PARTICIPANT1`.

## Lemmatisation

When working with dependencies, lemmatisation is handled by Stanford CoreNLP. When searching trees, WordNet is used.

If searching trees and using lemmatisation, `corpkit` will try to determine the word class you're searching for by looking at the first part of your Tregex query. If your query is:

> `/VB.?/ >> VP`

then `corpkit` will know that the output will be verbs. If lemmatisation of trees isn't working as expected, you can use the `Result word class` option to force `corpkit` to treat all results as a given part of speech.

## Speaker IDs

If you have used the `speaker segmentation` option, you can restrict your searches to specific speakers. You can use `shift+click` or `ctrl+click` to select multiple speaker IDs. Speaker IDs may slow down tree-based searching quite a lot, so if you don't care too much about them, leave the option as `False`, rather than `ALL`.

If you have selected `ALL` speakers, or have highlighted more than one, multiple interrogations will be performed, with the speaker ID appended to the interrogation name. Only one of these results will be shown as a spreadsheet, but you can use `Previous` and `Next` to navigate between them.

## Naming an interrogation

You are given the option of naming your interrogation. You don't *have to* to do this, but it will help you keep track of which interrogations contain which kinds of data.

If you forgot to name an interrogation before running it, you can head to the `Manage` tab to rename it at any time.

## Running interrogations

On large datasets, interrogations can take some time, especially for dependency searches with many options. Speaker IDs also come at the cost of speed. Be patient!

Be sure to name your interrogation, via the `Name interrogation` box. This makes it much easier to know at a glance what you'll be editing, plotting or exporting.

> Whenever you run an interrogation that produces results, all options used to generate the query are stored, and accessible via the `Manage` tab. You can head there to access previous queries, or to save interrogations to disk.

## Editing spreadsheets

Once results have been generated, the spreadsheets on the right are populated. Here, you can edit numbers, move columns, or delete particular results or subcorpora. You can flip back and forward between other interrogations with the `Previous` and `Next` buttons.

If you manually edit the results in either the results or totals spreadsheet, you can hit `'Update interrogation'` to update the version of the data that is stored in memory.

It's important to remember that the results and totals spreadsheets do not communicate with one another. As such, if you are adding or subtracting from individual results, you'd need to update the total results part to reflect these changes. 

Sorting the result order is performed in the edit window.

## Making dictionaries

If you want, you can use the `Save as dictionary` button to generate a reference corpus from an interrogation, comprised of each word and its total frequency. This will be stored in the `dictionaries/` folder of the project. Every dictionary file in this directory can be loaded when doing keywording in the `Edit` tab.

## Next steps

It can be hard to learn anything interesting from absolute frequencies alone. Generally, you'll next want to go to the `Edit` tab to modify the results into something more informative.