from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.templatetags.static import static
import os
from experta import *




def index(request):
    template = loader.get_template('index.html')

    return render(request, "index.html", None)

def iframe(request):
    return render(request, "quizform.html", None)

def rest(request, fact, reponse):
    #
    #return JsonResponse({"fdgdf":"dfgdfg"})
    engine = Welcome()
    engine.reset()
    if reponse != 'setup':
        initFacts(engine, fact, reponse)
    print('facts')
    print(engine.facts)

    engine.run()
    storeFacts(engine.facts)
    # args = {"mridh": "yes"}
    # engine.declare(Fact(**args))
    print(engine.next_question)
    if not engine.result:
        return JsonResponse({'end': 0,
                        'nv_question': engine.next_question,
                        'fact':engine.fact
                         })
    else:
        resetFacts()
        return JsonResponse({'end': 1,
                             'result': engine.result
                             })

def resetFacts():
    f = open(str(settings.BASE_DIR)+static('facts.txt'), 'w')
    f.write('')
    f.close()
def storeFacts(facts):
    f = open(str(settings.BASE_DIR)+static('facts.txt'), 'w')
    for fact in facts:
        dicti = facts[fact].items()
        for key, val in dicti:
            if key == '__factid__' or key == 'action':
                continue
            f.write(str(key) + ',' + str(val)+'|')
            # print(facts[fact].items()
    f.close()
def initFacts(engine, fact, reponse):
    f = open(str(settings.BASE_DIR)+static('facts.txt'), 'a')
    f.write(fact+','+reponse+'|')
    f.close()
    f = open(str(settings.BASE_DIR)+static('facts.txt'), 'r')
    data = f.read()
    rows = data.split('|')
    for row in rows:
        words = row.split(',')
        if(len(words)<2):
            continue
        args = dict()
        args[words[0]] = words[1]
        engine.declare(Fact(**args))
    f.close()


