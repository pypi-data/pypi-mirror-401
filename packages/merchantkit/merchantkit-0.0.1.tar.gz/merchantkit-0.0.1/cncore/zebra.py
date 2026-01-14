# This was originally written for the Hobby Engineering
# order processing and has been frunctional since around 2005.
# In 2021 bzBarcode was copied to the commercenode application,
# beginning a modernization.

import subprocess

PRODUCT_LABEL = "Product Label"
CARTON_LABEL = "Carton Label"
BAG_LABEL = "Bag Label"
BIN_BIG_LABEL = "Box LOC2 Label"
ADDRESS_LABEL = "Address Label"

PRINTER_FILE_NAMES = ["/dev/usb/lp1", "/dev/usb/lp0"]

PRINTER_1x2 = "Zebra_TLP2844"
PRINTER_3x5 = "Ups_LP2844"

# rotation 0=0, 1=90, 2=180, 3=270
# width_multiplier = 1-6 & 8
# height_multiplier = 1-9


class PrinterFont:
    __slots__ = ("width", "height")

    def __init__(self, width, height):
        self.width = width
        self.height = height


class PrinterSpecs:
    __slots__ = ("default_font", "dpi", "fonts")

    def __init__(self, dpi):
        self.default_font = None
        self.dpi = dpi
        self.fonts = {}

    def __getitem__(self, key):
        return self.fonts[str(key)]

    def add_font(self, name, font_spec):
        name = str(name)
        if self.default_font is None:
            self.default_font = name
        self.fonts[name] = font_spec


TLP2844_SPECS = PrinterSpecs(203)
TLP2844_SPECS.add_font(1, PrinterFont(8, 12))
TLP2844_SPECS.add_font(2, PrinterFont(10, 16))
TLP2844_SPECS.add_font(3, PrinterFont(12, 20))
TLP2844_SPECS.add_font(4, PrinterFont(14, 24))
TLP2844_SPECS.add_font(5, PrinterFont(32, 48))

BLACK_ON_WHITE = "N"
WHITE_ON_BLACK = "R"


class BarcodeEPL2:
    def __init__(self, printer_name):
        self.xOffsetDots = 200  # offset to start of label
        self.lineYDotsCur = 0
        self.lineYDotsNext = 0
        self.defaultLeftMarginDots = 30
        self.label_text = ""
        self.printer_name = printer_name
        self.printer_spec = TLP2844_SPECS

    def start_label(self):
        # N = clear printer buffer
        # q812 = label width 812, 4"
        # S2 = print 2 inches per second
        self.label_text = ".\nN\nq812\nS2\n"

    def end_label(self):
        # P1 = print one label
        self.label_text += "P1\n.\n"
        subprocess.run(
            ["lp", "-d", self.printer_name], input=self.label_text, text=True
        )

    def quote_text(self, text):
        result = []
        for this in text:
            if this in ['"', "\\"]:
                result.append("\\")
            result.append(this)
        return "".join(result)

    def print_text(
        self,
        x_position,
        y_position,
        text,
        font=None,
        rotation=0,
        width_multiplier=1,
        height_multiplier=1,
        color=BLACK_ON_WHITE,
    ):
        if x_position < 0:
            x_position = self.defaultLeftMarginDots
        if y_position < 0:
            y_position = self.lineYDotsNext
        self.lineYDotsCur = y_position
        if font is None:
            font = self.printer_spec.default_font
        font_spec = self.printer_spec[font]
        self.lineYDotsNext = self.lineYDotsCur + (100 + height_multiplier)
        text = self.quote_text(text)

        self.label_text += 'A{x},{y},{r},{f},{xmult},{ymult},{c},"{t}"\n'.format(
            x=x_position,
            y=y_position,
            r=rotation,
            f=font,
            xmult=width_multiplier,
            ymult=height_multiplier,
            c=color,
            t=text,
        )

    def print_barcode(
        self,
        x_position,
        y_position,
        parmText,
        BarcodeType="UA0",
        rotation=0,
        NarrowBar=3,
        WideBar=0,
        Size=100,
        HumanBN="B",
    ):
        if Size == 5:
            pass  # convert to upper case
        self.label_text += 'B%d,%d,%d,%s,%d,%d,%d,%s,"%s"\n' % (
            self.xOffsetDots + x_position,
            y_position,
            rotation,
            BarcodeType,
            NarrowBar,
            WideBar,
            Size,
            HumanBN,
            parmText,
        )


