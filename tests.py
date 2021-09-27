"""
The testing class and functions for this module

You can run this with e.g. nosetests, or run it as a python executable
"""
import sys, nose


class test_twocrows:
    _TC=None
    _TC2=None

    def setup(self):
        import twocrows as tc
        self._TC = tc.twocrows()
        """
        Test that my class learns correctly
        """
        self._TC.learn("The River Temarc in Winter", "stop")
        self._TC.learn("*%^#*(@Mowgli, his cHildhood Home", "--=   tHe j*ungle")
        nose.tools.eq_(len(self._TC.lex()),2)
        nose.tools.eq_(self._TC.lex(),{'mowgli his childhood home': 'the jungle', 'the river temarc in winter': 'stop'})
        self._TC.learn("In the middle of the night", "I go walking in my sleep")
        # Add some poison, in case of crossover
        self._TC2 = tc.twocrows()
        nose.tools.eq_(self._TC2.lex(),{})
        self._TC2.learn("this should not be translated", "poisoned")
        nose.tools.eq_(len(self._TC2.lex()),1)
        nose.tools.eq_(self._TC2.lex(),{'this should not be translated': 'poisoned'})
        #check for poison
        nose.tools.eq_(len(self._TC.lex()),3)

    def test_persist(self):
        """
        Test that my class learns correctly
        """
        nose.tools.eq_(len(self._TC.lex()),3)
        nose.tools.eq_(self._TC.lex(),{'mowgli his childhood home': 'the jungle', \
            'the river temarc in winter': 'stop',\
               "in the middle of the night": "i go walking in my sleep" })

    def test_poision(self):
        """
        Test that my class does not accidentally poision other classes
        """
        nose.tools.eq_(len(self._TC2.lex()),1)
        nose.tools.eq_(self._TC2.lex(),{'this should not be translated': 'poisoned'})

    def test_simple(self):
        nose.tools.eq_(self._TC.translate_str("this should not be translated, Mowgli, his childhood home"), \
            "this should not be translated the jungle")
        
    def test_smart_single(self):
        nose.tools.eq_(self._TC.translate_first("this should not be translated, Mowgli, his childhood home"), \
            ("this should not be translated", "the jungle", None))
    
    def test_smart(self):
        nose.tools.eq_(self._TC.translate("this should not be translated, Mowgli, his childhood home"), \
            ["this should not be translated", "the jungle"])
    
    def test_smarter(self):
        nose.tools.eq_(self._TC.translate("this should not be translated, \
            Mowgli, his childhood home\
                The River Temarc Mowgli his childhood home in winter\
                    this should not be translated M()*owgli, his childhood home,\
                        The River Temarc in Winter"), \
            ['this should not be translated', 'the jungle', \
                'the river temarc', 'the jungle', \
                    'in winter this should not be translated', \
                        'the jungle', 'stop']
                        )
    def test_reverse(self):
        nose.tools.eq_(self._TC.translate_r("this should not be translated, \
            the jungle\
                the stop jungle\
                    this should not be translated M()*owgli, his childhood home,\
                        The River Temarc in Winter"), \
            [
                'this should not be translated', 'mowgli his childhood home',
                'the', 'the river temarc in winter',
                'jungle this should not be translated mowgli his childhood home ' 
                + 'the river temarc in winter']
                        )

if __name__ == '__main__':
    nose.runmodule()
