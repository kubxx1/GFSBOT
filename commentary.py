import random
from config import *

class CommentaryEngine:
    def __init__(self):
        self.last_templates = []
        self.last_prefixes = []
        self.last_suffixes = []
        self.history_size = 15 # Increased for even more variety
        self.extra_history_size = 8 # History for prefixes/suffixes

        self.templates = {
            EVENT_NOTHING: {
                "early_neutral": [
                    "Początek spotkania, obie drużyny witają się nawzajem.",
                    "Spokojne tempo w pierwszych minutach, nikt nie chce popełnić błędu.",
                    "Gra toczy się głównie w środku pola, czekamy na otwarcie.",
                    "Obrońcy wymieniają podania, budując akcję od tyłu.",
                    "Zespoły skupione na defensywie, środek boiska jest bardzo zagęszczony.",
                    "Bramkarz spokojnie wznawia grę od bramki.",
                    "Wzajemne szukanie słabych punktów, piłka krąży leniwie.",
                    "Trenerzy obserwują uważnie, korygując ustawienie z linii bocznej.",
                    "Krótkie podania na własnej połowie, {team} nie spieszy się z atakiem.",
                    "Murawa dzisiaj w idealnym stanie, piłka szybko chodzi między zawodnikami.",
                    "Lekki wiatr utrudnia precyzyjne przerzuty, gra toczy się nisko.",
                    "Stadion wypełniony po brzegi, atmosfera gęstnieje z każdą minutą.",
                    "{team} wymienia dziesiątki podań na własnej połowie.",
                    "Spokojne wprowadzenie piłki przez  {team}.",
                ],
                "mid_neutral": [
                    "Taktyczne szachy na murawie, walka o każdy metr kwadratowy.",
                    "Piłka krąży od nogi do nogi, ale podania są mało konkretne.",
                    "Trochę niedokładności w środku pola, gra nieco straciła na płynności.",
                    "Zacięta walka o piłkę w kole środkowym, dużo fizycznych starć.",
                    "Mecz wszedł w fazę stabilizacji, obie strony czekają na błąd rywala.",
                    "Próba rozciągnięcia gry do boku, ale obrona rywala jest czujna.",
                    "Krótki fragment szarpanej gry, dużo niecelnych zagrań.",
                    "Drużyny wymieniają się posiadaniem, brakuje jednak ostatniego podania.",
                    "Trybuny zaczynają się niecierpliwić, czekamy na jakiś impuls.",
                    "Środkowi pomocnicy mają dzisiaj mnóstwo pracy, to tam rozstrzyga się los meczu.",
                    "{team} próbuje przejąć kontrolę, ale brakuje im kreatywności w ofensywie.",
                    "Solidna gra w defensywie obu ekip, napastnicy są dzisiaj odcięci od podań.",
                    "Gra 'na rzut monety' w środku pola, nikt nie dominuje.",
                    "Oba zespoły zdają się być zadowolone z obecnego tempa.",
                    "Techniczny popis w wykonaniu pomocników zespołu {team}.",
                    "Szukanie luki w szczelnej defensywie przeciwnika.",
                ],
                "late_neutral": [
                    "Zmęczenie daje o sobie znać, zawodnicy poruszają się nieco wolniej.",
                    "Zegar tyka, a sytuacja na boisku wciąż patowa w tym fragmencie.",
                    "Próba długiego podania 'na aferę', ale defensywa pewnie to czyści.",
                    "Końcówka meczu, nikt nie chce zaryzykować decydującego błędu.",
                    "Gra staje się coraz bardziej nerwowa, dużo chaosu w środku pola.",
                    "Szatkowanie gry faulami, tempo spotkania drastycznie spadło.",
                    "Zawodnicy czekają na sygnał do końcowego ataku, póki co spokój.",
                    "Niewiele dzieje się pod bramkami, piłka utknęła w gąszczu nóg w środku.",
                    "Łapią ich skurcze, sędzia prawdopodobnie doliczy sporo czasu.",
                    "Gra na czas z jednej strony, nieporadne ataki z drugiej.",
                    "Napięcie rośnie z każdą sekundą, jedna bramka może teraz rozstrzygnąć wszystko.",
                    "Wyraźny brak tchu u niektórych zawodników, to już walka charakterów.",
                    "Obie ekipy zdają się czekać na rzuty karne.",
                    "Ostatnie akordy tego spotkania, chaos bierze górę nad taktyką.",
                    "Piłka wybita na oślep pod pole karne rywala.",
                    "Bramkarz kradnie cenne sekundy przy wznowieniu gry.",
                ],
                "low_pressure": [
                    "{team} próbuje wyżej podejść pod rywala, zaczyna się lekki nacisk.",
                    "Wyraźna chęć przejęcia inicjatywy przez zespół {team}.",
                    "{team} ustawia się wyżej, starając się zepchnąć przeciwnika do defensywy.",
                    "Piłka coraz częściej ląduje na połowie rywala drużyny {team}.",
                    "Oblężenie pola karnego jeszcze nie trwa, ale {team} już krąży wokół 'szesnastki'.",
                    "{team} kontroluje teraz środek boiska, rywal musi się głęboko cofnąć.",
                ],
                "high_pressure": [
                    "{team} zamyka rywala na własnej połowie, to jest oblężenie!",
                    "Kolejna fala ataku {team}, obrona rozpaczliwie odpiera ciosy!",
                    "To jest prawdziwy test dla defensywy, {team} nie wypuszcza ich z pola karnego.",
                    "Pachnie bramką! {team} naciska coraz mocniej, brakuje centymetrów.",
                    "Kibice {team} wstali z miejsc, czują, że przełamanie jest blisko!",
                    "Zmasowany atak {team}, piłka niemal nie opuszcza 'szesnastki' rywala.",
                    "Głowa przy głowie w polu karnym, {team} bije głową w mur, ale mur zaczyna pękać!",
                    "Totalna dominacja zespołu {team}, obrońcy ledwo nadążają z wybijaniem piłki.",
                    "Piłka jak bumerang wraca pod pole karne rywali {team}!",
                ],
                "low_chaos": [
                    "Trochę nerwowości w szeregach obu drużyn, piłka odbija się przypadkowo.",
                    "Mecz staje się nieskładny, gra staje się rwana i nieprzewidywalna.",
                    "Wzajemne błędy w wyprowadzaniu piłki, nikt nie potrafi jej dłużej utrzymać.",
                    "Piłka krąży w powietrzu, dużo walki o górne futbolówki.",
                    "Seria rzutów z autu, gra przestała być płynna.",
                    "Nikt nie chce zaryzykować, dużo asekuracyjnej gry i ratowania się wybiciem.",
                ],
                "high_chaos": [
                    "Kompletny chaos w polu karnym! Piłka odbija się jak w bilardzie!",
                    "Nikt nie panuje nad sytuacją, to jest prawdziwa bitwa na murawie!",
                    "To już nie jest czysty futbol, to walka wręcz o każdą bezpańską piłkę!",
                    "Sędzia traci kontrolę nad spotkaniem, robi się bardzo gęsta atmosfera!",
                    "Piłka-bilard! Niewiarygodne zamieszanie, nikt nie wie gdzie jest piłka!",
                    "Seria pomyłek z obu stron, boisko zamieniło się w poligon doświadczalny.",
                    "Panika w defensywie! Piłka lata wszędzie, tylko nie tam gdzie powinna.",
                    "Gracze wchodzą w zwarcie za zwarciem, to mecz walki u schyłku sił!",
                ]
            },
            EVENT_ATTACK: [
                "{player} urywa się obrońcom, to może być ta jedna jedyna akcja!",
                "Świetny rajd {player} skrzydłem, ależ on ma gaz w nogach!",
                "{team} wyprowadza zabójczą kontrę, idą trzy na dwa!",
                "Genialne prostopadłe podanie do {player}, ma przed sobą tylko słońce i bramkę!",
                "{player} mija rywala balansem ciała i wpada w pole karne z impetem!",
                "Szybka wymiana podań zawodników {team}, rozbijają mur defensywny!",
                "{player} zabiera się z piłką, obrona zostaje daleko w tyle!",
                "Ależ podanie zewnętrzną częścią stopy! {player} melduje się w szesnastce!",
                "{player} przepycha się na skraju pola karnego, szuka miejsca do dośrodkowania.",
                "Znakomite przerzucenie ciężaru gry przez {team}, {player} ma mnóstwo swobody!",
                "{player} tańczy z piłką na skrzydle, obrońca jest całkowicie zagubiony.",
                "Zabójcza szybkość {player}! Defensywa rywala pęka w szwach.",
                "{player} balansem ciała gubi dwóch rywali i wchodzi w pole karne!",
            ],
            EVENT_SHOT: [
                "{player} składa się do strzału... POTĘŻNE UDERZENIE!",
                "Bomba z dystansu w wykonaniu {player}, sypią się iskry!",
                "{player} próbuje technicznej podcinki, szał na trybunach!",
                "Błyskawiczny zwód i strzał {player} w krótki róg bramki!",
                "{player} uderza z pierwszej piłki, to była sytuacja sytuacyjna!",
                "{player} próbuje szczęścia zza pola karnego, piłka leci z dużą siłą!",
                "Główka {player} po dośrodkowaniu! Piłka zmierza pod poprzeczkę!",
                "{player} huknął jak z armaty, ależ to miało rotację!",
                "Próba nożyc w wykonaniu {player}, co za ekwilibrystyka!",
                "{player} znajduje lukę w murze i oddaje mierzony strzał.",
                "Ależ pociągnął z woleja {player}! Bramkarz musiał to poczuć w rękach.",
                "{player} uderza technicznie, dokręcona piłka szuka okienka!",
            ],
            EVENT_SAVE: [
                "Niewiarygodne! {player} wyjmuje piłkę niemal z samego okienka!",
                "Parada kolejki! {player} rzuca się jak pantera i broni!",
                "{player} wygrywa ten pojedynek jeden na jeden! Absolutna klasa!",
                "To musiał być gol, ale {player} mówi dzisiaj stanowcze NIE!",
                "{player} instynktownie broni na linii! Co za refleks, niesamowite!",
                "Bramkarz {player} wyrasta na bohatera, co on dzisiaj wyczynia!",
                "Świetne wyjście z bramki {player}, skraca kąt i zatrzymuje atak!",
                "{player} końcówkami palców wybija piłkę na rzut rożny!",
                "Ależ interwencja! {player} pokazuje, dlaczego jest numerem jeden!",
                "Pewny chwyt {player} po groźnym strzale z dystansu.",
                "Robinsonada w wielkim stylu! {player} ratuje swój zespół!",
                "{player} wybija piłkę z linii bramkowej! Co za poświęcenie!",
            ],
            EVENT_GOAL: {
                "opening": [
                    "⚽ GOOOOL! {player} otwiera wynik, stadion oszalał!",
                    "⚽ Stadiony świata! {player} daje prowadzenie drużynie {team}!",
                    "⚽ Pierwszy cios należy do {team}! {player} trafia do siatki!",
                ],
                "equalizer": [
                    "⚽ Ależ comeback! {player} wyrównuje stan spotkania!",
                    "⚽ Remis! {player} nie daje za wygraną i doprowadza do wyrównania!",
                    "⚽ Wszystko zaczyna się od nowa, {player} daje wyrównanie!",
                ],
                "lead": [
                    "⚽ Stadiony świata! {player} daje prowadzenie drużynie {team}!",
                    "⚽ {team} wychodzi na prowadzenie! {player} bohaterem akcji!",
                    "⚽ Przełamanie! {player} wyprowadza swój zespół na przód!",
                ],
                "increase": [
                    "⚽ To jest nokaut! {player} wykorzystuje błąd rywali i podwyższa prowadzenie!",
                    "⚽ Kolejne uderzenie {team}! {player} nie ma litości!",
                    "⚽ Dystans rośnie! {player} strzela, a {team} ucieka z wynikiem!",
                    "⚽ Dominacja potwierdzona! {player} trafia na {home_score}:{away_score}!",
                ],
                "catch_up": [
                    "⚽ Kontakt! {player} strzela gola i {team} wciąż ma nadzieję!",
                    "⚽ Gol pocieszenia? A może początek pogoni! {player} trafia na {home_score}:{away_score}!",
                    "⚽ {team} odrabia straty! {player} daje sygnał do ataku!",
                ],
                "generic": [
                    "⚽ ALEŻ BRAMKA! {player} zdejmuje pajęczynę z samego spojenia!",
                    "⚽ Bramkarz bez szans, precyzyjny strzał {player} ociera się o słupek i wpada!",
                    "⚽ Fenomenalne uderzenie! {player} celebruje gola z kolegami z {team}!",
                    "⚽ Siatka pęka! {player} nie dał cienia szansy bramkarzowi!",
                    "⚽ Co za zimna krew! {player} mija bramkarza i pakuje piłkę do pustej bramki!",
                    "⚽ Radość na ławce rezerwowych! {player} trafia po genialnej akcji zespołowej!",
                    "⚽ Gol widmo? Nie, sędzia wskazuje na środek! {player} bohaterem!",
                    "⚽ Czysta poezja! {player} umieszcza piłkę tuż przy słupku!",
                    "⚽ Kapitan {player} bierze ciężar na swoje barki i strzela gola!",
                    "⚽ Fantastyczny wolej! {player} trafia w samo okienko!",
                    "⚽ Egzekucja! {player} nie marnuje takiej okazji w szesnastce!",
                    "⚽ Piłka po rykoszecie myli bramkarza, ale gol to gol! Strzelcem {player}!",
                ]
            },
            EVENT_FOUL: [
                "Chujowy faul, {player} zdecydowanie przesadził z agresją w tej walce.",
                "Gwizdek sędziego. {player} przerywa akcję rywala w sposób nieprzepisowy.",
                "Ostry wjazd {player}, sędzia musi tutaj interweniować.",
                "{player} przejebał w środku pola, rzut wolny dla przeciwnika.",
            ],
            EVENT_YELLOW_CARD: [
                "🟨 Żółta kartka! {player} ukarany za to uporczywe faulowanie.",
                "🟨 Sędzia wyciąga kartonik, {player} musi uważać, to jego pierwsze ostrzeżenie.",
                "🟨 Nie ma zmiłuj, żółta kartka dla zawodnika {player}.",
            ],
            EVENT_RED_CARD: [
                "🟥 CZERWONA KARTKA! {player} wypierdala z boiska, co za osłabienie!",
                "🟥 Brutalny faul! Sędzia bez wahania pokazuje {player} drogę do szatni!",
                "🟥 Skandaliczne zachowanie {player}, czerwony kartonik wędruje w górę!",
            ],
            # POSITION SPECIFIC OVERRIDES
            "attack_ST": [
                "{player} obraca się z obrońcą na plecach i szuka luki w szesnastce!",
                "Klasyczna 'dziewiątka'! {player} czeka na prostopadłe podanie.",
                "{player} walczy o pozycję w polu karnym, zaraz będzie groźnie!",
                "{player} prosi o piłkę na wolne pole, chce to sam wykończyć!",
                "Snajperski instynkt {player}, już czai się na błąd stoperów.",
            ],
            "attack_MF": [
                "{player} dyktuje tempo gry, rozrzuca piłkę na skrzydła.",
                "Genialny przegląd pola {player}, szuka luki w obronie.",
                "{player} holuje piłkę przez środek boiska, nikt go nie atakuje.",
                "Precyzyjne kierowanie ruchem przez {player}, prawdziwy dyrygent.",
                "{player} szuka partnerów krótkimi podaniami, uspokaja grę.",
            ],
            "attack_DF": [
                "{player} podłącza się do akcji ofensywnej, odważne wyjście obrońcy!",
                "Długi przerzut od {player}, szuka napastników dalekim podaniem.",
                "Stoper {player} zapędził się pod pole karne rywala!",
                "Siłowe rozwiązanie {player}, przepycha się w środku pola.",
                "Defensywa {team} zaczyna akcję od {player}.",
            ],
            "shot_ST": [
                "{player} uderza z półobrotu! Co za technika!",
                "Typowy strzał snajpera, {player} mierzony uderzeniem szuka rogu!",
                "Potężny szczupak {player}! Piłka leci jak pocisk!",
                "{player} odwraca się z piłką i natychmiast uderza, bramkarz zaskoczony!",
            ],
            "shot_MF": [
                "{player} huknął z dystansu, sypią się iskry!",
                "Techniczny strzał {player} zza pola karnego, piłka dokręcona!",
                "{player} próbuje zaskoczyć bramkarza strzałem 'z fałsza'!",
                "Ależ bomba {player}! Bramkarz odprowadza piłkę tylko wzrokiem!",
            ],
            "shot_DF": [
                "{player} najwyżej skacze do główki! Potężne uderzenie obrońcy!",
                "Obrońca {player} spróbował sił z dystansu, co za bomba!",
                "{player} zamyka akcję na długim słupku, strzał rozpaczy!",
            ],
            # GOALKEEPER REACTIONS TO SHOTS (New)
            "shot_reaction_GK": [
                "Bramkarz z niepokojem odprowadza piłkę wzrokiem.",
                "GK pewnie kontroluje tor lotu futbolówki.",
                "Bramkarz koryguje ustawienie, widząc tor lotu piłki.",
                "Golkiper tylko wzrokiem sprawdził, czy piłka nie wpada pod poprzeczkę.",
            ],
            "meta": [
                "Mimo optycznej przewagi, {dominator} wciąż nie potrafi tego udokumentować.",
                "Obraz gry sugeruje dominację jednej strony, ale wynik wciąż pozostaje otwarty.",
                "To niesamowite, że mamy taki wynik przy tak dużej liczbie sytuacji.",
                "Taktyka {dominator} wydaje się przynosić owoce, kontrolują przebieg meczu.",
                "Widzimy wyraźny pomysł na grę u planu {dominator}.",
                "Statystyki posiadania piłki są miażdżące dla rywali {dominator}.",
                "Mecz toczy się pod dyktando jednej drużyny, {dominator} dyktuje warunki.",
            ]
        }

    def get_commentary(self, match, event_type, context=None):
        if match.mode == 'fast' and event_type not in [EVENT_GOAL, EVENT_RED_CARD]:
             return None

        # Base templates selection
        options = []
        
        if event_type == EVENT_NOTHING:
            # RANDOM META TRIGGER (12% chance for meta commentary instead of neutral)
            if random.random() < 0.12:
                options = self.templates["meta"]
            # 1. GRADUAL CHAOS LOGIC
            elif match.chaos_level > 0.8:
                options = self.templates[EVENT_NOTHING]["high_chaos"]
            elif match.chaos_level > 0.45:
                options = self.templates[EVENT_NOTHING]["low_chaos"]
            # 2. GRADUAL PRESSURE LOGIC
            elif (match.possession_streak > 4 or abs(match.home_team.momentum - match.away_team.momentum) > 35):
                options = self.templates[EVENT_NOTHING]["high_pressure"]
            elif (match.possession_streak > 2 or abs(match.home_team.momentum - match.away_team.momentum) > 18):
                options = self.templates[EVENT_NOTHING]["low_pressure"]
            # 3. PHASE-BASED NEUTRAL LOGIC
            else:
                if match.current_minute <= 30:
                    options = self.templates[EVENT_NOTHING]["early_neutral"]
                elif match.current_minute <= 75:
                    options = self.templates[EVENT_NOTHING]["mid_neutral"]
                else:
                    options = self.templates[EVENT_NOTHING]["late_neutral"]
        
        elif event_type == "meta":
             options = self.templates["meta"]
        elif event_type == EVENT_GOAL:
            goal_dict = self.templates.get(EVENT_GOAL, {})
            att_team = context.get('team')
            def_team = context.get('opponent')
            
            # Determine score state (Scores are already updated in simulation.py)
            if att_team.score == 1 and def_team.score == 0:
                sub_key = "opening"
            elif att_team.score == def_team.score:
                sub_key = "equalizer"
            elif att_team.score > def_team.score:
                if att_team.score == def_team.score + 1:
                    sub_key = "lead"
                else:
                    sub_key = "increase"
            else:
                sub_key = "catch_up"
            
            options = goal_dict.get(sub_key, []) + goal_dict.get("generic", [])
        else:
            options = self.templates.get(event_type, [])

        if not options:
            return "..."

        # VARIETY CHECK: Avoid repeating the same core template
        valid_options = [t for t in options if t not in self.last_templates]
        if not valid_options:
            valid_options = [t for t in options if t not in self.last_templates[-5:]]
            if not valid_options:
                 valid_options = options 

        template = random.choice(valid_options)
        self.last_templates.append(template)
        if len(self.last_templates) > self.history_size:
            self.last_templates.pop(0)

        # Context Preparation
        team_obj = context.get('team') if context else match.possession_team
        team_name = team_obj.name if team_obj else "Drużyna"
        
        player_obj = context.get('player') if context else None
        player_name = player_obj.name if player_obj else "Zawodnik"
        player_pos = player_obj.position.strip().upper() if player_obj else "Unknown"

        # Position Grouping logic
        pos_group = "MF"
        if any(x in player_pos for x in ["ST", "CF", "NAPASTNIK"]): pos_group = "ST"
        elif any(x in player_pos for x in ["CB", "LB", "RB", "GK", "OBROŃCA", "BR", "ŚO", "LO", "PO"]): pos_group = "DF"
        
        # Position-aware overrides (ATTACK or SHOT)
        if event_type in [EVENT_ATTACK, EVENT_SHOT] and random.random() < 0.40:
            prefix_key = "attack" if event_type == EVENT_ATTACK else "shot"
            pos_key = f"{prefix_key}_{pos_group}"
            if pos_key in self.templates:
                pos_options = self.templates[pos_key]
                valid_pos = [t for t in pos_options if t not in self.last_templates]
                if valid_pos:
                    template = random.choice(valid_pos)

        dominator = match.home_team.name if match.home_team.momentum > match.away_team.momentum else match.away_team.name
        
        try:
            msg = template.format(
                team=team_name, 
                player=player_name, 
                dominator=dominator,
                home_score=match.home_team.score,
                away_score=match.away_team.score
            )
            
            # GOALKEEPER REACTION INJECTOR FOR SHOTS
            if event_type == EVENT_SHOT and random.random() < 0.3:
                gk_options = self.templates.get("shot_reaction_GK", [])
                if gk_options:
                    msg += " " + random.choice(gk_options)

            # BROADCAST STYLE VARIATION INJECTOR
            if random.random() < 0.30:
                p_list = ["Warto zauważyć, że ", "Wydaje się, że ", "Faktycznie, ", "Często widzimy, że ", 
                          "Niezmiennie ", "Można odnieść wrażenie, że ", "Proszę państwa, ", "Bez wątpienia ",
                          "Z perspektywy komentatora, ", "Analizując ustawienie, "]
                
                s_list_neutral = ["", " sędzia bacznie spogląda na murawę.", " kibice reagują głośnym pomrukiem.", 
                                  " tempo na chwilę siadło.", " zawodnicy obu stron szukają rytmu.", " gra toczy się w słońcu.",
                                  " w powietrzu czuć napięcie.", " trener gestykuluje przy linii.", " walka w środku pola nie ustaje."]
                
                s_list_action = [" Akcja nabiera rumieńców!", " Obrona musi być czujna.", " To może być kluczowy moment.", 
                                 " Napięcie rośnie!", " Kibice wstają z miejsc!", " Ależ to wygląda dynamicznie!",
                                 " Trybuny szaleją!", " Każdy detal ma teraz znaczenie."]

                if event_type == EVENT_NOTHING:
                    # Pick Prefix
                    valid_p = [p for p in p_list if p not in self.last_prefixes]
                    if not valid_p: valid_p = p_list
                    prefix = random.choice(valid_p)
                    self.last_prefixes.append(prefix)
                    if len(self.last_prefixes) > self.extra_history_size: self.last_prefixes.pop(0)

                    if random.random() < 0.5: msg = prefix + msg[0].lower() + msg[1:]

                    # Pick Suffix
                    valid_s = [s for s in s_list_neutral if s not in self.last_suffixes]
                    if not valid_s: valid_s = s_list_neutral
                    suffix = random.choice(valid_s)
                    self.last_suffixes.append(suffix)
                    if len(self.last_suffixes) > self.extra_history_size: self.last_suffixes.pop(0)
                    msg += suffix

                elif event_type == EVENT_ATTACK:
                    valid_s = [s for s in s_list_action if s not in self.last_suffixes]
                    if not valid_s: valid_s = s_list_action
                    suffix = random.choice(valid_s)
                    self.last_suffixes.append(suffix)
                    if len(self.last_suffixes) > self.extra_history_size: self.last_suffixes.pop(0)
                    msg += suffix
                
            return msg
        except Exception:
            return template
