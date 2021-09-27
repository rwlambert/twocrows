"""
Simple python module for looking for strings within strings for known specific
 translations of idiomatic phrases or allagories.

 E.g. to build a block-wise translator for the Tamarian langage from star trek
 or similar kinds of situations

Usage:

Instantiate your class, and then teach it all the translations you know so far

>>> from twocrows import twocrows as tc
>>> mytc = tc()

>>> mytc.learn("to translate this idiomatic phrase", "into this one")

Then use this class to translate back and forth

>>> mytc.translate("to translate this idiomatic phrase")
["into this one"]

>>> mytc.translate_r("into this one")
["to translate this idiomatic phrase"]

This translation is greedy, in that it will start by looking for the longest string it 
can before looking for shorter options. It will translate all instances of those strings.

When using the translate and translate_r functions, what you will get
back is a _list_ of parts of the message in order, tokenized by what could be
translated and what could not be, e.g.

>>> tc.translate("please to translate this idiomatic phrase please thanks")
["please","into this one","please thanks"]


"""
##################################
#   Copyright 2021 Dr. R.W. Lambert PhD.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
##################################
import re, copy, pprint


class twocrows:
    """
    A class to hold a lexicon and to translate forwards
    """
    # the lexicon (dictionary) of translations I know already
    _known = None
    # a regex that removes special characters
    _sc = re.compile(r"[^a-zA-Z0-9 ]")
    def __init__(self, lexicon={}):
        """
        Initialize the class, with an empty lexicon,
        or clone in a lexicon, sanatizing the entries
        """
        self._known={}
        for k,v in lexicon.items():
            self.learn(k,v)
        self._known=copy.deepcopy(self._known)
        return
    
    def learn(self,s,means):
        "Add a new translation to the known list"
        self._known[self._sanatize(s)]=self._sanatize(means)

    def printlist(self):
        "print what I have learnt so far"
        pprint.pprint(self._known)
    
    def lex(self):
        "return a copy of what I have learnt so far"
        return copy.deepcopy(self._known)
    
    def lexicon(self):
        "return a copy of what I have learnt so far"
        return self.lex()
    
    def _sanatize(self,s):
        """
        Internal method to remove all special characters,
        move all text to lower,
        replace any long whitespace with single spaces,
        and not have any whitespace at the start or end
        """
        return ' '.join(self._sc.sub("",s.lower()).split()).strip()
    
    def translate_str(self,message):
        """Just replace everything in the string in a simple way,
        using the string.replace function"""
        translation = self._sanatize(copy.deepcopy(message))
        for k in sorted(self._known.keys(),key=len,reverse=True):
            translation = translation.replace(k,self._known[k])
        return translation.replace("  "," ").strip()
    
    def translate_first(self,remains,ready=False):
        """single step of translation to begin building a tree
        separate a string based upon the first thing found in the list
        return things from before the discovery, the translated thing, 
        then the things from afterwards, to enable building a list
        """
        if not ready:
            remains=self._sanatize(remains)
        before = None
        after = None
        #Here I am only trying to split remains into the first match
        for k in sorted(self._known.keys(),key=len,reverse=True):
            if len(k)>len(remains):
                continue
            p = remains.find(k)
            if p<0:
                continue
            if p>0:
                before = remains[:p].strip()
            e = p + len(k)
            if e<len(remains):
                after = remains[e:].strip()
            return before, self._known[k], after
        return None, None, remains
    
    def translate(self,message,ready=False):
        """build and flatten a tree of what has been translated
        E.g. Untranslatable Translatable Translatable untranslatable Translatable
        becomes
        ["Untranslatable","Translated","Translated","Untranslatable","Translated"]
        So you can know what is still remaining to translate
        """
        before=[]
        after=[]
        if not ready:
            message=self._sanatize(message)
        bi, ti, ai = self.translate_first(message,ready=True)
        # nothing to be found, skip it
        if ti is None:
            return before + [message] + after
        # iterate on tree to the left ... , and flatten
        if bi is not None and len(bi):
            before = before + self.translate(bi,ready=True)
        # iterate on tree to the right ..., and flatten
        if ai is not None and len(ai):
            after = self.translate(ai,ready=True)+after
        # return the list
        return before + [ti] + after
    
    def translate_r(self,message):
        "create a reversed version of myself, and use that to translate"
        lexr = {v:k for k,v in self._known.items()}
        tcr = twocrows(lexr)
        return tcr.translate(message)
