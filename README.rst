The ngram module offers string similarity calculation and 
approximate string matching based on N-Grams.

Here is the documentation_ annd the tutorial_.

How does it work?
=================

The NGram class extents the Python set class with the ability 
to search for set members ranked by their N-Gram string similarity 
to the query. There are also methods for comparing a pair of strings.

The set stores arbitrary items by using a specified "key" function 
to produce the string representation of set members for the n-gram indexing.

N-grams are obtained by splitting strings into overlapping substrings
of N (usually N=3) characters in length.o

To find items similar to a query string, it splits the query into N-grams,
collects all items sharing at least one N-gram with the query,
and ranks the items by score based on the ratio of shared to unshared
N-grams between strings.


Credits
=======

The starting point was the Perl String::Trigram_ module by Tarek Ahmed.
In 2007, Michel Albert (exhuma) wrote the ngram module and submitted 2.0.0b2 to
Sourceforge. Since late 2008 python-ngram has been developed by Graham Poulter,
adding features, documentation, performance improvements and Python 3 support.

.. _documentation: http://packages.python.org/ngram/
.. _tutorial: http://packages.python.org/ngram/tutorial.html
.. _Trigram: http://search.cpan.org/dist/String-Trigram/