def MakeDateCode(parmDateYMD):
    wsYear = bzUtil.Int(parmDateYMD[:4])
    wsMo = bzUtil.Int(parmDateYMD[4:6])
    wsDay = bzUtil.Int(parmDateYMD[6:])
    wsDateCode = chr(ord("A") + wsYear - 2000)
    wsDateCode += chr(ord("F") + wsMo)
    if wsDay <= 26:
        wsDateCode += chr(ord("A") + wsDay - 1)
    else:
        wsDateCode += chr(ord("2") + wsDay - 27)
    return wsDateCode


#
# 2-1/4" x 1-1/4" Product Label
#
#
def PrintOneProductLabel(parmPtr, parmLabelInfo, parmVPack, parmDate):
    wsSku = parmLabelInfo[0]
    wsProductTitle = parmLabelInfo[2]
    wsLabelTitle = parmLabelInfo[3]
    if not wsLabelTitle:
        wsLabelTitle = wsProductTitle
    wsLabelTitle = wsLabelTitle[:20]
    wsLabelDesc1 = parmLabelInfo[4][:20]
    wsLabelDesc2 = bzUtil.Str(parmLabelInfo[5])
    wsLabelDesc2 = wsLabelDesc2[:20]
    wsPackSize = bzUtil.Int(parmLabelInfo[7])
    if wsPackSize < 1:
        wsPackSize = 1
    if parmVPack < 1:
        parmVPack = 1
    wsDateCodeRequired = parmLabelInfo[17]
    if wsDateCodeRequired == "Y":
        wsDateCodeRequired = True
    else:
        wsDateCodeRequired = False

    parmPtr.start_label()
    parmPtr.print_text(
        20, 235, wsSku[:6], Size=5, rotation=3, width_multiplier=1, height_multiplier=1
    )
    parmPtr.print_text(
        75, 125, wsSku[7:], Size=5, rotation=3, width_multiplier=1, height_multiplier=1
    )
    parmPtr.print_text(
        140, 20, wsLabelTitle, Size=2, width_multiplier=1, height_multiplier=1
    )
    if wsLabelDesc1:
        parmPtr.print_text(
            140, 40, wsLabelDesc1, Size=2, width_multiplier=1, height_multiplier=1
        )
    if wsLabelDesc2 != "":
        parmPtr.print_text(
            140, 60, wsLabelDesc2, Size=2, width_multiplier=1, height_multiplier=1
        )
    # wsPackSize = 1
    # parmVPack = 2
    # wsDateCodeRequired = False
    if (wsPackSize > 1) or (parmVPack > 0) or wsDateCodeRequired:
        wsMsg = ""
        if wsPackSize > 1:
            wsMsg += "Pack of %d" % (wsPackSize)
        if parmVPack > 1:
            if wsMsg:
                wsMsg += " "
            wsMsg += "VPACK %d*%d=%d" % (parmVPack, wsPackSize, parmVPack * wsPackSize)
        if wsDateCodeRequired:
            if wsMsg:
                wsMsg += " "
            wsMsg += "Lot: " + MakeDateCode(parmDate)
        # if wsMsg == "": wsMsg = "XXXXXX"
        wsMsg = wsMsg[:20]
        parmPtr.print_text(
            140, 100, wsMsg, Size=2, width_multiplier=1, height_multiplier=1
        )
    wsBarPartno = "%sV%d" % (wsSku, parmVPack)
    parmPtr.print_barcode(
        80, 140, wsBarPartno, BarcodeType="3", Size=70, NarrowBar=2, WideBar=4
    )
    parmPtr.end_label()


