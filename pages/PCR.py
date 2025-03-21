import pandas as pd 
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import time
import datetime as dt
import json
import gspread
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
#ssssssss

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
                "KALUNGU" : ["AHF UGANDA CARE","BUKULULA HC IV","KABAALE HC III", "KALUNGU HC III","KASAMBYA (KALUNGU) HC III",  "KIGAJU HC II"
                               "KIGAJU HC II","KIGASA HC II","KIRAGGA HC III",  "KITI HC III","KYAMULIBWA HC III", "LUKAYA HC III","MRC KYAMULIBWA HC II","NABUTONGWA HC II"],
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
                "BULWADDA HC III", "BUYANJA (GOMBA) HC II","KANONI HC III","KIFAMPA HC III", "KISOZI HC III", "KITWE HC II", "KYAYI HC III","MADDU HC IV",
                          "MAMBA HC III","MAWUKI HC II","MPENJA HC III","NGERIBALYA HC II","NGOMANENE HC III",
               "BUBEKE HC III","BUFUMIRA HC III","BUKASA HC IV","BWENDERO HC III",
                            "JAANA HC II","KACHANGA ISLAND HC II","KALANGALA HC IV","KASEKULO HC II","LUJJABWA ISLAND HC II",
                            "LULAMBA HC III","MAZINGA HC III","MUGOYE HC III","MULABANA HC II","SSESE ISLANDS AFRICAN AIDS PROJECT (SIAAP) HC II",
                "AHF UGANDA CARE","BUKULULA HC IV","KABAALE HC III", "KALUNGU HC III","KASAMBYA (KALUNGU) HC III",  "KIGAJU HC II"
                               "KIGAJU HC II","KIGASA HC II","KIRAGGA HC III",  "KITI HC III","KYAMULIBWA HC III", "LUKAYA HC III","MRC KYAMULIBWA HC II","NABUTONGWA HC II",
                "KABIRA (KYOTERA) HC III","KABUWOKO GOVT HC III","KAKUUTO HC IV","KALISIZO GENERAL HOSPITAL","KASAALI HC III",
                                        "KASASA HC III","KASENSERO HC II","KAYANJA HC II","KIRUMBA HC III","KYEBE HC III","LWANKONI HC III","MAYANJA HC II",
                                        "MITUKULA HC III","MUTUKULA HC III","NABIGASA HC III","NDOLO HC II","RHSP CLINIC",
                "KAKOMA HC III","KATOVU HC III","KIWANGALA HC IV",
                                "KYAZANGA HC IV","KYETUME HC III","LWENGO HC IV","LWENGO KINONI GOVT HC III","NANYWA HC III", 
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
                    
ididistricts = ['BUKOMANSIMBI','BUTAMBALA', 'GOMBA','KALANGALA','KALUNGU','KYOTERA', 'LYANTONDE', 'LWENGO', 'MASAKA CITY', 
                'MASAKA DISTRICT', 'MPIGI','RAKAI', 'SEMBABULE', 'WAKISO']  
# Access the credentials from the correct path
secrets = st.secrets["connections"]["gsheets"]

# Prepare the credentials dictionary
credentials_info = {
    "type": secrets["type"],
    "project_id": secrets["project_id"],
    "private_key_id": secrets["private_key_id"],
    "private_key": secrets["private_key"],
    "client_email": secrets["client_email"],
    "client_id": secrets["client_id"],
    "auth_uri": secrets["auth_uri"],
    "token_uri": secrets["token_uri"],
    "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": secrets["client_x509_cert_url"]
}

# Define the scopes needed for your application
scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

# # Create credentials object
# credentials = Credentials.from_service_account_info(credentials_info)
# Create credentials object with the required scopes
credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)

# Authorize and access Google Sheets
client = gspread.authorize(credentials)

# Open the Google Sheet by URL
spreadsheetu = "https://docs.google.com/spreadsheets/d/1q7oeVZ6UNhDxAj24qk3hLFLX2d0pGfxCsM9XycocqYQ"
spreadsheet = client.open_by_url(spreadsheetu)

