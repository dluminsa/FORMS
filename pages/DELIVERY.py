import pandas as pd 
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import time

CLUSTER = {
    "KALANGALA": ["KALANGALA"],
    "KYOTERA": ["KYOTERA", "RAKAI"],
    "LYANTONDE": ["LYANTONDE", "LWENGO"],
    "MASAKA": ['BUKOMANSIMBI', "KALUNGU",'MASAKA CITY', 'MASAKA DISTRICT','SEMBABULE'],
    "MPIGI": ['BUTAMBALA', 'GOMBA', 'MPIGI'],
    "WAKISO": ['WAKISO']
}

FACILITIES ={  
                "BUKOMANSIMBI":["BIGASA HC III","BUTENGA HC IV","KAGOGGO HC II","KIGANGAZZI HC II",
                              "KISOJJO HC II","KITANDA HC III","MIRAMBI HC III","ST. MARY'S MATERNITY HOME"],
                "BUTAMBALA" : ["BULO HC III","BUTAAKA HC III","EPI-CENTRESENGE HC III","GOMBE GENERAL HOSPITAL", 
                             "KALAMBA COMMUNITY HC II", "KIBUGGA HC II","KITIMBA HC III", "KIZIIKO HC II","KYABADAZA HC III",
                             "NGANDO HC III"],
                "GOMBA"  : ["BULWADDA HC II", "BUYANJA (GOMBA) HC II","KANONI HC III","KIFAMPA HC III", "KISOZI HC III", "KITWE HC II", "KYAYI HC III","MADDU HC IV",
                          "MAMBA HC III","MAWUKI HC II","MPENJA HC III","NGERIBALYA HC II","NGOMANENE HC III"],
               "KALANGALA": ["BUBEKE HC III","BUFUMIRA HC III","BUKASA HC IV","BWENDERO HC III",
                            "JAANA HC II","KACHANGA ISLAND HC II","KALANGALA HC IV","KASEKULO HC II","LUJJABWA ISLAND HC II",
                            "LULAMBA HC III","MAZINGA HC III","MUGOYE HC III","MULABANA HC II","SSESE ISLANDS AFRICAN AIDS PROJECT (SIAAP) HC II"],
                "KALUNGU" : ["AHF UGANDA CARE","BUKULULA HC IV","KABAALE HC III", "KALUNGU HC III","KASAMBYA (KALUNGU) HC III",  "KIGAJU HC II"
                               "KIGAJU HC II","KIGASA HC II","KIRAGGA HC III",  "KITI HC III","KYAMULIBWA HC III", "LUKAYA HC III","MRC KYAMULIBWA HC II","NABUTONGWA HC II"],
                "KYOTERA" : ["KABIRA (KYOTERA) HC III""KABUWOKO GOVT HC III","KAKUUTO HC IV","KALISIZO GENERAL HOSPITAL","KASAALI HC III",
                                        "KASASA HC III","KASENSERO HC II","KAYANJA HC II","KIRUMBA HC III","KYEBE HC III","LWANKONI HC III","MAYANJA HC II",
                                        "MITUKULA HC III","MUTUKULA HC III","NABIGASA HC III","NDOLO HC II","RHSP CLINIC"],
                "LWENGO" : ["KAKOMA HC III","KATOVU HC III","KIWANGALA HC IV",
                                "KYAZANGA HC IV","KYETUME HC III","LWENGO HC IV","LWENGO HC III","NANYWA HC III"], 
                "LYANTONDE" :["KABATEMA HC II","KABAYANDA HC II","KALIIRO HC III","KASAGAMA HC III",
                                "KINUUKA HC III","KYEMAMBA HC II","LYAKAJURA HC III","LYANTONDE HOSPITAL","MPUMUDDE HC III"],
                "MASAKA CITY": ["BUGABIRA HC II","BUKOTO HC III","KITABAAZI HC III","KIYUMBA HC IV","KYABAKUZA HC II",
                                        "MASAKA MUNICIPAL CLINIC","MASAKA POLICE HC III","MPUGWE HC III","NYENDO HC III","TASO MASAKA"],
                "MASAKA DISTRICT": ["BUKAKATA HC III","BUKEERI HC III","BUWUNGA HC III","BUYAGA HC II","KAMULEGU HC III","KYANAMUKAAKA HC IV"],
                "MPIGI" : ["BUJUUKO HC III","BUKASA HC II","BUNJAKO HC III",
                            "BUTOOLO HC III","BUWAMA HC III","BUYIGA HC III","DONA MEDICAL CENTRE","FIDUGA MEDICAL CENTRE","GGOLO HC III",
                            "KAMPIRINGISA HC III","KIRINGENTE EPI HC II","KITUNTU HC III","MPIGI HC IV","MUDUUMA HC III",
                            "NABYEWANGA HC II","NINDYE HC III","NSAMU/KYALI HC III","SEKIWUNGA HC III","ST. ELIZABETH KIBANGA IHU HC III"],
                "RAKAI" : ["BUGONA HC II","BUTITI HC II","BUYAMBA HC III","BYAKABANDA HC III",
                                    "KACHEERA HC III","KASANKALA HC II","KAYONZA KACHEERA HC II","KIBAALE HC II","KIBANDA HC III","KIBUUKA HC II",
                                    "KIFAMBA HC III","KIMULI HC III","KYABIGONDO HC II","KYALULANGIRA HC III","LWABAKOOBA HC II","LWAKALOLO HC II",
                                    "LWAMAGGWA GOVT HC III","LWANDA HC III","LWEMBAJJO HC II","MAGABI HC II","RAKAI HOSPITAL","RAKAI KIZIBA HC III",],
                "SEMBABULE":["BUSHEKA HC III","KABUNDI HC II","KAYUNGA HC II",
                                        "KYABI HC III","KYEERA HC II","LUGUSULU HC III","LWEBITAKULI HC III","LWEMIYAGA HC III","MAKOOLE HC II","MATEETE HC III",
                                        "MITIMA HC II","NTETE HC II","NTUUSI HC IV","SEMBABULE KABAALE HC II","SSEMBABULE HC IV"],
                                            
                "WAKISO" : ["BULONDO HC III","BUNAMWAYA HC II","BUSAWAMANZE HC III","BUSSI HC III","BUWAMBO HC IV","BWEYOGERERE HC III","COMMUNITY HEALTH PLAN UGANDA",
                        "GGWATIRO NURSING HOME HOSPITAL","GOMBE (WAKISO) HC II","JOINT CLINICAL RESEARCH CENTER (JCRC) HC IV",
                        "KABUBBU HC IV","KAJJANSI HC IV","KAKIRI HC III","KASANGATI HC IV","KASANJE HC III","KASENGE HC II",
                        "KASOOZO HC III","KATABI HC III","KAWANDA HC III","KIGUNGU HC III","KIMWANYI HC II","KIRA HC III",
                        "KIREKA HC II","KIRINYA (BWEYOGERERE) HC II","KITALA HC II","KIZIBA HC III","KYENGERA HC III",
                        "KYENGEZA HC II","LUBBE HC II","LUFUKA VALLEY HC III","MAGANJO HC II","MAGOGGO HC II","MATUGA HC II",
                        "MENDE HC III","MIGADDE HC II","MILDMAY UGANDA HOSPITAL","MUTUNDWE HC II","MUTUNGO HC II","NABUTITI HC III",
                        "NABWERU HC III","NAKAWUKA HC III","NAKITOKOLO NAMAYUMBA HC III","NALUGALA HC II","NAMAYUMBA EPI HC III",
                        "NAMAYUMBA HC IV","NAMUGONGO FUND FOR SPECIAL CHILDREN CLINIC","NAMULONGE HC III","NANSANA HC II",
                        "NASSOLO WAMALA HC III","NDEJJE HC IV","NSAGGU HC II","NSANGI HC III","NURTURE AFRICA II SPECIAL CLINIC",
                        "SEGUKU HC II","TASO ENTEBBE SPECIAL CLINIC","TRIAM MEDICAL CENTRE HC II","TTIKALU HC III","WAGAGAI HC IV",
                        "WAKISO BANDA HC II","WAKISO EPI HC III","WAKISO HC IV","WAKISO KASOZI HC III","WATUBBA HC III","ZZINGA HC II"]
                    
                                        }



