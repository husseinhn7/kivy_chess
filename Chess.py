from requests import get
from kivy.config import Config
import socket
import threading
import pickle
triger=True
army_color=None
port=55555
ip='0.0.0.0'
sd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '560')
Config.set('graphics', 'height', '700')
host=False
from kivy.graphics import Line,Rectangle,Color
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.graphics import Line
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.spinner import MDSpinner
from kivy.clock import Clock

def if_won(co):
    p=[]
    pawn=[]
    pishop=[]
    roock=[]
    queen=[]
    k=get_king(co)
    if not king_states(k[1],k[0],co):
        for key in Piece.Data:
            if key.colo=='W':
                p.append(key)
        for i in p:
            if i.name=='pawn':
                pawn=pawnMovment(Piece.Data[i])
                for n in pawn:
                    if king_states(n,i,co):
                        return True
            elif i.name=='queen':
                queen=queenMovment(Piece.Data[i])
                for n2 in queen:
                    if king_states(n2,i,co):
                        return True
            elif i.name=='roock':
                roock=roockMovment(Piece.Data[i])
                for n3 in roock:
                    if king_states(n3,i,co):
                        return True
            elif i.name=='bishop':
                pishop=bishopMovment(Piece.Data[i])
                for n4 in pishop:
                    if king_states(n4,i,co):
                        return True
        return False
    else:
        return False
                
        
                
            
def get_king(co):
        B_king=[]
        W_king=[]
        for key in Piece.Data:
            if key.name=='king' and key.colo=='B':
                B_king.append(key)
                B_king.append(Piece.Data[key])
            elif key.name=='king' and key.colo=='W':
                W_king.append(key)
                W_king.append(Piece.Data[key])
        if co=='W':
            return W_king
        elif co=='B':
            return B_king
def get_name(pos):
    for i in Piece.Data:
        if Piece.Data[i]==pos:
            c=i.name
            return c
def get_color(pos):
    for i in Piece.Data:
        if Piece.Data[i]==pos:
            c=i.colo
            return c
def king(pos,co):
    if co=='W':
        op_co='B'
    elif co=='B':
        op_co='W'
        
    roock_treat=roockMovment(pos)
    bishop_threat=bishopMovment(pos)
    knight_threat=knightMovment(pos)
    pawn_threat=pawnMovment(pos)
    roock=False
    bishop=False
    knight=False
    pawn=False
    for i in roock_treat:
        n=get_name(i)
        c=get_color(i)
        if n in ['roock','queen']  and c==op_co  :
            roock=True
    for i in bishop_threat:
        n2=get_name(i)
        c2=get_color(i)
        if n2 in ['bishop','queen']  and c2==op_co:
            bishop=True
    for i in knight_threat:
        n3=get_name(i)
        c3=get_color(i)
        if n3 in ['knight']  and c3==op_co :
            knight=True
    for i in pawn_threat:
        n4=get_name(i)
        c4=get_color(i)
        if n4 in ['pawn']  and c4==op_co :
            pawn=True
    if roock:
        return False
    elif bishop:
        return False
    elif knight:
        return False
    elif pawn :
        return False
    else:
        return True
def king_states(pos,obj,color):
    pos_copy=Piece.Data[obj]
    a=Piece.cord.index(Piece.Data[obj])
    Piece.cord[a]=pos
    Piece.Data[obj]=pos
    
    state=king(get_king(color)[1],color)
    a=Piece.cord.index(Piece.Data[obj])
    Piece.cord[a]=pos_copy
    Piece.Data[obj]=pos_copy
    return state
def kingMovment(v,k):
    x=v[0]
    y=v[1]
    l=[[x,y+70],[x,y-70],[x+70,y],[x-70,y],
      [x+70,y+70],[x-70,y-70],[x-70,y+70],[x+70,y-70]]
    r=[[u ,z] for [u,z ] in l if u  in range(0,640,70) and z in range(0,640,70) ]
    for i in r:
        if not king_states(i,get_king(k.colo)[0],k.colo):
            r.remove(i)
    for i in r:
        if get_color(i)==k.colo:
            r.remove(i)
    return r
def queenMovment(v):
    return roockMovment(v)+bishopMovment(v)