file = r'DISTRICT.csv'
#backup = r'New BAK.xlsx'

dis = pd.read_csv(file)
dis1 = dis[dis['ORG'] == 'OTHERS'].copy()
alldistricts = dis1['DISTRICT'].unique()
alldistrictsidi = dis['DISTRICT'].unique()

#dfback = pd.read_excel(backup)

# Title of the Streamlit app
#st.title("PMTCT DASHBOARD DATA ENTRY FORM")
st.markdown("<h4><b>FIRST PCR ENTRY FORM</b></h4>", unsafe_allow_html=True)
st.markdown('***means required**')

##################UNIQUE NUMBER
arty = ''
unique = ''
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
phone = ''
phone2 = ''
mother = ''
ids = ''
visitfacility =''
visitdistrict = ''
ididistrict = ''
fromfacility = ''
visit = ''
ART = ''
outdistrict = ''
Name = ''
Ag = ''
dist = ''
par = ''
vil = ''
outfacility = ''
# Radio button to select a district
cluster = st.radio("**Choose a cluster:**", list(CLUSTER.keys()),horizontal=True, index=None)
def generate_unique_number():
    f = dt.datetime.now()  # Get the current datetime
    g = f.strftime("%Y-%m-%d %H:%M:%S.%f")  # Format datetime as a string including microseconds
    h = g.split('.')[1]  # Extract the microseconds part of the formatted string
    j = h[1:5]  # Get the second through fifth digits of the microseconds part
    return int(j)  # Convert the sliced string to an intege

# Initialize the unique number in session state if it doesn't exist
if 'unique_numer' not in st.session_state:
         st.session_state['unique_numer'] = generate_unique_number()
         #ID = st.session_state['unique_numb']

# Show the facilities for the selected district and allow selection
if cluster is not None:
    districts = CLUSTER[cluster]
    district = st.radio(f"**Choose a district in {cluster} cluster:**", districts, horizontal=True, index=None)

cola, colb = st.columns([1,1])
if district:
    pass
else:
    st.stop()
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
    
if facility:
    pass
else:
    st.stop()

cohort = st.radio(label="**Is this mother from this facility's EDD COHORT?**", options=['YES','NO'], index=None, horizontal=True)

if cohort:
    pass
else:
    st.stop()

    