def PrintOneCartonLabel_P4x6(
    parmPtr,
    parmPartno,
    parmTitle,
    parmType,
    parmDesc1,
    parmDesc2,
    parmDate,
    parmLOC2,
    parmVPack,
    Mfr,
    MfrPartno,
):
    wsPartno = parmLabelInfo[0]
    wsLabelTitle = parmLabelInfo[3]
    wsLabelDesc1 = parmLabelInfo[4]
    wsLabelDesc2 = parmLabelInfo[5]
    wsLabelLOC2 = parmLabelInfo[11]
    wsLabelMfr = parmLabelInfo[13]
    wsLabelMfrPartno = parmLabelInfo[14]

    parmPtr.xOffsetDots = 10  # offset to start of label
    parmPtr.start_label()
    parmPtr.print_text(
        20, 20, "H" + parmPartno, Size=5, width_multiplier=4, height_multiplier=4
    )
    # parmPtr.print_text(20, 20, "H" + parmPartno, Size=5, width_multiplier=3, height_multiplier=3)
    parmPtr.print_text(
        20,
        240,
        "M" + bzUtil.Str(parmVPack),
        Size=5,
        width_multiplier=4,
        height_multiplier=4,
    )
    parmPtr.print_text(
        20, 500, parmTitle, Size=2, width_multiplier=4, height_multiplier=3
    )
    parmPtr.print_text(
        20, 580, "Date: " + parmDate, Size=3, width_multiplier=2, height_multiplier=2
    )
    parmPtr.print_text(
        20, 660, "LOC2: " + parmLOC2, Size=3, width_multiplier=2, height_multiplier=2
    )
    parmPtr.print_text(
        20,
        740,
        "Qty: " + bzUtil.Str(parmVPack),
        Size=3,
        width_multiplier=2,
        height_multiplier=2,
    )
    parmPtr.print_text(
        20,
        820,
        "Mfr: %s / %s" % (Mfr, MfrPartno),
        Size=3,
        width_multiplier=2,
        height_multiplier=2,
    )
    wsBarPartno = "H%sM%d" % (parmPartno, parmVPack)
    parmPtr.print_barcode(
        20, 900, wsBarPartno, BarcodeType="3", Size=240, NarrowBar=2, WideBar=4
    )
    parmPtr.end_label()


def PrintOneCartonLabel_L3x5(parmPtr, parmLabelInfo, parmDate):
    wsPartno = parmLabelInfo[0]
    wsLabelTitle = parmLabelInfo[3]
    wsLOC2 = parmLabelInfo[11]
    wsMfr = parmLabelInfo[13]
    wsMfrPartno = parmLabelInfo[14]
    wsMasterCartonSize = bzUtil.Int(parmLabelInfo[12])
    if wsMasterCartonSize < 1:
        wsMasterCartonSize = 1

    parmPtr.xOffsetDots = 200  # offset to start of label
    parmPtr.start_label()
    parmPtr.print_text(
        500,
        20,
        "H" + wsPartno,
        Size=5,
        width_multiplier=4,
        height_multiplier=4,
        rotation=1,
    )
    parmPtr.print_text(
        280,
        20,
        "M" + bzUtil.Str(wsMasterCartonSize) + "   LOC2: " + wsLOC2,
        Size=3,
        rotation=1,
    )
    parmPtr.print_text(230, 20, wsLabelTitle, Size=3, rotation=1)
    parmPtr.print_text(
        180,
        20,
        "Qty: " + bzUtil.Str(wsMasterCartonSize) + "  Date: " + parmDate,
        Size=3,
        rotation=1,
    )
    parmPtr.print_text(
        130, 20, "Mfr: %s / %s" % (wsMfr, wsMfrPartno), Size=3, rotation=1
    )
    wsBarPartno = "H%sM%d" % (wsPartno, wsMasterCartonSize)
    parmPtr.print_barcode(
        70,
        20,
        wsBarPartno,
        BarcodeType="3",
        Size=120,
        NarrowBar=2,
        WideBar=4,
        rotation=1,
    )
    parmPtr.end_label()


