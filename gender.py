#!/usr/bin/python

import lib
import pywikibot
import wdapi

repo = lib.itwiki.data_repository()

prop = pywikibot.Claim(repo, 'P21')
male = pywikibot.ItemPage(repo, 'Q6581097')
female = pywikibot.ItemPage(repo, 'Q6581072')


def dictify(temp):
    data = {}
    for param in temp.params:
        data[unicode(param.name).strip().lower()] = unicode(param.value).strip()
    return data


def do_page(page, temp):
    print page
    params = dictify(temp)
    if not 'sesso' in params:
        return
    sex = params['sesso'].lower()
    if sex == 'm':
        target = male
    elif sex == 'f':
        target = female
    else:
        lib.log('sesso', sex, page)
        return

    item = pywikibot.ItemPage.fromPage(page)
    if not item.exists():
        item = wdapi.createItem(page)
    prop.setTarget(target)
    add, reason = wdapi.canClaimBeAdded(item, prop, checkDupe=True)
    if add:
        print 'Adding a claim...'
        item.addClaim(prop)
        prop.addSource(lib.claim)
    else:
        print 'Not adding because: "{0}"'.format(reason)


def main():
    #gen = lib.gen(resume='Aethelric di Deira')
    gen = lib.gen()
    for page in gen:
        text = page.get()
        temp = lib.get_templates(text)
        do_page(page, temp)

if __name__ == '__main__':
    main()