Infection
=========

[![Build Status](https://api.travis-ci.com/nickfrostatx/infection.svg?token=YeitCXiqqz9YFA7WLxxh)](https://travis-ci.com/nickfrostatx/infection)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/nickfrostatx/infection/master/LICENSE)

> A take-home interview question for Khan Academy.

### [Live Demo](https://lit-basin-6396.herokuapp.com/)

The algorithms live in [``infection.py``](infection.py), if that's what you're
looking for.

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

For the implementation, I'm going to add an "infection" data structure, which
contains the users in the connected component, and the version of the site those
users should have.

Since we can get an approximate value for the number of users, we can
technically solve this problem in polynomial time, using an approximate solution
to the subset sum. We're completely throwing that whole "exactly n users" thing
out the window now.

Alright, that solution seems to work. Now I need to visualize the process. That
sounds like some [D3.js](http://d3js.org/) to me. A quick Flask app to run the
functions on the data and we should be set.

The [force layout](https://github.com/mbostock/d3/wiki/Force-Layout) seems to be
the method of choice for D3.js graph visualization. I need to generate a graph,
and Wikipedia says a simple way to do that is the [Erdős–Rényi model]
(https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93R%C3%A9nyi_model).

After a couple edge-case modifications, I'd call that a working demo!