def PrintBinBigLabel_L3x5(parmLoc, parmParts):
    b = BarcodeEPL2()
    b.OpenPrinter(PRINTER_3x5)
    b.xOffsetDots = 200  # offset to start of label
    b.start_label()
    b.print_text(
        500, 20, parmLoc, Size=5, width_multiplier=3, height_multiplier=3, rotation=1
    )
    wsY = 325
    for wsThisPart in parmParts[:6]:
        b.print_text(
            wsY,
            20,
            wsThisPart[0] + "  " + wsThisPart[1][:20],
            Size=3,
            width_multiplier=2,
            height_multiplier=2,
            rotation=1,
        )
        wsY -= 50
    if parmParts[6:]:
        wsText = "..."
        for wsThisPart in parmParts[6:]:
            wsText += " " + wsThisPart[0]
        b.print_text(
            wsY, 20, wsText, Size=3, width_multiplier=2, height_multiplier=2, rotation=1
        )
    b.end_label()
    b.printer.close()


def PrintOneBagLabel_L3x5(parmPtr, parmLabelInfo, parmDate):
    wsSku = parmLabelInfo[0]
    wsLabelTitle = parmLabelInfo[2]
    wsX = wsLabelTitle.find('"')
    if wsX >= 0:
        wsLabelTitle = wsLabelTitle[:wsX] + wsLabelTitle[wsX + 1 :]
    wsPackSize = bzUtil.Int(parmLabelInfo[7])
    if wsPackSize < 1:
        wsPackSize = 1
    wsLOC2 = parmLabelInfo[11]
    wsMfr = parmLabelInfo[13]
    wsMfrPartno = parmLabelInfo[14]
    wsPackagingCode = parmLabelInfo[15]
    wsROHS = parmLabelInfo[16]
    if wsROHS == "Y":
        wsROHS = "ROHS"
    else:
        wsROHS = "N/ROHS"

    parmPtr.xOffsetDots = 200  # offset to start of label
    parmPtr.start_label()
    parmPtr.print_text(
        500, 20, wsSku, Size=5, width_multiplier=2, height_multiplier=2, rotation=1
    )
    parmPtr.print_text(
        325,
        20,
        "LOC2: %s   Pack of %d" % (wsLOC2, wsPackSize),
        Size=3,
        width_multiplier=2,
        height_multiplier=2,
        rotation=1,
    )
    parmPtr.print_text(275, 20, "%s" % (wsLabelTitle[:40]), Size=2, rotation=1)
    parmPtr.print_text(225, 20, "Packaging: %s" % (wsPackagingCode), Size=3, rotation=1)
    parmPtr.print_text(175, 20, "Date: %s  %s" % (parmDate, wsROHS), Size=2, rotation=1)
    parmPtr.print_text(
        125, 20, "Mfr: %s / %s" % (wsMfr, wsMfrPartno), Size=2, rotation=1
    )
    parmPtr.print_barcode(
        75, 20, wsSku, BarcodeType="3", Size=120, NarrowBar=2, WideBar=4, rotation=1
    )
    parmPtr.end_label()


def PrintProductLabels(
    parmLabelInfo, Qty=1, VPack=1, Type=PRODUCT_LABEL, Date="", Mode=None
):
    Qty = bzUtil.Int(Qty)
    b = BarcodeEPL2()
    if Type in [BAG_LABEL, CARTON_LABEL, ADDRESS_LABEL]:
        b.OpenPrinter(PRINTER_3x5)
    else:
        b.OpenPrinter(PRINTER_1x2)

    if Qty > 50:
        Qty = 1
    for wsLabel in range(0, Qty):
        if Type == CARTON_LABEL:
            PrintOneCartonLabel_L3x5(b, parmLabelInfo, Date)
        elif Type == BAG_LABEL:
            PrintOneBagLabel_L3x5(b, parmLabelInfo, Date)
        elif Type == ADDRESS_LABEL:
            PrintShippingAddress(b, VPack, Mode=Mode)
        else:
            PrintOneProductLabel(b, parmLabelInfo, VPack, Date)
    b.printer.close()