ALL =[ "BIGASA HC III","BUTENGA HC IV","KAGOGGO HC II","KIGANGAZZI HC II",
                              "KISOJJO HC II","KITANDA HC III","MIRAMBI HC III","ST. MARY'S MATERNITY HOME",
                "BULO HC III","BUTAAKA HC III","EPI-CENTRESENGE HC III","GOMBE GENERAL HOSPITAL", 
                             "KALAMBA COMMUNITY HC II", "KIBUGGA HC II","KITIMBA HC III", "KIZIIKO HC II","KYABADAZA HC III",
                             "NGANDO HC III",
                "BULWADDA HC II", "BUYANJA (GOMBA) HC II","KANONI HC III","KIFAMPA HC III", "KISOZI HC III", "KITWE HC II", "KYAYI HC III","MADDU HC IV",
                          "MAMBA HC III","MAWUKI HC II","MPENJA HC III","NGERIBALYA HC II","NGOMANENE HC III",
               "BUBEKE HC III","BUFUMIRA HC III","BUKASA HC IV","BWENDERO HC III",
                            "JAANA HC II","KACHANGA ISLAND HC II","KALANGALA HC IV","KASEKULO HC II","LUJJABWA ISLAND HC II",
                            "LULAMBA HC III","MAZINGA HC III","MUGOYE HC III","MULABANA HC II","SSESE ISLANDS AFRICAN AIDS PROJECT (SIAAP) HC II",
                "AHF UGANDA CARE","BUKULULA HC IV","KABAALE HC III", "KALUNGU HC III","KASAMBYA (KALUNGU) HC III",  "KIGAJU HC II"
                               "KIGAJU HC II","KIGASA HC II","KIRAGGA HC III",  "KITI HC III","KYAMULIBWA HC III", "LUKAYA HC III","MRC KYAMULIBWA HC II","NABUTONGWA HC II",
                "KABIRA (KYOTERA) HC III""KABUWOKO GOVT HC III","KAKUUTO HC IV","KALISIZO GENERAL HOSPITAL","KASAALI HC III",
                                        "KASASA HC III","KASENSERO HC II","KAYANJA HC II","KIRUMBA HC III","KYEBE HC III","LWANKONI HC III","MAYANJA HC II",
                                        "MITUKULA HC III","MUTUKULA HC III","NABIGASA HC III","NDOLO HC II","RHSP CLINIC",
                "KAKOMA HC III","KATOVU HC III","KIWANGALA HC IV",
                                "KYAZANGA HC IV","KYETUME HC III","LWENGO HC IV","LWENGO HC III","NANYWA HC III", 
                "KABATEMA HC II","KABAYANDA HC II","KALIIRO HC III","KASAGAMA HC III",
                                "KINUUKA HC III","KYEMAMBA HC II","LYAKAJURA HC III","LYANTONDE HOSPITAL","MPUMUDDE HC III",
                "BUGABIRA HC II","BUKOTO HC III","KITABAAZI HC III","KIYUMBA HC IV","KYABAKUZA HC II",
                                        "MASAKA MUNICIPAL CLINIC","MASAKA POLICE HC III","MPUGWE HC III","NYENDO HC III","TASO MASAKA",
                "BUKAKATA HC III","BUKEERI HC III","BUWUNGA HC III","BUYAGA HC II","KAMULEGU HC III","KYANAMUKAAKA HC IV",
      "BUJUUKO HC III","BUKASA HC II","BUNJAKO HC III",
                            "BUTOOLO HC III","BUWAMA HC III","BUYIGA HC III","DONA MEDICAL CENTRE","FIDUGA MEDICAL CENTRE","GGOLO HC III",
                            "KAMPIRINGISA HC III","KIRINGENTE EPI HC II","KITUNTU HC III","MPIGI HC IV","MUDUUMA HC III",
                            "NABYEWANGA HC II","NINDYE HC III","NSAMU/KYALI HC III","SEKIWUNGA HC III","ST. ELIZABETH KIBANGA IHU HC III",
                "BUGONA HC II","BUTITI HC II","BUYAMBA HC III","BYAKABANDA HC III",
                                    "KACHEERA HC III","KASANKALA HC II","KAYONZA KACHEERA HC II","KIBAALE HC II","KIBANDA HC III","KIBUUKA HC II",
                                    "KIFAMBA HC III","KIMULI HC III","KYABIGONDO HC II","KYALULANGIRA HC III","LWABAKOOBA HC II","LWAKALOLO HC II",
                                    "LWAMAGGWA GOVT HC III","LWANDA HC III","LWEMBAJJO HC II","MAGABI HC II","RAKAI HOSPITAL","RAKAI KIZIBA HC III",
                "BUSHEKA HC III","KABUNDI HC II","KAYUNGA HC II",
                                        "KYABI HC III","KYEERA HC II","LUGUSULU HC III","LWEBITAKULI HC III","LWEMIYAGA HC III","MAKOOLE HC II","MATEETE HC III",
                                        "MITIMA HC II","NTETE HC II","NTUUSI HC IV","SEMBABULE KABAALE HC II","SSEMBABULE HC IV",
                                            
                "BULONDO HC III","BUNAMWAYA HC II","BUSAWAMANZE HC III","BUSSI HC III","BUWAMBO HC IV","BWEYOGERERE HC III","COMMUNITY HEALTH PLAN UGANDA",
                        "GGWATIRO NURSING HOME HOSPITAL","GOMBE (WAKISO) HC II","JOINT CLINICAL RESEARCH CENTER (JCRC) HC IV",
                        "KABUBBU HC IV","KAJJANSI HC IV","KAKIRI HC III","KASANGATI HC IV","KASANJE HC III","KASENGE HC II",
                        "KASOOZO HC III","KATABI HC III","KAWANDA HC III","KIGUNGU HC III","KIMWANYI HC II","KIRA HC III",
                        "KIREKA HC II","KIRINYA (BWEYOGERERE) HC II","KITALA HC II","KIZIBA HC III","KYENGERA HC III",
                        "KYENGEZA HC II","LUBBE HC II","LUFUKA VALLEY HC III","MAGANJO HC II","MAGOGGO HC II","MATUGA HC II",
                        "MENDE HC III","MIGADDE HC II","MILDMAY UGANDA HOSPITAL","MUTUNDWE HC II","MUTUNGO HC II","NABUTITI HC III",
                        "NABWERU HC III","NAKAWUKA HC III","NAKITOKOLO NAMAYUMBA HC III","NALUGALA HC II","NAMAYUMBA EPI HC III",
                        "NAMAYUMBA HC IV","NAMUGONGO FUND FOR SPECIAL CHILDREN CLINIC","NAMULONGE HC III","NANSANA HC II",
                        "NASSOLO WAMALA HC III","NDEJJE HC IV","NSAGGU HC II","NSANGI HC III","NURTURE AFRICA II SPECIAL CLINIC",
                        "SEGUKU HC II","TASO ENTEBBE SPECIAL CLINIC","TRIAM MEDICAL CENTRE HC II","TTIKALU HC III","WAGAGAI HC IV",
                        "WAKISO BANDA HC II","WAKISO EPI HC III","WAKISO HC IV","WAKISO KASOZI HC III","WATUBBA HC III","ZZINGA HC II"]
                    
                                                     

