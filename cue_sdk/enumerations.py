from enum import Enum, EnumMeta

__all__ = ['CLK', 'CDT', 'CPL', 'CLL', 'CDC', 'CAM', 'CE']


# Taken from six.py. I didn't use enough six functionality to justify requiring the entire module.
def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})


class CEnum(Enum):
    """ctypes compatible Enum"""
    @classmethod
    def from_param(cls, obj):
        return obj.value


class KeywordMeta(EnumMeta):
    """god help me
    things such as CLK_1 and CDC_None don't work as enums, as 1 and None are invalid Python identifiers.
    So, to make it more convinient, this maps CLK[1] to CLK._1, CDC[None] to CDC._None, etc.

    Also, it allows more convinient membership testing for string values.
    """

    def __getitem__(self, item):
        if not isinstance(item, str):
            return super(KeywordMeta, self).__getitem__(str(item))
        return super(KeywordMeta, self).__getitem__(item)

    def __contains__(self, item):
        contains = super(KeywordMeta, self).__contains__(item)
        if contains is False:
            return item in self.__members__
        return contains


class CLK(with_metaclass(KeywordMeta, CEnum)):
    """
    Enumeration containing available keys
    """
    CLI_Invalid = 0  # dummy value

    # keyboard leds
    Escape = 1
    F1 = 2
    F2 = 3
    F3 = 4
    F4 = 5
    F5 = 6
    F6 = 7
    F7 = 8
    F8 = 9
    F9 = 10
    F10 = 11
    F11 = 12
    GraveAccentAndTilde = 13
    _1 = 14
    _2 = 15
    _3 = 16
    _4 = 17
    _5 = 18
    _6 = 19
    _7 = 20
    _8 = 21
    _9 = 22
    _0 = 23
    MinusAndUnderscore = 24
    Tab = 25
    Q = 26
    W = 27
    E = 28
    R = 29
    T = 30
    Y = 31
    U = 32
    I = 33
    O = 34
    P = 35
    BracketLeft = 36
    CapsLock = 37
    A = 38
    S = 39
    D = 40
    F = 41
    G = 42
    H = 43
    J = 44
    K = 45
    L = 46
    SemicolonAndColon = 47
    ApostropheAndDoubleQuote = 48
    LeftShift = 49
    NonUsBackslash = 50
    Z = 51
    X = 52
    C = 53
    V = 54
    B = 55
    N = 56
    M = 57
    CommaAndLessThan = 58
    PeriodAndBiggerThan = 59
    SlashAndQuestionMark = 60
    LeftCtrl = 61
    LeftGui = 62
    LeftAlt = 63
    Lang2 = 64
    Space = 65
    Lang1 = 66
    International2 = 67
    RightAlt = 68
    RightGui = 69
    Application = 70
    LedProgramming = 71
    Brightness = 72
    F12 = 73
    PrintScreen = 74
    ScrollLock = 75
    PauseBreak = 76
    Insert = 77
    Home = 78
    PageUp = 79
    BracketRight = 80
    Backslash = 81
    NonUsTilde = 82
    Enter = 83
    International1 = 84
    EqualsAndPlus = 85
    International3 = 86
    Backspace = 87
    Delete = 88
    End = 89
    PageDown = 90
    RightShift = 91
    RightCtrl = 92
    UpArrow = 93
    LeftArrow = 94
    DownArrow = 95
    RightArrow = 96
    WinLock = 97
    Mute = 98
    Stop = 99
    ScanPreviousTrack = 100
    PlayPause = 101
    ScanNextTrack = 102
    NumLock = 103
    KeypadSlash = 104
    KeypadAsterisk = 105
    KeypadMinus = 106
    KeypadPlus = 107
    KeypadEnter = 108
    Keypad7 = 109
    Keypad8 = 110
    Keypad9 = 111
    KeypadComma = 112
    Keypad4 = 113
    Keypad5 = 114
    Keypad6 = 115
    Keypad1 = 116
    Keypad2 = 117
    Keypad3 = 118
    Keypad0 = 119
    KeypadPeriodAndDelete = 120
    G1 = 121
    G2 = 122
    G3 = 123
    G4 = 124
    G5 = 125
    G6 = 126
    G7 = 127
    G8 = 128
    G9 = 129
    G10 = 130
    VolumeUp = 131
    VolumeDown = 132
    MR = 133
    M1 = 134
    M2 = 135
    M3 = 136
    G11 = 137
    G12 = 138
    G13 = 139
    G14 = 140
    G15 = 141
    G16 = 142
    G17 = 143
    G18 = 144
    International5 = 145
    International4 = 146
    Fn = 147

    # Mouse leds
    CLM_1 = 148
    CLM_2 = 149
    CLM_3 = 150
    CLM_4 = 151

    # Headset leds
    CLH_LeftLogo = 152
    CLH_RightLogo = 153

    Logo = 154
    CLI_Last = 154
CLK._member_map_['1'] = CLK._1
CLK._member_map_['2'] = CLK._2
CLK._member_map_['3'] = CLK._3
CLK._member_map_['4'] = CLK._4
CLK._member_map_['5'] = CLK._5
CLK._member_map_['6'] = CLK._6
CLK._member_map_['7'] = CLK._7
CLK._member_map_['8'] = CLK._8
CLK._member_map_['9'] = CLK._9
CLK._member_map_['0'] = CLK._0


class CDT(CEnum):
    """
    Enumeration containing available device types.
    """
    Unknown = 0
    Mouse = 1
    Keyboard = 2
    Headset = 3


class CPL(CEnum):
    """
    Enumeration containing available device types.
    """
    Invalid = 0  # dummy value

    # valid values for keyboard
    US = 1
    UK = 2
    BR = 3
    JP = 4
    KR = 5

    # valid values for mouse
    Zones1 = 6
    Zones2 = 7
    Zones3 = 8
    Zones4 = 9


class CLL(CEnum):
    """
    Enumeration containing available logical layouts for keyboards.
    """
    Invalid = 0  # dummy value
    US_Int = 1
    NA = 2
    EU = 3
    UK = 4
    BE = 5
    BR = 6
    CH = 7
    CN = 8
    DE = 9
    ES = 10
    FR = 11
    IT = 12
    ND = 13
    RU = 14
    JP = 15
    KR = 16
    TW = 17
    MEX = 18


# contains list of device capabilities
class CDC(with_metaclass(KeywordMeta, CEnum)):
    _None = 0
    Lighting = 1
CDC._member_map_['None'] = CDC._None


# contains list of available SDK access modes
class CAM(CEnum):
    ExclusiveLightingControl = 0


# contains shared list of all errors which could happen during calling of Corsair* functions
class CE(CEnum):
    # if previously called function completed successfully
    Success = 0
    # CUE is not running or was shut down or third-party control is disabled in CUE settings(runtime error)
    ServerNotFound = 1
    # if some other client has or took over exclusive control (runtime error)
    NoControl = 2
    # if developer did not perform protocol handshake(developer error)
    ProtocolHandshakeMissing = 3
    # if developer is calling the function that is not supported by the server (either because protocol has broken by
    # server or client or because the function is new and server is too old. Check CorsairProtocolDetails for details)
    # (developer error)
    IncompatibleProtocol = 4
    # if developer supplied invalid arguments to the function (for specifics look at function descriptions).
    # (developer error)
    InvalidArguments = 5
