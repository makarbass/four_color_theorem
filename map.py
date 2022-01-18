WA  = 'Западная Австралия'
NT  = 'Северная территория'
SA  = 'Южная Австралия'
Q   = 'Квинсленд'
NSW = 'Новый Южный Уэльс'
V   = 'Виктория'
T   = 'Тасмания'
AL = "Alabama"
AK = "Alaska"
AZ = "Arizona"
AR = "Arkansas"
CA = "California"
CO = "Colorado"
CT = "Connecticut"
DC = "District of Columbia"
DE = "Delaware"
FL = "Florida"
GA = "Georgia"
HI = "Hawaii"
ID = "Idaho"
IL = "Illinois"
IN = "Indiana"
IA = "Iowa"
KS = "Kansas"
KY = "Kentucky"
LA = "Louisiana"
ME = "Maine"
MD = "Maryland"
MA = "Massachusetts"
MI = "Michigan"
MN = "Minnesota"
MS = "Mississippi"
MO = "Missouri"
MT = "Montana"
NE = "Nebraska"
NV = "Nevada"
NH = "New Hampshire"
NJ = "New Jersey"
NM = "New Mexico"
NY = "New York"
NC = "North Carolina"
ND = "North Dakota"
OH = "Ohio"
OK = "Oklahoma"
OR = "Oregon"
PA = "Pennsylvania"
RI = "RhodeIsland"
SC = "South Carolina"
SD = "South Dakota"
TN = "Tennessee"
TX = "Texas"
UT = "Utah"
VT = "Vermont"
VA = "Virginia"
WA = "Washington"
WV = "West Virginia"
WI = "Wisconsin"
WY = "Wyoming"

usa = {
AL: {GA, FL, TN, MS},
AK: {},
AZ: {CA, NV, UT, CO, NM},
AR: {MO, OK, TX, LA, TN, MS},
CA: {OR, NV, AZ},
CO: {WY, NE, KS, OK, NM, AZ, UT},
CT: {RI,MA,NY},
DE: {NJ,PA,MD},
DC: {MD, VA},
FL: {AL, GA},
GA: {SC, NC, TN, AL, FL},
HI: {},
ID: {WA, MT, OR, WY, UT, NV},
IL: {WI, IA, MO, KY, IN, MI},
IN: {MI, WI, IL, KY, OH},
IA: {MN, SD, NE, MO, WI, IL},
KS: {NE, CO, OK, MO},
KY: {IN, IL, MO, TN, OH, WV, VA},
LA: {AR, TX, MS},
ME: {NH},
MD: {DC,DE,VA},
MA: {CT,NH,RI,VT,NY},
MI: {IL, WI, IN, OH},
MN: {ND, SD, IA, WI},
MS: {TN, AR, LA, AL},
MO: {IA, NE, KS, OK, AR, IL, KY, TN}, MT: {ID, WY, SD, ND},
NE: {SD, WY, CO, KS, MO, IA},
NV: {OR, ID, UT, AZ, CA},
NH: {ME,VT,MA},
NJ: {DE,NY,PA},
NM: {AZ, UT, CO, OK, TX},
NY: {CT,NJ,PA,VT,MA},
NC: {GA, TN, SC, VA},
ND: {MT, SD, MN},
OH: {MI, IN, KY, WV,PA},
OK: {KS, CO, NM, TX, AR},
OR: {WA, ID, NV, CA},
PA: {DE,NJ,NY,OH,WV},
RI: {CT,MA},
SC: {GA, NC},
SD: {ND, MT, WY, NE, MN},
TN: {KY, MO, AR, MS, MO},
TX: {OK, NM, AR, LA},
UT: {ID, NV, WY, CO, AZ},
VT: {NH,MA,NY},
VA: {WV, KY, NC, DC, MD},
WA: {OR, ID},
WV: {OH, VA, KY,PA},
WI: {MN, IA, IL, MI, IN},
WY: {MT, SD, NE, CO, UT, ID},
}

australia = { T:   {V},
              WA:  {NT, SA},
              NT:  {WA, Q, SA},
              SA:  {WA, NT, Q, NSW, V},
              Q:   {NT, SA, NSW},
              NSW: {Q, SA, V},
              V:   {SA, NSW, T}
              }

def check_valid(graph):
    for node,nexts in graph.items():
        assert(node not in nexts) 
        for next in nexts:
            assert(next in graph and next in graph[node])

def check_solution(graph, solution):
    if solution is not None:
        colist = []
        for i in solution:
            colist.append(solution[i])
            colist2 = {i for i in colist}
        print("🔴 Использовано цветов: " + str(len(colist2)))
        for node,nexts in graph.items():
            assert(node in solution)
            color = solution[node]
            for next in nexts:
                assert(next in solution and solution[next] != color)
    else:    
        print("❗️ Не хватает цветов!")

def find_best_candidate(graph, guesses):
    if True: 
        candidates_with_add_info = [
        (
            -len({guesses[neigh] for neigh in graph[n] if neigh in guesses}),
            -len({neigh for neigh in graph[n] if neigh not in guesses}),
            n    
        ) for n in graph if n not in guesses]
        candidates_with_add_info.sort()
        candidates = [n for _,_,n in candidates_with_add_info]
    else:
        candidates = [n for n in graph if n not in guesses] 
        candidates.sort()
    if candidates:
        candidate = candidates[0]
        assert(candidate not in guesses)
        return candidate
    assert(set(graph.keys()) == set(guesses.keys()))
    return None

def solve(graph, colors, guesses, depth):
    n = find_best_candidate(graph, guesses)
    if n is None:
        return guesses
    for c in colors - {guesses[neigh] for neigh in graph[n] if neigh in guesses}:
        assert(n not in guesses)
        assert(all((neigh not in guesses or guesses[neigh] != c) for neigh in graph[n]))
        guesses[n] = c
        print ("🌀 Попробуем " + c +" для " + n)
        if solve(graph, colors, guesses, depth+1):
            print ("✅ Присвоим " + c + " для " + n)
            return guesses
        else:
            del guesses[n]
            print ("⚠️ Не удается присвоить " +c+ " для " +n)
    return None

def solve_problem(graph, colors):
    check_valid(graph)
    print("========")
    solution = solve(graph, colors, dict(), 0)
    #print(solution)
    check_solution(graph,solution)


usa = {n:neigh for n,neigh in usa.items() if neigh}
colors  = {'красный', 'зеленый', 'синий', 'желтый'} 

solve_problem(australia, colors)
solve_problem(usa, colors)