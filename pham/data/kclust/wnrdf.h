/****************************************************************************

COPYRIGHT NOTICE:

  The source code in this directory is provided free of
  charge to anyone who wants it.  It is in the public domain
  and therefore may be used by anybody for any purpose.  It
  is provided "AS IS" with no warranty of any kind
  whatsoever.  For further details see the README files in
  the wnlib parent directory.

****************************************************************************/

/*
  table of random feedback taps and constants
*/
/*
feedback_munge_array[] = 
{
*/
/* constant        lin_tap1  lin_tap2  quad_tap1 quad_tap2*/
/* --------------- --------- --------- --------- ---------*/
  {(int)0xdcc93837,      238,      319,      297,      388},
  {(int)0xf5aa0166,       37,       31,      316,      297},
  {(int)0x162e257f,       67,      565,      574,      499},
  {(int)0x122f6c4d,       80,      566,      199,       88},
  {(int)0x93c1fa3a,      398,      255,      540,      448},
  {(int)0x273a5357,      546,      223,      583,       97},
  {(int)0x80da9d05,      180,      420,       83,      529},
  {(int)0xd8758fcf,      407,      144,      337,      401},
  {(int)0x60c46259,      297,      128,      363,      257},
  {(int)0xb0b999e6,       17,      548,      396,      217},
  {(int)0xf5254699,      443,      518,      202,      196},
  {(int)0x1a32a01e,      272,      572,      561,      511},
  {(int)0x41ddffe6,      133,       85,      435,       41},
  {(int)0x0244b3cd,      250,      251,      551,      395},
  {(int)0x882928f1,       29,      486,      492,      470},
  {(int)0xbff18952,      476,      512,       78,      535},
  {(int)0x13f0d11b,      546,      322,      170,      399},
  {(int)0xf9370aee,      175,      323,      426,       21},
  {(int)0xb4dcd3a9,      559,      376,        9,      457},
  {(int)0x1c4eb8e5,      487,      578,      151,      304},
  {(int)0x678983e5,      382,      432,      573,      147},
  {(int)0x87e2f202,      583,      323,      224,      198},
  {(int)0x6ed9e07f,      250,      287,      149,      558},
  {(int)0xced68a86,      207,      243,      154,      196},
  {(int)0x3a1b9f97,      479,      148,      209,      495},
  {(int)0x0651df57,      487,      463,      260,      164},
  {(int)0xffead45d,      332,      488,      540,       99},
  {(int)0x27ea2b82,      424,       61,      459,      422},
  {(int)0x399881eb,      476,      106,      400,      513},
  {(int)0xef6acedf,      170,      584,      380,      132},
  {(int)0xa9b8bc97,      346,      349,       78,       83},
  {(int)0x4a1dd55e,      236,      132,        6,      167},
  {(int)0x65298271,      489,      480,      568,      524},
  {(int)0xc70478a9,      349,      400,      261,       71},
  {(int)0x0e3b116f,       87,      411,      405,      183},
  {(int)0x80e80a2d,       73,      459,      213,       34},
  {(int)0xcb280fa0,      456,      427,      127,      374},
  {(int)0x2cf27f6f,      492,      360,      427,      227},
  {(int)0x4af4f4e2,      511,      221,       44,      543},
  {(int)0x1ce08911,      579,      482,      187,      299},
  {(int)0xf8f1c1d5,      457,      571,      475,      193},
  {(int)0x5b1ae326,       20,       67,      129,      238},
  {(int)0xdc24903d,       59,      136,      256,      157},
  {(int)0x54d962d4,      560,      447,      145,      124},
  {(int)0x54744700,      566,      294,      394,      376},
  {(int)0x84d561f0,      473,      172,      374,      196},
  {(int)0xcaf80195,      211,      515,      249,       55},
  {(int)0xf177cfff,      427,      206,      531,      432},
  {(int)0x56162b93,      116,      449,      152,      279},
  {(int)0xc392248b,      550,      360,      558,      568},
  {(int)0xbc156d16,        1,      452,      350,      101},
  {(int)0x47991d32,      235,      519,      476,       18},
  {(int)0x92e57afe,      296,      490,      166,      348},
  {(int)0x54eff716,      369,       28,      512,      446},
  {(int)0xbd91d28f,      270,      112,      233,      455},
  {(int)0xad255ca2,       22,      500,      356,      209},
  {(int)0x5c39e173,      387,      326,      520,      133},
  {(int)0x428ab0cb,      101,      461,      510,      188},
  {(int)0xcfc71d3c,      540,      385,      403,       10},
  {(int)0x7904f1d9,      224,      245,       50,      304},
  {(int)0xa8ce24d1,      167,      561,      471,       57},
  {(int)0x4db0b920,      495,      229,      284,      365},
  {(int)0x62c3e78a,      203,      486,      311,      136},
  {(int)0x24baba22,        9,      460,      320,      441},
  {(int)0xa27ebf77,      577,      217,      260,      575},
  {(int)0xe4f25d01,       79,      331,       86,      254},
  {(int)0xd6054f27,      182,      341,      292,       88},
  {(int)0xb9af9c08,      503,      232,      133,      379},
  {(int)0xbf71ca1c,      292,      322,      275,      178},
  {(int)0x6826c24e,       33,      310,      391,       69},
  {(int)0xafd0d198,      467,      302,      338,      316},
  {(int)0xa65302d6,      343,      494,      179,      427},
  {(int)0x4787a68a,      144,      390,      566,      554},
  {(int)0x1bf2560e,       48,       82,      384,      400},
  {(int)0x76f2c785,      548,       24,      111,      226},
  {(int)0x54c3f051,      116,       43,      211,      129},
  {(int)0x0cb51d34,      176,      420,      205,      320},
  {(int)0x7927b02c,      547,      373,       91,      225},
  {(int)0xaeabef57,      538,      512,      140,      363},
  {(int)0x35018408,      536,       80,      523,      367},
  {(int)0x45166161,      203,      148,      431,      172},
  {(int)0x86495618,      515,      255,      525,      278},
  {(int)0xa61054fb,      106,        8,       44,      128},
  {(int)0xb3606c02,      242,      416,      573,      383},
  {(int)0xd79f0538,      445,      582,      290,      525},
  {(int)0x74e783b2,      161,      150,      212,       17},
  {(int)0x7c2337de,       37,        0,      106,      281},
  {(int)0xca97c00d,      454,      284,      187,       67},
  {(int)0x216bc5d9,      526,      217,      187,      583},
  {(int)0x773c7577,      410,      157,      586,      133},
  {(int)0x4769ce4e,      565,      177,       53,      430},
  {(int)0x5b1b8195,      459,      306,      440,      528},
  {(int)0x72446cc6,      277,       17,      144,      404},
  {(int)0xdae524b9,      407,      364,      574,      514},
  {(int)0xb0015d96,       25,       27,      332,      553},
  {(int)0xb1801863,      387,       80,      544,       69},
  {(int)0x5046fb4f,       40,      583,      481,      137},
  {(int)0x73afa0d6,       99,      314,      399,      339},
  {(int)0x2a714def,      564,      125,      450,      474},
  {(int)0x802952e9,      126,      149,      188,      276},
  {(int)0x933821d3,      129,      168,      397,      187},
  {(int)0xab89ce42,      180,      524,      126,      544},
  {(int)0xbf1eca34,      531,      175,       84,      490},
  {(int)0x37e99f68,       66,      446,      163,      385},
  {(int)0x7b9b1031,       71,      412,      291,      382},
  {(int)0x91f3aba1,      551,      452,      240,      519},
  {(int)0x30c96be7,      391,      117,      223,      509},
  {(int)0xeb839453,      249,      482,      110,      232},
  {(int)0x8ca9a808,      566,      412,      192,      377},
  {(int)0x8b5524c4,      425,      135,      276,       33},
  {(int)0xb2bc2b08,      519,      494,      284,      359},
  {(int)0xf705dfe5,      533,      495,      450,       13},
  {(int)0xb6de339c,      153,      583,      319,      216},
  {(int)0x0636e6c9,      202,       43,      514,       44},
  {(int)0x7753942a,      378,      286,      178,      219},
  {(int)0x15c576c3,      389,      391,      416,      444},
  {(int)0xced31d76,        0,      362,      198,       86},
  {(int)0xbf6dce21,      241,      388,      210,      167},
  {(int)0x3ab801d7,      443,      288,      507,      155},
  {(int)0x685d3363,      263,       83,      354,      386},
  {(int)0x9d909f26,      417,      571,      307,      257},
  {(int)0xf1536558,      198,      197,      255,       24},
  {(int)0x3c563773,      534,      459,      401,      186},
  {(int)0x1394d9f2,      340,      208,      301,      361},
  {(int)0x4a9ff96b,      264,      385,      248,      584},
  {(int)0x1843be5a,      348,      444,      116,       20},
  {(int)0x36107f64,      110,        3,      103,       32},
  {(int)0x8e9d80c9,      231,      188,      539,      288},
  {(int)0x32cf342b,       46,      584,      192,      548},
  {(int)0xa44d088f,      139,      435,      420,      325},
  {(int)0x398a0d84,      118,        0,      365,      459},
  {(int)0xc732a711,      454,      389,      498,      192},
  {(int)0x4f1e5089,       16,      232,      149,      516},
  {(int)0x6ea3394a,      358,      459,      465,      242},
  {(int)0x49210451,      386,      156,      221,      475},
  {(int)0x04c9c593,      472,      173,      585,       14},
  {(int)0x878f5019,      509,      560,      183,        7},
  {(int)0xbe9d00d0,      352,      276,      419,      476},
  {(int)0x8225fb7f,      337,       28,      140,      522},
  {(int)0xe7e39150,      579,      442,      380,      333},
  {(int)0xa3b60127,      126,       33,      433,      178},
  {(int)0x8c073cec,      198,      311,      382,        3},
  {(int)0xf44ec00e,      476,      491,       22,      556},
  {(int)0x85d5e1f9,      338,      473,      342,      399},
  {(int)0x573e549a,      275,      472,      522,      124},
  {(int)0xe68544a1,      131,      168,      177,      386},
  {(int)0xe589908c,      513,      180,      469,      181},
  {(int)0xb96dd6e4,      236,      514,      491,      399},
  {(int)0x7bc4b6ef,      313,      561,      230,      513},
  {(int)0x84e69d92,      123,       66,      535,      330},
  {(int)0x3c869251,       49,       13,      224,       23},
  {(int)0xc1b5929d,      154,      130,       11,      175},
  {(int)0x07d569ea,      298,      162,      282,       71},
  {(int)0x789f4c10,      112,      321,      355,      117},
  {(int)0x5fdf56c3,      550,      288,      178,      150},
  {(int)0x9ea886e9,      442,      516,      482,      122},
  {(int)0x006bb164,      106,      112,      482,       53},
  {(int)0x85b80ade,       56,      341,      432,      382},
  {(int)0xeb0987a9,      339,      576,      188,       43},
  {(int)0xd86e0f1b,      527,      575,      460,       35},
  {(int)0x33aa4b89,      559,      274,       34,      118},
  {(int)0x33c3f6e9,      407,      156,      426,      157},
  {(int)0x93a30768,      325,      268,       68,      349},
  {(int)0x227d0150,      420,      403,      206,      523},
  {(int)0x20073dfa,      472,      528,      297,      409},
  {(int)0x2598f5fb,      365,        5,      420,      111},
  {(int)0x67ade6c7,      494,      196,      387,      330},
  {(int)0x3b82e9e0,      222,      549,      103,      583},
  {(int)0xfe01396f,       11,      270,      301,      307},
  {(int)0xe5eb5746,      443,      516,      397,      549},
  {(int)0x8a6a16b6,      514,      134,      128,      486},
  {(int)0x099a1cd7,      398,      292,      305,      266},
  {(int)0xd546cce7,       71,      304,      189,      573},
  {(int)0x4950fff2,      252,      445,      582,      199},
  {(int)0x8df3f650,      487,      184,      450,      357},
  {(int)0xd0a2bbff,      320,      469,      433,      182},
  {(int)0xd45fa227,      186,        3,      271,      396},
  {(int)0xb9ca480a,      305,      177,      236,      170},
  {(int)0x002d8f73,      210,      433,       24,       54},
  {(int)0x1a4537c5,       99,      308,       77,      460},
  {(int)0x0d1b2839,      451,      388,      313,       15},
  {(int)0xcc42a90a,      388,       77,      353,      262},
  {(int)0x41e331b5,      445,      306,       12,      217},
  {(int)0x8de3d73a,      373,      227,      274,      187},
  {(int)0x7f9120f9,      292,      378,      217,      398},
  {(int)0xcdfe8ea5,      576,       92,      342,      471},
  {(int)0xf682b350,      368,      255,      429,      392},
  {(int)0x52e33e95,      328,      316,      275,      387},
  {(int)0x3ae85526,      283,      314,       59,      578},
  {(int)0xf9975f71,      428,      332,      345,       10},
  {(int)0xe09bb290,      545,      564,       63,      544},
  {(int)0xc4915f5f,      531,      440,        4,      192},
  {(int)0x2cce8aca,      428,      470,      235,      471},
  {(int)0xd0fd79c2,      212,      480,      400,      311},
  {(int)0x5c3c6fe3,      424,      348,      452,      300},
  {(int)0x9f4c085a,      266,      245,      261,      148},
  {(int)0x55009113,      477,      505,      294,      554},
  {(int)0xa5d32c35,      235,      191,      238,      446},
  {(int)0x77437ba3,      300,      111,      255,      168},
  {(int)0xa0ad0410,      569,      176,      470,      181},
  {(int)0x03918b90,       84,      255,      362,       83},
  {(int)0x8f81efe2,      244,      180,      355,      315},
  {(int)0xd5f9a834,      522,       68,      526,      210},
  {(int)0x7019aed5,      240,      271,       25,      257},
  {(int)0xb0ec66b3,      158,      373,      362,       41},
  {(int)0x48dcac44,      387,      580,      321,      494},
  {(int)0x98efe782,      439,      301,       74,      341},
  {(int)0xc555a091,      173,      515,       81,      411},
  {(int)0x34a04cf5,       60,      448,      282,       23},
  {(int)0x9d8c11ce,      451,      302,      492,      583},
  {(int)0x384d8f32,       48,       11,       96,      506},
  {(int)0x6298fc9b,      572,      517,      455,      172},
  {(int)0xebc33955,      130,      336,      501,      437},
  {(int)0x214eb458,       31,      532,      195,        9},
  {(int)0xc287267a,       34,       40,      205,      411},
  {(int)0x429a6468,      107,      136,      114,      483},
  {(int)0x0adc93d9,      127,      333,      433,      352},
  {(int)0xdde07e2c,      457,      526,      435,       37},
  {(int)0xdd74a393,      174,      229,      290,      304},
  {(int)0xbd798135,      177,      249,       35,      478},
  {(int)0xe7dcc820,       46,       54,      321,      221},
  {(int)0x30c3a525,      320,       64,      555,      164},
  {(int)0x74753182,       20,      358,      555,      562},
  {(int)0xf1dca673,      189,      582,      181,       58},
  {(int)0xb90938d3,      568,      489,      358,      211},
  {(int)0x42853eab,      335,      473,      367,      199},
  {(int)0x85a32f5c,      567,      583,      464,       51},
  {(int)0x9eed1556,      127,      113,      517,      369},
  {(int)0x74ae56b0,      163,      330,      152,      408},
  {(int)0xdf3e4e3a,      509,      239,      521,      415},
  {(int)0x48b75697,      109,      102,      254,       26},
  {(int)0x9fd597fa,      554,       30,       52,      176},
  {(int)0x0e70f383,      334,      409,      438,      346},
  {(int)0x8448a35a,      284,      568,      383,      431},
  {(int)0x38638cc4,      563,      476,       15,      241},
  {(int)0x2355605d,      503,      167,      287,      556},
  {(int)0xf8936441,      201,       72,      141,       46},
  {(int)0xf2ed31bf,      118,      517,      423,      267},
  {(int)0x749a14ff,      474,      288,      179,      372},
  {(int)0xe93ccc33,       28,       97,      541,      437},
  {(int)0x334bedc0,      285,      392,      247,      211},
  {(int)0x4e667493,      168,      135,      268,      504},
  {(int)0xfe40c2db,      541,      247,      555,      121},
  {(int)0xce9567c3,       10,      343,      128,      103},
  {(int)0xd08dd9b9,       19,      537,      156,      407},
  {(int)0xff1f3939,      341,      566,      426,      501},
  {(int)0x33cfff83,       14,      127,      285,       24},
  {(int)0xf0614406,      368,      389,      418,      360},
  {(int)0xd7455281,      366,      236,      558,      583},
  {(int)0x7be7f217,      472,      200,      389,       10},
  {(int)0x920ba892,      102,      385,      164,      286},
  {(int)0x2c18a974,       74,      403,      443,      145},
  {(int)0x7e3e9e04,      261,      468,       22,      146},
  {(int)0x7a009d2b,       99,      512,      117,      220},
  {(int)0xdc786166,       68,      192,      569,      449},
  {(int)0x1d662ec3,      532,       42,      360,      462},
  {(int)0x8711c230,      383,       63,      493,      209},
  {(int)0xb4fc77e0,      459,      526,      108,      374},
  {(int)0x51278dee,      437,      104,      191,      167},
  {(int)0x86973d4f,      430,      138,      253,      540},
  {(int)0xa301e155,      211,      326,       81,       51},
  {(int)0x1d257e9a,       33,      270,      134,      352},
  {(int)0xf635c79a,      315,      368,      226,      329},
  {(int)0xc28effb9,      134,      156,      463,      433},
  {(int)0x08f884fe,      188,      233,      531,       52},
  {(int)0x8a76c947,       33,      448,      549,      199},
  {(int)0x343c698f,      190,      260,      315,       35},
  {(int)0x736d5ccd,      204,      494,      479,      546},
  {(int)0xfcf13e77,      405,      516,      499,      392},
  {(int)0x614ca699,      578,      143,       84,      511},
  {(int)0xbf783bf6,      365,      110,      248,       51},
  {(int)0xecd9ab22,      513,       43,      149,      481},
  {(int)0xf802efeb,      362,      467,      583,      252},
  {(int)0x4eb3ee90,      501,       94,      442,      532},
  {(int)0x4dc6fb04,      339,       30,      294,      583},
  {(int)0x4c85abd8,      174,      477,      576,      299},
  {(int)0x8e4f7c87,      135,       23,        0,      376},
  {(int)0x54508fa2,       26,      574,      229,       71},
  {(int)0xa2dd6551,      368,      296,      161,      317},
  {(int)0x3aaca9ce,      354,      582,      205,       88},
  {(int)0x3c4f890f,      486,       51,      239,      310},
  {(int)0x827d424e,      306,      171,      364,       77},
  {(int)0x1ccc6db9,       48,       28,      557,      285}
/*
}
*/