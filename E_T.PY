import pandas as pd

InterviewsFacts = pd.read_csv('SourceData\candidates.csv', sep=';')

#Implementacion de la regla HIRED
HiresFacts = InterviewsFacts[(InterviewsFacts['Code Challenge Score'] >= 7) & (InterviewsFacts['Technical Interview Score'] >= 7)]

HiresFacts['Full Name'] = HiresFacts['First Name'] + ' ' + HiresFacts['Last Name']
HiresFacts['Application Date'] = pd.to_datetime(HiresFacts['Application Date'])

#Creacion de tablas para modelo dimensional
TechnologiesDim = pd.DataFrame()
TechnologiesDim['technology_id'] = range(len(HiresFacts['Technology'].unique()))
TechnologiesDim['technology'] = HiresFacts['Technology'].unique()

SeniorityDim = pd.DataFrame()
SeniorityDim['seniority_id'] = range( len(HiresFacts['Seniority'].unique()))
SeniorityDim['seniority'] = HiresFacts['Seniority'].unique()

CountriesDim = pd.DataFrame()
CountriesDim['country_id'] = range( len(HiresFacts['Country'].unique()))
CountriesDim['country'] = HiresFacts['Country'].unique()

DateDim = pd.DataFrame()
DateDim['date_id'] = HiresFacts['Application Date'].unique()
DateDim['day'] = DateDim['date_id'].dt.day
DateDim['month'] = DateDim['date_id'].dt.month
DateDim['year'] = DateDim['date_id'].dt.year

#Diccionarios para mapear ids
CountryToID = dict(zip(CountriesDim['country'], CountriesDim['country_id']))
SeniorotyToID = dict(zip(SeniorityDim['seniority'], SeniorityDim['seniority_id']))
TechnologyToID = dict(zip(TechnologiesDim['technology'], TechnologiesDim['technology_id']))


UniqueCandidates = HiresFacts.drop_duplicates('Full Name')

CandidatesDim = pd.DataFrame({
    'candidate_id': range(len(UniqueCandidates)),
    'full_name': UniqueCandidates['Full Name'].values,
    'first_name': UniqueCandidates['First Name'].values,
    'last_name': UniqueCandidates['Last Name'].values,
    'email': UniqueCandidates['Email'].values,
    'yoe': UniqueCandidates['YOE'].values,
    'country_id': UniqueCandidates['Country'].map(CountryToID).values,
    'seniority_id': UniqueCandidates['Seniority'].map(SeniorotyToID).values,
    'technology_id': UniqueCandidates['Technology'].map(TechnologyToID).values
})

CandidateToID = dict(zip(CandidatesDim['full_name'], CandidatesDim['candidate_id']))

#Reestructuracion de la tabla de hechos para completar la implementacion
HiresFacts = HiresFacts.drop(columns=[ 'First Name', 'Last Name', 'Email', 'Country', 'YOE', 'Seniority', 'Technology' ], axis=1)
HiresFacts['interview_id'] = range(len(HiresFacts))
HiresFacts['Full Name'] = HiresFacts['Full Name'].map(CandidateToID).values

HiresFacts = HiresFacts.rename(columns={
    'Application Date': 'date_id',
    'Full Name': 'candidate_id',
    'Code Challenge Score': 'code challenge score',
    'Technical Interview Score': 'technical interview score'
})

#Export

Tables = {
    'TechnologiesDim': TechnologiesDim,
    'CountriesDim': CountriesDim,
    'CandidatesDim': CandidatesDim,
    'DateDim': DateDim,
    'SeniorityDim': SeniorityDim,
    'HiresFacts': HiresFacts
}

for Name, Table in Tables.items():
    Table.to_csv(f'LoadData/{Name}.csv', index=False)