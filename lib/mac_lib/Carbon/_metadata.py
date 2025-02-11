# This file is generated by objective.metadata
#
# Last update: Fri Jun 21 23:32:49 2024
#
# flake8: noqa

import objc, sys
from typing import NewType

if sys.maxsize > 2**32:

    def sel32or64(a, b):
        return b

else:

    def sel32or64(a, b):
        return a


if objc.arch == "arm64":

    def selAorI(a, b):
        return a

else:

    def selAorI(a, b):
        return b


misc = {}
misc.update(
    {
        "EventHotKeyID": objc.createStructType(
            "Carbon.EventHotKeyID", b"{EventHotKeyID=II}", ["signature", "id"]
        ),
        "HICommand": objc.createStructType(
            "Carbon.HICommand",
            b"{HICommand=II{struct (unnamed at /Users/ronald/Applications/Xcode-beta.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.0.sdk/System/Library/Frameworks/Carbon.framework/Frameworks/HIToolbox.framework/Headers/CarbonEvents.h:11932:3)=^{OpaqueMenuRef=}S}{struct (unnamed at /Users/ronald/Applications/Xcode-beta.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX15.0.sdk/System/Library/Frameworks/Carbon.framework/Frameworks/HIToolbox.framework/Headers/CarbonEvents.h:11932:3)=^{OpaqueMenuRef=}S}}",
            ["attributes", "commandID", "menu"],
        ),
        "TabletProximityRec": objc.createStructType(
            "Carbon.TabletProximityRec",
            b"{TabletProximityRec=SSSSSSIQICC}",
            [
                "vendorID",
                "tabletID",
                "pointerID",
                "deviceID",
                "systemTabletID",
                "vendorPointerType",
                "pointerSerialNumber",
                "uniqueID",
                "capabilityMask",
                "pointerType",
                "enterProximity",
            ],
        ),
        "TabletPointRec": objc.createStructType(
            "Carbon.TabletPointRec",
            b"{TabletPointRec=iiiSSssSsSsss}",
            [
                "absX",
                "absY",
                "absZ",
                "buttons",
                "pressure",
                "tiltX",
                "tiltY",
                "rotation",
                "tangentialPressure",
                "deviceID",
                "vendor1",
                "vendor2",
                "vendor3",
            ],
        ),
        "TabletPointerRec": objc.createStructType(
            "Carbon.TabletPointerRec", b"{TabletPointRec=iiiSSssSsSsss}", []
        ),
    }
)
constants = """$$"""
enums = """$kAHInternalErr@-10790$kAHInternetConfigPrefErr@-10791$kAHTOCTypeDeveloper@1$kAHTOCTypeUser@0$kEventHotKeyExclusive@1$kEventHotKeyNoOptions@0$kHIHotKeyModeAllDisabled@1$kHIHotKeyModeAllDisabledExceptUniversalAccess@2$kHIHotKeyModeAllEnabled@0$"""
misc.update({})
misc.update({})
misc.update(
    {
        "kHISymbolicHotKeyCode": "kHISymbolicHotKeyCode",
        "kHIServicesMenuItemName": "kHIServicesMenuItemName",
        "kHIServicesMenuProviderName": "kHIServicesMenuProviderName",
        "kHISymbolicHotKeyModifiers": "kHISymbolicHotKeyModifiers",
        "kHISymbolicHotKeyEnabled": "kHISymbolicHotKeyEnabled",
        "kHIServicesMenuCharCode": "kHIServicesMenuCharCode",
        "kHIServicesMenuKeyModifiers": "kHIServicesMenuKeyModifiers",
    }
)
functions = {
    "UnregisterEventHotKey": (b"i^{OpaqueEventHotKeyRef=}",),
    "AHLookupAnchor": (b"i^{__CFString=}^{__CFString=}",),
    "AHRegisterHelpBookWithURL": (b"i^{__CFURL=}",),
    "AHSearch": (b"i^{__CFString=}^{__CFString=}",),
    "AHRegisterHelpBook": (
        b"i^{FSRef=[80C]}",
        "",
        {"arguments": {0: {"type_modifier": "n"}}},
    ),
    "GetSymbolicHotKeyMode": (b"I",),
    "RegisterEventHotKey": (
        b"iII{EventHotKeyID=II}^{OpaqueEventTargetRef=}I^^{OpaqueEventHotKeyRef=}",
        "",
        {"arguments": {5: {"type_modifier": "o"}}},
    ),
    "PushSymbolicHotKeyMode": (b"qI",),
    "AHGotoMainTOC": (b"is",),
    "AHGotoPage": (b"i^{__CFString=}^{__CFString=}^{__CFString=}",),
    "PopSymbolicHotKeyMode": (b"vq",),
    "CopySymbolicHotKeys": (
        b"i^^{__CFArray=}",
        "",
        {
            "retval": {"already_cfretained": True},
            "arguments": {0: {"already_cfretained": True, "type_modifier": "o"}},
        },
    ),
}
aliases = {
    "kEventUpdateActiveInputArea": "kEventTextInputUpdateActiveInputArea",
    "kEventWindowDefHitTest": "kEventWindowHitTest",
    "kEventWindowDefStateChanged": "kEventWindowStateChanged",
    "kMouseTrackingMouseReleased": "kMouseTrackingMouseUp",
    "kEventParamTSMDocAccessSendComponentInstance": "kEventParamTSMSendComponentInstance",
    "kEventHighLevelEvent": "kEventAppleEvent",
    "kEventGetSelectedText": "kEventTextInputGetSelectedText",
    "kEventWindowDefInit": "kEventWindowInit",
    "kEventParamModalClickResult": "typeModalClickResult",
    "kEventShowHideBottomWindow": "kEventTextInputShowHideBottomWindow",
    "typeRefCon": "typeVoidPtr",
    "kEventParamGDevice": "kEventParamDisplayDevice",
    "kEventWindowDefDrawGrowBox": "kEventWindowDrawGrowBox",
    "kEventWindowDefDispose": "kEventWindowDispose",
    "kEventParamWindowModality": "typeWindowModality",
    "kEventParamTextInputSendComponentInstance": "kEventParamTSMSendComponentInstance",
    "kEventProcessCommand": "kEventCommandProcess",
    "kEventPosToOffset": "kEventTextInputPosToOffset",
    "kEventParamTextInputSendGlyphInfoArray": "kEventParamTextInputGlyphInfoArray",
    "kEventWindowDefDragHilite": "kEventWindowDragHilite",
    "kEventWindowDefDrawPart": "kEventWindowDrawPart",
    "kEventWindowDefMeasureTitle": "kEventWindowMeasureTitle",
    "kEventOffsetToPos": "kEventTextInputOffsetToPos",
    "kMouseTrackingMousePressed": "kMouseTrackingMouseDown",
    "kEventClassEPPC": "kEventClassAppleEvent",
    "kEventParamTextInputSendRefCon": "kEventParamTSMSendRefCon",
    "kEventParamTSMDocAccessSendRefCon": "kEventParamTSMSendRefCon",
    "kEventTabletPointer": "kEventTabletPoint",
    "kEventUnicodeForKeyEvent": "kEventTextInputUnicodeForKeyEvent",
    "kEventWindowDefSetupProxyDragImage": "kEventWindowSetupProxyDragImage",
    "kEventWindowDefGetRegion": "kEventWindowGetRegion",
    "kEventWindowDefGetGrowImageRegion": "kEventWindowGetGrowImageRegion",
    "kEventWindowDefModified": "kEventWindowModified",
    "kEventControlGetSubviewForMouseEvent": "kEventControlInterceptSubviewClick",
    "kEventWindowDefDrawFrame": "kEventWindowDrawFrame",
}
misc.update(
    {
        "EventHotKeyRef": objc.createOpaquePointerType(
            "EventHotKeyRef", b"^{OpaqueEventHotKeyRef=}"
        )
    }
)
expressions = {}

# END OF FILE
