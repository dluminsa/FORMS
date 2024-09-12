import pandas as pd 
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import time
import datetime as dt

st.set_page_config(
     page_title= 'PMTCT FORMS'
)


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
                "GOMBA"  : ["BULWADDA HC III", "BUYANJA (GOMBA) HC II","KANONI HC III","KIFAMPA HC III", "KISOZI HC III", "KITWE HC II", "KYAYI HC III","MADDU HC IV",
                          "MAMBA HC III","MAWUKI HC II","MPENJA HC III","NGERIBALYA HC II","NGOMANENE HC III"],
               "KALANGALA": ["BUBEKE HC III","BUFUMIRA HC III","BUKASA HC IV","BWENDERO HC III",
                            "JAANA HC II","KACHANGA ISLAND HC II","KALANGALA HC IV","KASEKULO HC II","LUJJABWA ISLAND HC II",
                            "LULAMBA HC III","MAZINGA HC III","MUGOYE HC III","MULABANA HC II","SSESE ISLANDS AFRICAN AIDS PROJECT (SIAAP) HC II"],
                "KALUNGU" : ["AHF UGANDA CARE","BUKULULA HC IV","KABAALE HC III", "KALUNGU HC III","KASAMBYA (KALUNGU) HC III",  "KIGAJU HC II",
                               "KIGASA HC II","KIRAGGA HC III",  "KITI HC III","KYAMULIBWA HC III", "LUKAYA HC III","MRC KYAMULIBWA HC II","NABUTONGWA HC II"],
                "KYOTERA" : ["KABIRA (KYOTERA) HC III","KABUWOKO GOVT HC III","KAKUUTO HC IV","KALISIZO GENERAL HOSPITAL","KASAALI HC III",
                                        "KASASA HC III","KASENSERO HC II","KAYANJA HC II","KIRUMBA HC III","KYEBE HC III","LWANKONI HC III","MAYANJA HC II",
                                        "MITUKULA HC III","MUTUKULA HC III","NABIGASA HC III","NDOLO HC II","RHSP CLINIC"],
                "LWENGO" : ["KAKOMA HC III","KATOVU HC III","KIWANGALA HC IV",
                                "KYAZANGA HC IV","KYETUME HC III","LWENGO HC IV","LWENGO KINONI GOVT HC III","NANYWA HC III"], 
                "LYANTONDE" :["KABATEMA HC II","KABAYANDA HC II","KALIIRO HC III","KASAGAMA HC III",
                                "KINUUKA HC III","KYEMAMBA HC II","LYAKAJURA HC III","LYANTONDE HOSPITAL","MPUMUDDE HC III"],
                "MASAKA CITY": ["BUGABIRA HC II","BUKOTO HC III","KITABAAZI HC III","KIYUMBA HC IV","KYABAKUZA HC III",
                                        "MASAKA MUNICIPAL CLINIC","MASAKA POLICE HC III","MPUGWE HC III","NYENDO HC III","TASO MASAKA"],
                "MASAKA DISTRICT": ["BUKAKATA HC III","BUKEERI HC III","BUWUNGA HC III","BUYAGA HC II","KAMULEGU HC III","KYANAMUKAAKA HC IV"],
                "MPIGI" : ["BUJUUKO HC III","BUKASA HC II","BUNJAKO HC III",
                            "BUTOOLO HC III","BUWAMA HC III","BUYIGA HC III","DONA MEDICAL CENTRE","FIDUGA MEDICAL CENTRE","GGOLO HC III",
                            "KAMPIRINGISA HC III","KIRINGENTE EPI HC II","KITUNTU HC III","MPIGI HC IV","MUDUUMA HC III",
                            "NABYEWANGA HC II","NINDYE HC III","NSAMU/KYALI HC III","SEKIWUNGA HC III","ST. ELIZABETH KIBANGA IHU HC III"],
                "RAKAI" : ["BUGONA HC II","BUTITI HC II","BUYAMBA HC III","BYAKABANDA HC III",
                                    "KACHEERA HC III","KASANKALA HC II","KAYONZA KACHEERA HC II","KIBAALE HC II","KIBANDA HC III","KIBUUKA HC II",
                                    "KIFAMBA HC III","KIMULI HC III","KYABIGONDO HC II","KYALULANGIRA HC III","LWABAKOOBA HC II","LWAKALOLO HC II",
                                    "LWAMAGGWA GOVT HC III","LWANDA HC III","LWEMBAJJO HC II","MAGABI HC II","RAKAI HOSPITAL","RAKAI KIZIBA HC III"],
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
                "BULWADDA HC III", "BUYANJA (GOMBA) HC II","KANONI HC III","KIFAMPA HC III", "KISOZI HC III", "KITWE HC II", "KYAYI HC III","MADDU HC IV",
                          "MAMBA HC III","MAWUKI HC II","MPENJA HC III","NGERIBALYA HC II","NGOMANENE HC III",
               "BUBEKE HC III","BUFUMIRA HC III","BUKASA HC IV","BWENDERO HC III",
                            "JAANA HC II","KACHANGA ISLAND HC II","KALANGALA HC IV","KASEKULO HC II","LUJJABWA ISLAND HC II",
                            "LULAMBA HC III","MAZINGA HC III","MUGOYE HC III","MULABANA HC II","SSESE ISLANDS AFRICAN AIDS PROJECT (SIAAP) HC II",
                "AHF UGANDA CARE","BUKULULA HC IV","KABAALE HC III", "KALUNGU HC III","KASAMBYA (KALUNGU) HC III",  "KIGAJU HC II",
                               "KIGASA HC II","KIRAGGA HC III",  "KITI HC III","KYAMULIBWA HC III", "LUKAYA HC III","MRC KYAMULIBWA HC II","NABUTONGWA HC II",
                "KABIRA (KYOTERA) HC III","KABUWOKO GOVT HC III","KAKUUTO HC IV","KALISIZO GENERAL HOSPITAL","KASAALI HC III",
                                        "KASASA HC III","KASENSERO HC II","KAYANJA HC II","KIRUMBA HC III","KYEBE HC III","LWANKONI HC III","MAYANJA HC II",
                                        "MITUKULA HC III","MUTUKULA HC III","NABIGASA HC III","NDOLO HC II","RHSP CLINIC",
                "KAKOMA HC III","KATOVU HC III","KIWANGALA HC IV",
                                "KYAZANGA HC IV","KYETUME HC III","LWENGO HC IV","LWENGO KINONI GOVT HC III","NANYWA HC III", 
                "KABATEMA HC II","KABAYANDA HC II","KALIIRO HC III","KASAGAMA HC III",
                                "KINUUKA HC III","KYEMAMBA HC II","LYAKAJURA HC III","LYANTONDE HOSPITAL","MPUMUDDE HC III",
                "BUGABIRA HC II","BUKOTO HC III","KITABAAZI HC III","KIYUMBA HC IV","KYABAKUZA HC III",
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
                    