def GetLabelInfo(parmType, parmKeyValue):
    if parmType == "C":  # Contact Info
        wsFunc = "C"
        wsKey = "Contactno"
    elif parmType == "B":  # Bill-To address of order
        wsFunc = "B"
        wsKey = "Ordnum"
    elif parmType == "T":  # Ship-To address of order
        wsFunc = "T"
        wsKey = "Ordnum"
    else:  # Default L / Product Info
        wsFunc = "L"
        wsKey = "Partno"
    wsCcServer = "cart.hobbyengineering.com"  # production server
    wsContact = bzHtml.HttpSendReceive(
        wsCcServer,
        "/cgi/label.cgi?func=%s&%s=%s" % (wsFunc, wsKey, parmKeyValue),
        False,
        debug=0,
    )
    return bzCommaStr.CommaStrToList(wsContact)


def PrintShippingAddress(parmPtr, id, Mode=None):
    if not Mode:
        Mode = ""
    if Mode == "B":
        wsContactList = GetLabelInfo("B", id)  # Bill-To Address
    else:
        wsContactList = GetLabelInfo("T", id)  # Ship-ToAddress
    parmPtr.xOffsetDots = 200  # offset to start of label
    parmPtr.start_label()
    wsFreightCode = bzUtil.GetArrayFieldAsStr(wsContactList, 1)
    wsNameFirst = bzUtil.GetArrayFieldAsStr(wsContactList, 3)
    wsNameMiddle = bzUtil.GetArrayFieldAsStr(wsContactList, 4)
    wsNameLast = bzUtil.GetArrayFieldAsStr(wsContactList, 5)
    wsName = wsNameFirst
    if wsNameMiddle:
        wsName += " " + wsNameMiddle
    wsName += " " + wsNameLast
    wsName = bzUtil.Upper(wsName)
    wsCompany = bzUtil.Upper(bzUtil.GetArrayFieldAsStr(wsContactList, 7))
    wsAddress1 = bzUtil.Upper(bzUtil.GetArrayFieldAsStr(wsContactList, 8))
    wsCity = bzUtil.GetArrayFieldAsStr(wsContactList, 9)
    wsState = bzUtil.GetArrayFieldAsStr(wsContactList, 10)
    wsZip = bzUtil.GetArrayFieldAsStr(wsContactList, 11)
    wsAddress2 = bzUtil.Upper(bzUtil.GetArrayFieldAsStr(wsContactList, 14))
    wsCountryName = bzUtil.GetArrayFieldAsStr(wsContactList, 15)
    wsLastLine = wsCity + ", " + wsState
    if (len(wsLastLine) + len(wsZip)) < 25:
        wsLastLine += " " + wsZip
        wsCountryLine = ""
    else:
        wsCountryLine = wsZip
    wsLastLine = bzUtil.Upper(wsLastLine)
    if wsCountryName != "USA":
        if wsCountryLine != "":
            wsCountryLine += " "
        wsCountryLine += wsCountryName
    wsCountryLine = bzUtil.Upper(wsCountryLine)
    #
    parmPtr.print_text(
        500,
        20,
        "Hobby Engineering HE" + id,
        Size=3,
        width_multiplier=1,
        height_multiplier=1,
        rotation=1,
    )
    parmPtr.print_text(
        470,
        20,
        "282 Harbor Way, Unit D",
        Size=3,
        width_multiplier=1,
        height_multiplier=1,
        rotation=1,
    )
    parmPtr.print_text(
        440,
        20,
        "South San Francisco, CA 94080",
        Size=3,
        width_multiplier=1,
        height_multiplier=1,
        rotation=1,
    )
    #
    if (Mode == "B") or (Mode == "F") or ((wsFreightCode == "fcpe") and (Mode == "")):
        parmPtr.print_text(
            375,
            200,
            "FIRST CLASS MAIL",
            Size=3,
            width_multiplier=2,
            height_multiplier=2,
            rotation=1,
        )
    elif (Mode == "P") or (
        (wsFreightCode in ["priority", "prtyenvl"]) and (Mode == "")
    ):
        if wsCountryName == "USA":
            wsMailText = "PRIORITY MAIL"
        else:
            wsMailText = "GLOBAL PRIORITY MAIL"
        parmPtr.print_text(
            375,
            200,
            wsMailText,
            Size=3,
            width_multiplier=2,
            height_multiplier=2,
            rotation=1,
        )
    elif (Mode == "A") or ((wsFreightCode == "gairlp") and (Mode == "")):
        parmPtr.print_text(
            375,
            200,
            "AIR MAIL",
            Size=3,
            width_multiplier=2,
            height_multiplier=2,
            rotation=1,
        )
    elif wsFreightCode == "gexp":
        parmPtr.print_text(
            375,
            200,
            "GLOBAL EXPRESS MAIL (EMS)",
            Size=3,
            width_multiplier=2,
            height_multiplier=2,
            rotation=1,
        )
    else:
        parmPtr.print_text(
            375,
            200,
            wsFreightCode,
            Size=3,
            width_multiplier=2,
            height_multiplier=2,
            rotation=1,
        )
    #
    parmPtr.print_text(
        250, 200, wsName, Size=3, width_multiplier=2, height_multiplier=2, rotation=1
    )
    wsX = 200
    if wsCompany:
        parmPtr.print_text(
            wsX,
            200,
            wsCompany,
            Size=3,
            width_multiplier=2,
            height_multiplier=2,
            rotation=1,
        )
        wsX -= 50
    parmPtr.print_text(
        wsX,
        200,
        wsAddress1,
        Size=3,
        width_multiplier=2,
        height_multiplier=2,
        rotation=1,
    )
    wsX -= 50
    if wsAddress2:
        parmPtr.print_text(
            wsX,
            200,
            wsAddress2,
            Size=3,
            width_multiplier=2,
            height_multiplier=2,
            rotation=1,
        )
        wsX -= 50
    parmPtr.print_text(
        wsX,
        200,
        wsLastLine,
        Size=3,
        width_multiplier=2,
        height_multiplier=2,
        rotation=1,
    )
    wsX -= 50
    if wsCountryLine:
        parmPtr.print_text(
            wsX,
            200,
            wsCountryLine,
            Size=3,
            width_multiplier=2,
            height_multiplier=2,
            rotation=1,
        )
        wsX -= 50
    parmPtr.end_label()