if cohort=='YES':
        which = st.radio(f"**WHEN WAS SHE REGISTERD IN THE DATA BASE?**", options = ['DURING ANC', 'AFTER DELIVERY'], index=None, horizontal=True)
        if not which:
            st.stop()
        elif which == 'DURING ANC':
            st.write('**SEARCHING ANC DATABASE**')
            time.sleep(1)            
            try:
                conn = st.connection('gsheets', type=GSheetsConnection)
                if 'exist_df' not in st.session_state:
                      exist = conn.read(worksheet= 'PMTCT', usecols=list(range(26)),ttl=0)
                      back = conn.read(worksheet= 'BACK1', usecols=list(range(26)),ttl=0)
                      df = pd.concat([back, exist])
                                  # Store the fetched data in session state
                      st.session_state['exist_df'] = df
                else:
                   df = st.session_state['exist_df']
                arts = df.copy()
                arts =  arts[arts['HEALTH FACILITY']== facility].copy()
                #st.write(arts)
                
                number = arts[['ART No.']].copy()
                #st.write(number)
                number = number.dropna(subset = ['ART No.'])
                n = number.shape[0]
                number['ART No.'] = number['ART No.'].astype(int)
                numbers = number['ART No.'].unique()
                #st.write(n)
    
                id = arts[['UNIQUE ID']].copy()
                id = id.dropna(subset = ['UNIQUE ID'])
                ien = id.shape[0]
                id['UNIQUE ID'] = id['UNIQUE ID'].astype(int)
                ids = id['UNIQUE ID'].unique()
    
                search = st.radio(label="**SEARCH HER BY?**", options = ['ART NO', 'UNIQUE ID'], horizontal=True, index=None)
                if search:
                    pass
                else:
                    st.stop()
                if search == 'ART NO':
                    unique = 'NONE'
                    #st.write('**If you don't find her ART NO, either search her by ID or register or click NO above to register her first**')
                    if n == 0:
                        st.write(f'FOUND NO MOTHER FOR {facility} IN THE DATABASE**')
                        st.write('**SEARCH HER BY ID OR REGISTER HER FIRST**')
                        st.stop()
                    else:
                        st.write(f'**FOUND {n} ART NOs FOR MOTHERS IN {facility} ANC DATA BASE**')
                        st.write("**If you don't find her ART NO, either search her by ID or register or click NO above to register her first**")
                        cola, colb,colc = st.columns([2,1,1])
                        arty = cola.selectbox('**SEARCH HER ART NO**', numbers, index=None)
                        if arty:
                            pass
                        else:
                            st.stop()
    
                elif search == 'UNIQUE ID':
                    arty = 'NONE'
                    #st.write('**If you don't find her ART NO, either search her by ID or click on NO above to register her first**')
                    if ien == 0:
                        st.write(f'FOUND NO MOTHER FOR {facility} IN THE DATABASE**')
                        st.write('**SEARCH HER BY ID OR REGISTER HER FIRST**')
                        st.stop()
                    else:
                        st.write(f'**FOUND {ien} UNIQUE IDS FOR MOTHERS IN {facility} ANC DATA BASE**')
                        st.write("**If you don't find her UNIQUE ID, either search her by ART NO or click on NO above to register her first**")
                        cola, colb,colc = st.columns([2,1,1])
                        unique = cola.selectbox(f'**SEARCH HER UNIQUE ID**', ids, index=None)
                        if unique:
                            pass
                        else:
                            st.stop()
            except:
                 st.write("POOR NETWORK, COULDN'T CONNECT TO THE ANC DATABASE")
                 st.write('GET GOOD NETWORK AND TRY AGAIN')
                 st.stop()

        elif which == 'AFTER DELIVERY':
                 st.write('**SEARCHING DELIVERY DATABASE**')
                 time.sleep(1)  
                 try:
                        conn = st.connection('gsheets', type=GSheetsConnection)
                        if 'exist_d' not in st.session_state:
                            art = conn.read(worksheet= 'DELIVERYA', usecols=list(range(25)),ttl=0)
                            st.session_state['exist_d'] = art
                        else:
                            art = st.session_state['exist_d']
                        #st.write(arts.columns)
                        arts = art.copy()
                        number = arts[['NEW ART NO.']].copy()
                        #st.write(number)
                        number = number[~number['NEW ART NO.'].isnull()]
                        number = number.dropna(subset = ['NEW ART NO.'])
                        n = number.shape[0]
                        number['NEW ART NO.'] = number['NEW ART NO.'].astype(int)
                        numbers = number['NEW ART NO.'].unique()
                        #st.write(numbers)
    
                        id = arts[['UNIQUE ID']].copy()
                        id = id[~id['UNIQUE ID'].isnull()]
                        id = id[id['UNIQUE ID']!='NONE']
                        id = id.dropna(subset = ['UNIQUE ID'])
                        ien = id.shape[0]
                        id['UNIQUE ID'] = id['UNIQUE ID'].astype(int)
                        ids = id['UNIQUE ID'].unique()
    
                        search = st.radio(label="**SEARCH HER BY?**", options = ['ART NO', 'UNIQUE ID'], horizontal=True, index=None)
                        if search:
                            pass
                        else:
                            st.stop()
                        if search == 'ART NO':
                            unique = 'NONE'
                            #st.write('**If you don't find her ART NO, either search her by ID or register or click NO above to register her first**')
                            if n == 0:
                                st.write(f'FOUND NO MOTHER FOR {facility} IN THE DATABASE**')
                                st.write('**SEARCH HER BY ID OR REGISTER HER FIRST**')
                                st.stop()
                            else:
                                st.write(f'**FOUND {n} ART NOs FOR MOTHERS IN {facility} ANC DATA BASE**')
                                st.write("**If you don't find her ART NO, either search her by ID or register or click NO above to register her first**")
                                cola, colb,colc = st.columns([2,1,1])
                                arty = cola.selectbox('**SEARCH HER ART NO**', numbers, index=None)
                                if arty:
                                    pass
                                else:
                                    st.stop()
            
                        elif search == 'UNIQUE ID':
                            arty = 'NONE'
                            #st.write('**If you don't find her ART NO, either search her by ID or register or click NO above to register her first**')
                            if ien == 0:
                                st.write(f'FOUND NO MOTHER FOR {facility} IN THE DATABASE**')
                                st.write('**SEARCH HER BY ID OR REGISTER HER FIRST**')
                                st.stop()
                            else:
                                st.write(f'**FOUND {ien} UNIQUE IDS FOR MOTHERS IN {facility} ANC DATA BASE**')
                                st.write("**If you don't find her UNIQUE ID, either search her by ART NO or register or click NO above to register her first**")
                                cola, colb,colc = st.columns([2,1,1])
                                unique = cola.selectbox(f'**SEARCH HER UNIQUE ID**', ids, index=None)
                                if unique:
                                    pass
                                else:
                                    st.stop()
                 except Exception as e:
                         st.write(f"An error occurred: {e}")
                         st.info("POOR NETWORK, COULDN'T CONNECT TO THE DATABASE")
                         st.info('GET GOOD NETWORK AND TRY AGAIN')
                         st.stop()

      
