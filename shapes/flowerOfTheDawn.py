import pymel.core as pym
from connsFlower import conns
from shapes import iterConns, Shapes


def clearShapeSys():
    for ctl in conns:
        ctl = "_".join(ctl.split("_")[:-2])
        print ctl
        # oCtl = pym.PyNode(ctl)
        nodes = [
            ctl + "_wmDecomp",
            ctl + "_relativeX"
        ]
        for node in nodes:
            try:
                node = pym.PyNode(node)
            except pym.MayaNodeError:
                pass
            else:
                pym.delete(node)


def connectShapeSys():
    # baseTM = pym.PyNode("global_control_offgrp")
    globalInvTMM = pym.PyNode("global_control_invMatrix")
    for ctl in conns:
        ctl = "_".join(ctl.split("_")[:-2])
        print ctl
        oCtl = pym.PyNode(ctl)
        toGlobTMM = ctl + "_global_Matrix"
        try:
            relTMM = pym.PyNode(toGlobTMM)
        except pym.MayaNodeError:
            relTMM = pym.createNode("multMatrix", n=toGlobTMM)

        connsInM1 = [
            attr for attr in relTMM.attr("matrixIn[1]").inputs(p=True)
        ]
        connsInM2 = [
            attr for attr in relTMM.attr("matrixIn[2]").inputs(p=True)
        ]
        if not connsInM1:
            oCtl.attr("worldMatrix[0]").connect(relTMM.attr("matrixIn[1]"))
        if not connsInM2:
            globalInvTMM.outputMatrix.connect(relTMM.attr("matrixIn[2]"))

        ctlDecompName = ctl + "_decomp"
        try:
            ctlDecomp = pym.PyNode(ctlDecompName)
        except pym.MayaNodeError:
            ctlDecomp = pym.createNode("decomposeMatrix", n=ctlDecompName)

        connsInTMM = [
                attr for attr in ctlDecomp.inputMatrix.inputs(p=True)
        ]

        if not connsInTMM:
            relTMM.matrixSum.connect(ctlDecomp.inputMatrix)

        rsysName = ctl + "_result_sys"
        try:
            rsys = pym.PyNode(rsysName)
        except pym.MayaNodeError:
            rsys = pym.createNode("transform", n=rsysName)

        connsInTranslateX = [
                attr for attr in rsys.translateX.inputs(p=True)
        ]
        if not connsInTranslateX:
            ctlDecomp.outputTranslateX.connect(rsys.translateX)


def directConnect(factor):
    for ctl, chan, drv, tgt, alias, val in iterConns("MEm.shapes.connsFlower"):
        oCtl = pym.PyNode(ctl)
        oShape = Shapes(tgt)
        tgtAttr = oShape[alias]
        factorName = ctl + "_factorNode"
        factorNode = [
            node for node in oCtl.translateX.listConnections()
            if node.name() == factorName
        ]
        print "s:", factorNode
        if not factorNode:
            try:
                factorNode = pym.PyNode(factorName)
            except pym.MayaNodeError:
                factorNode = pym.createNode("multiplyDivide", n=factorName)
                factorNode = pym.PyNode(factorNode)
            print "c:", factorNode
            oCtl.translateX.connect(factorNode.input1X)
        else:
            factorNode = factorNode[0]

        print "o:", factorNode
        factorNode.input2X.set(factor)

        tgtNode = [
            attr for attr in factorNode.outputX.listConnections(p=True)
            if attr == tgtAttr
        ]
        print "factor2Tgt", tgtNode
        if not tgtNode:
            factorNode.outputX.connect(tgtAttr)
