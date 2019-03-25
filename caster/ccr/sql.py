'''
Created on Sep 2, 2015

@author: synkarius
'''
from dragonfly import Choice
from caster.lib.actions import Key, Text, Mouse

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class SQL(MergeRule):
    pronunciation = "sequel"

    mapping = {

        "lodge <logical>":
            R(Text("%(logical)s")),

        "<general>":
            R(Text("%(general)s")),

        "fun <function>":
            R(Text("%(function)s") + Key("left:2")),
    }

    extras = [
        Choice("logical", {
            "and":"AND ",
            "or":" OR ",
            "in":" IN ",
            "not":" NOT ",
        }),
        Choice("general", {
            "from":"FROM ",
            "select":"SELECT ",
            "select every":"SELECT *",
            "where":"WHERE ",
            "delete":"DELETE ",
            "update":"UPDATE",
            "insert into": "INSERT INTO ",

            "between":" BETWEEN ",
            "group by":"GROUP BY ",
            "not equals":" <> ",
            "like":"LIKE ",
            "not like":"NOT LIKE ",

            "order by":"ORDER BY ",
            "order ascending":"ASC ",
            "order descending":"DESC ",

            "left join":"LEFT JOIN ",
            "inner join":"INNER JOIN ",
            "right join":"RIGHT JOIN ",
            "full join":"FULL JOIN ",
            "normal join":"JOIN ",
            "on columns":"ON ",
            "union":"UNION ",
            "using":"USING ",

            "is null":" IS NULL",
            "is not null": " IS NOT NULL",
            "alias as":" AS ",
            "distinct":"DISTINCT ",
            "having": "HAVING ",
            "limit": "LIMIT ",
        }),
        Choice("function", {
            "average":"AVG() ",
            "count":"COUNT() ",
            "max":"MAX() ",
            "min":"MIN() ",
            "sum":"SUM() ",
        }),
    ]
    defaults = {}


control.nexus().merger.add_global_rule(SQL())