ididistricts = ['BUKOMANSIMBI','BUTAMBALA', 'GOMBA','KALANGALA','KALUNGU','KYOTERA', 'LYANTONDE', 'LWENGO', 'MASAKA CITY', 
                'MASAKA DISTRICT', 'MPIGI','RAKAI', 'SEMBABULE', 'WAKISO']                                                     

file = r'DISTRICT.csv'
dis = pd.read_csv(file)
dis1 = dis[dis['ORG'] == 'OTHERS'].copy()
alldistricts = dis1['DISTRICT'].unique()
alldistrictsidi = dis['DISTRICT'].unique()

# Title of the Streamlit app
#st.title("PMTCT DASHBOARD DATA ENTRY FORM")
st.markdown("<h4><b>PMTCT DASHBOARD ANC DATA ENTRY FORM</b></h4>", unsafe_allow_html=True)
st.markdown('***means required**')

ART =  ""
aa = ''
facility = ""
visitfacility = ""
others = ""
art = ""
fromfacility = ""
phone = ""
EDD = ""
dates = ""
PMTCT =''
idis = ''
#st.session_state['unique_numbe'] = ''
district = ''
visitdistrict = ''
ididistrict= ''
otherfacility = ''
otherdistrict = ''
Age= ''
ID  = ''
par = ''
dist = ''
# Radio button to select a district
cluster = st.radio("**Choose a cluster:**", list(CLUSTER.keys()),horizontal=True, index=None)
def generate_unique_number():
    f = dt.datetime.now()  # Get the current datetime
    g = f.strftime("%Y-%m-%d %H:%M:%S.%f")  # Format datetime as a string including microseconds
    h = g.split('.')[1]  # Extract the microseconds part of the formatted string
    j = h[1:5]  # Get the second through fifth digits of the microseconds part
    return int(j)  # Convert the sliced string to an intege

