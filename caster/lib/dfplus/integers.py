from dragonfly.language.base.integer_internal import MapIntBuilder, MagnitudeIntBuilder, IntegerContentBase, CollectionIntBuilder
from dragonfly.language.loader import language
from dragonfly.language.base.integer import Integer
from dragonfly.grammar.elements_basic import RuleWrap
from dragonfly import Choice

int_0           = MapIntBuilder({
                                 "zero":       0,
                               })
int_1_9         = MapIntBuilder({
                                 "one":        1,
                                 "two":        2,
                                 "three":      3,
                                 "four":       4,
                                 "five":       5,
                                 "six":        6,
                                 "seven":      7,
                                 "eight":      8,
                                 "nine":       9,
                               })
int_10_19       = MapIntBuilder({
                                 "ten":       10,
                                 "eleven":    11,
                                 "twelve":    12,
                                 "thirteen":  13,
                                 "fourteen":  14,
                                 "fifteen":   15,
                                 "sixteen":   16,
                                 "seventeen": 17,
                                 "eighteen":  18,
                                 "nineteen":  19,
                               })
int_20_90_10    = MapIntBuilder({
                                 "twenty":     2,
                                 "thirty":     3,
                                 "forty":      4,
                                 "fifty":      5,
                                 "sixty":      6,
                                 "seventy":    7,
                                 "eighty":     8,
                                 "ninety":     9,
                               })
int_20_99       = MagnitudeIntBuilder(
                   factor      = 10,
                   spec        = "<multiplier> [<remainder>]",
                   multipliers = [int_20_90_10, int_1_9],
                   remainders  = [int_1_9],
                  )
int_and_1_99    = CollectionIntBuilder(
                   spec        = "[and] <element>",
                   set         = [int_1_9, int_10_19, int_20_99],
                  )
int_100s        = MagnitudeIntBuilder(
                   factor      = 100,
                   spec        = "<multiplier> [hundred] [<remainder>]",
                   multipliers = [int_1_9],
                   remainders  = [int_and_1_99],
                  )
int_100big      = MagnitudeIntBuilder(
                   factor      = 100,
                   spec        = "<multiplier> [hundred] [<remainder>]",
                   multipliers = [int_10_19, int_20_99],
                   remainders  = [int_and_1_99]
                  )
int_1000s       = MagnitudeIntBuilder(
                   factor      = 1000,
                   spec        = "<multiplier> [thousand] [<remainder>]",
                   multipliers = [int_1_9, int_10_19, int_20_99, int_100s],
                   remainders  = [int_and_1_99, int_100s]
                  )
int_1000000s    = MagnitudeIntBuilder(
                   factor      = 1000000,
                   spec        = "<multiplier> [million] [<remainder>]",
                   multipliers = [int_1_9, int_10_19, int_20_99, int_100s, int_1000s],
                   remainders  = [int_and_1_99, int_100s, int_1000s],
                  )


#------------------------------------------------

class IntegerContent(IntegerContentBase):
    builders = [int_0, int_1_9, int_10_19, int_20_99,
                int_100s, int_100big, int_1000s, int_1000000s]


#------------------------------------------------
# Integer reference class.

class IntegerRefMF(RuleWrap):
    def __init__(self, name, min, max, default=None):
        element = Integer(None, min, max, content=IntegerContent)
        RuleWrap.__init__(self, name, element, default=default)

#--------------------------------------------------

class ShortIntegerRefNo8(RuleWrap):
    def __init__(self, name, min, max, default=None):
        content = language.ShortIntegerContent

        content.builders[1] = MapIntBuilder({
                                 "one"  : 1,
                                 "two"  : 2,
                                 "three": 3,
                                 "four" : 4,
                                 "five" : 5,
                                 "six"  : 6,
                                 "seven": 7,
                                 "eigen": 8,
                                 "nine" : 9,
                               })

        element = Integer(None, min, max, content=content)
        RuleWrap.__init__(self, name, element, default=default)

class IntegerRef(RuleWrap):
    def __init__(self, name, min, max, default=None):
        content = language.IntegerContent
        content.builders[1] = MapIntBuilder({
                                 "one"  : 1,
                                 "two"  : 2,
                                 "three": 3,
                                 "four" : 4,
                                 "five" : 5,
                                 "six"  : 6,
                                 "seven": 7,
                                 "eight": 8,
                                 "nine" : 9,
                               })

        element = Integer(None, min, max, content=content)
        RuleWrap.__init__(self, name, element, default=default)

class ShortIntegerRef(RuleWrap):
    def __init__(self, name, min, max, default=None):
        content = language.ShortIntegerContent
        content.builders[1] = MapIntBuilder({
                                 "one"  : 1,
                                 "two"  : 2,
                                 "three": 3,
                                 "four" : 4,
                                 "five" : 5,
                                 "six"  : 6,
                                 "seven": 7,
                                 "eight": 8,
                                 "nine" : 9,
                               })

        element = Integer(None, min, max, content=content)
        RuleWrap.__init__(self, name, element, default=default)

def TestInteger(name, min, max, default=None):
  return Choice(name, {str(i): i for i in range(min, max)}, default=default)

# IntegerRef = TestInteger
# ShortIntegerRef = TestInteger