#mother = st.number_input("**MOTHER'S ART No.**", min_value=1, value=None)
elif cohort=='NO':
    unique = 'NONE'
    arty = 'NONE'
    st.write("**FIRST REGISTER THIS MOTHER IN THE DATABASE BEFORE FILLING IN HER DELIVERY DETAILS**")
    st.write('')
    visit = st.radio(label="**Is this mother from this facility's ART CLINIC?**", options=['YES','NO'], index=None, horizontal=True)
    if visit=='NO':
        st.write(f'**THIS MOTHER WILL BE ASSIGNED A UNIQUE ID, WE SHALL USE THIS TO TRACK HER FOR PCR**')
        visitdistrict = st.radio(label='**Does She get ART from an IDI supported DISTRICT?**', options=['YES','NO'], index=None, horizontal=True)
        if not visitdistrict:
             st.stop()
        elif visitdistrict =='YES':
             colr, colt = st.columns([2,1])
             ididistrict = colr.selectbox(f"**Select the IDI supported district where she gets ART from***", ididistricts, index=None)
             if ididistrict:
                 pass
             else:
                 st.stop()
             visitfacility = st.radio(label='**Is She from an IDI supported facility?**', options=['YES','NO'], index=None, horizontal=True)
             if not visitfacility:
                 st.stop()
             elif visitfacility =='YES':
                 col4,col5 = st.columns([2,1])
                 fromfacility= col4.selectbox(label='**Name of her parent facility***',options=ALL, index=None)
                 art = col5.number_input(label= '**Her ART No. at the parent facility:**', value=None, min_value=1)
             else:
                 col4,col5 = st.columns([2,1])
                 otherfacility = col4.text_input(label= '**Name of her parent facility:**')
        elif visitdistrict=='NO':
             colr, colt = st.columns([1,1])
             outdistrict = colr.selectbox(label='**Select here the District of her ART Clinic**',options= alldistricts, index=None)
             outfacility = colt.text_input('**Write here the facility name from this district**') 
        else:
            st.stop()
    elif visit=='YES':
        col4,col5 = st.columns([2,1])
        ART = col4.number_input(label= '**Her ART No:**', value=None, min_value=1)
    else:
        st.stop()
else:
    st.stop()
    
if 'preview_click' not in st.session_state:
    st.session_state.preview_click = False
if 'submit_click' not in st.session_state:
    st.session_state.submit_click = False