# Initialize the unique number in session state if it doesn't exist
if 'unique_numbe' not in st.session_state:
         st.session_state['unique_numbe'] = generate_unique_number()
         ID = st.session_state['unique_numbe']

# Show the facilities for the selected district and allow selection
if cluster:
    districts = CLUSTER[cluster]
    district = st.radio(f"**Choose a district in {cluster} cluster:**", districts, horizontal=True, index=None)
else:
     st.stop()
if district:
     pass
else:
     st.stop()

cola, colb = st.columns([1,1])
with cola:
    if not district:
            st.stop()
    else:        
        facilities = FACILITIES[district]
        facility = st.selectbox(f"**Name of this Reporting facility in {district}:***", facilities, index=None)
    
#Display the selection
with colb:
    st.write('**You selected:**')
    st.write(f"**{district} district, and {facility}**")

visit = st.radio(label="**Is this mother from this facility?'s ART CLINIC**", options=['YES','NO'], index=None, horizontal=True)
if not visit:
    st.stop()
elif visit=='NO':
    st.write(f'**THIS MOTHER WILL BE ASSIGNED A UNIQUE ID, WE SHALL USE THIS TO TRACK HER FOR PCR**')
    visitdistrict = st.radio(label='**Is her ART CLINIC from an IDI supported DISTRICT?**', options=['YES','NO'], index=None, horizontal=True)
    if not visitdistrict:
         st.stop()
    elif visitdistrict =='YES':
         colr, colt = st.columns([1,1])
         ididistrict = colr.selectbox(f"**Select the IDI supported district where her ART CLINIC is from***", ididistricts, index=None)
         if ididistrict:
              pass
         else:
              st.stop()
         visitfacility = st.radio(f'**In {ididistrict}, is She from an IDI supported facility?**', options=['YES','NO'], index=None, horizontal=True)
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

if 'preview_clicke' not in st.session_state:
    st.session_state.preview_clicke = False
if 'submit_clicke' not in st.session_state:
    st.session_state.submit_clicke = False

#with st.form(key='PMTCT'):
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
#preview = st.form_submit_button(label='**PREVIEW BEFORE SUBMISSION**')
preview = st.button(label='**PREVIEW BEFORE SUBMISSION**')
     
