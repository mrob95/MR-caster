from caster.imports import *

class OutlookRule(MergeRule):
    pronunciation = "outlook"
    mcontext = AppContext(executable="outlook")

    mapping = {
        # create new thing
        "new (appointment | event)": Key("sc-a"),
        "new contact": Key("cs-c"),
        "new folder": Key("cs-e"),
        "advanced (search| find)": Key("cs-f"),
        "new office document": Key("cs-h"),
        "(inbox | go to inbox)": Key("cs-i"),
        "new journal entry": Key("cs-j"),
        "new task": Key("cs-k"),
        "new contact group": Key("cs-l"),
        "(new message| new mail)": Key("cs-m"),
        "new note": Key("cs-n"),
        "open the new search folder window": Key("cs-p"),
        "new meeting request": Key("cs-q"),
        "new task request": Key("cs-u"),

        # new message window
        "to field": Key("a-dot"),
        "c c field": Key("a-c"),
        "subject [field]": Key("a-u"),
        "subject <text>": Function(lambda text:Key("a-u") + Text(text.capitalize()) + Key("tab")),
        "attach file": Key("n, a, f"),
        "add to textionary": Key("s-f10/2, a"),
        "click send message": Key("a-s"),  # be careful
        "find and replace": Key("c-h"),
        "check names": Key("c-k"),
        "spell check": Key("f7"),
        "save as": Key("f12"),  # only in mail view

        # folders pane
        "expand [that]": Key("asterisk"),
        "collapse [that]": Key("minus"),

        # folders navigation
        # some of these may be user dependent, depends on the order of your folders
        # which you can inspect by pressing control y
        # also I think some of these are built into Dragon
        "[go to] sent mail": Key("c-y/10, s, enter"),
        "go to drafts": Key("c-y/10, d, enter"),
        "go to trash": Key("c-y/10, t, enter"),
        "go to spam": Key("c-y/10, s:2, enter"),
        "go to starred": Key("c-y/10, s:3, enter"),
        "go to important": Key("c-y/10, i:2, enter"),
        "go to outbox": Key("cs-o"),

        # center pane
        "sort by [<sort_by>]": Key("a-v/5, a, b/5, %(sort_by)s"),
        "reverse sort": Key("a-v, r, s"),
        "block sender": Key("a-h/3, j/3, b"),
        "search [bar] [<text>]": Key("c-e") + Text("%(text)s"),
        "(message list | messages)": Key("tab:3"),
        "(empty | clear) search [bar]": Key("c-e, c-a, del/3, escape"),
        # from the search bar to get the focus into the messages is three tabs
        # pressing escape also seems to work.
        "refresh [mail]": Key("f9"),

        # reading pane
        "open attachment": Key("s-tab, enter"),
        "[open] attachment menu": Key("s-tab, right"),
        "next message [<n>]": Key("s-f6/10, down:%(n)s"),
        "(prior | previous) message [<n>]": Key("s-f6/10, up:%(n)s"),

        # calendar
        "workweek [view]": Key("ca-2"),
        "full week [view]": Key("ca-3"),
        "month view": Key("ca-4"),

        # message shortcuts
        "reply": Key("c-r"),
        "reply all": Key("cs-r"),
        "forward": Key("c-f"),
        "Mark [as] read": Key("c-q"),
        "Mark [as] unread": Key("c-u"),
        "(folder | go to folder)": Key("c-y"),

        # navigation
        "next pane [<n>]": Key("f6:%(n)s"),
        "(un|prior|previous) pane [<n>]": Key("s-f6:%(n)s"),
        "mail view": Key("c-1"),
        "calendar": Key("c-2"),
        "contacts": Key("c-3"),
        "tasks": Key("c-4"),
        "go to notes": Key("c-5"),
        "folder list": Key("c-6"),
        "find contact": Key("f11"),
        "address book": Key("cs-a"),
        "next open message": Key("c-dot"),
        "(prior | previous) open message": Key("c-comma"),
        "previous view": Key("a-left"),
        "next view": Key("a-right"),

        # misc
        "[go] back": Key("a-left"),
    }
    extras = [
        Choice(
            "sort_by", {
                "date": "d",
                "from": "f",
                "to": "t",
                "size": "s",
                "subject": "j",
                "type": "t",
                "attachments": "c",
                "account": "o",
            }, ""),
    ]

control.non_ccr_app_rule(OutlookRule())
"""
Command-module for Microsoft Outlook
Note (from Alex Boche 2019): In my opinion, Microsoft Outlook probably most Dragon-friendly email application.
All text fields are full text control, and all of the menus should be say-what-you-see natively in Dragon.
A good alternative to using Outlook is to use an e-mail website in Chrome or Firefox since these applications
support Wolfmanstout's accessibility API commands which can replace full text control.
Outlook users may want to consider purchasing Voice Computer which provides good numbering software
for the buttons and text fields in Outlook although a free and better alternative
to Voice Computer may be coming soon.
"""