# Title of the Streamlit app
#st.title("PMTCT DASHBOARD DATA ENTRY FORM")
st.markdown("<h4><b>DELIVERY OUTCOME ENTRY FORM</b></h4>", unsafe_allow_html=True)
st.markdown('***means required**')

art =  ""
facility = ""
parenta = ""
parentb = ""
cohort = ""
parentc = ""
parentd = ""
date = ""
outcome =''
parent = ''
district=''
mother = ''
ids = ''
# Radio button to select a district
cluster = st.radio("**Choose a cluster:**", list(CLUSTER.keys()),horizontal=True, index=None)

# Show the facilities for the selected district and allow selection
if cluster is not None:
    districts = CLUSTER[cluster]
    district = st.radio(f"**Choose a district in {cluster} cluster:**", districts, horizontal=True, index=None)

cola, colb = st.columns([1,1])
with cola:
    if not district:
            st.stop()
    else:        
        facilities = FACILITIES[district]
        facility = st.selectbox(f"**Name of this Reporting facility in {district}:**", facilities, index=None)
    
#Display the selection
with colb:
    st.write('**You selected:**')
    st.write(f"**{district} district, and {facility}**")

cohort = st.radio(label="**Is this mother from this facility's EDD COHORT?**", options=['YES','NO'], index=None, horizontal=True)