if preview:

     # def generate_unique_number():
     #      f = dt.datetime.now()  # Get the current datetime
     #      g = f.strftime("%Y-%m-%d %H:%M:%S.%f")  # Format datetime as a string including microseconds
     #      h = g.split('.')[1]  # Extract the microseconds part of the formatted string
     #      j = h[1:5]  # Get the second through fifth digits of the microseconds part
     #      return int(j)  # Convert the sliced string to an intege

     # # Initialize the unique number in session state if it doesn't exist
     # if 'unique_numbe' not in st.session_state:
     #          st.session_state['unique_numbe'] = generate_unique_number()
     #          ID = st.session_state['unique_numbe']
     colx,coly = st.columns([1,2])
     if visit=='YES':
          if not ART:
               colx.write('**ERROR!!!**')
               coly.warning("ART number not provided, input and try again")
               st.stop()

     if not facility:              
               colx.write('**ERROR!!!**')
               coly.warning("You didn't select the reporting facility, select and try again")
               st.stop() 

     if visit =='NO':
          if visitfacility=='YES' and not fromfacility:
               colx.write('**ERROR!!!**')
               coly.warning("You didn't provide her parent facility")
               st.stop()
          elif visitfacility =='NO' and not others:
               colx.write('**ERROR!!!**')
               coly.warning("You didn't provide her parent facility") 
               st.stop()     
     if not Name:
          colx.write('**ERROR!!!**')
          coly.warning("You didn't provide the mother's name")
          st.stop() 
     if visitdistrict == 'NO':
          if not otherdistrict:
               colx.write('**ERROR!!!**')
               coly.warning("You didn't provide her other district") 
               st.stop()  
          elif not otherfacility:
               colx.write('**ERROR!!!**')
               coly.warning("You didn't provide her parent facility") 
               st.stop()  
  
     if not Ag:
          colx.write('**ERROR!!!**')
          coly.warning("You didn't provide the mother's AGE")
          st.stop()
     else:
          Age = int(Ag) 

     if not GA:
          colx.write('**ERROR!!!**')
          coly.warning("You didn't provide the mother's GESTATION AGE")
          st.stop()

     if not dates:
          colx.write('**ERROR!!!**')
          coly.warning("In put either her ANC VISIT DATE")
          st.stop() 

     if not EDD:
          colx.write('**ERROR!!!**')
          coly.warning("In put either her EDD")
          st.stop() 
     elif dates > EDD:
          colx.write('**ERROR!!!**')
          coly.warning("ANC VISIT DATE CAN'T BE GREATER THAN EDD")
          st.stop()
     elif dates == EDD:
          colx.write('**ERROR!!!**')
          coly.warning("ANC VISIT DATE CAN'T BE EQUAL TO EDD")
          st.stop()

     if not PMTCT:
          colx.write('**ERROR!!!**')
          coly.warning("YOU DIDN'T CHOOSE A PMTCT CODE")
          st.stop() 

     if not vil:
          colx.write('**ERROR!!!**')
          coly.warning("Mother's village is required")
          st.stop() 

     if visitdistrict =='YES':
          if not ididistrict: 
               colx.write('**ERROR!!!**')
               coly.warning("SELECT AN IDI SUPPORTED DISTRICT")
               st.stop() 
     if phone: 
          if len(phone)!=10:
               colx.write('**ERROR!!!**')
               coly.warning("PHONE NUMBER MUST BE TEN CHARACTERS")
               st.stop()
     if phone2:
          if len(phone2)!=10:
               colx.write('**ERROR!!!**')
               coly.warning("PHONE NUMBER MUST BE TEN CHARACTERS")
               st.stop()
     if not dist:
          colx.write('**ERROR!!!**')
          coly.warning("In put either her home District")
          st.stop() 
     else:
          pass
     if not vil:
          colx.write('**ERROR!!!**')
          coly.warning("You didn't provide her village")
          st.stop()

     st.session_state.preview_clicke = True
     #st.session_state.submit_clicke = False