class Welcome(KnowledgeEngine):
    def __init__(self):
        self.response_used = False
        self.next_question=''
        self.result = ''
        self.fact = ''
        super().__init__()


    @DefFacts()
    def initial(self):
        print("start game")
        yield Fact(action="jeweb")
    #traditions
    @Rule(NOT(Fact(nord=W())), salience=1)
    def nord(self):
        if not self.response_used:
            print("dkhal nord")
            if not self.next_question:
                self.next_question='Est-il situé au nord?'
                self.fact = 'nord'
                self.response_used = True

    @Rule(NOT(Fact(mer=W())), salience=1)
    def mer(self):
        if not self.response_used:
            print("dkhal mer")
            if not self.next_question:
                self.next_question = 'Contient-il une mer?'
                self.fact = 'mer'
                self.response_used = True
    @Rule(AND(NOT(Fact(neige=W()))), Fact(nord='yes'), salience=1)
    def neige(self):
        if not self.response_used:
            print("dkhal neige")
            if not self.next_question:
                self.next_question = "Est-ce l'une des régions où il neige?"
                self.fact = 'neige'
                self.response_used = True

    @Rule(AND(NOT(Fact(fromage=W())), Fact(region='nord_ouest')), salience=1)
    def fromage(self):
        if not self.response_used:
            print("dkhal fromage")
            if not self.next_question:
                self.next_question = 'Est-il célébre par la production du fromage?'
                self.fact = 'fromage'
                self.response_used = True

    @Rule(NOT(Fact(aeroport=W())), salience=1)
    def aeroport(self):
        if not self.response_used:
            print("dkhal aeroport")
            if not self.next_question:
                self.next_question = "Comporte t-il un aréoroport?"
                self.fact = 'aeroport'
                self.response_used = True

    @Rule(NOT(Fact(port_maritime=W())), salience=1)
    def port_maritime(self):
        if not self.response_used:
            print("dkhal port_maritime")
            if not self.next_question:
                self.next_question = "Comporte t-il un port maritime?"
                self.fact = 'port_maritime'
                self.response_used = True
    @Rule(AND(NOT(Fact(rutacees=W())), Fact(region='nord_est')), salience=1)
    def rutacees(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal rutacees")
                self.next_question = 'Est-il célébre par la production des rutacées (orange, citron)?'
                self.fact = 'rutacees'
                self.response_used = True

    @Rule(AND(NOT(Fact(kaak_warka=W())), Fact(region='nord_est')), salience=1)
    def kaak_warka(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal kaak_warka")
                self.next_question = 'Est-il connu par la production du "Kaak warka"?'
                self.fact = 'kaak_warka'
                self.response_used = True

    @Rule(AND(NOT(Fact(chaanbi=W())), Fact(region='centre')), salience=1)
    def chaanbi(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal chaanbi")
                self.next_question = 'Dans ce gouvernorat, trouve t-on le montagne "Djebel Chambi"?'
                self.fact = 'chaanbi'
                self.response_used = True

    @Rule(AND(NOT(Fact(Bassins_des_Aghlabides=W())), Fact(region='centre')), salience=1)
    def Bassins_des_Aghlabides(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal Bassins_des_Aghlabides")
                self.next_question = "A-t-il comme monument célébre \"les bassins d'Aghlabides\"?"
                self.fact = 'Bassins_des_Aghlabides'
                self.response_used = True

    @Rule(AND(NOT(Fact(mines=W())), Fact(region='sud')), salience=1)
    def mines(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal mines")
                self.next_question = 'Trouve-t-on des mines de phosphates dans cette ville?'
                self.fact = 'mines'
                self.response_used = True

    @Rule(AND(NOT(Fact(ile=W())), Fact(region='sud')), salience=1)
    def ile(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal ile")
                self.next_question = 'Comporte t-il une île?'
                self.fact = 'ile'
                self.response_used = True

    @Rule(AND(NOT(Fact(Carnaval_dAoussou=W())), Fact(region='cotiere')), salience=1)
    def Carnaval_dAoussou(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal Carnaval_dAoussou")
                self.next_question = "L'événement festif \"Carnaval d'Aoussou\" prend-il lieu dans ce gouvernorat?"
                self.fact = 'Carnaval_dAoussou'
                self.response_used = True

    @Rule(AND(NOT(Fact(frontiere=W())), Fact(region='nord_ouest')), salience=1)
    def frontiere(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal frontiere")
                self.next_question = 'Présente-t-il une fontière tuniso-algérienne?'
                self.fact = 'frontiere'
                self.response_used = True

    @Rule(AND(NOT(Fact(jrid=W())), Fact(region='sud')), salience=1)
    def jrid(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal jrid")
                self.next_question = 'le Chott el-Jérid, est-il situé dans ce gouvernorat?'
                self.fact = 'jrid'
                self.response_used = True

    @Rule(NOT(Fact(epicee=W())), salience=1)
    def epicee(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal epicee")
                self.next_question = 'Ses habitants aiment-ils la nourriture épicée?'
                self.fact = 'epicee'
                self.response_used = True

    @Rule(AND(NOT(Fact(poisson=W()))), salience=1)
    def poisson(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal poisson")
                self.next_question = 'Le poisson est-il considéré comme un aliment de base pour ses habitants ?'
                self.fact = 'poisson'
                self.response_used = True

    @Rule(AND(NOT(Fact(dattes=W())), NOT(Fact(region=W()))), salience=1)
    def dattes(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal poisson")
                self.next_question = "Est-ce l'une des régions connues par la production de dattes?"
                self.fact = 'dattes'
                self.response_used = True

    @Rule(AND(NOT(Fact(desert=W())), NOT(Fact(region=W()))), salience=1)
    def desert(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal desert")
                self.next_question = "Contient-il du désert?"
                self.fact = 'desert'
                self.response_used = True

    @Rule(AND(NOT(Fact(legmi=W())), NOT(Fact(region=W()))), salience=1)
    def legmi(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal legmi")
                self.next_question = "Est-ce l'une des régions qui produisent le \"Legmi\"?"
                self.fact = 'legmi'
                self.response_used = True

    @Rule(AND(NOT(Fact(olive=W())), NOT(Fact(region=W()))), salience=1)
    def olive(self):
        if not self.response_used:
            if not self.next_question:
                print("dkhal olive")
                self.next_question = "L'olive est-elle considérée comme sa principale production agricole ?"
                self.fact = 'olive'
                self.response_used = True

    @Rule(AND(NOT(Fact(ichkel=W())), Fact(region='nord_est')), salience=1)
    def ichkel(self):
        print(Fact(nord=W()))
        if not self.response_used:
            if not self.next_question:
                print("dkhal ichkel")
                self.next_question = "Le lac Ichkeul, est-il situé dans ce gouvernorat?"
                self.fact = 'ichkel'
                self.response_used = True

    #set region
    @Rule(AND(Fact(nord='yes'), Fact(neige='no'), NOT(Fact(region=W()))))
    def nord_est(self):
        print('dkhal nord_est')
        self.declare(Fact(region='nord_est'))

    @Rule(AND(Fact(nord='yes'), Fact(neige='yes'), NOT(Fact(region=W()))))
    def nord_ouest(self):
        print('dkhal nord_ouest')
        self.declare(Fact(region='nord_ouest'))

    @Rule(AND(Fact(mer='yes'), Fact(olive='yes'), Fact(epicee='yes'), Fact(poisson='yes'), NOT(Fact(region=W()))))
    def cotiere(self):
        print('dkhal cotiere')
        self.declare(Fact(region='cotiere'))

    @Rule(AND(Fact(mer='no'), Fact(epicee='no'), Fact(port_maritime='no'), Fact(aeroport='no'),NOT(Fact(region=W()))))
    def centre(self):
        print('dkhal centre')
        self.declare(Fact(region='centre'))

    @Rule(AND(Fact(desert='yes'), Fact(dattes='yes'), Fact(legmi='yes'),NOT(Fact(region=W()))))
    def sud(self):
        self.declare(Fact(region='sud'))



    @Rule(AND(Fact(region="nord_ouest"), Fact(mer='yes'), Fact(fromage='yes')), salience=-1)
    def beja(self):
        self.result="le resultat c'est <b>Beja</b>"
    @Rule(AND(Fact(region="nord_ouest"), Fact(mer='yes'), Fact(fromage='no')), salience=-2)
    def jendouba(self):
        self.result="le resultat c'est <b>Jendouba</b>"

    @Rule(AND(Fact(region="nord_ouest"), Fact(mer='no'), Fact(frontiere='yes')), salience=-3)
    def kef(self):
        self.result="le resultat c'est <b>Kef</b>"
    @Rule(AND(Fact(region="nord_ouest"), Fact(mer='no'), Fact(frontiere='no')), salience=-4)
    def siliana(self):
        self.result="le resultat c'est <b>Siliana</b>"

    @Rule(AND(Fact(region="cotiere"), Fact(Carnaval_dAoussou='no'), Fact(aeroport='yes'), Fact(port_maritime='no')), salience=-5)
    def monastir(self):
        self.result = "le resultat c'est <b>Monastir</b>"

    @Rule(AND(Fact(region="cotiere"), Fact(aeroport='no'), Fact(port_maritime='no')),
          salience=-6)
    def mahdia(self):
        self.result = "le resultat c'est <b>Mahdia</b>"

    @Rule(AND(Fact(region="sud"), Fact(mer='yes'), Fact(aeroport='yes'), Fact(port_maritime='yes'), Fact(ile='no')), salience=-7)
    def gabes(self):
        self.result = "le resultat c'est <b>Gabes</b>"

    @Rule(AND(Fact(region="sud"), Fact(mer='yes'), Fact(aeroport='yes'), Fact(port_maritime='yes'), Fact(ile='yes'), Fact(poisson='no')),
          salience=-8)
    def mednine(self):
        self.result = "le resultat c'est <b>Mednine</b>"

    @Rule(AND(Fact(region="sud"), Fact(mer='yes'), Fact(aeroport='yes'), Fact(port_maritime='yes'), Fact(ile='yes'),
              Fact(poisson='yes')),
          salience=-9)
    def sfax(self):
        self.result = "le resultat c'est <b>Sfax</b>"

    @Rule(AND(Fact(region="sud"), Fact(mer='no'), Fact(aeroport='yes'), Fact(port_maritime='no'), Fact(mines='no'), Fact(jrid='yes')),
          salience=-10)
    def tozeur(self):
        self.result = "le resultat c'est <b>Tozeur</b>"

    @Rule(AND(Fact(region="sud"), Fact(mer='no'), Fact(aeroport='no'), Fact(port_maritime='no')),
          salience=-11)
    def kebili(self):
        self.result = "le resultat c'est <b>Kebili</b>"

    @Rule(AND(Fact(region="sud"), Fact(mines='yes'), Fact(aeroport='yes'), Fact(port_maritime='no')),
          salience=-12)
    def gafsa(self):
        self.result = "le resultat c'est <b>Gafsa</b>"

    @Rule(AND(Fact(region="sud"), Fact(mines='no'), Fact(aeroport='yes'), Fact(mer='no'), Fact(jrid='no')),
          salience=-13)
    def tataouine(self):
        self.result = "le resultat c'est <b>Tataouine</b>"

    @Rule(AND(Fact(region="centre"), Fact(chaanbi='no'), Fact(Bassins_des_Aghlabides='no'), Fact(port_maritime='no')),
          salience=-14)
    def sidibouzid(self):
        self.result = "le resultat c'est <b>Sidibouzid</b>"

    @Rule(AND(Fact(region="centre"), Fact(chaanbi='yes')),
          salience=-15)
    def kasserine(self):
        self.result = "le resultat c'est <b>Kasserine</b>"

    @Rule(AND(Fact(region="centre"), Fact(chaanbi='no'), Fact(Bassins_des_Aghlabides='yes')),
          salience=-16)
    def kairouan(self):
        self.result = "le resultat c'est <b>Kairouan</b>"

    @Rule(AND(Fact(region="nord_est"), Fact(mer='no'), Fact(kaak_warka='yes')),
          salience=-17)
    def zaghouan(self):
        self.result = "le resultat c'est <b>Zaghouan</b>"

    @Rule(AND(Fact(region="nord_est"), Fact(mer='yes'), Fact(aeroport='no'), Fact(ichkel='yes'), Fact(port_maritime='yes')),
          salience=-18)
    def bizerte(self):
        self.result = "le resultat c'est <b>Bizerte</b>"

    @Rule(AND(Fact(region="nord_est"), Fact(mer='yes'), Fact(aeroport='no'), Fact(port_maritime='no'), Fact(rutacees='no')),
          salience=-19)
    def ariana(self):
        self.result = "le resultat c'est <b>Ariana</b>"

    @Rule(AND(Fact(region="nord_est"), Fact(mer='yes'), Fact(aeroport='yes')),
          salience=-20)
    def tunis(self):
        self.result = "le resultat c'est <b>Tunis</b>"

    @Rule(AND(Fact(region="nord_est"), Fact(mer='yes'), Fact(aeroport='no'), Fact(port_maritime='yes'), Fact(ichkel='no')),
          salience=-21)
    def benarous(self):
        self.result = "le resultat c'est <b>Ben-Arous</b>"

    @Rule(AND(Fact(region="nord_est"), Fact(mer='yes'), Fact(aeroport='no'), Fact(port_maritime='no'), Fact(rutacees='yes')),
          salience=-22)
    def nabeul(self):
        self.result = "le resultat c'est <b>Nabeul</b>"

    @Rule(AND(Fact(region="nord_est"), Fact(mer='no'), Fact(kaak_warka='no')),
          salience=-23)
    def manouba(self):
        self.result = "le resultat c'est <b>Manouba</b>"

    @Rule(AND(Fact(region="cotiere"), Fact(Carnaval_dAoussou='yes'), Fact(aeroport='yes'), Fact(port_maritime='yes')),
          salience=-24)
    def sousse(self):
        self.result = "le resultat c'est <b>Sousse</b>"