def PrintContactAddress(b, id):
    wsContactList = GetLabelInfo("L", id)
    b.start_label()
    wsCallSign = wsContactList[10]
    wsName = wsContactList[1]
    if wsContactList[2]:
        wsName += " " + wsContactList[2]
    wsName += " " + wsContactList[3]
    # if wsCallSign: wsName  += " (%s)" % (wsCallSign)
    b.print_text(-1, 0, wsName)
    # if wsCallSign: b.print_text(-1, -1, wsCallSign)
    if wsContactList[4]:
        b.print_text(-1, -1, wsContactList[4])
    b.print_text(-1, -1, wsContactList[5])
    if wsContactList[6]:
        b.print_text(-1, -1, wsContactList[6])
    wsCityStateZip = "%s, %s" % (wsContactList[7], wsContactList[8])
    b.print_text(-1, -1, wsCityStateZip)
    b.print_text(250, -1, wsContactList[9])
    b.end_label()


def print_sample():
    print("Test")
    b = BarcodeEPL2("TLP2844")
    print("Start Label")
    b.start_label()
    print("Print Text")
    b.print_text(50, 0, "Line 1", font=3, rotation=1)
    b.print_text(50, 0, "Line 1", font=3)
    b.print_text(50, 50, "Line 2", font=4)
    b.print_text(50, 50, "Line 2", font=4, width_multiplier=2, height_multiplier=2)
    b.print_text(50, 100, "LINE 3", font=5)
    b.print_barcode(50, 200, "123456789012")
    print("End Label")
    b.end_label()
    print("Done")


if __name__ == "__main__":
    # for id in range(1, 62+1):
    #  PrintAddress(b, id)
    # wsLabelInfo = GetLabelInfo("L", "1433")
    # PrintProductLabels(wsLabelInfo, Type=PRODUCT_LABEL, VPack=0, Date="20060804")
    print_sample()