if st.session_state.preview_clicke:
          if not phone:
               phone = 'NOT FILLED'
          if visit == 'YES':
               st.session_state['unique_numbe'] = ''
          else:
                st.session_state['unique_number'] = generate_unique_number()


     #if st.session_state.preview_clicke and not st.session_state.submit_clicke:
          # if not st.session_state.submit_clicke:    
          datey = datetime.now().date()
          formatted = datey.strftime("%d-%m-%Y")
          #st.write(formatted)
          df = pd.DataFrame([{ 'DATE OF SUBMISSION': formatted,
                              'CLUSTER': cluster,
                              'FACILITY DISTRICT':district,
                              'HEALTH FACILITY' : facility,
                              'IS THIS HER PARENT FACILITY?' : visit,
                              'ART No.' : ART,
                              'MWP IDI DISTRICT?': visitdistrict,
                              'IDI SUPPORTED DISTRICT':ididistrict,
                              'FROM IDI FACILITY?': visitfacility,
                              'IDI PARENT FACILITY?'  : fromfacility,
                              'OTHER PARENT FACILITY': others,
                              'ART NO AT PARENT FACILITY': art,
                              'OTHER DISTRICT': otherdistrict,
                              'OUTSIDE FACILITY': otherfacility,
                              'NAME': Name,
                              'AGE': Age,
                              'HER DISTRICT':dist,
                              'SUBCOUNTY':sub,
                              'PARISH':par,
                              'VILLAGE':vil,
                              'TELEPHONE':phone,
                              'GESTATION AGE': GA,
                              'EDD': EDD,
                              'ANC DATE':dates,
                              'CODE': PMTCT,
                              'UNIQUE ID': st.session_state['unique_numbe'],
                              }]) 
     
          if visit =='YES':
               cola,colb = st.columns(2)
               cola.write(f'**CLUSTER: {cluster}**')
               cola.write(f'**FACILITY DISTRICT: {district}**')
               cola.write(f'**HEALTH FACILITY: {facility}**')
               cola.write(f'**IS THIS HER PARENT FACILITY?: {visit}**')
               cola.write(f'**ART No: {ART}**')
               cola.write(f'**NAME: {Name}**')
               cola.write(f'**AGE: {Ag}**')
               cola.write(f'**HER DISTRICT: {dist}**')
               #colb.write(f'**SUBCOUNTY: {sub}**')
               #colb.write(f'**PARISH: {par}**')
               colb.write(f'**VILLAGE: {vil}**')
               colb.write(f'**GESTATION AGE: {GA}**')
               colb.write(f'**EDD: {EDD}**')
               colb.write(f'**ANC DATE: {dates}**')
               colb.write(f'**CODE: {PMTCT}**')
               colb.write(f'**TELEPHONE: {phone}**')     
                 
          if visitfacility=='YES':
               cola, colb, colc, cold = st.columns(4)
               cola.write (f"**UNIQUE ID:**") 
               colb.write(f"**{st.session_state['unique_numbe']}**")
               st.write('')
               st.write (f"**UNIQUE ID:   {st.session_state['unique_numbe']}  , write it in the EDD COHORT REGISTER**")
               cola,colb = st.columns(2)
               cola.write(f'**CLUSTER: {cluster}**')
               cola.write(f'**FACILITY DISTRICT: {district}**')
               cola.write(f'**HEALTH FACILITY: {facility}**')
               cola.write(f'**IS THIS HER PARENT FACILITY?: {visit}**')
               cola.write(f'**FROM IDI SUPPORTED DISTRICT?: {visitdistrict}**')
               cola.write(f'**IDI SUPPORTED DISTRICT: {ididistrict}**')
               cola.write(f'**FROM IDI FACILITY?: {visitfacility}**')
               cola.write(f'**IDI PARENT FACILITY?: {fromfacility}**')
               #cola.write(f'**OTHER PARENT FACILITY: {others}**')
               cola.write(f'**ART NO AT PARENT FACILITY: {art}**')
               #colb.write(f'**OUTSIDE FACILITY: {otherfacility}**')
               colb.write(f'**NAME: {Name}**')
               colb.write(f'**AGE: {Ag}**')
               colb.write(f'**HER DISTRICT: {dist}**')
               #colb.write(f'**SUBCOUNTY: {sub}**')
               #colb.write(f'**PARISH: {par}**')
               colb.write(f'**VILLAGE: {vil}**')
               colb.write(f'**GESTATION AGE: {GA}**')
               colb.write(f'**EDD: {EDD}**')
               colb.write(f'**ANC DATE: {dates}**')
               colb.write(f'**CODE: {PMTCT}**')
               colb.write(f'**TELEPHONE: {phone}**')
          
          if visitfacility =='NO':
               cola, colb, colc, cold = st.columns(4)
               cola.write (f"**UNIQUE ID:**") 
               colb.write(f"**{st.session_state['unique_numbe']}**")
               st.write('')
               st.write (f"**UNIQUE ID:   {st.session_state['unique_numbe']}  , write it in the EDD COHORT REGISTER**")
               cola,colb = st.columns(2)
               cola.write(f'**CLUSTER: {cluster}**')
               cola.write(f'**FACILITY DISTRICT: {district}**')
               cola.write(f'**HEALTH FACILITY: {facility}**')
               cola.write(f'**IS THIS HER PARENT FACILITY?: {visit}**')
               cola.write(f'**FROM IDI SUPPORTED DISTRICT?: {visitdistrict}**')
               cola.write(f'**IDI SUPPORTED DISTRICT: {ididistrict}**')
               cola.write(f'**FROM IDI FACILITY?: {visitfacility}**')
               #cola.write(f'**OTHER PARENT FACILITY: {fromfacility}**')
               colb.write(f'**NAME: {Name}**')
               colb.write(f'**AGE: {Ag}**')
               colb.write(f'**HER DISTRICT: {dist}**')
               #colb.write(f'**SUBCOUNTY: {sub}**')
               #colb.write(f'**PARISH: {par}**')
               colb.write(f'**VILLAGE: {vil}**')
               colb.write(f'**GESTATION AGE: {GA}**')
               colb.write(f'**EDD: {EDD}**')
               colb.write(f'**ANC DATE: {dates}**')
               cola.write(f'**CODE: {PMTCT}**')
               colb.write(f'**TELEPHONE: {phone}**')
                          
          if visitdistrict =='NO':
               cola, colb, colc, cold = st.columns(4)
               cola.write (f"**UNIQUE ID:**") 
               colb.write(f"**{st.session_state['unique_numbe']}**")
               st.write('')
               st.write (f"**UNIQUE ID:   {st.session_state['unique_numbe']}  , write it in the EDD COHORT REGISTER**")
               cola,colb = st.columns(2)
               cola.write(f'**CLUSTER: {cluster}**')
               cola.write(f'**FACILITY DISTRICT: {district}**')
               cola.write(f'**HEALTH FACILITY: {facility}**')
               cola.write(f'**IS THIS HER PARENT FACILITY?: {visit}**')
               cola.write(f'**FROM IDI SUPPORTED DISTRICT?: {visitdistrict}**')
               cola.write(f'**OTHER DISTRICT: {otherdistrict}**')
               cola.write(f'**OUTSIDE FACILITY?: {otherfacility}**')
               colb.write(f'**NAME: {Name}**')
               colb.write(f'**AGE: {Ag}**')
               colb.write(f'**HER DISTRICT: {dist}**')
               #colb.write(f'**SUBCOUNTY: {sub}**')
               #colb.write(f'**PARISH: {par}**')
               colb.write(f'**VILLAGE: {vil}**')
               colb.write(f'**GESTATION AGE: {GA}**')
               colb.write(f'**EDD: {EDD}**')
               colb.write(f'**ANC DATE: {dates}**')
               cola.write(f'**CODE: {PMTCT}**')
               colb.write(f'**TELEPHONE: {phone}**')
          
          if not st.session_state.preview_clicke:
              st.stop()
          else:
              submit = st.button('Submit')
          
          if not submit:
               st.session_state.submit_clicke = False
               st.stop()
          else:
               colx,coly = st.columns([1,2])
               if visit=='YES':
                    if not ART:
                         colx.write('**ERROR!!!**')
                         coly.warning("ART number not provided, input and try again")
                         st.stop()
          
               if not facility:              
                         colx.write('**ERROR!!!**')
                         coly.warning("You didn't select the reporting facility, select and try again")
                         st.stop() 
          
               if visit =='NO':
                    if visitfacility=='YES' and not fromfacility:
                         colx.write('**ERROR!!!**')
                         coly.warning("You didn't provide her parent facility")
                         st.stop()
                    elif visitfacility =='NO' and not others:
                         colx.write('**ERROR!!!**')
                         coly.warning("You didn't provide her parent facility") 
                         st.stop()     
               if not Name:
                    colx.write('**ERROR!!!**')
                    coly.warning("You didn't provide the mother's name")
                    st.stop() 
               if visitdistrict == 'NO':
                    if not otherdistrict:
                         colx.write('**ERROR!!!**')
                         coly.warning("You didn't provide her other district") 
                         st.stop()  
                    elif not otherfacility:
                         colx.write('**ERROR!!!**')
                         coly.warning("You didn't provide her parent facility") 
                         st.stop()  
            
               if not Ag:
                    colx.write('**ERROR!!!**')
                    coly.warning("You didn't provide the mother's AGE")
                    st.stop()
               else:
                    Age = int(Ag) 
          
               if not GA:
                    colx.write('**ERROR!!!**')
                    coly.warning("You didn't provide the mother's GESTATION AGE")
                    st.stop()
          
               if not dates:
                    colx.write('**ERROR!!!**')
                    coly.warning("In put either her ANC VISIT DATE")
                    st.stop() 
          
               if not EDD:
                    colx.write('**ERROR!!!**')
                    coly.warning("In put either her EDD")
                    st.stop() 
               elif dates > EDD:
                    colx.write('**ERROR!!!**')
                    coly.warning("ANC VISIT DATE CAN'T BE GREATER THAN EDD")
                    st.stop()
               elif dates == EDD:
                    colx.write('**ERROR!!!**')
                    coly.warning("ANC VISIT DATE CAN'T BE EQUAL TO EDD")
                    st.stop()
          
               if not PMTCT:
                    colx.write('**ERROR!!!**')
                    coly.warning("YOU DIDN'T CHOOSE A PMTCT CODE")
                    st.stop() 
          
               if not vil:
                    colx.write('**ERROR!!!**')
                    coly.warning("Mother's village is required")
                    st.stop() 
          
               if visitdistrict =='YES':
                    if not ididistrict: 
                         colx.write('**ERROR!!!**')
                         coly.warning("SELECT AN IDI SUPPORTED DISTRICT")
                         st.stop() 
               if phone: 
                    if len(phone)!=10:
                         colx.write('**ERROR!!!**')
                         coly.warning("PHONE NUMBER MUST BE TEN CHARACTERS")
                         st.stop()
               if phone2:
                    if len(phone2)!=10:
                         colx.write('**ERROR!!!**')
                         coly.warning("PHONE NUMBER MUST BE TEN CHARACTERS")
                         st.stop()
               if not dist:
                    colx.write('**ERROR!!!**')
                    coly.warning("In put either her home District")
                    st.stop() 
               else:
                    pass
               if not vil:
                    colx.write('**ERROR!!!**')
                    coly.warning("You didn't provide her village")
                    st.stop()
               else:
                    pass
               
               #st.session_state.submit_clicke = True
               if submit:
                    MAX_RETRIES = 5  # Maximum number of retries
                    WAIT_SECONDS = 2  # Time to wait between retries
                    try:
                        # Connect to the Google Sheet
                        conn = st.connection('gsheets', type=GSheetsConnection)
                    
                        # Initialize retry loop
                        for attempt in range(MAX_RETRIES):
                            # Read the existing data from the worksheet
                            exist = conn.read(worksheet='PMTCT', usecols=list(range(26)), ttl=0)
                            
                            # Combine the existing data with new data (df)
                            updated = pd.concat([exist, df], ignore_index=True)
                            
                            # Check if the number of rows is sufficient (100 in this case)
                            if updated.shape[0] >= 100:
                                st.write('SUBMITTING')
                                conn.update(worksheet='PMTCT', data=updated)
                                #st.success("Your data has been successfully submitted.")
                                st.success('Your data above has been submitted')
                                time.sleep(2)
                                st.write('RELOADING PAGE')
                                st.success('SUBMITTED SUCCESSFULLY')
                                time.sleep(1)
                                st.cache_data.clear()
                                st.cache_resource.clear()
                                st.markdown("""
                                 <meta http-equiv="refresh" content="0">
                                   """, unsafe_allow_html=True)
                                break  # Exit the loop and stop retrying since submission was successful
                            else:
                                st.write(f"Attempt {attempt + 1}: Waiting for other users... Retrying in {WAIT_SECONDS} seconds...")
                                time.sleep(WAIT_SECONDS)  # Wait before retrying
                        else:
                            # If after MAX_RETRIES, the data is still insufficient, notify the user and stop the script
                            st.warning('**TOO MANY PEOPLE SUBMITTING AT THE SAME TIME**') 
                            st.info('**PRESS SUBMIT AGAING TO RETRY**')
                            st.stop()  # Stop the Streamlit app here to let the user manually retry
                    
                    except ConnectionError:
                        st.write("Couldn't submit, poor network")




