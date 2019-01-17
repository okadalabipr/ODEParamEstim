def setSearchParam():

    x = setParamConst()
    y0 = initialValues()

    #write param index for optimization
    SearchConstIdx = [\
        V1,
        Km1,
        #V2,
        #Km2,
        #V3,
        #Km3,
        #V4,
        #Km4,
        V5,
        Km5,
        #V6,
        #Km6,
        #KimERK,
        #KexERK,
        #KimpERK,
        #KexpERK,
        #KimppERK,
        #KexppERK,
        V10,
        Km10,
        n10,
        p11,
        p12,
        p13,
        V14,
        Km14,
        V15,
        Km15,
        #p16,
        #p17,
        KimDUSP,
        KexDUSP,
        #KimpDUSP,
        #KexpDUSP,
        V20,
        Km20,
        V21,
        Km21,
        #p22,
        #p23,
        V24,
        Km24,
        V25,
        Km25,
        KimRSK,
        KexRSK,
        V27,
        Km27,
        V28,
        Km28,
        V29,
        Km29,
        V30,
        Km30,
        V31,
        Km31,
        n31,
        p32,
        p33,
        #p34,
        V35,
        Km35,
        V36,
        Km36,
        V37,
        Km37,
        #p38,
        #p39,
        KimFOS,
        KexFOS,
        #KimpcFOS,
        #KexpcFOS,
        V42,
        Km42,
        V43,
        Km43,
        V44,
        Km44,
        #p45,
        #p46,
        p47,
        m47,
        p48,
        p49,
        m49,
        p50,
        p51,
        m51,
        #p52,
        #m52,
        #p53,
        #p54,
        #m54,
        #p55,
        #p56,
        #m56,
        V57,
        Km57,
        n57,
        p58,
        p59,
        p60,
        #p61,
        KimF,
        KexF,
        #p63,
        KF31,
        nF31,
        #
        a\
    ]

    #initialvalues(not necessary)
    SearchInitIdx= []

    SearchParam = np.empty(len(SearchConstIdx)+len(SearchInitIdx))
    for i in range(len(SearchConstIdx)):
        SearchParam[i] = x[SearchConstIdx[i]]
    for i in range(len(SearchInitIdx)):
        SearchParam[i+len(SearchConstIdx)] = y0[SearchInitIdx[i]]

    return SearchConstIdx, SearchInitIdx, SearchParam

SearchConstIdx, SearchInitIdx, SearchParam = setSearchParam()

if np.any(SearchParam == 0.):
    print('Error: SearchParam must not contain zero.')
    sys.exit()