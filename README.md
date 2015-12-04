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

> build passing

Sweet.

Now let's get into the meat of the problem. I need to infect a subset of the
graph, optimizing for two factors: the number of nodes infected (aiming for a
specified target), and the minimal number of edges between infected and
uninfected nodes.

The spec suggests we can get exactly n nodes. I like a challenge, so let's do
that! (And this actually makes things "simpler", since we're only optimizing
one variable now.)

This sounds like graph coloring, but it isn't. In fact, a valid colored graph
would be the least optimal solution to this problem.

Actually, reading a little more, it turns out this is an improper vertex
coloring problem. There's a whole subclass of graph coloring problems in this
space, including defective coloring. However, that isn't an exact fit for our
problem.

I'm going to go a different direction for now. The spec says to fail if an exact
solution isn't possible. In context, I guess this means we're going to constrain
the problem to allow no two connected verticies to run different colors. That's
much easier.

This approach actually makes more sense. We don't care about infecting exactly
n nodes, we care about seamless user experience, while testing with *about* n
users on the new feature.

Let's break the our user graph down into connected components. We'll grab a
subset of these components to try to get close to n total users. The subset sum
problem is NP-complete, hence "this can be (really) slow" in the spec.
