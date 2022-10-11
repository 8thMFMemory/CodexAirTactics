from re import M
from this import d
from tkinter import W
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Codex Air Tactics Encounter Builder",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="auto"
)
st.title(("Codex Air Tactics"))
colx,coly=st.columns([1,1])
with colx:
    st.subheader("Encounter Builder")
#with coly:
    #st.subheader(st.text_input(label="Nome Scontro",label_visibility="hidden"))
#ho moddato il codice sorgente per non fare l'errore - file utils.py righe commentate
# Resource Variables
modpath='.\data\ModList.xlsx'
@st.cache
def getmodlist():
    global modlist
    modlist=pd.read_excel(io=modpath,sheet_name=0,header=0,index_col=0)
    return modlist

dictlen = {"Breve":4,"Medio":6,"Lungo":8,"Epico":10}
dictblocks = {0:0,1:1,2:2,3:3,4:4,5:5,6:6}
numlist = [1,2,3,4,5,6,7,8,9,10]
blocklist=[
    "AT","AT","AT","AT","AT","AT",
        "CS","CS","CS","CS","CS","CS",
            "BK","BK","BK","BK","BK","BK"]
blocklist2=[
    "🟥","🟥","🟥","🟥","🟥","🟥",
        "🟦","🟦","🟦","🟦","🟦","🟦",
            "🟩","🟩","🟩","🟩","🟩","🟩"]
number_emoji_list=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣"]
#Resource Functions
modlist=getmodlist()

def calc_mod_cost_blocks(a=tuple,b=tuple,c=tuple,d=tuple,e=tuple,f=tuple):
    result= b[0] - a[0]*3 + d[0] -c[0]*3 + f[0] - e[0]*3
    return result

def write_expanders(number_of_enemies=int,liss=list):
    #create_other_enemies(a)
    #create__other_layout(a)
    global d
    d=0
    global M
    M=0
    global lot
    lot=[]
    for i in range(NumSc):
        r=str(i)
        k=1+i
        s={"exp"+r:st.expander("Schema "+number_emoji_list[i]+": "+liss[i])}
        with s["exp"+r]:
            tab1,tab2=st.tabs(["Blocchi","Mods"])
            with tab1:
                col1,col2,col3=st.columns(spec=[1,1,1],gap="small")
                with col1:
                    t={"SC"+r+"AT":st.number_input("🟥 Blocchi AT",0,6,0,1,key=k*"A")}
                    t2={"SC"+r+"ATHP":st.number_input("🟥 Vulnerabilità AT",(t["SC"+r+"AT"])*2,(t["SC"+r+"AT"])*4,(t["SC"+r+"AT"])*3,1,key=k*"B")}
                with col2:
                    u={"SC"+r+"CS":st.number_input("🟦 Blocchi CS",0,6,0,1,key=k*"C")}
                    u2={"SC"+r+"CSHP":st.number_input("🟦 Vulnerabilità CS",(u["SC"+r+"CS"])*2,(u["SC"+r+"CS"])*4,(u["SC"+r+"CS"])*3,1,key=k*"D")}
                with col3:
                    v={"SC"+r+"BK":st.number_input("🟩 Blocchi BK",0,6,0,1,key=k*"E")}
                    v2={"SC"+r+"BKHP":st.number_input("🟩 Vulnerabilità BK",(v["SC"+r+"BK"])*2,(v["SC"+r+"BK"])*4,(v["SC"+r+"BK"])*3,1,key=k*"F")}
            with tab2:
                col1,col2=st.columns(spec=[1.25,2],gap="small")
                with col1:
                    a={"SC"+r+"FIGModNames":st.selectbox("🃏 Mod di Figura",modlist.loc[modlist["Tipo"] == "Figura"].index,0,key=k*"H")}
                with col2:
                    b={"SC"+r+"ModNames":st.multiselect("🚀 Mod Extra",modlist.index,key=k*"I")}
        
                #c=
                st.dataframe(data=modlist.loc[b["SC"+r+"ModNames"]+[a["SC"+r+"FIGModNames"]],'Descrizione'],use_container_width=True)


            w={"SC"+r+"B":t["SC"+r+"AT"]+u["SC"+r+"CS"]+v["SC"+r+"BK"]}
            w2={"SC"+r+"ModCostBlocks":t2["SC"+r+"ATHP"]+u2["SC"+r+"CSHP"]+v2["SC"+r+"BKHP"]-3*w["SC"+r+"B"]}
        
            z={"SC"+r+"MCost": sum(modlist.loc[b["SC"+r+"ModNames"],"Costo"]) + w2["SC"+r+"ModCostBlocks"] + modlist.loc[a["SC"+r+"FIGModNames"],"Costo"]} 
            st.write("Costo Totale Mod: ",z["SC"+r+"MCost"])
        d=d+w["SC"+r+"B"]
        M=M+z["SC"+r+"MCost"]
        lot.append([t2,u2,v,a,b])


