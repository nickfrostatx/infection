Infection
=========

[![Build Status](https://api.travis-ci.com/nickfrostatx/infection.svg?token=YeitCXiqqz9YFA7WLxxh)](https://travis-ci.com/nickfrostatx/infection)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/nickfrostatx/infection/master/LICENSE)

> A take-home interview question for Khan Academy.

You can find the code in [``infection.py``](infection.py).

Writeup
-------

Take-home interview, you say? Alright, we can do this.

So looking at the spec, we've got a graph of coaching relationships. Since any
user can coach any other user, there's no concept of someone being always a
"coach" and someone else only a "student", so unfortunately this isn't a nice
bipartite graph.

Total Infection sounds like a quick graph traversal. Shouldn't be too bad.