def roockMovment(v):

    cords=[]
    p1,p2,p3,p4=[],[],[],[]
    r=[]
    x , y=xp(v[0]) , xp(v[1])
    for i in range(0,70*8,70): 
        for u in range(70,70*9,70):
            if  i==x or u==y:
                cords.append([i,u])
    
    for i in range(0,70*9,70):
        a=[x+i,y]
        if a in Piece.cord and a!= [x,y]:
            r.append(a)
            p1=calc2(a,1)
            break
    for i in range(0,70*9,70):
        a=[x-i,y]
        if a in Piece.cord and a!= [x,y]:
            r.append(a)
            p2=calc2(a,2)
            break
    for i in range(0,70*9,70):
        a=[x,y+i]
        if a in Piece.cord and a!= [x,y]:
            r.append(a)
            p3=calc2(a,3)
            break
    for i in range(0,70*9,70):
        a=[x,y-i]
        if a in Piece.cord and a!= [x,y]:
            r.append(a)
            p4=calc2(a,4)
            break
    m=p1+p2+p3+p4
    p=[z for z in cords if z not in m ]+r
    return p
def calc2(p,t):
    x,y=p[0],p[1]
    l=[]
    if t==1:
        for i in range(0,70*9,70):
            a=[x+i,y]
            l.append(a)
    elif t==2:
        for i in range(0,70*9,70):
            a=[x-i,y]
            l.append(a)
    elif t==3:
        for i in range(0,70*9,70):
            a=[x,y+i]
            l.append(a)
    elif t==4:
        for i in range(0,70*9,70):
            a=[x,y-i]
            l.append(a)
    return l

def bishopMovment(v):
    cords=[]
    r=[]
    p1,p2,p3,p4=[],[],[],[]
    x , y=v[0] , v[1]
    for i in range(00,70*9,70): 
        for u in range(70,70*9,70):
            if (xp(x)-i)**2==(xp(y)-u)**2:
                cords.append([i,u])
    
    for i in range(0,70*9,70):
        a=[x+i,y+i]
        if a in Piece.cord and a!= [x,y]:
            p1=calc(a,1)
            r.append(a)
            break
    for i in range(0,70*9,70):
        a=[x-i,y-i]
        if a in Piece.cord and a!= [x,y]:
            p2=calc(a,2)
            r.append(a)
            break
    for i in range(0,70*9,70):
        a=[x-i,y+i]
        if a in Piece.cord and a!= [x,y]:
            p3=calc(a,3)
            r.append(a)
            break
    for i in range(0,70*9,70):
        a=[x+i,y-i]
        if a in Piece.cord and a!= [x,y]:
            p4=calc(a,4)
            r.append(a)
            break
        
    m=p1+p2+p3+p4
    t=[z for z in cords if z not in m] +r
    return t

def calc(p,t):
    x,y=p[0],p[1]
    l=[]
    if t==1:
        for i in range(0,70*9,70):
            a=[x+i,y+i]
            l.append(a)
    elif t==2:
        for i in range(0,70*9,70):
            a=[x-i,y-i]
            l.append(a)
    elif t==3:
        for i in range(0,70*9,70):
            a=[x-i,y+i]
            l.append(a)
    elif t==4:
        for i in range(0,70*9,70):
            a=[x+i,y-i]
            l.append(a)
    return l

def knightMovment(v):
    cords=[]
    x , y=xp(v[0]) , xp(v[1])
    for i in [-70,70]:
        for t in [-140,140]:
            cords.append([x+i,y+t])
            cords.append([x+t,y+i])
    return cords

def pawnMovment(v):
    x , y=xp(v[0]) , xp(v[1])
    m=[]
    s=[[x+70,y+70],[x-70,y+70]]
    if y ==140 and [x,y+70] not in Piece.cord :
        m.append([x,y+70])
        m.append([x,y+140])
    elif [x,y+70] not in Piece.cord:
        m.append([x,y+70])
    f=[i for i in m if i not in  Piece.cord ]
    for i in s :
        if i in Piece.cord :
            f.append(i)
    return f
def piece_type(s,v2):
    if v2.name=='queen':
        return queenMovment(s)
    elif v2.name=='king':
        return ote(v2.colo)
    elif v2.name=='pawn':
        return pawnMovment(s)
    elif v2.name=='roock':
        return roockMovment(s)
    elif v2.name=='knight':
        return knightMovment(s)
    elif v2.name=='bishop':
        return bishopMovment(s)