if cohort == 'NO':
     st.write("**MOTHER'S DEMOGRAPHICS**")
     coly, colz = st.columns([4,1])
     Name = coly.text_input(label="**Mother's name**")
     Ag = colz.number_input(label='**Age in years**', max_value=50, value=None)
     cole,colf = st.columns(2)
     
     dist = cole.selectbox(label="**SELECT HER HOME DISTRICT****", options =alldistrictsidi, index=None)
     sub = colf.text_input("**SUBCOUNTY**")
     par = cole.text_input("**PARISH**")
     vil = colf.text_input("**VILLAGE**")
     phone = cole.text_input("**Mother's Tel No.**", placeholder='eg 07XXXXXXXX')
     phone2 = colf.text_input("**Alt Tel No.**", placeholder='eg 07XXXXXXXX')
else:
    pass

st.write('**FIRST PCR DETAILS**')
st.write('')
cola,colb = st.columns(2)
outcome = cola.number_input("**BABY'S AGE IN MONTHS AT FIRST PCR**",value=None, max_value= 18.0, min_value=1.0,format="%.1f")    
date = colb.date_input(label='**DATE WHEN THIS PCR WAS DONE**', value=None)
#outcome = st.radio('**DELIVERY OUTCOME**', options =['LIVE BIRTH', 'FRESH STILL BIRTH', 'MACERATED STILL BIRTH', 'EARLY NEONATAL DEATH', 'ABORTION / MISCARRIAGE', 'OTHERS'], index=None, horizontal=True)    
#cola,colb,colc =st.columns([2,1,1])
#date = cola.date_input(label='**DATE WHEN THIS OUTCOME HAPPENED**', value=None)
preview = st.button(label='**PREVIEW BEFORE SUBMISSION**')
    
if preview:
    colx,coly = st.columns([1,2])
    if visitfacility =='YES':
        if not fromfacility:
            colx.write('**ERROR!!!**')
            coly.warning("PARENT FACILITY not provided, input and try again")
            st.stop()
    elif visitfacility =='NO':
        if not otherfacility:
            colx.write('**ERROR!!!**')
            coly.warning("PARENT FACILITY not provided, input and try again")
            st.stop()
    else:
        pass
    if visit == 'YES':
        if not ART:
            colx.write('**ERROR!!!**')
            coly.warning("ART NO. not provided, input and try again")
            st.stop()

    if visitdistrict == 'NO':
        if not outdistrict:
            colx.write('**ERROR!!!**')
            coly.warning("DISTRICT OF HER ART CLINIC not provided, input and try again")
            st.stop()
        if not outfacility:
            colx.write('**ERROR!!!**')
            coly.warning("FACILITY NAME NOT PROVIDED, input and try again")
            st.stop()
    if cohort =='NO':
        if not Name:
            colx.write('**ERROR!!!**')
            coly.warning("HER NAME IS REQUIRED, input and try again")
            st.stop()
        elif not Ag:
            colx.write('**ERROR!!!**')
            coly.warning("HER AGE IS REQUIRED, input and try again")
            st.stop()
        elif not dist:
            colx.write('**ERROR!!!**')
            coly.warning("HER HOME DISTRICT IS REQUIRED, input and try again")
            st.stop()
        elif not vil:
            colx.write('**ERROR!!!**')
            coly.warning("HER HOME VILLAGE IS REQUIRED, input and try again")
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
    if not outcome:
            colx.write('**ERROR!!!**')
            coly.warning("INPUT BABY'S AGE AT PCR")
            st.stop()
    if not date:
            colx.write('**ERROR!!!**')
            coly.warning("IN PUT DATE OF PCR")
            st.stop()
    
    st.session_state.preview_click  = True
