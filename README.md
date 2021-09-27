# twocrows

A short excercise in python string manipulation to make a mini literal 
translation app

# why?

I was running a little role-playing game, where the group encountered a 
race of peoples reminiscent the tamarians from TNG, who spoke only in allegory 
i.e. using long idomatic phrases in the place of simple nouns and verbs.

The players requested a translation app they could use to make their
lives easier in terms of remembering the translations they already had worked out.

I thought this was a cool idea so I created a little python module as an excercise

# quick start

No non-standard requirements, python 3+ please.

Put the folder somewhere on your pythonpath.

See if it is working with the nosetests:
```bash
$ pip install nose
$ nosetests tests.py
```

import and run it:

```python
>>> from twocrows import twocrows as tc

>>> tc.learn("that this phrase should be translated", "to this one")

>>> tc.translate("that this phrase should be translated")
["to this one"]

>>> tc.translate_r("to this one")
["that this phrase should be translated"]
```

Try help on the class and its fuctions for more information.

Shared under Apache 2.0.

# greedy


When using the translate and translate_r functions, what you will get
back is a _list_ of parts of the message in order, tokenized by what could be
translated and what could not be, e.g.

```python
>>> tc.translate("please to translate this idiomatic phrase please thanks")
["please","into this one","please thanks"]
```


This translation is greedy, in that it will start by looking for the longest string it can before looking for shorter options. It will translate all instances of those strings.