conn = st.connection('gsheets', type=GSheetsConnection)
exist = conn.read(worksheet= 'PMTCT', usecols=list(range(30)),ttl=5)
arts = exist.dropna(how='all')
st.write(arts.columns)
arts =  arts[arts['HEALTH FACILITY']== facility].copy()
numbers = arts['ART No.'].unique()
ids = arts['UNIQUE ID'].unique()
search = st.radio('**SEARCH HER BY**')
cola,colb,colc = st.columns([3,1,3])
art = cola.selectbox('**ART NO.**', numbers, index=None)
colb.write('**OR**')
id = colc.selectbox('**UNIQUE ID**', ids, index=False)


if not cohort:
     st.stop()
elif cohort=='YES':
        try:
            conn = st.connection('gsheets', type=GSheetsConnection)
            exist = conn.read(worksheet= 'PMTCT', usecols=list(range(27)),ttl=5)
            arts = exist.dropna(how='all')
            arts =  arts[arts['HEALTH FACILITY']== facility].copy()
            st.write(arts.columns)
            st.stop()
            numbers = arts['ART No.'].unique()
            ids = arts['UNIQUE ID'].unique()
            search = st.radio('**SEARCH HER BY**')
            cola,colb,colc = st.columns([3,1,3])
            art = cola.selectbox('**ART NO.**', numbers, index=None)
            colb.write('**OR**')
            id = colc.selectbox('**UNIQUE ID**', ids, index=False)
        except:
            st.write("POOR NETWORK, COULDN'T CONNECT TO COHORT")
            st.write('GET GOOD NETWORK AND TRY AGAIN')
            time.sleep(5)
            st.markdown("""
                 <meta http-equiv="refresh" content="0">
                     """, unsafe_allow_html=True)
      