# if preview:
#     st.session_state.preview_click = True
# else:
#     st.stop()
if st.session_state.preview_click: 
    if not phone:
         phone = 'NOT FILLED'
    if visit == 'YES':
         st.session_state['unique_numer'] = 'NONE'
    else:
         st.session_state['unique_numy'] = generate_unique_number()
        
    #if st.session_state.preview_click and not st.session_state.submit_click:
    dates = datetime.now().date()
    formatted = dates.strftime("%d-%m-%Y")
    data = pd.DataFrame([{ 'DATE OF SUBMISSION': formatted,
            'CLUSTER': cluster,                
            'DISTRICT': district,
            'FACILITY': facility,
            'IN COHORT?' : cohort,
            'SEARCHED ART NO.' : arty,
            'SEARCHED ID': unique,
            'UNIQUE ID':  st.session_state['unique_numer'],
            'FROM THIS FACILITY?': visit,
            'FROM IDI SUPPORTED DISTRICT': visitdistrict,
            'IDI DISTRICT': ididistrict,
            'FROM IDI FACILITY':visitfacility,
            'PARENT FACILITY': fromfacility,
            'OTHER DISTRICT': outdistrict,
            'OUTSIDE FACILITY': outfacility,
            'NAME': Name,
            'NEW ART NO.': ART,
            'AGE': Ag,
            'HER DISTRICT':dist,
            'SUBPARISH': par,
            'VILLAGE': vil,
            'PHONE': phone, 
            'PHONE2': phone2,
            'AGE AT PCR': outcome,
            'DATE OF PCR': date
            }])   
    
    ad =  st.session_state['unique_numer']
    formatted = str(formatted)#.strftime('%Y-%m-%d') if isinstance(formatted, date) else formatted
    date = str(date)#.strftime('%Y-%m-%d') if isinstance(dates, date) else dates
     
    row_to_append =   [formatted, cluster, district, facility,cohort, arty,unique, ad,visit,visitdistrict,
            ididistrict,visitfacility,fromfacility,outdistrict,outfacility,Name, ART,Ag,dist, par,vil,
            phone, phone2,outcome, date] 

    if cohort =='YES':
                cola,colb = st.columns(2)
                cola.write(f'**CLUSTER: {cluster}**')               
                cola.write(f'**DISTRICT: {district}**')
                cola.write(f'**FACILITY: {facility}**')
                cola.write(f'**IN COHORT? : {cohort}**')
                colb.write(f'**SEARCHED ART NO. : {arty}**')
                colb.write(f'**SEARCHED ID: {unique}**')
                #colb.write(f"**UNIQUE ID:  {st.session_state['unique_numer']}**")
                #cola.write(f'**FROM THIS FACILITY?: {visit}**')
                #cola.write(f'**FROM IDI SUPPORTED DISTRICT: {visitdistrict}**')
                #cola.write(f'**IDI DISTRICT: {ididistrict}**')
                #colb.write(f'**FROM IDI FACILITY:{visitfacility}**')
                #cola.write(f'**PARENT FACILITY: {fromfacility}**')
                #colb.write(f'**OTHER DISTRICT: {outdistrict}**')
                #colb.write(f'**OUTSIDE FACILITY: {outfacility}**')
                #colb.write(f'**NAME: {Name}**')
                #colb.write(f'**NEW ART NO.: {ART}**')
                #colb.write(f'**AGE: {Ag}**')
                #colb.write(f'**HER DISTRICT: {dist}**')
                #colb.write(f'**SUBPARISH: {par}**')
                #colb.write(f'**VILLAGE: {vil}**')
                #colb.write(f'**PHONE: {phone}**')
                #colb.write(f'**PHONE2: {phone2}**')
                colb.write(f'**OUTCOME: {outcome}**')
                colb.write(f'**DATE OF DELIVERY: {date}**')
    
    
    if visit =='YES':
                cola,colb = st.columns(2)
                cola.write(f'**CLUSTER: {cluster}**')               
                cola.write(f'**DISTRICT: {district}**')
                cola.write(f'**FACILITY: {facility}**')
                cola.write(f'**IN COHORT? : {cohort}**')
                #cola.write(f'**SEARCHED ART NO. : {arty}**')
                #cola.write(f'**SEARCHED ID: {unique}**')
                #cola.write(f"**UNIQUE ID:  {st.session_state['unique_numer']}**")
                cola.write(f'**FROM THIS FACILITY?: {visit}**')
                #cola.write(f'**FROM IDI SUPPORTED DISTRICT: {visitdistrict}**')
                #cola.write(f'**IDI DISTRICT: {ididistrict}**')
                #cola.write(f'**FROM IDI FACILITY:{visitfacility}**')
                #cola.write(f'**PARENT FACILITY: {fromfacility}**')
                #colb.write(f'**OTHER DISTRICT: {outdistrict}**')
                #colb.write(f'**OUTSIDE FACILITY: {outfacility}**')
                cola.write(f'**NAME: {Name}**')
                cola.write(f'**ART NO.: {ART}**')
                colb.write(f'**AGE: {Ag}**')
                colb.write(f'**HER DISTRICT: {dist}**')
                #colb.write(f'**SUBPARISH: {par}**')
                colb.write(f'**VILLAGE: {vil}**')
                colb.write(f'**PHONE: {phone}**')
                #colb.write(f'**PHONE2: {phone2}**')
                colb.write(f'**AGE AT PCR: {outcome}**')
                colb.write(f'**DATE OF PCR: {date}**')
    
    if visitfacility =='YES':
                cola, colb, colc, cold = st.columns(4)
                cola.write (f"**UNIQUE ID:**") 
                colb.write(f"**{st.session_state['unique_numer']}**")
                st.write('')
                st.write (f"**UNIQUE ID:   {st.session_state['unique_numer']}  , write it in the EDD COHORT REGISTER**")
                cola,colb = st.columns(2)
                cola.write(f'**CLUSTER: {cluster}**')               
                cola.write(f'**DISTRICT: {district}**')
                cola.write(f'**FACILITY: {facility}**')
                cola.write(f'**IN COHORT? : {cohort}**')
                #cola.write(f'**SEARCHED ART NO. : {arty}**')
                #cola.write(f'**SEARCHED ID: {unique}**')
                cola.write(f"**UNIQUE ID:  {st.session_state['unique_numer']}**")
                cola.write(f'**FROM THIS FACILITY?: {visit}**')
                cola.write(f'**FROM IDI SUPPORTED DISTRICT: {visitdistrict}**')
                cola.write(f'**IDI DISTRICT: {ididistrict}**')
                cola.write(f'**FROM IDI FACILITY:{visitfacility}**')
                colb.write(f'**PARENT FACILITY: {fromfacility}**')
                #colb.write(f'**OTHER DISTRICT: {outdistrict}**')
                #colb.write(f'**OUTSIDE FACILITY: {outfacility}**')
                colb.write(f'**NAME: {Name}**')
                #colb.write(f'**NEW ART NO.: {ART}**')
                colb.write(f'**AGE: {Ag}**')
                colb.write(f'**HER DISTRICT: {dist}**')
                #colb.write(f'**SUBPARISH: {par}**')
                colb.write(f'**VILLAGE: {vil}**')
                colb.write(f'**PHONE: {phone}**')
                #colb.write(f'**PHONE2: {phone2}**')
                colb.write(f'**AGE AT PCR: {outcome}**')
                colb.write(f'**DATE OF PCR: {date}**')
    
    
    if visitfacility =='NO':
                cola, colb, colc, cold = st.columns(4)
                cola.write (f"**UNIQUE ID:**") 
                colb.write(f"**{st.session_state['unique_numer']}**")
                st.write('')
                st.write (f"**UNIQUE ID:   {st.session_state['unique_numer']}  , write it in the EDD COHORT REGISTER**")
                cola,colb = st.columns(2)
                cola.write(f'**CLUSTER: {cluster}**')               
                cola.write(f'**DISTRICT: {district}**')
                cola.write(f'**FACILITY: {facility}**')
                cola.write(f'**IN COHORT? : {cohort}**')
                #cola.write(f'**SEARCHED ART NO. : {arty}**')
                #cola.write(f'**SEARCHED ID: {unique}**')
                cola.write(f"**UNIQUE ID:  {st.session_state['unique_numer']}**")
                cola.write(f'**FROM THIS FACILITY?: {visit}**')
                cola.write(f'**FROM IDI SUPPORTED DISTRICT: {visitdistrict}**')
                cola.write(f'**IDI DISTRICT: {ididistrict}**')
                #cola.write(f'**FROM IDI FACILITY? :{visitfacility}**')
                #cola.write(f'**PARENT FACILITY: {fromfacility}**')
                #colb.write(f'**OTHER DISTRICT: {outdistrict}**')
                #colb.write(f'**OUTSIDE FACILITY: {outfacility}**')
                colb.write(f'**NAME: {Name}**')
                #colb.write(f'**NEW ART NO.: {ART}**')
                colb.write(f'**AGE: {Ag}**')
                colb.write(f'**HER DISTRICT: {dist}**')
                #colb.write(f'**SUBPARISH: {par}**')
                colb.write(f'**VILLAGE: {vil}**')
                colb.write(f'**PHONE: {phone}**')
                #colb.write(f'**PHONE2: {phone2}**')
                colb.write(f'**AGE AT PCR: {outcome}**')
                colb.write(f'**DATE OF PCR: {date}**')
    
    if visitdistrict =='NO':
                cola, colb, colc, cold = st.columns(4)
                cola.write (f"**UNIQUE ID:**") 
                colb.write(f"**{st.session_state['unique_numer']}**")
                st.write('')
                st.write (f"**UNIQUE ID:   {st.session_state['unique_numer']}  , write it in the EDD COHORT REGISTER**")
                cola,colb = st.columns(2)
                cola.write(f'**CLUSTER: {cluster}**')               
                cola.write(f'**DISTRICT: {district}**')
                cola.write(f'**FACILITY: {facility}**')
                cola.write(f'**IN COHORT? : {cohort}**')
                #cola.write(f'**SEARCHED ART NO. : {arty}**')
                #cola.write(f'**SEARCHED ID: {unique}**')
                cola.write(f"**UNIQUE ID:  {st.session_state['unique_numer']}**")
                cola.write(f'**FROM THIS FACILITY?: {visit}**')
                cola.write(f'**FROM IDI SUPPORTED DISTRICT: {visitdistrict}**')
                #cola.write(f'**IDI DISTRICT: {ididistrict}**')
                #cola.write(f'**FROM IDI FACILITY:{visitfacility}**')
                #cola.write(f'**PARENT FACILITY: {fromfacility}**')
                cola.write(f'**FACILITY DISTRICT: {outdistrict}**')
                colb.write(f'**OUTSIDE FACILITY: {outfacility}**')
                colb.write(f'**NAME: {Name}**')
                #colb.write(f'**NEW ART NO.: {ART}**')
                colb.write(f'**AGE: {Ag}**')
                colb.write(f'**HER DISTRICT: {dist}**')
                #colb.write(f'**SUBPARISH: {par}**')
                colb.write(f'**VILLAGE: {vil}**')
                colb.write(f'**PHONE: {phone}**')
                #colb.write(f'**PHONE2: {phone2}**')
                colb.write(f'**AGE AT PCR: {outcome}**')
                colb.write(f'**DATE OF PCR: {date}**')
    
    submit = st.button('SUBMIT')          
    if  submit:
            try:
                # Connect to the Google Sheet
                #conn = st.connection('gsheets', type=GSheetsConnection)
                st.write('SUBMITTING')
                # Initialize retry loop
                
                sheet1 = spreadsheet.worksheet("PCRA")
                sheet1.append_row(row_to_append, value_input_option='RAW')
                sheet2 = spreadsheet.worksheet("PCRB")
                sheet2.append_row(row_to_append, value_input_option='RAW')
                sheet3 = spreadsheet.worksheet("PCRC")
                sheet3.append_row(row_to_append, value_input_option='RAW')

                st.write('RELOADING PAGE')
                time.sleep(1)
                st.cache_data.clear()
                st.cache_resource.clear()
                st.markdown("""
                          <meta http-equiv="refresh" content="0">
                            """, unsafe_allow_html=True)
            
            except ConnectionError:
                st.write("Couldn't submit, poor network")
