'''
See COPYRIGHT.md for copyright information.
'''
from collections import defaultdict
import os, datetime
from arelle import (ModelObject)

def setup(view):
    relsSet = view.modelXbrl.relationshipSet(view.arcrole, view.linkrole, view.linkqname, view.arcqname)
    view.concepts = {fact.concept for fact in view.modelXbrl.facts}
    view.linkroles = {
        rel.linkrole
        for c in view.concepts
        for rels in (relsSet.fromModelObject(c), relsSet.toModelObject(c))
        for rel in rels
    }

def setupLinkrole(view, linkrole):
    view.linkrole = linkrole
    relsSet = view.modelXbrl.relationshipSet(view.arcrole, view.linkrole, view.linkqname, view.arcqname)
    concepts = {
        c
        for c in view.concepts
        if relsSet.fromModelObject(c) or relsSet.toModelObject(c)
    }
    facts = {f for f in view.modelXbrl.facts if f.concept in concepts}
    contexts = {f.context for f in facts}

    view.periodContexts = defaultdict(set)
    contextStartDatetimes = {}
    view.dimensionMembers = defaultdict(set)
    view.entityIdentifiers = set()
    for context in contexts:
        if context.isForeverPeriod:
            contextkey = datetime.datetime(datetime.MINYEAR,1,1)
        else:
            contextkey = context.endDatetime
        objectId = context.objectId()
        view.periodContexts[contextkey].add(objectId)
        if context.isStartEndPeriod:
            contextStartDatetimes[objectId] = context.startDatetime
        view.entityIdentifiers.add(context.entityIdentifier[1])
        for modelDimension in context.qnameDims.values():
            if modelDimension.isExplicit:
                view.dimensionMembers[modelDimension.dimension] = modelDimension.member

    view.periodKeys = sorted(view.periodContexts.keys())