aaaaaaa


               
          
               # if st.session_state.submit_clicke:
               #      try:
               #           conn = st.connection('gsheets', type=GSheetsConnection)
               #           exist = conn.read(worksheet= 'PMTCT', usecols=list(range(26)),ttl=0)
               #           # if 'exist_df' not in st.session_state:
               #           #      exist = conn.read(worksheet= 'PMTCT', usecols=list(range(26)),ttl=0)
               #           #          # Store the fetched data in session state
               #           #      st.session_state['exist_df'] = exist
               #           # else:
               #           #      exist = st.session_state['exist_df']
               #           # if exist.shape[0]<400:
               #           #      st.info("SOMETHING WENT WRONG, COULDN'T CONNECT TO DATABASE")
               #           #      time.sleep(1)
               #           #      st.write("REFRESHING PAGE, RE-ENTER THIS MOTHER'S DETAILS")
               #           #      time.sleep(2)
               #           #      st.rerun(scope='app')
               #           #      st.stop()
               #           # else:
               #           #      pass 
               #           # #existing= exist.dropna(how='all')
               #           # if 'my_df' not in st.session_state:
               #           #      st.session_state['my_df'] = df
               #           # else:
               #           #      pass
               #           # df = st.session_state['my_df']
                         
               #           # if df.shape[0]==0:
               #           #      st.write('YOUR ENTRIES FOR THIS MOTHER WERE NOT CAPTURED')
               #           #      time.sleep(1)
               #           #      st.write("REFRESHING PAGE, RE-ENTER THIS MOTHER'S DETAILS")
               #           #      time.sleep(2)
               #           #      st.rerun(scope='app')
               #           #      st.stop()
               #           # else:
               #           #      pass  
               #           updated = pd.concat([exist, df], ignore_index =True)
               #           # if updated.shape[0]<400:
               #           #      st.stop()
               #           #      st.write("SOMETHING WENT WRONG, RE-ENTER THIS MOTHER'S DETAILS")
               #           #      time.sleep(1)
               #           #      st.write("REFRESHING PAGE, RE-ENTER THIS MOTHER'S DETAILS")
               #           #      time.sleep(2)
               #           #      st.rerun(scope='app')
               #           #      st.stop()
               #           # else:
               #           conn.update(worksheet = 'PMTCT', data = updated)         
               #           st.success('Your data above has been submitted')
               #           time.sleep(2)
               #           st.write('RELOADING PAGE')
               #           st.success('SUBMITTED SUCCESSFULLY')
               #           time.sleep(1)
               #           st.cache_data.clear()
               #           st.cache_resource.clear()
               #           st.markdown("""
               #                <meta http-equiv="refresh" content="0">
               #                     """, unsafe_allow_html=True)
          
               #      except:
               #           st.write("Couldn't submit, poor network") 
     
               #      try:
               #           conn = st.connection('gsheets', type=GSheetsConnection)
               #           exist = conn.read(worksheet= 'PMTCT', usecols=list(range(26)),ttl=0)
               #           updated = pd.concat([exist, df], ignore_index =True)
               #           if updated.shape[0] <100:
               #                time.sleep(2)
               #                conn = st.connection('gsheets', type=GSheetsConnection)
               #                exist = conn.read(worksheet= 'PMTCT', usecols=list(range(26)),ttl=0)
               #                updated = pd.concat([exist, df], ignore_index =True)
               #                if updated.shape[0] <100:
               #                     time.sleep(2)
               #                     st.write('SUBMITTING')
               #                     conn = st.connection('gsheets', type=GSheetsConnection)
               #                     exist = conn.read(worksheet= 'PMTCT', usecols=list(range(26)),ttl=0)
               #                     updated = pd.concat([exist, df], ignore_index =True)
               #                     if updated.shape[0] <100:
               #                          time.sleep(2)
               #                          st.write('SUBMITTING')
               #                          conn = st.connection('gsheets', type=GSheetsConnection)
               #                          exist = conn.read(worksheet= 'PMTCT', usecols=list(range(26)),ttl=0)
               #                          updated = pd.concat([exist, df], ignore_index =True)
               #                          if updated.shape[0] <100:
               #                               time.sleep(2)
               #                               st.write('SUBMITTING')
               #                               conn = st.connection('gsheets', type=GSheetsConnection)
               #                               exist = conn.read(worksheet= 'PMTCT', usecols=list(range(26)),ttl=0)
               #                               updated = pd.concat([exist, df], ignore_index =True)
               #                               if updated.shape[0] <100:
               #                                         time.sleep(2)
               #                                         st.write('SUBMITTING')
               #                                         conn = st.connection('gsheets', type=GSheetsConnection)
               #                                         exist = conn.read(worksheet= 'PMTCT', usecols=list(range(26)),ttl=0)
               #                                         updated = pd.concat([exist, df], ignore_index =True)
               #                                        if updated.shape[0] <100:
               #                                              time.sleep(2)
               #                                              st.write('SUBMITTING')
               #                                              conn = st.connection('gsheets', type=GSheetsConnection)
               #                                              exist = conn.read(worksheet= 'PMTCT', usecols=list(range(26)),ttl=0)
               #                                              updated = pd.concat([exist, df], ignore_index =True)
                                             
                                             
                              
                              
               #           conn.update(worksheet = 'PMTCT', data = updated)
               #           if conn
               #           st.success('Your data above has been submitted')
               #      except:
               #           st.write("Couldn't submit, poor network") 