#sidebar part
with st.sidebar:
    with st.expander("⚙️ Opzioni Incontro",expanded=False):
        enc_params= st.empty()
            
        with enc_params.container():
            EncLen = st.selectbox("Durata Incontro",
            dictlen.keys(),
            1,
            help="La durata dello scontro",
            key="enc_length"
            )
            NumSc = st.number_input("Numero Schemi", 1,6,1,0)  
            numlist[0:int(dictlen[EncLen])]
            charlev=st.number_input("Livello del Party",1,15,1)
            
    with st.expander("💀 Impostazioni Difficoltà",expanded=False):
        tab1,tab2 = st.tabs(["Impostazioni","Riepilogo"])
        with tab1:
            Modnum = st.number_input("Numero di Mod Base",(NumSc+2),20,step=1)
        with tab2:
            diff_score=Modnum+(dictlen[EncLen]//2)+NumSc-charlev
            st.subheader("Punteggio Difficoltà:  "+str(diff_score))
            st.write("Blocchi: ",dictlen[EncLen]//2)
            st.write("Numero Schemi: ", NumSc)
            st.write("Livello Party: ", -charlev)
            st.write("Mod Base: ", Modnum-NumSc)

        if diff_score in range(8,12):
            st.success("Il tuo scontro è Bilanciato!",icon="✅")
        elif diff_score in range(12,17):
            st.warning("Il tuo scontro è Difficile!",icon="⚠️")
        elif diff_score >= 17:
            st.error("Il tuo scontro è Molto Difficile!",icon="💀")
        else:
            st.info("Il tuo scontro è Facile!",icon="🤡")
    with st.expander("✏️ Nomi Schemi"):
        liss=[]
        for bla in range(NumSc):
            blu=str(bla+1)
            blaa=bla+1
            liss.append(st.text_input(label="Nome",value="Nome Schema "+blu,label_visibility="hidden",key=blaa*W))
       

st.write("Numero totale di Blocchi: ",
    dictlen[EncLen],
     " su ", NumSc,
     (" Schemi" if NumSc != 1 else "Schema")) 

#Blocchi e Mod layout
BlockCol, ModCol=st.columns(spec=2,gap="small")

write_expanders(NumSc,liss)

with BlockCol:
    rem= dictlen[EncLen]-d
    if rem > 0:
        st.info("Da assegnare: "+str(rem)+(' Blocco ' if rem == 1 else ' Blocchi '))
    elif rem == 0:
        st.success("Blocchi assegnati!",icon="✅")
        #st.snow()
    else:
        st.warning(body=str(abs(rem)) +(' Blocco ' if rem == -1 else ' Blocchi ')+'in eccesso',icon="⚠️")
 

with ModCol:
    mod= int(Modnum)-M
    if mod>0:
        st.info("Da assegnare: "+str(mod)+" Mod")
    elif mod == 0:
        st.success("Mod assegnate!",icon="✅")
    else:
        st.warning(f"{abs(mod)} Mod in eccesso",icon="⚠️")

def download_printable(encounter):
    strencounter=""
    prp=0
    for i in encounter:
        strencounter += liss[prp]+"\n"
        prp += 1
        for part in i[0:3]:
            k, v= list(part.items())[0]
            strencounter += k[3:] + " " + str(v) + " " +v*"[ ]"+ " "
        strencounter += "\n"

        for part in i[3:5]:
            k,v=list(part.items())[0]
            strencounter += k[:] + " " + str(v) + "\n"
        #strencounter += str(i)
        
        strencounter += "\n"
    return strencounter


st.download_button(("Stampa Scontro"), data=download_printable(lot))
st.write("CAT Encounter Builder ver 0.1 ©️ Team Tactics 2022")
       


