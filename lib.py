#!/usr/bin/python

import pywikibot
import mwparserfromhell

itwiki = pywikibot.Site('it', 'wikipedia')
repo = itwiki.data_repository()

claim = pywikibot.Claim(repo, 'p143')
claim.setTarget(pywikibot.ItemPage(repo, 'Q11920'))


def gen(resume=None):
    cat = pywikibot.Category(itwiki, 'Category:BioBot')
    if resume:
        g = cat.articles(namespaces=[0], content=True, sortby='sortkey', startsort=resume)
    else:
        g = cat.articles(namespaces=[0], content=True, sortby='sortkey')
    for art in g:
        yield art


def get_templates(text):
    code = mwparserfromhell.parse(text)
    for temp in code.filter_templates():
        if temp.name.lower().strip() == 'bio':
            return temp


def log(param, value, page):
    pg = u'User:Legobot/itwiki persondata/' + param
    pg = pywikibot.Page(repo, pg)
    if pg.exists():
        text = pg.get()
    else:
        text = ''
    text += u'\n*On [[w:it:{0}]], encountered a value of "{1}"'.format(page.title(), value)
    pg.put(text, 'Adding new error report')