#mother = st.number_input("**MOTHER'S ART No.**", min_value=1, value=None)
elif cohort=='NO':
    visit = st.radio(label='**Is this mother from this facility?**', options=['YES','NO'], index=None, horizontal=True)
if not visit:
    st.stop()
elif visit=='NO':
    visitdistrict = st.radio(label='**Is She from an IDI supported DISTRICT?**', options=['YES','NO'], index=None, horizontal=True)
    if not visitdistrict:
         st.stop()
    elif visitdistrict =='YES':
         colr, colt = st.columns([1,1])
         ididistrict = colr.selectbox(f"**Select the IDI supported district where she comes from***", ididistricts, index=None)
         visitfacility = st.radio(label='**Is She from an IDI supported facility?**', options=['YES','NO'], index=None, horizontal=True)
         if not visitfacility:
             st.stop()
         elif visitfacility =='YES':
             col4,col5 = st.columns([2,1])
             fromfacility= col4.selectbox(label='**Name of her parent facility***',options=ALL, index=None)
             art = col5.number_input(label= '**Her ART No. at the parent facility:**', value=None, min_value=1)
         else:
             col4,col5 = st.columns([2,1])
             others = col4.text_input(label= '**Name of her parent facility:**')
    elif visitdistrict=='NO':
         colr, colt = st.columns([1,1])
         otherdistrict = colr.selectbox(label='**Select here her District of Origin**',options= alldistricts, index=None)
         otherfacility = colt.text_input('**Write here the facility name from this district**') 
else:
    col4,col5 = st.columns([2,1])
    ART = col4.number_input(label= '**Her ART No:**', value=None, min_value=1)

if 'preview_clicked' not in st.session_state:
    st.session_state.preview_clicked = False
if 'submit_clicked' not in st.session_state:
    st.session_state.submit_clicked = False

