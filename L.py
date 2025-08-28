from sqlalchemy import Column, Integer, String, Date, ForeignKey, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
import pandas as pd

DBURL = "mysql+pymysql://root:@localhost:3333/workshop1"

engine = create_engine(DBURL, echo=True)
Session = sessionmaker(bind=engine)
Session = Session()

Base = declarative_base()

class Technologies(Base):

    __tablename__ = 'technologies'

    technology_id = Column(Integer, primary_key=True, autoincrement=False)
    technology = Column(String(50), nullable=False)


class Senioritys(Base):

    __tablename__ = 'senioritys'

    seniority_id = Column(Integer, primary_key=True, autoincrement=False)
    seniority = Column(String(50), nullable=False)



class Countries(Base):

    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True, autoincrement=False)
    country = Column(String(100), nullable=False)



class Dates(Base):

    __tablename__ = 'dates'

    date_id = Column(Date, primary_key=True)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)



class Candidates(Base):

    __tablename__ = 'candidates'


    candidate_id = Column(Integer, primary_key=True, autoincrement=False)
    full_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100))
    yoe = Column(Integer, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.country_id'), nullable = False)
    seniority_id = Column(Integer, ForeignKey('senioritys.seniority_id'), nullable = False)
    technology_id = Column(Integer, ForeignKey('technologies.technology_id'), nullable = False)

    country = relationship('Countries')
    seniority = relationship('Senioritys')
    technology = relationship('Technologies')



class Hires(Base):

    __tablename__ = 'hires'

    date_id = Column(Date,ForeignKey('dates.date_id'), nullable=False)
    code_challenge_score = Column(Integer, nullable=False)
    technical_interview_score = Column(Integer, nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'), nullable=False)
    interview_id = Column(Integer, primary_key=True, autoincrement=False)

    candidates = relationship('Candidates')
    dates = relationship('Dates')



Base.metadata.create_all(engine)


SeniorityDf = pd.read_csv('LoadData/SeniorityDim.csv')

for _, Row in SeniorityDf.iterrows():

    SeniorityInsert = Senioritys(seniority_id = Row['seniority_id'], seniority = Row['seniority'])
    Session.add(SeniorityInsert)

CountriestyDf = pd.read_csv('LoadData\CountriesDim.csv')

for _, Row in CountriestyDf.iterrows():

    CountriesInsert = Countries(country_id = Row['country_id'], country = Row['country'])
    Session.add(CountriesInsert)

DateDf = pd.read_csv('LoadData\DateDim.csv')

for _, Row in DateDf.iterrows():

    DateInsert = Dates(date_id = Row['date_id'], day = Row['day'], month = Row['month'], year = Row['year'])
    Session.add(DateInsert)


TechnologiesDf = pd.read_csv('LoadData\TechnologiesDim.csv')

for _, Row in TechnologiesDf.iterrows():

    TechnologiesInsert = Technologies(technology_id = Row['technology_id'], technology = Row['technology'])
    Session.add(TechnologiesInsert)


CandidatesDf = pd.read_csv('LoadData\CandidatesDim.csv')

for _, Row in CandidatesDf.iterrows():

    CandidatesInsert = Candidates(candidate_id = Row['candidate_id'], 
                                full_name = Row['full_name'], 
                                first_name = Row['first_name'], 
                                last_name = Row['last_name'], 
                                email = Row['email'], 
                                yoe = Row['yoe'], 
                                country_id = Row['country_id'], 
                                seniority_id = Row['seniority_id'], 
                                technology_id = Row['technology_id'])
    
    Session.add(CandidatesInsert)


HiresDf = pd.read_csv('LoadData\HiresFacts.csv')

for _, Row in HiresDf.iterrows():

    CandidatesInsert = Hires(date_id = Row['date_id'], 
                                code_challenge_score = Row['code challenge score'], 
                                technical_interview_score = Row['technical interview score'], 
                                candidate_id = Row['candidate_id'],
                                interview_id = Row['interview_id'])
    
    Session.add(CandidatesInsert)




Session.commit()