def xp(h):
    return int(70 * (h//70))


class Piece(ButtonBehavior,Image):
    name=StringProperty('')
    colo=StringProperty('')
    obj=0
    king_ststs=True
    l2=False
    Data={}
    cord=[]
    co=0
    W_king_inf,B_king_inf=[],[]
    del_obj=0
    def __init__(self, **kwargs):
        super(Piece,self).__init__(**kwargs)
        if Piece.co<=32:
            Piece.Data[self]=self.pos
            Piece.co+=1
    def __repr__(self):
        return f'{self.name}'
    def on_release(self):
        Piece.Data[self]=self.pos
        Piece.obj=self
        Piece.l2=True
        Piece.cord.clear()
        for key in Piece.Data:
            Piece.cord.append(Piece.Data[key])
        if Piece.obj!=0:
            Piece.del_obj=self
        '''with self.canvas:
            Color(0,1,0,0.5, mode="rgba")
            Line(points=(0,70,0,140,70,140,70,70,0,70),width=3)
            
            '''
            
            
    
def valid_move(p,obj):
    x,y =Piece.Data[obj],obj
    if p in piece_type(x,y):
        return True
    else:
        return False
        
def CordsTransformation(l):
    x=l[0]
    y=l[1]
    return [70*7-x,70*9-y]

thename=[]

class GameScreen(Screen):
    Host_Game=False
    on_line=False
    scr=[]
    def Host(self):       
        GameScreen.Host_Game=True
    def Guest(self):
        GameScreen.Host_Game=False
    def onLine(self):
        GameScreen.on_line=True
    def offLine(self):
        GameScreen.on_line=False
    def Create(self):
        thename.append(self.ids.tx.text)
        M.nam=M.nam+self.ids.tx.text
        if GameScreen.Host_Game and GameScreen.on_line:
            ip='0.0.0.0'
            sd.bind((ip,port))
            sd.listen()       
            t=threading.Thread(target=wait)
            t.start()
            self.parent.current='inv'
        elif GameScreen.Host_Game and not GameScreen.on_line:
            ip='0.0.0.0'
            sd.bind((ip,port))
            sd.listen()       
            t=threading.Thread(target=wait)
            t.start()
            GameScreen.scr.append(self.parent)
            GameScreen.scr[0].current='guest' 
            Clock.schedule_interval(self.chang, 1)
        elif not GameScreen.Host_Game and GameScreen.on_line:
            for k in Piece.Data:
                p=CordsTransformation(Piece.Data[k])
                a=Animation(x=p[0],y=p[1],duration=0.3)
                a.start(k)
            print(self.parent)
            self.parent.current='Connetion'  
            
        elif not GameScreen.Host_Game and not GameScreen.on_line:
            ip=socket.gethostbyname(socket.gethostname())
            sd.connect((ip,port))
            t=threading.Thread(target=rec)
            t.start()
            for k in Piece.Data:
                p=CordsTransformation(Piece.Data[k])
                a=Animation(x=p[0],y=p[1],duration=0.3)
                a.start(k)
            self.parent.current='menu'
    def chang(self,dt):
        print(self.parent)
        if len(clint)>=1:
            GameScreen.scr[0].current='menu'
            Clock.unschedule(self.chang)
            
    
def ote(co):
    a=get_king(co)
    l=kingMovment(a[1],a[0])
    for i in l:
        if not king_states(i,a[0],co):
            l.remove(i)
    return l
            
        
a=0

class M(Screen):
    nam=''
    def on_touch_up(self, touch):  
        if GameScreen.Host_Game:
            army_color='W'
        elif not GameScreen.Host_Game:
            army_color='B'
        image_to_move=Piece.obj
        image_to_del=Piece.del_obj
        point=[xp(touch.pos[0]),xp(touch.pos[1])]
        try:
            for k in Piece.Data:
                if Piece.Data[k]==point:    
                    image_to_del=k
        except:
            pass
        k=True
        
        if image_to_del !=0 and image_to_move !=0 and image_to_move.colo==image_to_del.colo:
            image_to_move=image_to_del
            image_to_del=0
        if Piece.l2:
            k=king_states(point,image_to_move,army_color)
        if Piece.l2 and not king(get_king(army_color)[1],army_color):
            k=king_states(point,image_to_move,army_color)
               
        if Piece.l2 and valid_move(point,image_to_move) and point!=get_king(army_color)[1] and k :
            print(king_states(point,image_to_move,army_color))
            a=Animation(x=point[0],y=point[1],duration=0.3)  
            if image_to_del !=0 and image_to_move !=0 and image_to_move.colo!=image_to_del.colo and image_to_del.name!='king':
                a1=Animation(x=10000,y=10000,duration=0)
                sendf(image_to_del,'del')
                a1.start(image_to_del)
                image_to_del.source=''
                image_to_del.remove_from_cache()
                image_to_del=0
            sendf(image_to_move,'move',point)
            a.start(image_to_move)
            Piece.l2=False

    def change(self):
        self.ids.namel=thename[0]
        Clock.schedule_interval(self.clok, 1)
    def clok(self,dt):
        global a
        self.ids.time.text=f"{a}"
        a+=1    
class Invtation(Screen):
    scr=[]
    def chang_on_connect(self):
        Invtation.scr.append(self.parent)
        print(self.parent)
        Clock.schedule_interval(self.chang, 1)
    def chang(self,dt):
        print(self.parent)
        if len(clint)>=1:
            Invtation.scr[0].current='menu'
            Clock.unschedule(self.chang)
    @staticmethod
    def gett():
        a=MDApp.get_running_app().root
        print(a.ids.invt)
        

class ConnetionScreen(Screen):
    def conn(self):
        la=Label(text="waiting for connection")
        lod=MDSpinner()
        lod.size_hint= (None, None)
        lod.size= (40,40)
        self.ids.m.add_widget(la)
        self.ids.m.add_widget(lod)
    def conk(self):
        try:
            ip=self.ids.tx.text
            sd.connect((ip,port))
            t=threading.Thread(target=rec)
            t.start()
            self.parent.current='menu'
        except:
            print('didnt workout body')
        
class GuestScreen(Screen):
    pass
class Chess(MDApp):
    @staticmethod
    def getname():
        name=thename[0]
        return  name   
    @staticmethod
    def getip():
        ip=get('https://api.ipify.org').text
        return  ip     
    def on_request_close(self,j):
        try:
            sd.close()
        except:
            pass 
    def build(self):
        global sm
        Window.bind(on_request_close=self.on_request_close)
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(GameScreen(name='settings'))
        sm.add_widget(M(name='menu'))
        
        sm.add_widget(GuestScreen(name='guest'))
        sm.add_widget(ConnetionScreen(name='Connetion'))  
        sm.add_widget(Invtation(name='inv'))   
        return sm
    
def move(p):
    t=CordsTransformation(p[0])
    r=[]
    for i in Piece.Data:
        if Piece.Data[i]==t:
            r.append(i) 
    o=CordsTransformation(p[1])
    a=Animation(x=o[0],y=o[1],duration=0.3)
    a.start(r[0])
            

def delt(p):
    if type(p) is tuple:
        t=CordsTransformation(p)
        r=[]
        for i in Piece.Data:
            if Piece.Data[i]==t:
                r.append(i)
        a=Animation(x=10000,y=10000,duration=0)
        r[0].source=''
        r[0].remove_from_cache()
        a.start(r[0])
def sendf(obj,oper,poin=0):
    if oper=='move':
        o=Piece.Data[obj]
        nh=[o[0],o[1]]
        try:
            if GameScreen.Host_Game:
                p=pickle.dumps([nh,poin])
                clint[0].send(p)
            elif not GameScreen.Host_Game:
                p=pickle.dumps([nh,poin])
                sd.send(p)
        except:
            pass
    elif oper=='del':
        o=Piece.Data[obj]
        nh=(o[0],o[1])
        if GameScreen.Host_Game:
            p=pickle.dumps(nh)
            clint[0].send(p)
        elif not GameScreen.Host_Game:
            p=pickle.dumps(nh)
            sd.send(p)
        

    
    
clint=[]

def hc(c):
    while 1:
        try:
            a=c.recv(1024)
            m=pickle.loads(a)
            if type(m)==list:
                move(m)
            elif type(m)==tuple:
                delt(m)
            print(m)         
        except:
            break
        
def wait():
    while 1:
        cli,addr=sd.accept()
        clint.append(cli)
        print(cli)
        tr=threading.Thread(target=hc,args=(cli,))
        tr.start()
        
        if len(clint)>=1:
            break

def rec():
    while 1:
        a=sd.recv(1024)
        m=pickle.loads(a)
        print(m)
        if type(m)==tuple:  
            delt(m)
        else:
            move(m)  
        
        



if __name__ == '__main__':
    Chess().run()