with st.form(key='PMTCT'):
     coly, colz = st.columns([4,1])
     Name = coly.text_input(label="**Mother's name**")
     Ag = colz.number_input(label='**Age in years**', max_value=50, value=None)
     
     cole,colf, colg = st.columns([2,1,1])
     GA = cole.number_input(label='**Gestation Age in weeks,(Write 3 if N/A or HCG pos)**', max_value=50, value=None)
     phone = colf.text_input("**Mother's Tel No.**", placeholder='eg 07XXXXXXXX')
     phone2 = colg.text_input("**Alt Tel No.**", placeholder='eg 07XXXXXXXX')
     cole,colf = st.columns(2)
     EDD = cole.date_input(label='**EXPECTED DATE OF DELIVERY (EDD)**', value=None)
     dates = colf.date_input(label='**DATE OF THIS ANC VISIT**', value=None) 
     PMTCT = cole.radio("**Enter Client's PMTCT code**", options = ['TRR', 'TRRK', 'TRR+'], index=None)
     colf.write("MOTHER'S ADDRESS")
     dist = colf.selectbox(label="**SELECT HER HOME DISTRICT****", options =alldistrictsidi, index=None)
     sub = colf.text_input("**SUBCOUNTY**")
     par = colf.text_input("**PARISH**")
     vil = colf.text_input("**VILLAGE**")
     preview = st.form_submit_button(label='**PREVIEW BEFORE SUBMISSION**')



















# st.stop()
#     parent = st.radio("**Is this her parent facility**", options=['YES', 'NO'], index=None, horizontal=True)
#     if not parent:
#          st.stop()
#     if parent == 'NO':
#          parentb = st.radio('**Is she from an IDI supported facilty?**', options=['YES','NO'], index=None, horizontal=True)
#          cola,colb= st.columns([2,1])
#          if not parentb:
#               st.stop() 
#          elif parentb=='YES':
#               facilities = ALL
#               parentc = cola.selectbox('**Name of her parent Facility**', options=facilities)
#               art = colb.text_input('**Write her at No if known**')
#          elif parentb == 'NO':
#               parentd = cola.text_input('**Write the name of her parent facility**')

# # if not parent:
# #     st.stop()
# if cohort:
#     outcome = st.radio('**DELIVERY OUTCOME**', options =['LIVE BIRTH', 'FRESH STILL BIRTH', 'MACERATED STILL BIRTH', 'EARLY NEONATAL DEATH', 'ABORTION / MISCARRIAGE', 'OTHERS'], index=None, horizontal=True)    
#     if outcome =='OTHERS':
#         others = st.text_input('If others, specify')
#     date = st.date_input(label='**DATE WHEN THIS OUTCOME HAPPENED**', value=None)
#     submit =st.button(label='SUBMIT DATA', key='PREVIEW')
#     if submit:
#         colx,coly = st.columns([1,2])
#         if cohort =='YES':
#             if not mother: 
#                 colx.write('**MISSING DATA**')
#                 coly.warning("ART number not provided, input and try again")
#                 st.stop() 
#         if not outcome:
#             colx.write('**MISSING DATA**')
#             coly.warning("CHOOSE AN OUT COME")
#             st.stop() 
#         if outcome == 'OTHERS':
#              if not others:
#                 colx.write('**MISSING DATA**')
#                 coly.warning("Specify the other delivery")
#                 st.stop()     
#         if not date:
#             colx.write('**MISSING DATA**')
#             coly.warning("In put the date of the delivery out come")
#             st.stop()   
#         else:
#             date = datetime.now().date()
#             formatted = date.strftime("%d-%m-%Y")
#             data = pd.DataFrame([{ 'DATE OF SUBMISSION': formatted,
#                 'CLUSTER': cluster,                
#                 'DISTRICT': district,
#                 'FACILITY': facility,
#                 'IN COHORT?' : cohort,
#                 'ART NO.' : mother,
#                 'VISITOR': parent,
#                 'FROM IDI FACILITY?': parentb,
#                 'IDI FACILITY': parentc,
#                 'OTHER FACILITY': parentd,
#                 'OUTCOME': outcome,
#                 #'OTHERS': others,
#                 'DATE OF DELIVERY': date

#             }])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
#             #data = data.transpose()
#             try:
#                 conn = st.connection('gsheets', type=GSheetsConnection)
#                 exist = conn.read(worksheet= 'DELIVERY', usecols=list(range(13)),ttl=5)
#                 existing= exist.dropna(how='all')
#                     #st.write(existing)
#                 updated = pd.concat([existing, data], ignore_index =True)
#                 conn.update(worksheet = 'DELIVERY', data = updated)
#                 st.success('Your data above has been submitted')
#             except:
#                 st.write("Couldn't submit, poor network")

